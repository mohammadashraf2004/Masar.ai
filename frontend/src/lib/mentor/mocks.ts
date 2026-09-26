/**
 * The mentor page is built against three things the backend does not provide yet: a daily
 * message quota by plan, a score for each interview answer, and saved interviews (see
 * docs/backend-requests.md, "AI mentor and mock interview"). Each has a stand-in with "Mock" in
 * its name (`MockMentorQuota`, `MockAnswerScorer`, `MockInterviewStore`), so that the whole
 * screen can be built and checked without them.
 *
 * Two of them make a claim the product would be embarrassed by if it were mistaken for real: a
 * plan limit and a score. Those two are on only in development, or where a build opts in with
 * NEXT_PUBLIC_MENTOR_MOCKS=1 (a demo, a staging site). In a production build the page shows no
 * quota and no scores rather than made-up ones. The interview store is not a claim, only
 * storage in this browser, so it is on everywhere.
 */
export function mentorMocksEnabled(): boolean {
  return process.env.NODE_ENV !== 'production' || process.env.NEXT_PUBLIC_MENTOR_MOCKS === '1'
}
