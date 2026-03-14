# 🌐 ShadowAlpha — Domain Strategy Analysis

> **Agent 1 — ARCHITECT** | March 10, 2026  
> **Decision:** Final domain recommendation for platform launch

---

## Domain Evaluation Matrix

| Criteria | `shadowalpha.io` | `shadowalpha.co` | `shadowalpha.finance` |
|---|---|---|---|
| **Trust Score** | ★★★★★ 9/10 | ★★★★☆ 7/10 | ★★★★☆ 8/10 |
| **SEO Potential** | ★★★★★ 9/10 | ★★★★☆ 7/10 | ★★★☆☆ 6/10 |
| **Brand Recall** | ★★★★★ 10/10 | ★★★★☆ 8/10 | ★★★☆☆ 5/10 |
| **Industry Fit** | ★★★★★ 9/10 | ★★★☆☆ 6/10 | ★★★★★ 10/10 |
| **Global Appeal** | ★★★★★ 9/10 | ★★★★☆ 8/10 | ★★★☆☆ 6/10 |
| **Cost Est.** | $35–60/yr | $25–40/yr | $40–80/yr |
| **TOTAL** | **46/50** | **36/50** | **35/50** |

---

## Detailed Analysis

### 1. `shadowalpha.io` — ⭐ RECOMMENDED

**Strategic Reasoning:**  
`.io` is the gold standard for tech/fintech startups. It signals: *"We are a technology company."* Used by Vercel (`vercel.com` but launched as `zeit.co` → migrated), Linear (`linear.app`), and countless YC startups. In the quant/trading space, `.io` conveys API-first, developer-friendly, and modern.

**Pros:**
- Universally recognized as a tech domain — immediate credibility with developers, quants, and AI engineers
- Short, memorable, and easy to type: `shadowalpha.io` (15 chars)
- Perfect for sub-domains: `api.shadowalpha.io`, `docs.shadowalpha.io`, `app.shadowalpha.io`
- SEO: Google treats `.io` as generic TLD (not geo-targeted to British Indian Ocean Territory)
- High trust with fintech investors and enterprise clients
- Compatible with email: `founder@shadowalpha.io` feels elite

**Cons:**
- Slightly higher cost than `.com` alternatives
- Some non-tech audiences may be unfamiliar with `.io`

**SEO Notes:**
- Google confirmed `.io` is treated as gccTLD (generic country-code) — full global SEO capability
- No geographic penalties or restrictions
- Clean domain history (assuming fresh registration)

---

### 2. `shadowalpha.co`

**Strategic Reasoning:**  
`.co` is Colombia's country code but heavily marketed as "company." Used by some startups but carries less tech cachet than `.io`. Risk of user confusion with `.com`.

**Pros:**
- Affordable and widely available
- Recognized as startup-friendly TLD
- Short URL

**Cons:**
- Users frequently mistype as `.com` → traffic leakage
- Lower trust perception in enterprise/financial contexts
- Doesn't signal "tech/API-first" as strongly as `.io`
- Potential SEO confusion with Colombian geo-targeting

---

### 3. `shadowalpha.finance`

**Strategic Reasoning:**  
New gTLD that explicitly signals financial services. Strong vertical alignment but weak general tech perception.

**Pros:**
- Immediate industry association: *"This is a financial platform"*
- Regulatory-friendly perception
- Good for trust with traditional finance audiences

**Cons:**
- Long URL: `shadowalpha.finance` (22 chars) — poor for marketing
- Low adoption rate → unfamiliar to most users
- Higher registration cost
- Awkward sub-domains: `api.shadowalpha.finance` feels clunky
- Email `contact@shadowalpha.finance` is unwieldy
- Poor brand recall compared to `.io`

---

## 🏆 Final Recommendation

> **Register `shadowalpha.io` as primary domain.**

### Rationale
1. **Brand positioning:** ShadowAlpha is a *technology-first* platform with AI/ML at its core — `.io` is the native TLD for this identity
2. **Developer ecosystem:** The public API (`api.shadowalpha.io`) is a core revenue stream — `.io` signals API-first culture
3. **Investor perception:** VC-backed fintech startups live on `.io` — immediate pattern recognition
4. **Email authority:** `@shadowalpha.io` is short, clean, and elite
5. **Global reach:** No geo-targeting restrictions, full SEO capability worldwide

### Secondary Registration (defensive)
Also register `shadowalpha.com` if available, and `shadowalpha.co` as defensive domains. Redirect both to `shadowalpha.io`.

### DNS Architecture
```
shadowalpha.io          → Vercel (frontend)
api.shadowalpha.io      → Backend API (Railway/Render)
docs.shadowalpha.io     → API Documentation
app.shadowalpha.io      → Web Application (future)
mail.shadowalpha.io     → Email (Google Workspace)
```

### Action Items
1. Register `shadowalpha.io` via **Cloudflare Registrar** (cheapest renewal, free DNS, built-in DDoS protection)
2. Configure Cloudflare DNS immediately
3. Set up Google Workspace for `@shadowalpha.io` email
4. Register defensive domains within 48 hours
