# Masar AI credit economics

Assumptions checked on 2026-09-27:

- GPT-4o mini text pricing: $0.15 / 1M input tokens, $0.075 / 1M cached input tokens, and $0.60 / 1M output tokens.
- Conversion for planning: 52 EGP/USD, rounded conservatively from the Central Bank of Egypt's September 2026 USD rates.
- The web provider clips the combined prompt to 10,000 characters (about 2,500 English tokens), permits no SDK retries, and records actual provider token usage in metrics.
- Output caps are 300 tokens for hints, 500 for interview questions, 700 for AI grading, 800 for mentor chat, 1,000 for roadmap/skill-gap work, and 1,200 for code review.
- Embeddings are configurable but disabled; the active product code does not make a paid embedding call.
- A user action makes one model call. Provider or response failures refund wallet credits on metered routes. Challenge/project submissions are legacy flat-fee flows rather than recurring wallet deductions.

## Credit-to-cost estimate

Credits do not equal calls. Current prices range from 1 credit (a short hint) to 10 credits (exam grading), with mentor chat at 2, mock interview at 3, roadmap/code review at 5, and skill-gap analysis at 8.

A conservative representative blend is **$0.00035 per credit**, or **0.0182 EGP per credit**. The upper planning bound is **$0.000555 / 0.0289 EGP per credit**: a one-credit hint consuming the full 2,500-token input allowance and all 300 output tokens. Cached-input savings are deliberately excluded.

| Scenario | Credits | Estimated API cost | Upper-bound cost |
|---|---:|---:|---:|
| Free allocation | 40 once | $0.014 / 0.73 EGP | $0.022 / 1.15 EGP |
| Typical Pro month | 500 | $0.175 / 9.10 EGP | $0.278 / 14.43 EGP |
| Heavy Pro month | 2,000 | $0.70 / 36.40 EGP | $1.11 / 57.72 EGP |

At 299 EGP/month, the typical estimate is 3.0% of revenue (4.8% upper bound); the heavy estimate is 12.2% (19.3% upper bound). Over twelve months, those estimates are 109.20 EGP and 436.80 EGP, respectively, or 5.0% and 19.9% of the 2,199 EGP annual price. The annual upper bounds are 173.16 EGP (7.9%) and 692.64 EGP (31.5%). These figures exclude payment fees, VAT, support, infrastructure, and non-OpenAI providers.

## Pro allowance decision

Masar had no existing Pro credit grant, so this change does not invent one. Pro unlocks course content while AI operations continue to consume the existing wallet balance. If product policy later requires bundled recurring credits, **1,000 credits per paid month** is the calculated starting ceiling: about 18.20 EGP expected and 28.86 EGP at the upper bound (6.1%-9.7% of monthly revenue). Ship that only after production token metrics confirm the blend and after defining monthly replenishment for annual subscribers; never grant 12 months upfront.
