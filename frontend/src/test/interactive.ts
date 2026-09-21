import { expect } from 'vitest'

/**
 * A navigation control done right: an <a> with the shared button look on it,
 * holding nothing focusable. (`<Link><Button/></Link>` gives two tab stops for
 * one control and a button announced inside a link.)
 */
export function expectLinkStyledAsButton(link: HTMLElement, href: string) {
  expect(link.tagName).toBe('A')
  expect(link).toHaveAttribute('href', href)
  expect(link.querySelector('a, button, input, select, textarea, summary, [role="button"], [tabindex]')).toBeNull()
  // buttonStyles(): the same touch target the real <Button> has below `lg`.
  expect(link.className).toContain('min-h-[44px]')
}

/** The arrow inside it mirrors in a right-to-left page. */
export function expectMirroredArrow(link: HTMLElement) {
  const arrow = link.querySelector('svg')
  expect(arrow).not.toBeNull()
  expect(arrow!.getAttribute('class')).toContain('rtl:rotate-180')
}
