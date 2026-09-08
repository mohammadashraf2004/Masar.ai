// react-simple-code-editor ships no TypeScript declarations and there's
// no @types package for it — minimal hand-written types covering the
// props actually used in this project (see components/ui/CodeCell.tsx).
declare module 'react-simple-code-editor' {
  import { ComponentType, CSSProperties, ReactNode } from 'react'

  export interface EditorProps {
    value: string
    onValueChange: (value: string) => void
    highlight: (code: string) => string | ReactNode
    tabSize?: number
    insertSpaces?: boolean
    ignoreTabKey?: boolean
    padding?: number | string
    style?: CSSProperties
    className?: string
    textareaClassName?: string
    preClassName?: string
    placeholder?: string
    autoFocus?: boolean
    disabled?: boolean
    onKeyDown?: (e: React.KeyboardEvent) => void
    [key: string]: unknown
  }

  const Editor: ComponentType<EditorProps>
  export default Editor
}

declare module 'prismjs/components/prism-core' {
  export function highlight(code: string, grammar: unknown, language: string): string
  export const languages: Record<string, unknown>
}

declare module 'prismjs/components/prism-clike'
declare module 'prismjs/components/prism-python'
