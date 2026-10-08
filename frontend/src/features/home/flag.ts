/**
 * Whether `/` shows the designed Home with its mock overview instead of the live "Your
 * Masar" page. The data is invented (a readiness score, a LangGraph lesson at 62%), so
 * it shows in `next dev`, and in a build only when NEXT_PUBLIC_HOME_MOCKS=1 (a demo or
 * staging site). Real learners in production, and the existing tests, keep the live page.
 */
export function homeMocksEnabled(): boolean {
  return process.env.NODE_ENV === 'development' || process.env.NEXT_PUBLIC_HOME_MOCKS === '1'
}
