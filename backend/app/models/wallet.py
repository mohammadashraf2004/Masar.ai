"""
backend/app/models/wallet.py
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class TransactionType(str, enum.Enum):
    topup     = "topup"       # user bought credits
    deduction = "deduction"   # credits spent on AI action
    refund    = "refund"      # admin refund
    bonus     = "bonus"       # free credits granted


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

    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    credit_balance      = Column(Integer, default=0)          # current spendable credits
    lifetime_purchased  = Column(Integer, default=0)          # total credits ever bought
    lifetime_spent      = Column(Integer, default=0)          # total credits ever spent
    is_active           = Column(Boolean, default=True)
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    updated_at          = Column(DateTime(timezone=True), onupdate=func.now())

    user         = relationship("User", back_populates="wallet")
    transactions = relationship("WalletTransaction", back_populates="wallet", order_by="WalletTransaction.created_at.desc()")


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id               = Column(Integer, primary_key=True, index=True)
    wallet_id        = Column(Integer, ForeignKey("user_wallets.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status           = Column(Enum(TransactionStatus), default=TransactionStatus.confirmed)
    credits          = Column(Integer, nullable=False)        # positive = added, negative = spent
    egp_amount       = Column(Float, nullable=True)           # EGP paid (for topups)
    payment_method   = Column(Enum(PaymentMethod), nullable=True)
    payment_ref      = Column(String, nullable=True)          # Fawry/InstaPay reference number
    description      = Column(String, nullable=False)         # human-readable reason
    action_type      = Column(String, nullable=True)          # "mentor_chat", "code_review", etc.
    balance_after    = Column(Integer, nullable=False)        # snapshot for audit trail
    created_at       = Column(DateTime(timezone=True), server_default=func.now())

    wallet = relationship("UserWallet", back_populates="transactions")


class CreditPackage(Base):
    __tablename__ = "credit_packages"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)             # "Starter", "Standard", "Pro"
    credits      = Column(Integer, nullable=False)
    egp_price    = Column(Float, nullable=False)
    bonus_credits = Column(Integer, default=0)               # extra credits as promo
    is_active    = Column(Boolean, default=True)
    is_popular   = Column(Boolean, default=False)
    description  = Column(Text, nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())