'use client'
import { useEffect, useRef } from 'react'
import { Video, VideoOff } from 'lucide-react'
import { MasarMark } from '@/components/brand/MasarMark'
import { Button } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/index'
import type { Camera, CameraState } from '@/hooks/useCamera'
import { useI18n, type StringKey } from '@/lib/i18n'

const TILE = 'relative aspect-[16/10] overflow-hidden rounded-[10px] border border-border bg-panel'
const LABEL = 'absolute bottom-2.5 start-2.5 rounded-md bg-scrim/70 px-2 py-1 text-xs font-medium text-[#F7FAFC]'

const MESSAGE: Record<Exclude<CameraState, 'on'>, StringKey> = {
  idle: 'interview.cam.idle',
  pending: 'interview.cam.pending',
  denied: 'interview.cam.denied',
  none: 'interview.cam.none',
  unsupported: 'interview.cam.unsupported',
  error: 'interview.cam.error',
}

/**
 * The learner's own tile: the live camera, or, in each of the states it cannot be, a sentence
 * saying why and (where trying again can help) a button to do so. Not having a camera never
 * stops the interview: every state but `on` leaves the answer box and controls usable.
 */
export function CameraTile({ camera, label }: { camera: Camera; label: string }) {
  const { t } = useI18n()
  const video = useRef<HTMLVideoElement>(null)
  const { state, stream } = camera

  useEffect(() => {
    const el = video.current
    if (el) el.srcObject = stream
  }, [stream, state])

  if (state === 'on') {
    return (
      <div className={TILE} data-camera="on">
        {/* Mirrored, like every self-view: the learner's left is the left of the picture. */}
        <video
          ref={video}
          autoPlay
          playsInline
          muted
          aria-label={t('interview.cam.tile')}
          className="h-full w-full -scale-x-100 object-cover"
        />
        <span className={LABEL}>{label}</span>
      </div>
    )
  }

  const canRetry = state === 'idle' || state === 'denied' || state === 'error'
  return (
    <div className={TILE} data-camera={state}>
      <div className="flex h-full flex-col items-center justify-center gap-2.5 p-4 text-center">
        {state === 'pending' ? (
          <Spinner className="h-5 w-5" />
        ) : state === 'idle' ? (
          <Video size={22} aria-hidden="true" className="text-ghost" />
        ) : (
          <VideoOff size={22} aria-hidden="true" className="text-ghost" />
        )}
        <p role={state === 'denied' || state === 'error' ? 'alert' : 'status'} className="max-w-[24ch] text-[13px] leading-snug text-dim sm:max-w-[32ch]">
          {t(MESSAGE[state])}
        </p>
        {canRetry && (
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => void camera.request()}
          >
            {t(state === 'idle' ? 'interview.check.cameraBtn' : 'interview.cam.retry')}
          </Button>
        )}
      </div>
      <span className={LABEL}>{label}</span>
    </div>
  )
}

/**
 * The interviewer's tile. `busy` makes the halo breathe: there is no synthetic voice, so the
 * only time the interviewer is "doing something" is while it prepares the next question.
 */
export function InterviewerTile({ busy, label }: { busy: boolean; label: string }) {
  return (
    <div
      className={`${TILE} grid place-items-center`}
      style={{ backgroundImage: 'radial-gradient(60% 60% at 50% 50%, rgb(var(--acc) / var(--acc-soft-a)), transparent 70%)' }}
      data-busy={busy ? 'true' : 'false'}
    >
      <span
        aria-hidden="true"
        className={`grid h-16 w-16 place-items-center rounded-[14px] bg-amber text-on-amber shadow-[0_0_0_8px_rgb(var(--acc)/var(--acc-soft-a))] ${busy ? 'animate-masarHalo motion-reduce:animate-none' : ''}`}
      >
        <MasarMark size={30} />
      </span>
      <span className={LABEL}>{label}</span>
    </div>
  )
}
