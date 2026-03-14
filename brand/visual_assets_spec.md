# 🖼️ ShadowAlpha — Visual Assets Specification

> **Agent 1 — ARCHITECT** | March 10, 2026

---

## Asset Inventory

### Logos (3 Concepts)

| # | Name | File | Description |
|---|------|------|-------------|
| 1 | Geometric Shield | `logo_concept_1.png` | Angular faceted shield with SA monogram — financial authority + AI precision |
| 2 | SA Monogram | `logo_concept_2.png` | Interlocking S+A lettermark — minimal, works at all sizes |
| 3 | Alpha Circuit | `logo_concept_3.png` | Stylized α as neural network node — tech-forward, distinctive |

**Recommendation:** Use **Concept 2 (SA Monogram)** as primary favicon/app icon for its clarity at small sizes. Use **Concept 1 or 3** as the full-size product logo depending on preference.

---

### Favicon

| Size | Usage | Format | Background |
|------|-------|--------|------------|
| 16×16 | Browser tab | ICO/PNG | `#0A0A0A` |
| 32×32 | Browser tab (Retina) | PNG | `#0A0A0A` |
| 48×48 | Windows shortcut | PNG | `#0A0A0A` |
| 180×180 | Apple Touch Icon | PNG | `#0A0A0A` |
| 192×192 | Android Chrome | PNG | `#0A0A0A` |
| 512×512 | PWA / Manifest | PNG | `#0A0A0A` |

**Concept:** `favicon_concept.png` — Bold gold α on black square

**HTML Implementation:**
```html
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0A0A0A">
```

---

### Open Graph Image

| Property | Value |
|----------|-------|
| Dimensions | 1200 × 630 px |
| Format | PNG / JPG (< 300KB) |
| File | `og_image.png` |
| Background | `#0A0A0A` with geometric grid |
| Content | Brand name + tagline + subtle teal chart |

**HTML Implementation:**
```html
<meta property="og:image" content="https://shadowalpha.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ShadowAlpha — AI-Powered Quantitative Trading">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://shadowalpha.io/og-image.png">
```

---

### Social Media Banners

| Platform | Dimensions | File | Notes |
|----------|-----------|------|-------|
| **Facebook** | 820 × 312 px | `banner_facebook.png` | Cover photo — gold/teal split composition |
| **YouTube** | 2560 × 1440 px | `banner_youtube.png` | Safe area center: 1546×423. Cinematic wide |
| **Discord** | 960 × 540 px | `banner_discord.png` | Server banner — α symbol with glow |
| **Telegram** | 1280 × 640 px | `banner_telegram.png` | Channel header — neural network subtle bg |

**Profile Picture (all platforms):** Use logo Concept 2 (SA Monogram) or Concept 3 (Alpha Circuit), 500×500px minimum, centered on `#0A0A0A` square background.

---

### Twitter/X Assets

| Asset | Dimensions | Notes |
|-------|-----------|-------|
| Profile picture | 400 × 400 px | Logo on black, PNG |
| Header | 1500 × 500 px | Adapt YouTube banner (crop center) |

### LinkedIn Assets

| Asset | Dimensions | Notes |
|-------|-----------|-------|
| Company logo | 300 × 300 px | Logo on black, PNG |
| Cover image | 1128 × 191 px | Adapt Facebook banner (crop center) |

---

## Production Export Checklist

For final production, each logo should be exported as:

```
brand/assets/
├── logos/
│   ├── logo-shield-gold-dark.svg      # Concept 1 on transparent
│   ├── logo-shield-white-dark.svg     # Concept 1 white variant
│   ├── logo-monogram-gold-dark.svg    # Concept 2 on transparent
│   ├── logo-monogram-white-dark.svg   # Concept 2 white variant
│   ├── logo-alpha-gold-dark.svg       # Concept 3 on transparent
│   ├── logo-alpha-white-dark.svg      # Concept 3 white variant
│   └── logo-alpha-black-light.svg     # Concept 3 for light backgrounds
├── favicons/
│   ├── favicon.ico                     # Multi-size ICO
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── apple-touch-icon.png           # 180×180
│   ├── android-chrome-192x192.png
│   ├── android-chrome-512x512.png
│   └── site.webmanifest
├── social/
│   ├── og-image.png                   # 1200×630
│   ├── banner-facebook.png            # 820×312
│   ├── banner-youtube.png             # 2560×1440
│   ├── banner-discord.png             # 960×540
│   ├── banner-telegram.png            # 1280×640
│   ├── banner-twitter.png             # 1500×500
│   ├── banner-linkedin.png            # 1128×191
│   └── profile-pic-500.png            # 500×500
└── misc/
    ├── email-logo.png                 # 200×auto for email signature
    └── loading-spinner.svg            # Animated gold α
```

---

*All generated concept images are available in the brain artifacts directory for review.*
