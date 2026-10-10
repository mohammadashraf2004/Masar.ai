"""
backend/app/models/wallet.py
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Enum, Index, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class TransactionType(str, enum.Enum):
    topup     = "topup"       # user bought credits
    deduction = "deduction"   # credits spent on AI action
    refund    = "refund"      # admin refund
    bonus     = "bonus"       # free credits granted
    expiry    = "expiry"      # promo credits removed after their window closed
    reversal  = "reversal"    # purchased credits taken back after a refund or chargeback


class TransactionStatus(str, enum.Enum):
    pending   = "pending"     # payment submitted, awaiting confirmation
    confirmed = "confirmed"   # credits added
    failed    = "failed"      # payment failed


class PaymentMethod(str, enum.Enum):
    fawry         = "fawry"          # manual, admin-confirmed (legacy path)
    instapay      = "instapay"       # manual, admin-confirmed (legacy path)
    vodafone_cash = "vodafone_cash"  # via Paymob's mobile-wallet API (auto-confirmed by webhook)
    card          = "card"           # via Paymob's card/iframe API (auto-confirmed by webhook)
    admin         = "admin"          # manually granted by admin


class UserWallet(Base):
    __tablename__ = "user_wallets"
    # Supports reporting on outstanding promo liability (which wallets
    # still hold unexpired promo credits, and when they lapse).
    __table_args__ = (Index("ix_user_wallets_promo_expires_at", "promo_expires_at"),)

    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    credit_balance      = Column(Integer, default=0)          # current spendable credits
    lifetime_purchased  = Column(Integer, default=0)          # total credits ever bought
    lifetime_spent      = Column(Integer, default=0)          # total credits ever spent
    # ─── Launch-promo accounting ──────────────────────────────────────────
    # Promo credits are part of credit_balance like any other, but tracked
    # separately so the UNSPENT remainder can be withdrawn when the user's
    # promo window closes. Spending draws down promo credits first, so a
    # user never loses credits they actually paid for.
    #
    # Server-set only: no request schema exposes either column, so a client
    # cannot extend its own promo or mint credits.
    promo_credits_remaining = Column(Integer, default=0, nullable=False, server_default="0")
    # ─── Purchased credits ────────────────────────────────────────────────
    # The part of credit_balance that was bought (always <= credit_balance).
    # It never expires and survives every plan change. Spending draws on the
    # rest of the balance (signup and promo credits) first and on this last;
    # a Pro subscriber whose included allowance is used up can still spend it
    # (and only it). Server-set only, like the promo columns.
    purchased_credits       = Column(Integer, default=0, nullable=False, server_default="0")
    promo_expires_at        = Column(DateTime(timezone=True), nullable=True)
    is_active           = Column(Boolean, default=True)
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    updated_at          = Column(DateTime(timezone=True), onupdate=func.now())

    user         = relationship("User", back_populates="wallet")
    transactions = relationship("WalletTransaction", back_populates="wallet", order_by="WalletTransaction.created_at.desc()")


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    __table_args__ = (
        # One Paymob transaction settles at most one top-up (migration 034).
        Index(
            "uq_wallet_transactions_provider_txn", "provider_transaction_id", unique=True,
            postgresql_where=text("provider_transaction_id IS NOT NULL"),
        ),
        Index(
            "ix_wallet_transactions_request_key", "wallet_id", "request_key",
            postgresql_where=text("request_key IS NOT NULL"),
        ),
    )

    id               = Column(Integer, primary_key=True, index=True)
    wallet_id        = Column(Integer, ForeignKey("user_wallets.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status           = Column(Enum(TransactionStatus), default=TransactionStatus.confirmed)
    credits          = Column(Integer, nullable=False)        # positive = added, negative = spent
    egp_amount       = Column(Float, nullable=True)           # EGP paid (for topups)
    payment_method   = Column(Enum(PaymentMethod), nullable=True)
    payment_ref      = Column(String, nullable=True)          # Fawry/InstaPay reference number
    # Paymob top-ups only: the signed provider order this row was created for,
    # and the provider transaction that settled it.
    provider_order_id       = Column(String(100), nullable=True)
    provider_transaction_id = Column(String(100), nullable=True)
    description      = Column(String, nullable=False)         # human-readable reason
    action_type      = Column(String, nullable=True)          # "mentor_chat", "code_review", etc.
    balance_after    = Column(Integer, nullable=False)        # snapshot for audit trail
    created_at       = Column(DateTime(timezone=True), server_default=func.now())
    # ─── Purchase ledger links (migration 039) ────────────────────────────
    package_id       = Column(Integer, nullable=True)         # which credit pack a top-up order bought
    # How much of this row moved in (+) or out (-) of the wallet's purchased bucket: a
    # confirmed top-up adds its credits, a deduction records what it took from purchased
    # credits, a refund puts back what its deduction took, a reversal takes back what
    # it could recover.
    purchased_delta  = Column(Integer, nullable=False, default=0, server_default="0")
    related_tx_id    = Column(Integer, nullable=True, index=True)   # the row a refund or reversal answers
    reversed_credits = Column(Integer, nullable=False, default=0, server_default="0")  # of an order: credits reversed so far
    settled_at       = Column(DateTime(timezone=True), nullable=True)  # when the payment was confirmed
    request_key      = Column(String(160), nullable=True)     # Idempotency-Key a deduction was made under

    wallet = relationship("UserWallet", back_populates="transactions")


class CreditPackage(Base):
    __tablename__ = "credit_packages"
    __table_args__ = (Index("uq_credit_packages_code", "code", unique=True),)

    id           = Column(Integer, primary_key=True, index=True)
    # Stable key ("starter", "standard", "plus", "power"); packs without one are the old
    # seed's and are not sold. Prices live here and only here - a request never carries one.
    code         = Column(String(32), nullable=True)
    sort_order   = Column(Integer, nullable=False, default=0, server_default="0")
    name         = Column(String, nullable=False)             # "Starter", "Standard", "Plus", "Power"
    credits      = Column(Integer, nullable=False)
    egp_price    = Column(Float, nullable=False)
    bonus_credits = Column(Integer, default=0)               # extra credits as promo
    is_active    = Column(Boolean, default=True)
    is_popular   = Column(Boolean, default=False)
    description  = Column(Text, nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())