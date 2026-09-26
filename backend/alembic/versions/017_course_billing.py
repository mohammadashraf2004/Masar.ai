"""course offers, orders, transactions, enrollments and previews

Revision ID: 017_course_billing
Revises: 016_course_role_relation
Create Date: 2026-09-26
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "017_course_billing"
down_revision: Union[str, None] = "016_course_role_relation"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Preserve today's behaviour: all existing courses remain free and no
    # existing lesson becomes a preview-only entitlement by accident.
    op.add_column(
        "courses",
        sa.Column("is_free", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.add_column(
        "lessons",
        sa.Column("is_preview", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    op.create_table(
        "course_offers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("price_amount", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="EGP"),
        sa.Column("original_price_amount", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("currency = 'EGP'", name="ck_course_offers_egp_only"),
        sa.CheckConstraint("price_amount > 0", name="ck_course_offers_price_positive"),
        sa.CheckConstraint(
            "original_price_amount IS NULL OR original_price_amount >= price_amount",
            name="ck_course_offers_original_price",
        ),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_course_offers_id", "course_offers", ["id"])
    op.create_index("ix_course_offers_course_id", "course_offers", ["course_id"])
    op.create_index("ix_course_offers_is_active", "course_offers", ["is_active"])
    op.create_index(
        "uq_course_offers_one_active", "course_offers", ["course_id"], unique=True,
        postgresql_where=sa.text("is_active = true"),
    )

    op.create_table(
        "billing_orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("purchasable_type", sa.String(length=32), nullable=False, server_default="course"),
        sa.Column("purchasable_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("offer_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="EGP"),
        sa.Column("provider", sa.String(length=32), nullable=False, server_default="paymob"),
        sa.Column("merchant_order_id", sa.String(length=100), nullable=False),
        sa.Column("provider_order_id", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("amount >= 0", name="ck_billing_orders_amount_nonnegative"),
        sa.CheckConstraint("currency = 'EGP'", name="ck_billing_orders_egp_only"),
        sa.CheckConstraint("purchasable_type = 'course'", name="ck_billing_orders_course_v1"),
        sa.CheckConstraint(
            "status IN ('pending', 'paid', 'failed', 'cancelled', 'refunded')",
            name="ck_billing_orders_status",
        ),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["offer_id"], ["course_offers.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("merchant_order_id"),
    )
    for name, columns in (
        ("ix_billing_orders_id", ["id"]),
        ("ix_billing_orders_user_id", ["user_id"]),
        ("ix_billing_orders_course_id", ["course_id"]),
        ("ix_billing_orders_status", ["status"]),
        ("ix_billing_orders_merchant_order_id", ["merchant_order_id"]),
        ("ix_billing_orders_provider_order_id", ["provider_order_id"]),
        ("ix_billing_orders_user_created", ["user_id", "created_at"]),
        ("ix_billing_orders_course_status", ["course_id", "status"]),
    ):
        op.create_index(name, "billing_orders", columns)
    op.create_index(
        "uq_billing_orders_one_pending_course",
        "billing_orders",
        ["user_id", "course_id"],
        unique=True,
        postgresql_where=sa.text("status = 'pending'"),
    )

    op.create_table(
        "payment_transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("provider_transaction_id", sa.String(length=100), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("pending", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("response_code", sa.String(length=100), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("amount >= 0", name="ck_payment_transactions_amount_nonnegative"),
        sa.ForeignKeyConstraint(["order_id"], ["billing_orders.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider", "provider_transaction_id", name="uq_payment_transactions_provider_id"),
    )
    op.create_index("ix_payment_transactions_id", "payment_transactions", ["id"])
    op.create_index("ix_payment_transactions_order_id", "payment_transactions", ["order_id"])
    op.create_index("ix_payment_transactions_order_created", "payment_transactions", ["order_id", "created_at"])

    op.create_table(
        "course_enrollments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("enrolled_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("source IN ('purchase', 'admin_grant', 'free')", name="ck_course_enrollments_source"),
        sa.CheckConstraint("status IN ('active', 'revoked', 'expired')", name="ck_course_enrollments_status"),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["order_id"], ["billing_orders.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "course_id", name="uq_course_enrollments_user_course"),
    )
    for name, columns in (
        ("ix_course_enrollments_id", ["id"]),
        ("ix_course_enrollments_user_id", ["user_id"]),
        ("ix_course_enrollments_course_id", ["course_id"]),
        ("ix_course_enrollments_order_id", ["order_id"]),
        ("ix_course_enrollments_status", ["status"]),
        ("ix_course_enrollments_user_status", ["user_id", "status"]),
        ("ix_course_enrollments_course_status", ["course_id", "status"]),
    ):
        op.create_index(name, "course_enrollments", columns)


def downgrade() -> None:
    op.drop_table("course_enrollments")
    op.drop_table("payment_transactions")
    op.drop_table("billing_orders")
    op.drop_table("course_offers")
    op.drop_column("lessons", "is_preview")
    op.drop_column("courses", "is_free")
