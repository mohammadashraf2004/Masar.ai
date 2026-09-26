'use client'
import { useCallback, useEffect, useRef, useState } from 'react'

/**
 * idle        : not asked for yet
 * pending     : the browser's permission prompt is open
 * on          : `stream` is live
 * denied      : the learner (or the site's policy) said no
 * none        : no camera on this device
 * unsupported : the browser has no `getUserMedia` (or the page is not a secure context)
 * error       : anything else, most often another app already holding the camera
 */
export type CameraState = 'idle' | 'pending' | 'on' | 'denied' | 'none' | 'unsupported' | 'error'

/** What a failed `getUserMedia` call means for the learner, by the error's name. */
export function cameraFailure(error: unknown): Exclude<CameraState, 'idle' | 'pending' | 'on'> {
  const name = (error as { name?: string } | null)?.name
  if (name === 'NotAllowedError' || name === 'SecurityError' || name === 'PermissionDeniedError') return 'denied'
  if (name === 'NotFoundError' || name === 'DevicesNotFoundError' || name === 'OverconstrainedError') return 'none'
  return 'error'
}

function stopStream(stream: MediaStream | null) {
  stream?.getTracks().forEach((track) => track.stop())
}

/**
 * The learner's camera, for the interview's "you" tile. Nothing is asked for until `request()`:
 * the setup step calls it from a button, so the browser's prompt follows a click and not a page
 * load. The stream is stopped when the component using this goes away.
 */
export function useCamera({ resumeIfGranted = false }: { resumeIfGranted?: boolean } = {}) {
  const [state, setState] = useState<CameraState>('idle')
  const [stream, setStream] = useState<MediaStream | null>(null)
  const current = useRef<MediaStream | null>(null)
  // Bumped by every request and by unmount, so an answer that arrives late is dropped.
  const ticket = useRef(0)

  const stop = useCallback(() => {
    ticket.current += 1
    stopStream(current.current)
    current.current = null
    setStream(null)
    setState('idle')
  }, [])

  const request = useCallback(async () => {
    const devices = typeof navigator === 'undefined' ? undefined : navigator.mediaDevices
    if (!devices || typeof devices.getUserMedia !== 'function') {
      setState('unsupported')
      return
    }
    const mine = ++ticket.current
    setState('pending')
    try {
      const next = await devices.getUserMedia({ video: { facingMode: 'user' }, audio: false })
      if (mine !== ticket.current) {
        stopStream(next)
        return
      }
      stopStream(current.current)
      current.current = next
      setStream(next)
      setState('on')
    } catch (error) {
      if (mine !== ticket.current) return
      setState(cameraFailure(error))
    }
  }, [])

  useEffect(
    () => () => {
      ticket.current += 1
      stopStream(current.current)
      current.current = null
    },
    [],
  )

  // The interview page comes after the setup step, where the learner already said yes: start the
  // camera again when the browser remembers that, and never when it would have to ask (a prompt
  // with no click before it). Browsers without the Permissions API just wait for the button.
  useEffect(() => {
    if (!resumeIfGranted) return
    let alive = true
    try {
      void navigator.permissions
        ?.query({ name: 'camera' as PermissionName })
        .then((status) => {
          if (alive && status.state === 'granted') void request()
        })
        .catch(() => {})
    } catch {
      // No Permissions API, or it does not know "camera".
    }
    return () => {
      alive = false
    }
  }, [resumeIfGranted, request])

  return { state, stream, request, stop }
}

export type Camera = ReturnType<typeof useCamera>
