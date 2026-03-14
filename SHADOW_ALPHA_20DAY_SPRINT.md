# 🚀 SHADOW ALPHA PROTOCOL — 20-DAY LAUNCH SPRINT

> **Enterprise Name:** Shadow_Alpha | **Start:** March 10, 2026 | **Launch:** March 30, 2026
> **12 Antigravity Agents | 20 Days | Full Stack Launch**

---

# MASTER TIMELINE

| Phase | Days | Focus |
|---|---|---|
| **Phase 1: Foundation** | Day 1–4 | Branding, Architecture, Infra Setup, R&D Core |
| **Phase 2: Core Build** | Day 5–10 | Frontend, Backend, Bots, Database, API |
| **Phase 3: Integration** | Day 11–14 | Connect all systems, Auth, Payments, Security |
| **Phase 4: Polish & Deploy** | Day 15–18 | QA, Docker, Hosting, SEO, Social Channels |
| **Phase 5: Launch** | Day 19–20 | Final review, Go-Live, Monitoring |

---

# AGENT ROSTER & ASSIGNMENTS

---

## 🎨 AGENT 1 — "ARCHITECT" (Design & Branding)

**Role:** Brand identity, logo, UI/UX design system, domain procurement

### Day 1–2: Brand Foundation
- [ ] Register domain: `shadowalpha.io` (or `.co` / `.finance`)
- [ ] Design logo (dark mode, gold accents, terminal aesthetic) — generate 3 variants
- [ ] Define brand kit: color palette (Black #0A0A0A, Gold #C9A84C, Charcoal #1A1A2E, Accent #00D4AA), typography (Inter + JetBrains Mono)
- [ ] Create favicon, OG images, social media banners (FB, YouTube, Discord, Telegram)
- [ ] Design email signature template for `@shadowalpha.io`

### Day 3–5: UI/UX Design
- [ ] Design landing page wireframe (hero, features, pricing, CTA)
- [ ] Design dashboard wireframe (position tracker, portfolio, P2P marketplace)
- [ ] Design premium pricing cards with Veblen tiers (Free/Alpha/Premier/Black Card)
- [ ] Create component library spec: buttons, cards, modals, charts, tables
- [ ] Design Telegram bot conversation flows (UX wireframe for bot interactions)
- [ ] Design Discord server layout (channels, roles, permissions)
- [ ] 🆕 Design **Shadow Vault** page wireframe (deposit, yield display, performance chart)
- [ ] 🆕 Design **Shield Insurance** modal (position protection purchase flow, premium display, payout calculator)
- [ ] 🆕 Design **Gratitude popup** (post-win celebration screen with tip buttons: 5%/10%/15%/Non merci)
- [ ] 🆕 Design **Position Loan** modal (collateral value display, loan amount slider, fee preview)
- [ ] 🆕 Design **Cashout Instantané Prime** button + pricing card (market-making UX)

### Day 6–8: Asset Production
- [ ] Export all assets as SVG/PNG/WebP for frontend
- [ ] Create animated loading states, micro-interactions spec
- [ ] Design email templates (welcome, position alert, tontine update)
- [ ] Produce 5 mockup screenshots for social media launch posts
- [ ] 🆕 Design "Community Supporter 🌟" and "Top Supporter 🔥" badges for Gratitude system
- [ ] 🆕 Design Shield insurance activation confirmation animation

### Day 9–20: Support & Polish
- [ ] Review frontend implementation vs design spec
- [ ] Fix any design inconsistencies reported by Agent 11

**DELIVERABLES:** Logo, brand kit, domain, wireframes, UI component spec, social assets, Shadow Wealth Engine UI specs

---

## 🖥️ AGENT 2 — "FRONTEND" (Web Application)

**Role:** Build the full web frontend — Next.js + TailwindCSS on Vercel

### Day 1–2: Project Setup
- [ ] Initialize Next.js 14 project: `npx -y create-next-app@latest ./shadow-alpha-web --typescript --tailwind --eslint --app --src-dir`
- [ ] Configure TailwindCSS with brand colors, fonts, dark mode
- [ ] Install dependencies: `framer-motion`, `recharts`, `lucide-react`, `@tanstack/react-query`, `zustand`
- [ ] Set up project structure:
```
src/
├── app/              # Next.js app router pages
│   ├── (landing)/    # Public landing page
│   ├── (auth)/       # Login, signup, KYC
│   ├── dashboard/    # Authenticated dashboard
│   ├── exchange/     # P2P position marketplace
│   ├── tontine/      # Digital tontine management
│   ├── api/          # API routes (BFF)
│   └── docs/         # API documentation page
├── components/       # Reusable UI components
│   ├── ui/           # Primitives (Button, Card, Modal, Input)
│   ├── layout/       # Header, Sidebar, Footer
│   ├── charts/       # Position charts, portfolio graphs
│   └── features/     # Feature-specific components
├── lib/              # Utilities, API client, constants
├── hooks/            # Custom React hooks
├── stores/           # Zustand state stores
└── types/            # TypeScript interfaces
```

### Day 3–6: Core Pages
- [ ] **Landing Page:** Hero with animated gradient, feature grid (5 modules), pricing table (4 Veblen tiers), testimonials, CTA waitlist form, footer with social links
- [ ] **Auth Pages:** Login (email + Google + MoMo), Signup (with invite code field), KYC upload
- [ ] **Dashboard:** Portfolio overview (total value, P&L chart), active positions list, quick actions
- [ ] **Exchange Page:** P2P order book (bid/ask), position card with live pricing, buy/sell modal, stop-loss/take-profit controls
- [ ] **Tontine Page:** Group list, contribution tracker, yield display, invite members

### Day 7–9: Advanced Features + 🆕 Shadow Wealth Engine Pages
- [ ] **API Docs Page:** Interactive API reference (like Stripe docs) for the public API
- [ ] **Profile/Settings:** Account info, subscription tier display, payment method, KYC status
- [ ] **Leaderboard:** Top traders ranking with badges, weekly/monthly filters
- [ ] **Copy-Trading:** Browse top performers, one-click follow, P&L tracking
- [ ] 🆕 **Shadow Vault Page:** Deposit into yield fund, real-time APY display, performance chart (line + area), deposit/withdraw modal, allocation breakdown pie chart
- [ ] 🆕 **Shield Insurance Component:** On each position card: toggle for "Activate Shield 🛡️", show premium cost, coverage %, payout if loss — auto-calculate via pricing API
- [ ] 🆕 **Cashout Instantané Prime Button:** On each active position: one-click instant cashout with live price (spread-adjusted), confirmation modal showing "You receive X FCFA instantly"
- [ ] 🆕 **Position Loan Modal:** On each active position: "Get Cash Now" button → slider for loan amount (max 60% of position value), flat fee preview, confirm → instant credit
- [ ] 🆕 **Gratitude Popup:** Post-win celebration overlay: confetti animation + gain amount + tip buttons [🙏 5%] [💛 10%] [🔥 15%] [✕ Non merci] + social proof text ("87% des gagnants remercient la communauté")
- [ ] 🆕 **Top Supporters Leaderboard:** Tab in leaderboard for "Community Supporters" with badges and ranking by lifetime tips
- [ ] Connect all pages to backend API via `@tanstack/react-query` + Zustand stores

### Day 10–14: Integration & Polish
- [ ] Integrate Supabase Auth (email, Google, phone/OTP for MoMo users)
- [ ] Connect real-time position updates via WebSocket
- [ ] Add toast notifications (trade executed, position alert, tontine payout)
- [ ] 🆕 Connect Shield activation to backend `/shield/activate` endpoint
- [ ] 🆕 Connect Cashout Instantané to backend `/exchange/instant-cashout` endpoint
- [ ] 🆕 Connect Position Loan to backend `/loans/position-collateral` endpoint
- [ ] 🆕 Connect Shadow Vault to backend `/vault/deposit`, `/vault/withdraw`, `/vault/performance` endpoints
- [ ] 🆕 Connect Gratitude popup to backend `/gratitude/tip` endpoint + track tip in user profile
- [ ] Responsive design pass (mobile-first, tablet, desktop)
- [ ] Micro-animations: page transitions, hover effects, loading skeletons
- [ ] SEO: meta tags, OG images, sitemap.xml, robots.txt

### Day 15–18: Final Polish
- [ ] Performance audit (Lighthouse 90+ score)
- [ ] Accessibility pass (ARIA labels, keyboard navigation)
- [ ] Error boundaries, 404 page, empty states
- [ ] Cookie consent banner, privacy policy page, terms of service page
- [ ] 🆕 Test Gratitude popup trigger timing (only shows on confirmed win, with 3s delay for euphoria optimization)
- [ ] 🆕 Test Shield insurance UX flow end-to-end (activate → win/lose → payout/nothing)

**DELIVERABLES:** Full Next.js web app deployed on Vercel, all pages including Shadow Vault, Shield, Cashout Prime, Position Loans, and Gratitude system

---

## ⚙️ AGENT 3 — "BACKEND" (API Server)

**Role:** Build the core backend — Python FastAPI + PostgreSQL

### Day 1–2: Project Setup
- [ ] Initialize FastAPI project structure:
```
shadow-alpha-api/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Settings, env vars
│   ├── models/              # SQLAlchemy/Pydantic models
│   │   ├── user.py
│   │   ├── position.py
│   │   ├── order.py
│   │   ├── tontine.py
│   │   ├── loan.py
│   │   ├── subscription.py
│   │   ├── vault.py          # 🆕 Shadow Vault deposits/yields
│   │   ├── shield.py         # 🆕 Position insurance contracts
│   │   ├── gratitude.py      # 🆕 Tip/gratitude transactions
│   │   └── position_loan.py  # 🆕 Collateralized position loans
│   ├── routers/             # API route handlers
│   │   ├── auth.py
│   │   ├── positions.py
│   │   ├── exchange.py
│   │   ├── tontine.py
│   │   ├── credit.py
│   │   ├── portfolio.py
│   │   ├── admin.py
│   │   ├── public_api.py    # External API (like OpenAI)
│   │   ├── vault.py         # 🆕 Shadow Vault routes
│   │   ├── shield.py        # 🆕 Shield Insurance routes
│   │   ├── gratitude.py     # 🆕 Gratitude/Tip routes
│   │   └── position_loans.py # 🆕 Lombard loan routes
│   ├── services/            # Business logic
│   │   ├── pricing_engine.py
│   │   ├── order_matcher.py
│   │   ├── tontine_engine.py
│   │   ├── credit_scorer.py
│   │   ├── yield_engine.py
│   │   ├── float_engine.py       # 🆕 Shadow Float deployment
│   │   ├── market_maker.py       # 🆕 AMM + Instant Cashout
│   │   ├── shield_engine.py      # 🆕 Insurance pricing + hedging
│   │   ├── prop_fund.py          # 🆕 Anti-Portfolio Prop Trading
│   │   ├── vault_engine.py       # 🆕 Performance Fee calculator
│   │   ├── tranche_engine.py     # 🆕 Yield Tranching (CDO)
│   │   └── user_classifier.py    # 🆕 Sharp/Square classification
│   ├── middleware/           # Auth, rate limiting, CORS
│   ├── utils/               # Helpers
│   └── db/                  # Database connection, migrations
├── tests/
├── alembic/                 # DB migrations
├── Dockerfile
├── requirements.txt
└── docker-compose.yml
```
- [ ] Set up Supabase project (PostgreSQL + Auth + Storage + Realtime)
- [ ] Configure Alembic migrations
- [ ] Set up Redis for caching and rate limiting

### Day 3–6: Core API Endpoints
- [ ] **Auth:** `/auth/register`, `/auth/login`, `/auth/verify-otp`, `/auth/refresh`, `/auth/me`
- [ ] **Positions:** `/positions/create`, `/positions/{id}`, `/positions/my`, `/positions/{id}/value` (real-time pricing)
- [ ] **Exchange:** `/exchange/orderbook`, `/exchange/place-order`, `/exchange/cancel`, `/exchange/my-orders`, `/exchange/trades`
- [ ] **Portfolio:** `/portfolio/summary`, `/portfolio/pnl`, `/portfolio/history`
- [ ] **Tontine:** `/tontine/create-group`, `/tontine/join`, `/tontine/contribute`, `/tontine/groups/my`, `/tontine/{id}/ledger`
- [ ] **Credit:** `/credit/score`, `/credit/apply`, `/credit/my-loans`, `/credit/repay`
- [ ] **Subscriptions:** `/subscription/plans`, `/subscription/upgrade`, `/subscription/status`

### Day 7–9: Business Logic + 🆕 Shadow Wealth Engine Services
- [ ] Implement pricing engine service (Modified Black-Scholes — integrate with Agent 12 R&D)
- [ ] Implement order matching engine (price-time priority)
- [ ] Implement tontine rotation scheduler (round-robin + Monte Carlo optimization)
- [ ] Implement Kelly Criterion bankroll advisor endpoint
- [ ] WebSocket server for real-time price pushes and order book updates
- [ ] Implement promo code system (create, validate, track referrals, calculate commissions)
- [ ] 🆕 **Shadow Float Engine:** Background job that aggregates idle wallet balances + tontine dormant capital → deploys to yield protocols (DeFi/T-Bills). Track float_balance, deployed_amount, accrued_interest per 6-hour cycle
- [ ] 🆕 **Market Maker / Instant Cashout:** `/exchange/instant-cashout` endpoint — calculate fair value via Black-Scholes, apply 5-8% spread, execute instantly. Internal inventory management for acquired positions
- [ ] 🆕 **Shield Insurance Engine:**
  - `POST /shield/activate` — user pays premium (2-5% of stake), creates insurance contract
  - `POST /shield/claim` — auto-triggered on position loss, disburse 70% of original stake
  - Pricing: use Agent 12 Bayesian probability × coverage × hedge cost → premium calculation
  - Background hedging: auto-place inverse position on external exchange to cover risk
- [ ] 🆕 **Shadow Vault (Performance Fee Engine):**
  - `POST /vault/deposit` — user deposits capital into yield fund
  - `GET /vault/performance` — returns net yield (after 35% SA performance fee deducted)
  - `POST /vault/withdraw` — user withdraws capital + net profits
  - Background: deploy vault capital via DRL portfolio optimizer (Agent 12) into arbitrage/EV+ strategies
- [ ] 🆕 **Gratitude System:**
  - `POST /gratitude/tip` — record voluntary tip (5/10/15% of gain), credit SA treasury
  - `GET /gratitude/supporters` — leaderboard of top supporters
  - Trigger: auto-call on win confirmation with 3-second delay (behavioral optimization)
- [ ] 🆕 **Position Loan (Lombard):**
  - `POST /loans/position-collateral` — lock position as collateral, disburse 60% of Black-Scholes value, charge 1.5% flat fee
  - Auto-settlement: on position win → deduct loan + fee from payout; on loss → position was hedged via Mécanisme 3

### Day 10–14: Public API (The "OpenAI-style" API) + 🆕 Wealth Engine Admin
- [ ] Design API key management: `/api/keys/create`, `/api/keys/list`, `/api/keys/revoke`
- [ ] Public endpoints (require API key in header `Authorization: Bearer sap_xxxx`):
  - `GET /v1/positions/price` — get live position pricing
  - `POST /v1/positions/evaluate` — evaluate a bet position
  - `GET /v1/odds/live` — live odds feed
  - `GET /v1/analytics/ev` — expected value calculation
  - `GET /v1/analytics/kelly` — Kelly Criterion recommendation
  - `POST /v1/tontine/simulate` — Monte Carlo tontine simulation
- [ ] Rate limiting per API key tier (Free: 100/day, Pro: 10K/day, Enterprise: unlimited)
- [ ] Usage tracking and billing per API call
- [ ] Auto-generate OpenAPI spec and host interactive docs at `/api/docs`
- [ ] 🆕 **Admin Dashboard API (internal):**
  - `GET /admin/float-status` — current float deployed, accrued interest, APY
  - `GET /admin/prop-fund` — prop fund P&L, active positions, Sharp/Square signals
  - `GET /admin/shield-book` — active insurance contracts, net exposure, hedge status
  - `GET /admin/vault-aum` — total AUM, performance fee collected, net returns
  - `GET /admin/gratitude-stats` — total tips, conversion rate, top supporters
  - `GET /admin/revenue-streams` — breakdown of all 10 revenue mechanisms

### Day 15–18: Hardening
- [ ] Input validation on ALL endpoints (Pydantic strict mode)
- [ ] Error handling middleware (structured error responses)
- [ ] Logging (structured JSON logs via `structlog`)
- [ ] Database query optimization (indexes, connection pooling)
- [ ] Write unit tests for all services (pytest, 80%+ coverage target)
- [ ] 🆕 Write unit tests for all wealth engine services (float, market maker, shield, vault, gratitude, position loans)
- [ ] 🆕 Verify float deployment job runs atomically (no double-deployment)
- [ ] 🆕 Verify shield insurance payouts are mathematically correct vs actuarial model

**DELIVERABLES:** Full FastAPI backend, Supabase DB, WebSocket server, Public API, Shadow Wealth Engine (all 10 mechanisms)

---

## 🤖 AGENT 4 — "TELEGRAM" (Telegram Bot)

**Role:** Build the Telegram bot — the primary user interface for Phase 1

### Day 1–3: Bot Setup
- [ ] Create Telegram bot via @BotFather, get token
- [ ] Initialize project with `python-telegram-bot` (async)
- [ ] Design conversation flows:
  - `/start` → Welcome + invite code validation + registration
  - `/menu` → Main menu (inline keyboard)
  - `/newposition` → Log a new bet (sportsbook, odds, stake, teams)
  - `/mypositions` → List active positions with live values
  - `/sell` → List position on P2P marketplace
  - `/buy` → Browse available positions
  - `/portfolio` → Portfolio summary (total value, P&L, best/worst)
  - `/kelly` → Get Kelly Criterion recommendation for a bet
  - `/tontine` → Manage tontine groups
  - `/leaderboard` → Top traders this week/month
  - `/settings` → Subscription tier, notifications, language
  - `/invite` → Generate personal invite code
  - `/help` → Command guide
  - 🆕 `/vault` → Shadow Vault: deposit, check yield, withdraw
  - 🆕 `/shield` → Activate Shield insurance on a position
  - 🆕 `/cashout` → Instant Cashout Prime (market maker spread)
  - 🆕 `/loan` → Get a position-collateralized loan

### Day 4–7: Core Features
- [ ] Position tracking: user inputs bet details → bot calculates live value via pricing engine API
- [ ] P2P marketplace: list positions for sale, browse marketplace, buy with escrow
- [ ] Auto-alerts: notify user when position value crosses thresholds (stop-loss, take-profit)
- [ ] Kelly advisor: user inputs odds + estimated probability → bot returns optimal bet size
- [ ] Portfolio view: inline charts (generate matplotlib images, send as photo)
- [ ] Promo code system: `/redeem CODE` → apply streamer promo code

### Day 8–10: Advanced Features + 🆕 Shadow Wealth Engine
- [ ] Tontine management: create group, invite members (share Telegram deep link), track contributions
- [ ] Scheduled alerts: daily portfolio summary at user's chosen time
- [ ] Multi-language support: English, French (critical for Cameroon)
- [ ] Payment integration: MTN MoMo / Orange Money webhook for deposits/withdrawals
- [ ] Inline mode: users can share position cards in any Telegram chat
- [ ] 🆕 `/vault deposit <amount>` → deposit into Shadow Vault yield fund, show current APY
- [ ] 🆕 `/vault status` → show current balance, net yield (after 35% performance fee), chart
- [ ] 🆕 `/shield <position_id>` → show premium cost, coverage %, confirm → activate insurance
- [ ] 🆕 `/cashout <position_id>` → show instant cashout price (with spread), confirm → instant payout
- [ ] 🆕 `/loan <position_id>` → show max loan amount (60% of value), fee (1.5%), confirm → instant credit
- [ ] 🆕 **Gratitude Flow:** After confirmed win, bot auto-sends celebration message + tip inline keyboard [🙏5%][💛10%][🔥15%][✕Non] with 3s delay

### Day 11–18: Integration & Testing
- [ ] Connect all bot actions to backend API (Agent 3)
- [ ] 🆕 Connect all wealth engine commands (vault, shield, cashout, loan, gratitude) to backend
- [ ] Error handling: graceful messages for API failures
- [ ] Rate limiting per user
- [ ] Logging all interactions for analytics
- [ ] Test with 10 beta users (internal team)
- [ ] 🆕 Test gratitude tip flow: verify 3s delay, buttons work, tip recorded, badge assigned

**DELIVERABLES:** Fully functional Telegram bot with all commands + Shadow Wealth Engine features

---

## 🎮 AGENT 5 — "DISCORD" (Discord Bot + Server)

**Role:** Build Discord bot and configure the Shadow Alpha Discord server

### Day 1–3: Server Setup
- [ ] Create Discord server with premium structure:
  - **Categories:** Welcome, Announcements, Alpha Lounge, Exchange Floor, Tontine Hub, Streamer Zone, Support
  - **Channels:** #rules, #announcements, #general-chat, #position-alerts, #p2p-marketplace, #tontine-groups, #leaderboard, #streamer-codes, #alpha-signals, #support-tickets
  - **Roles:** Unverified, Member, Alpha Trader, Premier, Black Card, Ambassador, Streamer, Admin
- [ ] Set up role-gated channels (Premier+ only channels)

### Day 3–7: Bot Development
- [ ] Initialize bot with `discord.py` or `discord.js`
- [ ] Commands:
  - `!register` → Link Discord account to SAP account
  - `!portfolio` → Show portfolio embed (rich embed with charts)
  - `!price <position_id>` → Get live position price
  - `!sell <position_id> <price>` → List on marketplace
  - `!buy <position_id>` → Purchase a listed position
  - `!kelly <odds> <probability>` → Kelly recommendation
  - `!leaderboard` → Top 10 embed
  - `!tontine create <name>` → Create tontine group (creates private channel)
  - `!invite` → Generate invite code
  - 🆕 `!vault` → Shadow Vault status/deposit/withdraw
  - 🆕 `!shield <position_id>` → Activate/check Shield insurance
  - 🆕 `!cashout <position_id>` → Instant Cashout Prime
  - 🆕 `!loan <position_id>` → Position-collateralized loan
  - 🆕 `!supporters` → Top Supporters leaderboard (Gratitude)
- [ ] Auto-post: #position-alerts channel gets live notable trades
- [ ] Auto-post: #leaderboard updates daily
- [ ] 🆕 Auto-post: #vault-performance daily Shadow Vault yield update

### Day 8–12: Integration + 🆕 Wealth Engine
- [ ] Connect to backend API
- [ ] Webhook for real-time trade alerts
- [ ] Embed formatting: position cards, portfolio summaries, leaderboard tables
- [ ] Moderation: auto-delete spam, anti-scam filter
- [ ] 🆕 Connect vault, shield, cashout, loan commands to backend API
- [ ] 🆕 Post-win DM: send congratulations embed + Gratitude tip buttons (Discord button components)
- [ ] 🆕 Add #shadow-vault channel with daily yield performance embeds

### Day 13–18: Polish
- [ ] Welcome flow with onboarding tutorial
- [ ] Reaction roles for subscription tier selection
- [ ] Integration with Telegram (cross-platform notifications)
- [ ] 🆕 "Community Supporter 🌟" role auto-assigned to users who tip via Gratitude

**DELIVERABLES:** Discord server + bot, fully integrated with backend + Shadow Wealth Engine

---

## 🔌 AGENT 6 — "DEVOPS" (Infrastructure, Docker, Hosting, Deployment)

**Role:** All infrastructure — Docker, GitHub, Vercel, CI/CD, monitoring

### Day 1–3: Repository & Infra Setup
- [ ] Create GitHub organization: `shadow-alpha`
- [ ] Create repos: `shadow-alpha-web`, `shadow-alpha-api`, `shadow-alpha-bots`, `shadow-alpha-ml`, `shadow-alpha-docs`
- [ ] Set up branch protection rules (main → require PR + review)
- [ ] Configure GitHub Actions CI/CD:
  - On PR: lint + test
  - On merge to main: build + deploy
- [ ] Set up Vercel project for frontend (auto-deploy from `shadow-alpha-web` main branch)
- [ ] Set up Supabase project (production instance)

### Day 4–6: Containerization
- [ ] Write `Dockerfile` for backend API
- [ ] Write `Dockerfile` for Telegram bot
- [ ] Write `Dockerfile` for Discord bot
- [ ] 🆕 Write `Dockerfile` for ML/Quant services (Agent 12 models)
- [ ] Write `docker-compose.yml` (all services + Redis + PostgreSQL for local dev)
- [ ] Write `docker-compose.prod.yml` (production configuration)
- [ ] 🆕 Add `shadow-float-cron` container (6-hour cron job for Float deployment cycle)
- [ ] 🆕 Add `prop-fund-worker` container (background worker for Anti-Portfolio trading signals)
- [ ] Test local full-stack with `docker compose up`

### Day 7–10: Deployment
- [ ] Deploy backend to Railway / Render / Fly.io (affordable, auto-scaling)
- [ ] Deploy bots to dedicated VPS (Hetzner / DigitalOcean — $5-10/mo)
- [ ] Configure custom domain: `api.shadowalpha.io` → backend, `shadowalpha.io` → Vercel frontend
- [ ] SSL certificates (auto via Cloudflare)
- [ ] Set up Cloudflare for CDN + DDoS protection
- [ ] Configure environment variables securely (GitHub Secrets + Vercel env)
- [ ] 🆕 Deploy Float cron job + Prop Fund worker as isolated services
- [ ] 🆕 Set up separate secure vault for DeFi/T-Bill API keys (never in main backend env)

### Day 11–14: Monitoring & Logging
- [ ] Set up Sentry for error tracking (frontend + backend)
- [ ] Set up Uptime monitoring (UptimeRobot or Better Stack)
- [ ] Set up Grafana + Prometheus for API metrics (or Vercel Analytics for frontend)
- [ ] Configure structured logging → centralized log aggregation
- [ ] Set up automated database backups (Supabase built-in + external)
- [ ] 🆕 Set up **Shadow Wealth Dashboard** in Grafana: Float APY, Prop Fund P&L, Shield Book exposure, Vault AUM, Gratitude conversion rate, all 10 revenue streams in real-time
- [ ] 🆕 Alert rules: Float deployment failure, Shield hedge failure, Prop Fund drawdown > 5%

### Day 15–18: SEO & Referencing
- [ ] Submit sitemap to Google Search Console
- [ ] Submit to Bing Webmaster Tools
- [ ] Configure proper meta tags, OG images, structured data (JSON-LD)
- [ ] Set up Google Analytics 4
- [ ] Create and submit to Product Hunt, Hacker News launch plan
- [ ] Register on African fintech directories

### Day 19–20: Launch Day Ops
- [ ] Load testing (k6 or Artillery — target 1000 concurrent users)
- [ ] Verify all services healthy
- [ ] 🆕 Verify Float cron job, Prop Fund worker, and Shield hedging are all operational
- [ ] Monitor logs during launch
- [ ] Incident response plan documented

**DELIVERABLES:** Full CI/CD, Docker containers, production deployment, monitoring, SEO, Shadow Wealth Engine infrastructure

---

## 📱 AGENT 7 — "SOCIAL" (Social Media, Marketing Channels, Integrations)

**Role:** Set up ALL social presences, link integrations, marketing pages

### Day 1–5: Account Creation & Setup
- [ ] **Gmail:** Create `contact@shadowalpha.io` (Google Workspace or forwarding)
- [ ] **Facebook:** Create business page "Shadow Alpha" + configure Meta Business Suite
- [ ] **YouTube:** Create channel "Shadow Alpha" + brand banner + about section + first teaser video script
- [ ] **WhatsApp:** Create WhatsApp Business account + auto-reply flows + catalog
- [ ] **Telegram:** Create official channel @ShadowAlphaOfficial + group @ShadowAlphaCommunity
- [ ] **Discord:** (coordinate with Agent 5) — vanity invite link `discord.gg/shadowalpha`
- [ ] **Twitter/X:** Create @ShadowAlpha_ account + pin launch teaser
- [ ] **LinkedIn:** Create company page
- [ ] **TikTok:** Create account for short-form content

### Day 6–10: Content & Links
- [ ] Write "About Us" content for all platforms (consistent messaging from business plan)
- [ ] Create link-in-bio page (Linktree or custom) connecting ALL platforms
- [ ] Add social links to website footer and header (Agent 2 coordination)
- [ ] Set up UTM tracking for all social links
- [ ] Create 10 launch countdown posts (scheduled across platforms)
- [ ] Design WhatsApp stickers pack (branded)
- [ ] Write bot welcome messages referencing social channels

### Day 11–15: Pre-Launch Campaign
- [ ] Create waitlist landing page integration (email capture → Mailchimp/Resend)
- [ ] Draft 5 email sequences (welcome, feature reveal, launch day, post-launch, referral)
- [ ] Identify and contact 10 African streamers/influencers for promo code partnerships
- [ ] Create streamer media kit (logo, screenshots, talking points, promo code setup guide)
- [ ] Set up Facebook Pixel + Google Ads conversion tracking
- [ ] 🆕 Create marketing content for Shadow Vault: "Earn 9.75%/month on idle capital" social posts
- [ ] 🆕 Create marketing content for Shield: "Never lose your bet — insure it" social posts
- [ ] 🆕 Create "Cashout Instantané Prime" promo video script (“Get your money NOW, not after the match”)
- [ ] 🆕 Draft testimonial templates for Gratitude tippers ("I tipped 5% because Shadow Alpha made me 500K FCFA")

### Day 16–20: Launch Execution
- [ ] Publish launch posts across all channels simultaneously
- [ ] Activate influencer promo codes
- [ ] Monitor social mentions, respond to comments
- [ ] Post launch video on YouTube
- [ ] 🆕 Spotlight Shadow Vault yields in launch day social posts ("Our users earned X% this week")

**DELIVERABLES:** All social accounts live, content calendar, influencer partnerships, email sequences, Shadow Wealth Engine marketing collateral

---

## 🔒 AGENT 8 — "SENTINEL" (Security, KYC, Legal, Compliance)

**Role:** Tech lawyer — security hardening, KYC/AML, privacy, terms of service, regulatory compliance

### Day 1–4: Legal Documentation
- [ ] Draft **Terms of Service** (ToS) — covering P2P marketplace, no gambling, user liability, dispute resolution
- [ ] Draft **Privacy Policy** — GDPR-aligned, data collection, processing, retention, third-party sharing
- [ ] Draft **Cookie Policy** — consent mechanism, analytics cookies, essential cookies
- [ ] Draft **KYC/AML Policy** — user verification tiers, document requirements, sanctions screening
- [ ] Draft **Acceptable Use Policy** — prohibited activities, fraud prevention, account termination
- [ ] Draft **API Terms of Use** — rate limits, data usage restrictions, liability
- [ ] Research CEMAC fintech regulations (COSUMAF), Cameroon gambling law (No. 2015/012)
- [ ] Research UAE/ADGM fintech licensing requirements
- [ ] Document regulatory positioning: "We are a P2P marketplace, NOT a sportsbook"
- [ ] 🆕 Draft **Shadow Vault Terms** — yield fund participation, risk disclosure, performance fee disclosure (35%), withdrawal terms
- [ ] 🆕 Draft **Shield Insurance Terms** — coverage conditions, exclusions, payout timelines, premium non-refundability
- [ ] 🆕 Draft **Position Loan Agreement Template** — collateral seizure conditions, fee disclosure, auto-settlement
- [ ] 🆕 Draft **Data Monetization Policy (Shadow Oracle)** — anonymization guarantees, GDPR B2B data sharing compliance
- [ ] 🆕 Research legality of Prop Fund (internal trading with company capital) in target jurisdictions
- [ ] 🆕 Research insurance licensing requirements for Shield product (micro-insurance frameworks)

### Day 5–8: KYC/AML Implementation
- [ ] Design KYC verification tiers:
  - **Tier 0 (Unverified):** View-only, $0 transaction limit
  - **Tier 1 (Basic):** Phone + email verification → $100/day limit
  - **Tier 2 (Standard):** ID document upload + selfie → $1,000/day limit
  - **Tier 3 (Premium):** Full KYC + proof of address → unlimited
- [ ] Integrate KYC provider (Sumsub, Onfido, or Smile Identity for Africa)
- [ ] Implement sanctions screening (OFAC, EU, UN lists)
- [ ] Design suspicious activity reporting (SAR) workflow
- [ ] Implement transaction monitoring rules (velocity checks, amount thresholds)
- [ ] 🆕 Define Vault deposit/withdrawal limits per KYC tier
- [ ] 🆕 Define Shield activation limits per KYC tier

### Day 9–14: Security Hardening + 🆕 Wealth Engine Security
- [ ] Security audit checklist for backend (coordinate with Agent 3):
  - SQL injection prevention (parameterized queries — Supabase handles)
  - XSS prevention (Content Security Policy headers)
  - CSRF protection (SameSite cookies + CSRF tokens)
  - Rate limiting on all endpoints (Redis-backed)
  - Input validation (Pydantic strict mode)
  - JWT token security (short expiry, refresh rotation)
  - API key hashing (bcrypt, never store plaintext)
  - HTTPS everywhere (HSTS header)
  - Secrets management (no hardcoded keys)
- [ ] Set up dependency vulnerability scanning (Dependabot + Snyk)
- [ ] Configure WAF rules on Cloudflare
- [ ] Implement 2FA for admin accounts
- [ ] Design incident response procedure document
- [ ] 🆕 **Float Security Audit:** Verify DeFi/T-Bill API key isolation, deployment transaction signing, rollback procedures
- [ ] 🆕 **Prop Fund Security:** Ensure trading bot credentials are in hardware security module (HSM) or vault, not env vars
- [ ] 🆕 **Shield Hedge Security:** Verify hedge execution is atomic (no partial hedges), audit hedge log integrity
- [ ] 🆕 **Gratitude Anti-Fraud:** Ensure tips cannot be reversed, no self-tipping exploits, rate limit tip submissions

### Day 15–18: Review & Audit
- [ ] Review ALL legal pages on website (Agent 2 integration)
- [ ] Review KYC flow end-to-end
- [ ] Penetration testing (basic — OWASP ZAP automated scan)
- [ ] Validate cookie consent banner compliance
- [ ] Data retention policy implementation
- [ ] 🆕 Review Shadow Vault Terms, Shield Terms, Loan Agreement on website
- [ ] 🆕 Verify Shadow Oracle anonymization pipeline (no PII leakage in B2B API)

### Day 19–20: Launch Readiness
- [ ] Final security scan
- [ ] Confirm all legal pages are live and linked in site footer
- [ ] Verify GDPR/data rights request workflow
- [ ] 🆕 Final audit of all 10 revenue mechanism security surfaces

**DELIVERABLES:** All legal docs, KYC system, security hardening, compliance framework, Shadow Wealth Engine legal/security review

---

## 🔍 AGENT 9 — "GUARDIAN" (Code Review, QA, Integration Testing)

**Role:** Quality gatekeeper — review ALL code from all agents, ensure consistency, catch bugs, verify business plan alignment

### CONTINUOUS (Day 1–20):
- [ ] **Code Review:** PR review on EVERY merge request across all repos
  - Check: code quality, security, performance, naming conventions
  - Check: alignment with business plan and module specifications
  - Check: no conflicting implementations between agents
  - Check: consistent API contracts (frontend ↔ backend ↔ bots)
  - Check: no hallucinated features (features not in spec)
  - Check: proper error handling everywhere

### Day 5–8: API Contract Validation
- [ ] Define and enforce API contract document (OpenAPI spec as single source of truth)
- [ ] Verify frontend API calls match backend endpoints exactly
- [ ] Verify bot API calls match backend endpoints exactly
- [ ] Verify public API documentation matches actual implementation

### Day 9–14: Integration Testing + 🆕 Wealth Engine Tests
- [ ] Write integration test suite:
  - User registration → login → create position → sell on exchange → buyer purchases → settlement
  - Tontine: create group → invite → contribute → yield distributed
  - Subscription: free → upgrade → access premium features
  - API key: create → make API call → rate limit hit → upgrade
  - Promo code: create → share → redeem → referral tracked → commission calculated
  - 🆕 Shadow Vault: deposit → yield accrues → performance fee deducted → withdraw net
  - 🆕 Shield: activate on position → position loses → 70% refund disbursed automatically
  - 🆕 Shield: activate on position → position wins → no payout, premium kept
  - 🆕 Cashout Prime: request instant cashout → spread applied → instant payout → position enters SA inventory
  - 🆕 Position Loan: lock position → receive 60% → position wins → auto-repay from winnings
  - 🆕 Gratitude: user wins → popup shown after 3s → user tips 10% → tip recorded → badge assigned
  - 🆕 Float: deposit idle → float deployment cron runs → interest accrued → user balance unchanged
- [ ] Test Telegram bot ↔ backend integration end-to-end
- [ ] Test Discord bot ↔ backend integration end-to-end
- [ ] Test WebSocket real-time updates (frontend + bots)
- [ ] 🆕 Verify no cross-contamination between Vault capital and user wallets
- [ ] 🆕 Verify Shield hedging triggers correctly on external exchange

### Day 15–18: QA & Bug Bash
- [ ] Full regression test of all features
- [ ] Cross-browser testing (Chrome, Firefox, Safari, mobile browsers)
- [ ] Mobile responsiveness testing (iPhone SE, iPhone 14, Samsung Galaxy, Pixel)
- [ ] Performance testing: API response times < 200ms p95
- [ ] Database query audit: no N+1 queries, proper indexes
- [ ] Bug tracking: create GitHub Issues for all found bugs, prioritize P0/P1/P2
- [ ] 🆕 **Wealth Engine Math Verification:** Validate that performance fee = exactly 35% of gross yield, spread = exactly 5-8%, Shield premium pricing matches actuarial model
- [ ] 🆕 **Revenue Stream Reconciliation:** Verify all 10 revenue mechanisms are tracked and summed correctly in admin dashboard

### Day 19–20: Launch Sign-Off
- [ ] Final smoke test of all critical paths
- [ ] 🆕 Final smoke test of all 10 wealth engine mechanisms
- [ ] Verify all P0 and P1 bugs resolved
- [ ] Sign-off document: "GO / NO-GO" launch recommendation
- [ ] 🆕 Sign-off: confirm all wealth engine features match `SHADOW_ALPHA_SYSTEME_ENRICHISSEMENT_OCCULTE.md` spec

**DELIVERABLES:** Code review log, integration tests (incl. all 10 wealth mechanisms), bug tracker, launch sign-off

---

## 🔗 AGENT 10 — "INTEGRATOR" (Frontend-Backend Connection, Auth, Payments, Database)

**Role:** The glue — connect frontend to backend, set up auth flows, payment integrations, database schema

### Day 1–4: Database Schema (Supabase)
- [ ] Design and deploy schema:
```sql
-- Core tables
users (id, email, phone, display_name, tier, kyc_status, promo_code, referred_by, created_at)
positions (id, user_id, sportsbook, teams, odds, stake, max_payout, status, current_value, created_at)
orders (id, position_id, seller_id, buyer_id, order_type, price, status, created_at)
trades (id, order_id, price, fee, settled_at)
tontine_groups (id, name, creator_id, cycle_type, target_amount, current_amount, status)
tontine_members (id, group_id, user_id, role, contribution_total)
tontine_contributions (id, group_id, user_id, amount, created_at)
loans (id, user_id, amount, interest_rate, status, due_date, repaid_at)
subscriptions (id, user_id, plan, status, started_at, expires_at)
api_keys (id, user_id, key_hash, name, tier, usage_count, created_at)
promo_codes (id, code, creator_id, uses_remaining, commission_rate)
referrals (id, promo_code_id, referred_user_id, lifetime_revenue)

-- 🆕 Shadow Wealth Engine tables
vault_deposits (id, user_id, amount, deposited_at, withdrawn_at, status)
vault_yields (id, cycle_date, gross_yield, performance_fee, net_yield, strategy_used)
shield_contracts (id, position_id, user_id, premium_paid, coverage_pct, hedge_id, status, created_at)
shield_claims (id, contract_id, payout_amount, claimed_at)
instant_cashouts (id, position_id, user_id, fair_value, offered_price, spread_pct, status, created_at)
position_loans (id, position_id, user_id, loan_amount, collateral_value, fee, status, repaid_at)
gratitude_tips (id, user_id, win_amount, tip_pct, tip_amount, created_at)
float_deployments (id, total_float, deployed_to, apy, interest_accrued, cycle_start, cycle_end)
prop_fund_trades (id, signal_user_id, signal_type, direction, stake, pnl, created_at)
user_classifications (id, user_id, classification, confidence, last_updated)
oracle_queries (id, institution_id, query_type, credits_used, created_at)
revenue_ledger (id, mechanism, amount, description, created_at)
```
- [ ] Set up Row Level Security (RLS) policies on ALL tables (core + wealth engine)
- [ ] Configure Supabase Realtime for positions, orders, vault_yields, and shield_contracts tables
- [ ] Set up database indexes for frequent queries
- [ ] 🆕 Create DB triggers: auto-insert `revenue_ledger` row on every fee/tip/spread capture

### Day 5–8: Authentication
- [ ] Configure Supabase Auth providers:
  - Email + password
  - Google OAuth
  - Phone OTP (for mobile money users)
- [ ] Implement invite code validation during registration
- [ ] Set up JWT token flow: frontend → Supabase → backend validation
- [ ] Implement session management (refresh tokens, auto-logout)
- [ ] Connect Telegram bot auth (deep link → web auth → link account)
- [ ] Connect Discord OAuth (link Discord account to SAP account)

### Day 9–12: Payment Integration
- [ ] Integrate MTN MoMo API (Cameroon, Côte d'Ivoire)
- [ ] Integrate Orange Money API
- [ ] Integrate Stripe (for international cards + subscription billing)
- [ ] Build deposit flow: user → MoMo → webhook → credit wallet
- [ ] Build withdrawal flow: user → request → KYC check → MoMo disbursement
- [ ] Build subscription billing: Stripe Checkout → webhook → update tier
- [ ] 🆕 Build Vault deposit/withdraw flow: user → confirm → credit vault_deposits table → WebSocket update
- [ ] 🆕 Build Shield premium payment flow: calculate premium → debit wallet → create shield_contract
- [ ] 🆕 Build Position Loan disbursement flow: lock position → calculate 60% → debit fee → credit wallet

### Day 13–16: Frontend-Backend Wiring + 🆕 Wealth Engine Wiring
- [ ] Create API client library (`src/lib/api.ts`) with all endpoint methods
- [ ] Wire all frontend pages to live API data (replace mocks)
- [ ] Implement optimistic UI updates for trades
- [ ] Set up WebSocket connection for real-time data
- [ ] Error handling: retry logic, offline mode, error toasts
- [ ] 🆕 Wire Shadow Vault page to `/vault/*` endpoints (deposit, withdraw, performance)
- [ ] 🆕 Wire Shield toggle on position cards to `/shield/activate` endpoint
- [ ] 🆕 Wire Cashout Instantané button to `/exchange/instant-cashout` endpoint
- [ ] 🆕 Wire Position Loan modal to `/loans/position-collateral` endpoint
- [ ] 🆕 Wire Gratitude popup to `/gratitude/tip` endpoint (fire on WebSocket win confirmation)
- [ ] 🆕 Wire Top Supporters leaderboard to `/gratitude/supporters` endpoint

### Day 17–20: Testing & Edge Cases
- [ ] Test full user journey end-to-end (register → deposit → trade → withdraw)
- [ ] Test payment webhook reliability (retry, idempotency)
- [ ] Test concurrent order matching (race conditions)
- [ ] Verify RLS policies prevent unauthorized data access
- [ ] 🆕 Test Vault deposit → yield accrual → performance fee deduction → withdraw net
- [ ] 🆕 Test Shield activate → position loss → claim auto-triggered → 70% refund
- [ ] 🆕 Test Position Loan → position wins → auto-repay from winnings
- [ ] 🆕 Test Gratitude popup only fires on genuine wins, not on manual triggers

**DELIVERABLES:** Database schema (incl. wealth engine tables), auth flows, payment integrations, frontend-backend connection, all wealth engine features wired

---

## 📡 AGENT 11 — "PUBLIC API" (External API — The "OpenAI for Betting Analytics")

**Role:** Build and document the public-facing API that enterprises and developers can use

### Day 1–4: API Design
- [ ] Design RESTful public API specification (OpenAPI 3.0):
```
Base URL: https://api.shadowalpha.io/v1

Authentication: Bearer token (API key)
  Header: Authorization: Bearer sap_live_xxxxxxxxxxxx

Endpoints:
  POST /v1/positions/evaluate
    Body: { sportsbook, teams, odds, stake, match_time_remaining }
    Response: { fair_value, confidence, ev, kelly_fraction }

  GET /v1/odds/live?sport=football&league=EPL
    Response: { matches: [{ id, teams, odds, implied_prob }] }

  POST /v1/analytics/black-scholes
    Body: { current_prob, implied_prob, volatility, time_remaining }
    Response: { position_value, greeks: { delta, gamma, theta, vega } }

  POST /v1/analytics/kelly
    Body: { odds, probability, bankroll }
    Response: { optimal_fraction, optimal_stake, expected_growth }

  POST /v1/tontine/simulate
    Body: { members, contribution, cycles, yield_rate }
    Response: { simulation: [{ cycle, payouts, total_value }] }

  GET /v1/usage
    Response: { calls_today, calls_remaining, plan }
```

### Day 5–8: Implementation + 🆕 Shadow Oracle API
- [ ] Implement all public API endpoints on backend (coordinate with Agent 3)
- [ ] API key generation and management (hashed storage, prefix `sap_live_` / `sap_test_`)
- [ ] Rate limiting engine (token bucket per API key):
  - Free: 100 calls/day
  - Pro: 10,000 calls/day ($29/month)
  - Enterprise: Unlimited ($199/month + custom)
- [ ] Usage metering and billing integration
- [ ] 🆕 **Shadow Oracle B2B API (Mécanisme 4):**
  - `POST /v1/oracle/credit-score` — input: anonymized user behavioral profile → output: alternative credit score (0-1000) + risk tier
  - `POST /v1/oracle/batch-score` — batch scoring for institutions (up to 1000 profiles)
  - `GET /v1/oracle/risk-segments` — aggregate risk landscape of a demographic segment
  - Pricing: per-query credits ($0.50/query Standard, $0.20/query Enterprise volume)
  - Authentication: separate B2B API keys with institution-level access
- [ ] 🆕 **Shield API (for partners):**
  - `POST /v1/shield/quote` — get insurance premium quote for any position
  - `POST /v1/shield/activate` — activate shield via API (for integrated partners)

### Day 9–14: Documentation
- [ ] Build interactive API docs page (Swagger UI or custom — hosted at `api.shadowalpha.io/docs`)
- [ ] Write getting-started guide with code examples (Python, JavaScript, cURL)
- [ ] Create SDK stubs: `pip install shadowalpha` / `npm install @shadowalpha/sdk`
- [ ] Write use-case tutorials: "Build a Betting Analytics Dashboard", "Integrate Kelly Criterion into Your App"
- [ ] 🆕 Write Shadow Oracle B2B documentation: "Alternative Credit Scoring for African Lenders"
- [ ] 🆕 Write Shield API documentation for partner integrations

### Day 15–20: Testing & Launch
- [ ] Write API integration tests (all endpoints, error cases, rate limits)
- [ ] Security audit: API key leakage prevention, input sanitization
- [ ] Performance: < 100ms p95 response time
- [ ] Publish documentation on website
- [ ] 🆕 Test Shadow Oracle anonymization pipeline (zero PII in API responses)
- [ ] 🆕 Test Shield API quote accuracy vs internal actuarial model

**DELIVERABLES:** Public API + Shadow Oracle B2B API + Shield Partner API, documentation, SDK stubs, rate limiting, billing

---

## 🧪 AGENT 12 — "QUANT" (R&D, Mathematics, ML/DL, Research)

**Role:** The scientific brain — implement all mathematical models, ML pipelines, and quantitative research

### Day 1–4: Core Mathematical Models
- [ ] **Modified Black-Scholes Engine:**
  - Implement position pricing function in Python
  - Calibrate volatility (σ) per sport/league (historical data from football-data.co.uk)
  - Validate against known cash-out prices from 1xBet/Melbet
  - Output: `price_position(current_prob, implied_prob, sigma, time_remaining, max_payout) → fair_value`

- [ ] **Bivariate Poisson Match Model:**
  - Implement Dixon-Coles model for match score prediction
  - Calibrate scoring intensities (λ) from historical data
  - Real-time Bayesian updating: posterior probability after each goal
  - Output: `predict_match(team_home, team_away, time_remaining, current_score) → prob_distribution`

- [ ] **Kelly Criterion Advisor:**
  - Implement full Kelly + fractional Kelly (¼, ½)
  - Multi-bet Kelly for accumulator positions
  - Output: `kelly_optimal(odds, true_prob, bankroll, fraction=0.25) → stake, expected_growth`

### Day 5–8: Machine Learning Models + 🆕 Sharp/Square Classifier
- [ ] **Expected Value (EV) Calculator:**
  - Bayesian inference network for true probability estimation
  - Features: team form, H2H, xG, weather, injuries, market odds movement
  - Model: Gradient Boosted Trees (XGBoost) → calibrated probabilities
  - Dataset: scrape historical odds + results from football-data.co.uk

- [ ] **Copy-Trading Scorer:**
  - Compute Sharpe Ratio, Sortino Ratio, Max Drawdown per trader
  - Rank traders by risk-adjusted performance
  - Recommend top-N traders for copy-trading

- [ ] **Fraud Detection:**
  - Isolation Forest for anomalous trading patterns
  - Autoencoder (VAE) for unsupervised anomaly detection
  - Features: trade velocity, P&L distribution, position sizes, timing patterns

- [ ] 🆕 **Sharp/Square User Classifier (Mécanisme 2 — Anti-Portfolio):**
  - Classification model: user → Sharp (top 1-5% winners) vs Square (bottom 95%)
  - Features: win rate over 50+ bets, ROI, Kelly adherence, avg odds selected, streak patterns
  - Model: LightGBM classifier with Bayesian hyperparameter tuning
  - Confidence scoring: only act on classifications with >85% confidence
  - Output: `classify_user(user_id) → {classification: sharp|square, confidence: 0.0-1.0}`
  - Feed into Prop Fund: inverse Squares externally, copy Sharps externally

### Day 9–12: Deep Learning & Advanced Models + 🆕 Wealth Engine Models
- [ ] **DRL Portfolio Optimizer (Yield Engine / Shadow Vault):**
  - PPO agent for multi-asset allocation (arbitrage opportunities across bookmakers)
  - State: portfolio weights, returns, volatility, correlation matrix
  - Action: target weights rebalancing
  - Reward: Regret-based Sharpe penalty + transaction cost scheduler
  - Train on simulated/historical data, validate with walk-forward analysis
  - 🆕 This powers the Shadow Vault (Mécanisme 5): deploy user vault capital into optimal arbitrage/EV+ strategies

- [ ] **Alternative Credit Scorer (Shadow Oracle — Mécanisme 4):**
  - Graph Neural Network (GraphSAGE) on tontine social graph
  - Features: contribution regularity, peer vouching, transaction history, Kelly adherence
  - Unsupervised clustering (DBSCAN) for risk segmentation
  - Output: credit score 0–1000 + risk tier (A/B/C/D)
  - 🆕 This model is deployed behind the Shadow Oracle B2B API (Agent 11)

- [ ] **Sentiment Engine:**
  - Fine-tune BERT/DistilBERT on African sports Twitter/Telegram corpus
  - Sentiment → odds movement correlation analysis
  - Real-time sentiment signals for pricing engine

- [ ] 🆕 **Shield Insurance Pricing Model (Mécanisme 6):**
  - Actuarial model: premium = f(true_loss_prob, coverage_pct, hedge_cost, profit_margin)
  - Use Bayesian match probability from Poisson model as true_loss_prob
  - Dynamic hedge cost estimation based on external exchange liquidity
  - Calibrate against historical payout data to ensure SA profitability target (>15% margin)

- [ ] 🆕 **Market Maker Spread Optimizer (Mécanisme 3):**
  - Optimal spread calculation: f(liquidity, volatility, time_to_event, position_EV)
  - Tighter spreads for high-liquidity positions, wider for illiquid
  - Inventory risk model: limit SA exposure on any single event direction

### Day 13–16: Monte Carlo & Stochastic Processes + 🆕 Tranche & Float Models
- [ ] **Tontine Yield Optimizer:**
  - Monte Carlo simulation (10,000 runs) for tontine payout scenarios
  - Optimize rotation order, contribution schedules, yield allocation
  - Markov Chain model for member default probability

- [ ] **Value-at-Risk (VaR) Dashboard:**
  - Historical VaR and CVaR per user portfolio
  - 95% and 99% confidence intervals
  - Stress testing: "What if all your bets lose?"

- [ ] **Volatility Surface:**
  - Build implied volatility surface across sports/leagues/match-states
  - Use for dynamic position re-pricing (like options IV surface)

- [ ] 🆕 **Yield Tranching Model (Mécanisme 7 — CDO):**
  - Position classification: Senior (prob_win > 65%), Mezzanine (40-65%), Equity (<40%)
  - Monte Carlo simulation of tranche payouts (10,000 runs)
  - Default correlation modeling between positions in same tranche
  - Pricing model for structured products (expected return per tranche risk tier)

- [ ] 🆕 **Float Deployment Optimizer (Mécanisme 1):**
  - Model optimal float allocation across DeFi protocols / T-Bills
  - Constraint: maintain liquidity buffer (20% of float always liquid for withdrawals)
  - Objective: maximize APY while keeping risk < VaR threshold

### Day 17–20: Integration & Documentation
- [ ] Package all models as Python services callable via API
- [ ] Deploy ML models (MLflow model registry or simple pickle + FastAPI)
- [ ] Write mathematical documentation: formulas, derivations, assumptions, limitations
- [ ] Create research white paper draft (for website + investor materials)
- [ ] Benchmark model accuracy: pricing engine vs actual cash-out values
- [ ] 🆕 Benchmark Sharp/Square classifier accuracy (backtest over historical user data)
- [ ] 🆕 Benchmark Shield pricing: simulated payout ratio must show SA profit margin > 15%
- [ ] 🆕 Document all wealth engine mathematical models in white paper appendix

**DELIVERABLES:** All mathematical models, ML pipelines, Sharp/Square classifier, Shield pricing, Spread optimizer, Tranche model, Float optimizer, research documentation, white paper

---

# DAILY STANDUP SCHEDULE

| Time | Activity |
|---|---|
| **09:00** | All agents sync — blockers, dependencies, progress |
| **13:00** | Agent 9 (Guardian) reviews all morning PRs |
| **17:00** | Agent 9 (Guardian) reviews all afternoon PRs |
| **18:00** | End-of-day commit — all agents push progress |

---

# INTER-AGENT DEPENDENCY MAP

```
Agent 1 (Architect) ──→ Agent 2 (Frontend) [design specs + wealth engine UI wireframes]
Agent 1 (Architect) ──→ Agent 7 (Social) [brand assets + wealth engine marketing assets]
Agent 3 (Backend)   ──→ Agent 2 (Frontend) [API endpoints + vault/shield/cashout/loan/gratitude]
Agent 3 (Backend)   ──→ Agent 4 (Telegram) [API endpoints + wealth engine commands]
Agent 3 (Backend)   ──→ Agent 5 (Discord) [API endpoints + wealth engine commands]
Agent 3 (Backend)   ──→ Agent 11 (Public API) [endpoint impl + Shadow Oracle + Shield API]
Agent 10 (Integrator)──→ Agent 2 (Frontend) [auth + data + wealth engine wiring]
Agent 10 (Integrator)──→ Agent 3 (Backend) [DB schema incl. wealth engine tables]
Agent 12 (Quant)    ──→ Agent 3 (Backend) [pricing engine + Shield pricing + spread optimizer + classifier]
Agent 12 (Quant)    ──→ Agent 11 (Public API) [Shadow Oracle credit scoring model]
Agent 8 (Sentinel)  ──→ ALL [security + legal review + wealth engine terms + Prop Fund legality]
Agent 9 (Guardian)  ──→ ALL [code review + QA + wealth engine integration tests]
Agent 6 (DevOps)    ──→ ALL [infra + deployment + Float cron + Prop Fund worker + Grafana wealth dashboard]
```

---

# CRITICAL PATH (Blocking Dependencies)

1. **Day 1:** Agent 1 delivers brand kit → unblocks Agent 2 + Agent 7
2. **Day 2:** Agent 10 delivers DB schema (incl. wealth engine tables) → unblocks Agent 3
3. **Day 3:** Agent 12 delivers pricing engine + Shield pricing model → unblocks Agent 3 pricing/shield endpoints
4. **Day 5:** Agent 3 delivers core API + wealth engine endpoints → unblocks Agent 2, 4, 5 integration
5. **Day 7:** Agent 12 delivers Sharp/Square classifier + spread optimizer → unblocks Agent 3 Prop Fund + Market Maker
6. **Day 8:** Agent 8 delivers Vault/Shield/Loan legal terms + Prop Fund legality review → unblocks Agent 2 legal pages
7. **Day 10:** Agent 12 delivers Shadow Oracle credit model → unblocks Agent 11 Oracle B2B API
8. **Day 14:** Agent 9 completes integration tests (incl. wealth engine) → unblocks Day 15 polish
9. **Day 16:** Agent 6 deploys Float cron + Prop Fund worker + Grafana wealth dashboard → unblocks monitoring
10. **Day 18:** Agent 6 completes full deployment → unblocks Day 19 launch prep
11. **Day 19:** Agent 8 final security audit of all 10 revenue mechanisms → GO/NO-GO input
12. **Day 20:** Agent 9 signs off all wealth engine mechanisms → **🚀 LAUNCH**

---

*"20 days. 12 agents. 10 revenue streams. One protocol. Let's build the future of African finance."*
