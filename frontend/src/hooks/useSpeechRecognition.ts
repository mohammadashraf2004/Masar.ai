'use client'
import { useCallback, useEffect, useRef, useState, useSyncExternalStore } from 'react'

// TypeScript's DOM types do not include the Web Speech API, so the little of it this uses is
// described here.
interface RecognitionResult {
  isFinal: boolean
  0: { transcript: string }
}
interface RecognitionEvent {
  resultIndex: number
  results: ArrayLike<RecognitionResult>
}
interface Recognition {
  lang: string
  continuous: boolean
  interimResults: boolean
  onresult: ((event: RecognitionEvent) => void) | null
  onerror: ((event: { error?: string }) => void) | null
  onend: (() => void) | null
  start(): void
  stop(): void
  abort(): void
}
type RecognitionConstructor = new () => Recognition

function constructor(): RecognitionConstructor | null {
  if (typeof window === 'undefined') return null
  const w = window as unknown as { SpeechRecognition?: RecognitionConstructor; webkitSpeechRecognition?: RecognitionConstructor }
  return w.SpeechRecognition ?? w.webkitSpeechRecognition ?? null
}

const noSubscription = () => () => {}

/**
 * Whether this browser can turn speech into text. False on the server and on the first client
 * render (so both agree), then the real answer. Firefox has no Web Speech API at all, and the
 * interview's microphone control is hidden there rather than shown and broken.
 */
export function useSpeechSupported(): boolean {
  return useSyncExternalStore(noSubscription, () => constructor() !== null, () => false)
}

export type SpeechProblem = 'denied' | 'none' | 'error'

function problemOf(code: string | undefined): SpeechProblem | null {
  if (code === 'not-allowed' || code === 'service-not-allowed') return 'denied'
  if (code === 'audio-capture') return 'none'
  // No speech was heard, or the learner stopped it: not a problem to report.
  if (code === 'no-speech' || code === 'aborted') return null
  return 'error'
}

interface Options {
  /** BCP 47, e.g. `ar-SA` or `en-US`. */
  lang: string
  /** Each finished phrase, as the browser hears it. */
  onText: (text: string) => void
}

/**
 * Dictation into a text box. Chrome and Safari send the audio to the browser vendor's speech
 * service, which the interview's setup step says so the learner can decide.
 *
 * Only finished phrases are reported, so the box never has text in it that then changes under
 * the learner's cursor.
 */
export function useSpeechRecognition({ lang, onText }: Options) {
  const supported = useSpeechSupported()
  const [listening, setListening] = useState(false)
  const [problem, setProblem] = useState<SpeechProblem | null>(null)
  const recognition = useRef<Recognition | null>(null)
  const onTextRef = useRef(onText)
  useEffect(() => {
    onTextRef.current = onText
  })

  const stop = useCallback(() => {
    recognition.current?.stop()
  }, [])

  const start = useCallback(() => {
    const Ctor = constructor()
    if (!Ctor || recognition.current) return
    const next = new Ctor()
    next.lang = lang
    next.continuous = true
    next.interimResults = false
    next.onresult = (event) => {
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i]
        if (result.isFinal) onTextRef.current(result[0].transcript.trim())
      }
    }
    next.onerror = (event) => {
      setProblem(problemOf(event.error))
    }
    next.onend = () => {
      recognition.current = null
      setListening(false)
    }
    recognition.current = next
    setProblem(null)
    try {
      next.start()
      setListening(true)
    } catch {
      recognition.current = null
      setProblem('error')
    }
  }, [lang])

  useEffect(
    () => () => {
      const active = recognition.current
      if (active) {
        active.onend = null
        active.onerror = null
        active.onresult = null
        active.abort()
        recognition.current = null
      }
    },
    [],
  )

  return { supported, listening, problem, start, stop }
}
