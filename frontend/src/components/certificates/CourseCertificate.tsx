import type { CSSProperties } from 'react'
import { QRCodeSVG } from 'qrcode.react'
import { MasarMark } from '@/components/brand/MasarMark'
import { cn } from '@/lib/utils'
import { formatIssued } from '@/lib/certificates'

/**
 * The Masar certificate (handoff README §9): one component for the page, the print
 * export and the public /verify/[id] page.
 *
 * English only and left-to-right whatever the page around it is, so it is
 * `dir="ltr" lang="en"` and none of its words are in `lib/i18n`. Every size is in
 * container-query units (`cqw`, a hundredth of the certificate's own width), so the
 * same markup fills a phone, a desktop card and a 297mm A4 page. It follows the
 * theme through `--cert`; the seal and QR block are amber and paper in both.
 *
 * One component, two wordings, chosen by `variant` (the page picks one; there are not
 * two components):
 *   - `course` (the default): CERTIFICATE OF COMPLETION for a finished course, with its
 *     parent track and, in the info row, Date issued + Course duration.
 *   - `exam`: PROFESSIONAL CERTIFICATION for a passed proctored career exam, with Date
 *     issued + Exam score in the info row. This is what the API can issue today.
 * The info row is always exactly two cells and nothing else goes in it. A cell whose value
 * the caller does not have (no duration, no score) is left out, never filled with a guess.
 */

interface CommonProps {
  /** The holder's name. The certificate is English, so a Latin-script name reads best;
   *  an Arabic-only name is printed as given (there is no transliteration field yet). */
  recipient: string
  title: string
  certificateId: string
  issuedAt: string
  /** What the QR code encodes. */
  verifyUrl: string
  className?: string
}

export type CourseCertificateProps = CommonProps &
  (
    | {
        variant?: 'course'
        /** The career track the course belongs to. */
        trackTitle?: string
        /** How long the course is. */
        durationHours?: number
        examScore?: never
      }
    | {
        variant: 'exam'
        /** The score out of 100. */
        examScore?: number
        trackTitle?: never
        durationHours?: never
      }
  )

const COPY = {
  course: {
    label: 'CERTIFICATE OF COMPLETION',
    lead: 'for completing every lesson, exercise and graded project of',
    band: 'COURSE · CERTIFICATE',
  },
  exam: {
    label: 'PROFESSIONAL CERTIFICATION',
    lead: 'for passing the proctored certification exam for',
    band: 'CAREER · CERTIFICATE',
  },
} as const

// Theme tokens are space-separated RGB channels (see globals.css), so each is wrapped once here.
const rgb = (token: string, alpha?: string) => `rgb(var(--${token})${alpha ? ` / ${alpha}` : ''})`
const C = {
  cert: rgb('cert'),
  line: rgb('line'),
  card2: rgb('card2'),
  head: rgb('head'),
  text: rgb('text'),
  mute: rgb('mute'),
  faint: rgb('faint'),
  acc: rgb('acc'),
  accText: rgb('acc-text'),
  accSoft: rgb('acc', 'var(--acc-soft-a)'),
  ink: rgb('on-acc'),
  inkSoft: rgb('on-acc', '0.45'),
}

const mono = 'font-mono'
const display = 'font-display'

