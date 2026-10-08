FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# NEXT_PUBLIC_* vars are inlined into the client bundle at build time,
# so they must be passed as a build ARG, not a runtime container env var.
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_MENTOR_V2_LIVE
# Absolute base for metadata/link previews (src/app/layout.tsx); unset, every
# canonical and Open Graph URL points at http://localhost:3000.
ARG NEXT_PUBLIC_SITE_URL
# "paymob" turns on the Pro checkout (src/lib/billing/payments.ts). Unset, a
# production build offers no payment provider at all.
ARG NEXT_PUBLIC_PAYMENTS_PROVIDER
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV NEXT_PUBLIC_MENTOR_V2_LIVE=${NEXT_PUBLIC_MENTOR_V2_LIVE}
ENV NEXT_PUBLIC_SITE_URL=${NEXT_PUBLIC_SITE_URL}
ENV NEXT_PUBLIC_PAYMENTS_PROVIDER=${NEXT_PUBLIC_PAYMENTS_PROVIDER}
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
