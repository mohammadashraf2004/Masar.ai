import { redirect } from 'next/navigation'

/** Legacy learner-facing route. Tracks replaced Paths. */
export default function LegacyPathsPage(): never {
  return redirect('/tracks')
}