export function CourseCertificate({
  recipient,
  title,
  certificateId,
  issuedAt,
  verifyUrl,
  variant = 'course',
  trackTitle,
  durationHours,
  examScore,
  className,
}: CourseCertificateProps) {
  const copy = COPY[variant]
  const idUpper = certificateId.toUpperCase()
  const shortId = certificateId.replace(/-/g, '').slice(0, 8).toUpperCase()
  const issued = new Date(issuedAt)
  const year = Number.isNaN(issued.getTime()) ? '' : String(issued.getUTCFullYear())
  const host = verifyUrl.replace(/^https?:\/\//, '').split('/')[0]

  const cell: CSSProperties = {
    position: 'relative', display: 'flex', flexDirection: 'column', justifyContent: 'flex-end',
    gap: '0.7cqw', paddingTop: '1.5cqw', minWidth: 0,
  }
  const tick: CSSProperties = { position: 'absolute', top: -1, left: 0, width: '2.4cqw', height: 2, background: C.acc }
  const cellLabel: CSSProperties = {
    fontSize: '0.9cqw', letterSpacing: '0.16em', textTransform: 'uppercase', whiteSpace: 'nowrap', color: C.mute,
  }

  return (
    // `certificate-root` is what the print rules in globals.css keep on the page.
    <div
      dir="ltr"
      lang="en"
      className={cn('certificate-root w-full', className)}
      style={{ containerType: 'inline-size' }}
    >
      <div
        style={{
          position: 'relative', aspectRatio: '1.414', background: C.cert, border: `1px solid ${C.line}`,
          borderRadius: '1cqw', overflow: 'hidden', display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 25cqw 3cqw',
          printColorAdjust: 'exact', WebkitPrintColorAdjust: 'exact',
        }}
        className="font-sans"
      >
        {/* Dot grid: clear behind the text, denser toward the seal. */}
        <div
          aria-hidden="true"
          style={{
            position: 'absolute', inset: 0, pointerEvents: 'none', opacity: 0.55,
            backgroundImage: `radial-gradient(circle, ${C.faint} 0.09cqw, transparent 0.12cqw)`,
            backgroundSize: '1.5cqw 1.5cqw', backgroundPosition: '0.75cqw 0.75cqw',
            WebkitMaskImage: 'linear-gradient(100deg, transparent 20%, #000 75%)',
            maskImage: 'linear-gradient(100deg, transparent 20%, #000 75%)',
          }}
        />

        {/* ── Left column ── */}
        <div
          style={{
            position: 'relative', padding: '5cqw 3.4cqw 4.6cqw 4.6cqw', display: 'flex',
            flexDirection: 'column', justifyContent: 'space-between', minWidth: 0,
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '2cqw' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1cqw' }}>
              <div
                aria-hidden="true"
                style={{ width: '3.2cqw', height: '3.2cqw', borderRadius: '0.7cqw', background: C.acc, display: 'grid', placeItems: 'center', flex: 'none', color: C.ink }}
              >
                <MasarMark style={{ width: '1.7cqw', height: '1.7cqw' }} />
              </div>
              <span className={display} style={{ fontWeight: 700, fontSize: '1.9cqw', color: C.head }}>Masar</span>
            </div>
            <span
              className={mono}
              style={{ fontSize: '1.05cqw', letterSpacing: '0.12em', color: C.mute, minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}
            >
              NO. {idUpper}
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1cqw', minWidth: 0 }}>
            <span className={mono} style={{ fontSize: '1.2cqw', letterSpacing: '0.34em', color: C.accText }}>{copy.label}</span>
            <span style={{ fontSize: '1.6cqw', color: C.mute, marginTop: '1.6cqw' }}>Awarded to</span>
            <span
              className={display}
              style={{
                fontWeight: 800, fontSize: '5cqw', lineHeight: 1, letterSpacing: '-0.03em', whiteSpace: 'nowrap',
                color: C.head, overflow: 'hidden', textOverflow: 'ellipsis', paddingBottom: '0.4cqw',
              }}
            >
              {recipient}
            </span>
            <span style={{ fontSize: '1.6cqw', color: C.mute, marginTop: '1.8cqw' }}>{copy.lead}</span>
            <span className={display} style={{ fontWeight: 700, fontSize: '3cqw', lineHeight: 1.15, color: C.accText }}>{title}</span>
            {variant === 'course' && trackTitle && (
              <span style={{ fontSize: '1.4cqw', color: C.text }}>A core course of the {trackTitle} career track</span>
            )}
          </div>

          {/* Two cells at most, and nothing else goes in this row. */}
          <div style={{ display: 'grid', gridTemplateColumns: 'max-content max-content', columnGap: '8cqw', alignItems: 'stretch', borderTop: `1px solid ${C.line}` }}>
            <div style={cell}>
              <span aria-hidden="true" style={tick} />
              <span className={mono} style={cellLabel}>Date issued</span>
              <span className={display} style={{ fontWeight: 700, fontSize: '2.2cqw', lineHeight: 1, color: C.head, whiteSpace: 'nowrap' }}>
                {formatIssued(issuedAt)}
              </span>
            </div>
            {variant === 'course' && durationHours !== undefined && (
              <div style={cell}>
                <span aria-hidden="true" style={tick} />
                <span className={mono} style={cellLabel}>Course duration</span>
                <span style={{ display: 'flex', alignItems: 'baseline', gap: '0.5cqw', whiteSpace: 'nowrap' }}>
                  <span className={display} style={{ fontWeight: 700, fontSize: '2.2cqw', lineHeight: 1, color: C.head }}>{Math.round(durationHours)}</span>
                  <span className={mono} style={{ fontSize: '1cqw', color: C.faint }}>hours</span>
                </span>
              </div>
            )}
            {variant === 'exam' && examScore !== undefined && (
              <div style={cell}>
                <span aria-hidden="true" style={tick} />
                <span className={mono} style={cellLabel}>Exam score</span>
                <span style={{ display: 'flex', alignItems: 'baseline', gap: '0.5cqw', whiteSpace: 'nowrap' }}>
                  <span className={display} style={{ fontWeight: 700, fontSize: '2.2cqw', lineHeight: 1, color: C.head }}>{Math.round(examScore)}</span>
                  <span className={mono} style={{ fontSize: '1cqw', color: C.faint }}>/100</span>
                </span>
              </div>
            )}
          </div>
        </div>

        {/* ── Signature band: the mark's two rails, and its node made large as a seal ── */}
        <div
          style={{
            position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center',
            justifyContent: 'space-between', padding: '4.6cqw 0 4.2cqw', background: C.accSoft,
          }}
        >
          <span aria-hidden="true" style={{ position: 'absolute', top: 0, bottom: 0, left: '3.4cqw', width: 1, background: C.acc }} />
          <span aria-hidden="true" style={{ position: 'absolute', top: 0, bottom: 0, right: '3.4cqw', width: 1, background: C.acc }} />

          <span
            className={mono}
            style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)', fontSize: '1.1cqw', letterSpacing: '0.42em', color: C.accText }}
          >
            {copy.band}
          </span>

          <div
            aria-hidden="true"
            style={{
              position: 'relative', width: '15cqw', height: '15cqw', borderRadius: '50%', background: C.acc,
              // The gap ring is what cuts the two rails where the seal sits.
              boxShadow: `0 0 0 1.2cqw ${C.cert}, 0 0 0 1.35cqw ${C.acc}`,
              display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '0.8cqw', color: C.ink,
            }}
          >
            <span style={{ position: 'absolute', inset: '1cqw', borderRadius: '50%', border: `1px dashed ${C.inkSoft}` }} />
            <MasarMark style={{ width: '4cqw', height: '4cqw' }} />
            <span className={mono} style={{ fontWeight: 500, fontSize: '1.05cqw', letterSpacing: '0.3em', paddingLeft: '0.3em' }}>VERIFIED</span>
            <span style={{ width: '5cqw', height: 1, background: rgb('on-acc', '0.4') }} />
            <span className={mono} style={{ fontSize: '0.9cqw', letterSpacing: '0.18em' }}>{shortId}{year && ` · ${year}`}</span>
          </div>

          <div
            style={{
              position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.9cqw',
              background: C.cert, padding: '1cqw 0.8cqw', border: `1px solid ${C.line}`, borderRadius: '0.5cqw',
            }}
          >
            {/* Dark modules on a white square in both themes: a QR code is unreliable inverted. */}
            <div style={{ width: '7.4cqw', height: '7.4cqw', background: '#FFFFFF', borderRadius: '0.3cqw', overflow: 'hidden' }}>
              <QRCodeSVG
                value={verifyUrl}
                size={148}
                level="M"
                marginSize={1}
                bgColor="#FFFFFF"
                fgColor="#080A0E"
                title="QR code: verify this certificate"
                style={{ display: 'block', width: '100%', height: '100%' }}
              />
            </div>
            <span className={mono} style={{ fontSize: '0.9cqw', color: C.text }}>{host}/verify/{shortId}…</span>
          </div>
        </div>
      </div>
    </div>
  )
}
