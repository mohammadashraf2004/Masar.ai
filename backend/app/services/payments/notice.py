"""A verified provider callback, in one shape for every provider.

Settlement (subscriptions, course purchases, wallet top-ups, exam fees) reads only
this, so the same rules apply whichever provider took the money: Kashier for new
payments, Paymob for the orders it took before the switch (their payments and
refunds still reconcile). Each provider's adapter builds a notice only from a
callback whose signature it has verified.
"""
from dataclasses import dataclass, field
from typing import Literal, Optional

Kind = Literal["payment", "reversal", "authorization"]


@dataclass(frozen=True)
class PaymentNotice:
    provider: str                       # "kashier" | "paymob"
    event_id: str                       # the provider's transaction id: unique per provider
    merchant_order_id: str              # our order reference, as sent at checkout
    provider_order_id: Optional[str]    # what binds the callback to our row (Kashier session / Paymob order)
    amount: int                         # minor units (piasters); -1 when unreadable
    currency: str
    success: bool
    pending: bool
    kind: Kind                          # only "payment" may ever grant
    response_code: Optional[str] = None
    raw: dict = field(default_factory=dict)

    def binds(self, provider_order_id: Optional[str]) -> bool:
        """Whether this notice is for the row whose provider order id is given."""
        return (provider_order_id is not None and self.provider_order_id is not None
                and str(self.provider_order_id) == str(provider_order_id))

    @property
    def settles(self) -> bool:
        return self.success and not self.pending and self.kind == "payment"
