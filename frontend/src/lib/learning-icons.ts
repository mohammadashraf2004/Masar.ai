import {
  BarChart2, BookOpen, Brain, Code2, Cpu, Eye, Layers, MessageSquare, Mic, Server,
} from 'lucide-react'
import type { ElementType } from 'react'

/**
 * The backend stores an icon *key* on each field and career goal ("brain",
 * "mic"), never a component, so a new field needs no frontend release. This is
 * the one place a key becomes an icon; a key it does not know falls back to a
 * neutral book rather than rendering nothing.
 */
const ICONS: Record<string, ElementType> = {
  'bar-chart': BarChart2,
  brain: Brain,
  code: Code2,
  cpu: Cpu,
  eye: Eye,
  layers: Layers,
  'message-square': MessageSquare,
  mic: Mic,
  server: Server,
}

export function iconFor(key?: string | null): ElementType {
  return (key && ICONS[key]) || BookOpen
}
