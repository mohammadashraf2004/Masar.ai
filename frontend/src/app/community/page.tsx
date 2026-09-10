'use client'
import { useCallback, useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { cn, formatRelative, safeUrl } from '@/lib/utils'
import axios from 'axios'
import {
  Heart, MessageCircle, Github, Trophy,
  Plus, X, ChevronDown, ChevronUp,
  Flame, Lightbulb, FolderKanban, Star, BookOpen,
  Send, Users
} from 'lucide-react'

// ─── Types ────────────────────────────────────────────────────────────────────
type PostType = 'problem' | 'project' | 'achievement' | 'resource' | 'discussion'

interface Author {
  id: number
  full_name: string
  experience_level: string
  overall_readiness_score: number
  avatar_url?: string
}

interface Comment {
  id: number
  author: Author
  content: string
  created_at: string
}

interface Post {
  id: number
  post_type: PostType
  title: string
  content: string
  github_url?: string
  tags: string[]
  likes_count: number
  comments_count: number
  created_at: string
  author: Author
  liked_by_me: boolean
  comments: Comment[]
}

interface LeaderboardEntry {
  rank: number
  user: Author
  posts_count: number
  likes_received: number
  readiness_score: number
}

// ─── Axios instance — reuses the same auth token as the rest of the app ───────
const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

function getToken(): string {
  if (typeof window === 'undefined') return ''
  try {
    const raw = localStorage.getItem('auth-storage')
    if (!raw) return ''
    return JSON.parse(raw)?.state?.token ?? ''
  } catch { return '' }
}

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

const http = axios.create({ baseURL: BASE })
http.interceptors.request.use(config => {
  const token = getToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// ─── API calls ────────────────────────────────────────────────────────────────
async function fetchFeed(type?: PostType, page = 1) {
  const params: Record<string, string> = { page: String(page), per_page: '20' }
  if (type) params.post_type = type
  const res = await http.get<{ posts: Post[]; total: number }>('/community/feed', { params })
  return res.data
}

async function createPost(data: {
  post_type: PostType; title: string; content: string
  github_url?: string; tags: string[]
}) {
  const res = await http.post<Post>('/community/posts', data)
  return res.data
}

async function toggleLike(postId: number) {
  const res = await http.post<{ liked: boolean; likes_count: number }>(
    `/community/posts/${postId}/like`
  )
  return res.data
}

async function addComment(postId: number, content: string) {
  const res = await http.post<Comment>(`/community/posts/${postId}/comments`, { content })
  return res.data
}

async function fetchLeaderboard() {
  const res = await http.get<{ entries: LeaderboardEntry[] }>('/community/leaderboard')
  return res.data
}

// ─── Config ───────────────────────────────────────────────────────────────────
const POST_TYPES: Record<PostType, {
  label: string; icon: React.ElementType; color: string; bg: string
}> = {
  problem:     { label: 'Problem',     icon: Flame,        color: 'text-rose',    bg: 'bg-rose/10 border-rose/20' },
  project:     { label: 'Project',     icon: FolderKanban, color: 'text-sky',     bg: 'bg-sky/10 border-sky/20' },
  achievement: { label: 'Achievement', icon: Star,         color: 'text-amber',   bg: 'bg-amber/10 border-amber/20' },
  resource:    { label: 'Resource',    icon: Lightbulb,    color: 'text-emerald', bg: 'bg-emerald/10 border-emerald/20' },
  discussion:  { label: 'Discussion',  icon: BookOpen,     color: 'text-violet',  bg: 'bg-violet/10 border-violet/20' },
}

// ─── Avatar ───────────────────────────────────────────────────────────────────
function Avatar({ user, size = 'sm' }: { user: Author; size?: 'sm' | 'md' | 'lg' }) {
  const s = size === 'lg' ? 'w-10 h-10 text-sm'
          : size === 'md' ? 'w-8 h-8 text-xs'
          : 'w-6 h-6 text-xs'
  return (
    <div className={cn(
      s, 'rounded-full bg-amber/10 border border-amber/20 flex items-center justify-center shrink-0 font-medium text-amber'
    )}>
      {user.full_name.charAt(0).toUpperCase()}
    </div>
  )
}

// ─── Post card ────────────────────────────────────────────────────────────────
function PostCard({ post, onUpdate }: { post: Post; onUpdate: (p: Post) => void }) {
  const [expanded, setExpanded] = useState(false)
  const [commenting, setCommenting] = useState(false)
  const [commentText, setCommentText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const meta = POST_TYPES[post.post_type]
  const Icon = meta.icon

  async function handleLike() {
    try {
      const res = await toggleLike(post.id)
      onUpdate({ ...post, liked_by_me: res.liked, likes_count: res.likes_count })
    } catch {}
  }

  async function handleComment(e: React.FormEvent) {
    e.preventDefault()
    if (!commentText.trim()) return
    setSubmitting(true)
    try {
      const comment = await addComment(post.id, commentText)
      onUpdate({
        ...post,
        comments: [...post.comments, comment],
        comments_count: post.comments_count + 1,
      })
      setCommentText('')
      setExpanded(true)
    } catch {}
    setSubmitting(false)
  }

  return (
    <Card className="p-5 hover:border-muted transition-colors">
      {/* Header */}
      <div className="flex items-start gap-3 mb-3">
        <Avatar user={post.author} size="md" />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm font-medium text-bright">{post.author.full_name}</span>
            <span className={cn('text-xs px-2 py-0.5 rounded border', meta.bg)}>
              <Icon size={10} className={cn('inline me-1', meta.color)} />
              <span className={meta.color}>{meta.label}</span>
            </span>
            <span className="text-xs text-ghost">{formatRelative(post.created_at)}</span>
          </div>
          <div className="flex items-center gap-1.5 mt-0.5">
            <span className="text-xs text-ghost capitalize">{post.author.experience_level}</span>
            <span className="text-ghost">·</span>
            <span className="text-xs text-amber">
              {post.author.overall_readiness_score.toFixed(0)}% ready
            </span>
          </div>
        </div>
      </div>

      {/* Content */}
      <h3 className="font-medium text-bright mb-2 leading-snug">{post.title}</h3>
      <p className={cn(
        'text-sm text-soft leading-relaxed whitespace-pre-line',
        !expanded && 'line-clamp-3'
      )}>
        {post.content}
      </p>
      {post.content.length > 200 && (
        <button
          className="text-xs text-ghost hover:text-soft mt-1 flex items-center gap-1"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded
            ? <><ChevronUp size={12} /> Show less</>
            : <><ChevronDown size={12} /> Read more</>}
        </button>
      )}

      {/* GitHub link */}
      {safeUrl(post.github_url) && (
        <a
          href={safeUrl(post.github_url)}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 mt-3 text-xs text-ghost hover:text-bright transition-colors border border-border rounded px-2.5 py-1"
        >
          <Github size={12} /> View on GitHub
        </a>
      )}

      {/* Tags */}
      {post.tags.length > 0 && (
        <div className="flex gap-1.5 flex-wrap mt-3">
          {post.tags.map(tag => (
            <span key={tag} className="text-xs px-2 py-0.5 rounded bg-surface border border-border text-ghost">
              #{tag}
            </span>
          ))}
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-4 mt-4 pt-3 border-t border-border">
        <button
          onClick={handleLike}
          className={cn(
            'flex items-center gap-1.5 text-xs transition-colors',
            post.liked_by_me ? 'text-rose' : 'text-ghost hover:text-rose'
          )}
        >
          <Heart size={14} className={post.liked_by_me ? 'fill-current' : ''} />
          {post.likes_count}
        </button>
        <button
          onClick={() => setCommenting(!commenting)}
          className="flex items-center gap-1.5 text-xs text-ghost hover:text-bright transition-colors"
        >
          <MessageCircle size={14} />
          {post.comments_count}
        </button>
      </div>

      {/* Comment input */}
      {commenting && (
        <form onSubmit={handleComment} className="mt-3 flex gap-2">
          <input
            className="flex-1 bg-surface border border-border rounded px-3 py-2 text-base md:text-xs text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
            placeholder="Write a comment…"
            value={commentText}
            onChange={e => setCommentText(e.target.value)}
            autoFocus
          />
          <Button size="sm" type="submit" loading={submitting} className="px-3">
            <Send size={12} />
          </Button>
        </form>
      )}

      {/* Comments */}
      {expanded && post.comments.length > 0 && (
        <div className="mt-3 space-y-2 border-t border-border pt-3">
          {post.comments.map(c => (
            <div key={c.id} className="flex items-start gap-2">
              <Avatar user={c.author} />
              <div className="flex-1 bg-surface rounded px-3 py-2">
                <div className="flex items-center gap-2 mb-0.5">
                  <span className="text-xs font-medium text-bright">{c.author.full_name}</span>
                  <span className="text-xs text-ghost">{formatRelative(c.created_at)}</span>
                </div>
                <p className="text-xs text-soft leading-relaxed">{c.content}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  )
}

// ─── Create post modal ────────────────────────────────────────────────────────
function CreatePostModal({
  onClose,
  onCreated,
}: {
  onClose: () => void
  onCreated: (p: Post) => void
}) {
  const [form, setForm] = useState({
    post_type: 'discussion' as PostType,
    title: '', content: '', github_url: '', tags: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const post = await createPost({
        post_type: form.post_type,
        title: form.title,
        content: form.content,
        github_url: form.github_url || undefined,
        tags: form.tags.split(',').map(t => t.trim()).filter(Boolean),
      })
      onCreated(post)
      onClose()
    } catch {
      setError('Failed to create post. Try again.')
    }
    setLoading(false)
  }

  return (
    <div className="fixed inset-0 bg-void/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-xl p-6">
        <div className="flex items-center justify-between mb-5">
          <h2 className="font-display font-bold text-white">Share with the community</h2>
          <button onClick={onClose} className="text-ghost hover:text-bright">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Type selector */}
          <div>
            <label className="text-xs text-ghost uppercase tracking-wide block mb-2">Type</label>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
              {(Object.entries(POST_TYPES) as [PostType, typeof POST_TYPES[PostType]][]).map(
                ([key, meta]) => {
                  const Icon = meta.icon
                  return (
                    <button
                      key={key}
                      type="button"
                      onClick={() => setForm(p => ({ ...p, post_type: key }))}
                      className={cn(
                        'flex flex-col items-center gap-1 p-2.5 rounded border text-xs transition-all',
                        form.post_type === key
                          ? meta.bg
                          : 'bg-surface border-border text-ghost hover:border-muted'
                      )}
                    >
                      <Icon size={14} className={form.post_type === key ? meta.color : 'text-ghost'} />
                      <span className={form.post_type === key ? meta.color : ''}>{meta.label}</span>
                    </button>
                  )
                }
              )}
            </div>
          </div>

          <div>
            <label className="text-xs text-ghost uppercase tracking-wide block mb-1.5">Title</label>
            <input
              className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
              placeholder="What's on your mind?"
              value={form.title}
              onChange={e => setForm(p => ({ ...p, title: e.target.value }))}
              required
            />
          </div>

          <div>
            <label className="text-xs text-ghost uppercase tracking-wide block mb-1.5">Content</label>
            <textarea
              className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 min-h-32 resize-none"
              placeholder="Share your problem, project, or achievement in detail…"
              value={form.content}
              onChange={e => setForm(p => ({ ...p, content: e.target.value }))}
              required
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-ghost uppercase tracking-wide block mb-1.5">
                GitHub URL (optional)
              </label>
              <input
                className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
                placeholder="https://github.com/..."
                value={form.github_url}
                onChange={e => setForm(p => ({ ...p, github_url: e.target.value }))}
              />
            </div>
            <div>
              <label className="text-xs text-ghost uppercase tracking-wide block mb-1.5">
                Tags (comma separated)
              </label>
              <input
                className="w-full bg-surface border border-border rounded px-3 py-2.5 text-base md:text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50"
                placeholder="python, pytorch, rag"
                value={form.tags}
                onChange={e => setForm(p => ({ ...p, tags: e.target.value }))}
              />
            </div>
          </div>

          {error && <p className="text-xs text-rose">{error}</p>}

          <div className="flex gap-3 justify-end pt-2">
            <Button type="button" variant="ghost" size="sm" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" size="sm" loading={loading}>
              Post
            </Button>
          </div>
        </form>
      </Card>
    </div>
  )
}

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function CommunityPage() {
  const { isLoading: authLoading } = useAuth()
  const [posts, setPosts] = useState<Post[]>([])
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<PostType | undefined>(undefined)
  const [showCreate, setShowCreate] = useState(false)
  const [activeTab, setActiveTab] = useState<'feed' | 'leaderboard'>('feed')

  // Declared before the effect that uses it, and memoized on `filter`, so
  // the dependency array can name it honestly. Previously this was a
  // hoisted `function` called above its own declaration with `loadFeed`
  // missing from the deps — which the React Compiler flags as
  // "cannot access variable before it is declared".
  // Reset the spinner when the filter changes, in the render phase; the
  // callback below only fetches. `loading` already starts true for the
  // first load.
  const [trackedFilter, setTrackedFilter] = useState(filter)
  if (filter !== trackedFilter) {
    setTrackedFilter(filter)
    setLoading(true)
  }

  const loadFeed = useCallback(async () => {
    try {
      const data = await fetchFeed(filter)
      setPosts(data.posts)
    } catch {}
    setLoading(false)
  }, [filter])

  useEffect(() => {
    if (authLoading) return
    let cancelled = false
    ;(async () => {
      await loadFeed()
      try {
        const d = await fetchLeaderboard()
        if (!cancelled) setLeaderboard(d.entries)
      } catch { /* leaderboard is non-essential */ }
    })()
    return () => { cancelled = true }
  }, [authLoading, loadFeed])

  function updatePost(updated: Post) {
    setPosts(prev => prev.map(p => p.id === updated.id ? updated : p))
  }

  function handleCreated(post: Post) {
    setPosts(prev => [post, ...prev])
  }

  if (authLoading) return (
    <div className="min-h-dvh bg-void flex items-center justify-center">
      <Spinner className="w-6 h-6" />
    </div>
  )

  return (
    <AppShell>
      <PageHeader
        title="Community"
        subtitle="Share problems, projects, and wins with fellow AI engineers."
        action={
          <Button size="sm" onClick={() => setShowCreate(true)}>
            <Plus size={13} /> New post
          </Button>
        }
      />

      {showCreate && (
        <CreatePostModal onClose={() => setShowCreate(false)} onCreated={handleCreated} />
      )}

      <div className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

            {/* ── Main feed ── */}
            <div className="lg:col-span-2 space-y-4">

              {/* Tabs */}
              <div className="flex items-center gap-3">
                <div className="flex gap-1">
                  {(['feed', 'leaderboard'] as const).map(tab => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={cn(
                        'px-4 py-2 rounded text-sm transition-all capitalize',
                        activeTab === tab
                          ? 'bg-amber/10 text-amber border border-amber/20'
                          : 'text-ghost hover:text-bright border border-transparent'
                      )}
                    >
                      {tab === 'leaderboard'
                        ? <><Trophy size={13} className="inline me-1.5" />Leaderboard</>
                        : 'Feed'}
                    </button>
                  ))}
                </div>
              </div>

              {activeTab === 'feed' && (
                <>
                  {/* Type filters */}
                  <div className="flex gap-2 flex-wrap">
                    <button
                      onClick={() => setFilter(undefined)}
                      className={cn(
                        'px-3 py-1.5 rounded text-xs border transition-all',
                        !filter
                          ? 'bg-surface border-amber/30 text-bright'
                          : 'border-border text-ghost hover:border-muted'
                      )}
                    >
                      All
                    </button>
                    {(Object.entries(POST_TYPES) as [PostType, typeof POST_TYPES[PostType]][]).map(
                      ([key, meta]) => {
                        const Icon = meta.icon
                        return (
                          <button
                            key={key}
                            onClick={() => setFilter(filter === key ? undefined : key)}
                            className={cn(
                              'px-3 py-1.5 rounded text-xs border transition-all flex items-center gap-1.5',
                              filter === key ? meta.bg : 'border-border text-ghost hover:border-muted'
                            )}
                          >
                            <Icon size={11} className={filter === key ? meta.color : ''} />
                            {meta.label}
                          </button>
                        )
                      }
                    )}
                  </div>

                  {loading ? (
                    <div className="flex justify-center py-16">
                      <Spinner className="w-6 h-6" />
                    </div>
                  ) : posts.length === 0 ? (
                    <Card className="p-12 text-center">
                      <Users size={28} className="text-ghost mx-auto mb-3" />
                      <p className="text-bright font-medium mb-1">No posts yet</p>
                      <p className="text-sm text-ghost mb-4">Be the first to share something!</p>
                      <Button size="sm" onClick={() => setShowCreate(true)}>
                        <Plus size={12} /> Create first post
                      </Button>
                    </Card>
                  ) : (
                    posts.map(post => (
                      <PostCard key={post.id} post={post} onUpdate={updatePost} />
                    ))
                  )}
                </>
              )}

              {activeTab === 'leaderboard' && (
                <Card className="overflow-hidden">
                  <div className="px-5 py-4 border-b border-border">
                    <h3 className="font-medium text-bright flex items-center gap-2">
                      <Trophy size={15} className="text-amber" /> Top contributors
                    </h3>
                  </div>
                  <div className="divide-y divide-border">
                    {leaderboard.map(entry => (
                      <div
                        key={entry.rank}
                        className="flex items-center gap-4 px-5 py-3"
                      >
                        <div className={cn(
                          'w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0',
                          entry.rank === 1 ? 'bg-amber text-void' :
                          entry.rank === 2 ? 'bg-soft/30 text-bright' :
                          entry.rank === 3 ? 'bg-amber/30 text-amber' :
                          'bg-surface text-ghost'
                        )}>
                          {entry.rank}
                        </div>
                        <Avatar user={entry.user} size="md" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-bright truncate">
                            {entry.user.full_name}
                          </p>
                          <p className="text-xs text-ghost capitalize">{entry.user.experience_level}</p>
                        </div>
                        <div className="flex items-center gap-4 text-xs text-ghost shrink-0">
                          <span className="flex items-center gap-1">
                            <Heart size={11} className="text-rose" /> {entry.likes_received}
                          </span>
                          <span className="flex items-center gap-1">
                            <FolderKanban size={11} className="text-sky" /> {entry.posts_count}
                          </span>
                          <span className="text-amber font-mono">
                            {entry.readiness_score.toFixed(0)}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              )}
            </div>

            {/* ── Right sidebar ── */}
            <div className="space-y-4">
              <Card className="p-4">
                <h3 className="text-xs font-medium text-ghost uppercase tracking-widest mb-3">
                  Post types
                </h3>
                <div className="space-y-2">
                  {(Object.entries(POST_TYPES) as [PostType, typeof POST_TYPES[PostType]][]).map(
                    ([, meta]) => {
                      const Icon = meta.icon
                      return (
                        <div key={meta.label} className="flex items-start gap-2.5 text-xs text-ghost">
                          <Icon size={13} className={cn(meta.color, 'mt-0.5 shrink-0')} />
                          <div>
                            <span className="font-medium text-soft">{meta.label}</span>
                            <span>
                              {meta.label === 'Problem'     && ' — stuck? ask for help'}
                              {meta.label === 'Project'     && ' — show what you built'}
                              {meta.label === 'Achievement' && ' — celebrate your wins'}
                              {meta.label === 'Resource'    && ' — share useful links'}
                              {meta.label === 'Discussion'  && ' — start a conversation'}
                            </span>
                          </div>
                        </div>
                      )
                    }
                  )}
                </div>
              </Card>

              {activeTab === 'feed' && leaderboard.length > 0 && (
                <Card className="p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-xs font-medium text-ghost uppercase tracking-widest">Top 3</h3>
                    <button
                      onClick={() => setActiveTab('leaderboard')}
                      className="text-xs text-amber hover:text-amber2"
                    >
                      See all
                    </button>
                  </div>
                  <div className="space-y-2.5">
                    {leaderboard.slice(0, 3).map(entry => (
                      <div key={entry.rank} className="flex items-center gap-2.5">
                        <span className={cn(
                          'text-xs font-bold w-4 text-center',
                          entry.rank === 1 ? 'text-amber'
                          : entry.rank === 2 ? 'text-soft'
                          : 'text-amber/60'
                        )}>
                          {entry.rank === 1 ? '🥇' : entry.rank === 2 ? '🥈' : '🥉'}
                        </span>
                        <Avatar user={entry.user} />
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-medium text-bright truncate">
                            {entry.user.full_name}
                          </p>
                        </div>
                        <span className="text-xs text-rose flex items-center gap-0.5">
                          <Heart size={10} className="fill-current" /> {entry.likes_received}
                        </span>
                      </div>
                    ))}
                  </div>
                </Card>
              )}

              <Card className="p-4 bg-gradient-to-br from-amber/5 to-transparent border-amber/20">
                <p className="text-xs text-amber font-medium mb-1">💡 Tip</p>
                <p className="text-xs text-dim leading-relaxed">
                  Sharing your problems is as valuable as sharing solutions.
                  Someone in the community has faced the same issue.
                </p>
              </Card>
            </div>

          </div>
        </div>
      </div>
    </AppShell>
  )
}