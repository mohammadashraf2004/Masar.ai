'use client'
import { useCallback, useEffect, useRef, useState } from 'react'

/** idle: not tried. testing: the prompt is open. ok: a microphone answered. The rest say why not. */
export type MicCheck = 'idle' | 'testing' | 'ok' | 'denied' | 'none' | 'error'

/**
 * A one-shot "does the microphone work" check for the setup step: it opens the microphone, and
 * closes it again at once. Dictation itself is the browser's speech service and does not use
 * this stream; the check only settles the permission and the device before the interview starts.
 */
export function useMicCheck() {
  const [state, setState] = useState<MicCheck>('idle')
  const alive = useRef(true)

  useEffect(() => {
    alive.current = true
    return () => {
      alive.current = false
    }
  }, [])

  const test = useCallback(async () => {
    const devices = typeof navigator === 'undefined' ? undefined : navigator.mediaDevices
    if (!devices || typeof devices.getUserMedia !== 'function') {
      setState('error')
      return
    }
    setState('testing')
    try {
      const stream = await devices.getUserMedia({ audio: true, video: false })
      stream.getTracks().forEach((track) => track.stop())
      if (alive.current) setState('ok')
    } catch (error) {
      if (!alive.current) return
      const name = (error as { name?: string } | null)?.name
      if (name === 'NotAllowedError' || name === 'SecurityError' || name === 'PermissionDeniedError') setState('denied')
      else if (name === 'NotFoundError' || name === 'DevicesNotFoundError') setState('none')
      else setState('error')
    }
  }, [])

  return { state, test }
}
