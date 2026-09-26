/** What the backend charges for one mentor chat message (`mentor_chat` in wallet_service). */
export const MENTOR_MESSAGE_CREDITS = 2

/**
 * Whether a balance cannot pay for another message. `null` (balance not known: still loading, or
 * the request failed) is not "out": the composer stays, and the backend's 402 is the real answer.
 */
export function cannotAffordMessage(balance: number | null, spent = 0): boolean {
  return balance !== null && balance - spent < MENTOR_MESSAGE_CREDITS
}
