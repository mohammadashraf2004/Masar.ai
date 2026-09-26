import { StatusPage } from '@/components/layout/StatusPage'

/** Any URL the app has no page for, and any `notFound()` a page raises. */
export default function NotFound() {
  return <StatusPage code="404" title="err.notFound.title" body="err.notFound.body" />
}
