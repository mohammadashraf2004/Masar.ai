import type { ComponentType } from 'react'
import type { BillingCycle, CartItem, PaymentMethodId } from '@/lib/billing/types'
import { MockPaymentProvider, mockOutcomeFromUrl } from '@/lib/billing/mockPayments'
import { PaymobProvider } from '@/lib/billing/paymobProvider'

/**
 * The seam between the billing page and whatever takes the money.
 *
 * No gateway has been chosen. The page talks only to `PaymentProvider`; the one
 * implementation in use is `MockPaymentProvider`, which moves no money. `PaymobProvider` is a
 * stub for the gateway the backend already integrates: it lists its methods and throws "not
 * configured" for everything else, and is deliberately NOT returned below. A real gateway is
 * one implementation of this interface plus one line in `getPaymentProvider`, and nothing in
 * the page changes.
 *
 * Card data never touches a field of ours: a provider that takes cards supplies the
 * `CardFields` component (its own hosted fields), and the page mounts it.
 */

export interface PaymentRequest {
  cart: CartItem
  cycle: BillingCycle
  method: PaymentMethodId
  /** What is charged, in `currency`, VAT included. */
  amount: number
  currency: string
  /** A promo code the server has already accepted, if one was applied. */
  promoCode: string | null
}

export type PaymentFailure = 'declined' | 'cancelled' | 'unavailable'

export type PaymentResult =
  | { status: 'paid'; invoiceId: string }
  | { status: 'redirect'; url: string }
  | { status: 'failed'; reason: PaymentFailure }

/** What the success page shows about a payment that went through. */
export interface PaymentReceipt {
  invoiceId: string
  cart: CartItem
  cycle: BillingCycle
  amount: number
  currency: string
  method: PaymentMethodId
  paidAt: string
}

export interface CardFieldsProps {
  /** Tells the page whether the card can be submitted yet. Must be called with a stable identity. */
  onReadyChange: (ready: boolean) => void
}

export interface PaymentProvider {
  readonly id: string
  /** True for a provider that moves no money: the page says so, so nobody mistakes it. */
  readonly isMock: boolean
  /** The methods this provider can take, in the order to show them. Asked, not assumed: a gateway
   *  decides what it supports (and could vary it by account), so the page keeps no list of its own. */
  listMethods(): Promise<readonly PaymentMethodId[]>
  pay(request: PaymentRequest): Promise<PaymentResult>
  /** After a gateway redirect or webhook, the success page asks what the invoice was. */
  getReceipt(invoiceId: string): Promise<PaymentReceipt | null>
  downloadInvoice(invoiceId: string): Promise<void>
  /** The provider's hosted card fields. Absent when the provider takes no cards. */
  readonly CardFields?: ComponentType<CardFieldsProps>
}

/**
 * The provider in use, or null when payments are not open.
 *
 * The mock is available in development and, in a production build, only when
 * `NEXT_PUBLIC_PAYMENTS_MOCK=1` is set on purpose (a staging site). A production build
 * with no gateway and no such switch has NO provider, and the page says payments are not
 * open yet instead of showing "payment successful" for a payment that never happened.
 */
export function getPaymentProvider(): PaymentProvider | null {
  if (process.env.NEXT_PUBLIC_PAYMENTS_PROVIDER === 'paymob') return new PaymobProvider()
  const mockAllowed = process.env.NODE_ENV !== 'production' || process.env.NEXT_PUBLIC_PAYMENTS_MOCK === '1'
  return mockAllowed ? new MockPaymentProvider({ outcome: mockOutcomeFromUrl }) : null
}
