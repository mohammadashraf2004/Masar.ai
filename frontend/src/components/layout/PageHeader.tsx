import { cn } from '@/lib/utils'

interface PageHeaderProps {
  title: string
  subtitle?: string
  action?: React.ReactNode
  className?: string
}

export function PageHeader({ title, subtitle, action, className }: PageHeaderProps) {
  return (
    <div className={cn('flex items-start justify-between px-8 pt-7 pb-6 border-b border-border shrink-0', className)}>
      <div>
        <h1 className="font-display font-700 text-xl text-white tracking-tight">{title}</h1>
        {subtitle && <p className="text-sm text-ghost mt-0.5">{subtitle}</p>}
      </div>
      {action && <div className="ml-4 shrink-0">{action}</div>}
    </div>
  )
}
