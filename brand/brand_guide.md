# 📐 ShadowAlpha — Brand Guide

> **Agent 1 — ARCHITECT** | Version 1.0 | March 10, 2026  
> *This document is the single source of truth for all visual communications.*

---

## 1. Brand Identity

**Name:** ShadowAlpha  
**Tagline:** *AI-Powered Quantitative Trading Intelligence*  
**Positioning:** Elite, technology-first quantitative trading platform  
**Tone:** Dark · Secretive · Technical · Authoritative · Futuristic  
**Visual DNA:** Trading terminals · Cybersecurity dashboards · CLI interfaces · Hedge fund aesthetics

---

## 2. Logo System

### 2.1 Logo Concepts

| Concept | Name | Description | Best For |
|---------|------|-------------|----------|
| **1** | Geometric Shield | Angular faceted shield with SA monogram — evokes financial authority + AI precision | Product UI, landing page hero |
| **2** | SA Monogram | Interlocking "S" + "A" lettermark — minimal geometric precision, candlestick pattern echo | Favicon, app icon, watermarks |
| **3** | Alpha Circuit | Stylized α reimagined as neural network node with data pathways | Technical docs, API branding, merch |

### 2.2 Logo Usage Rules

- **Minimum size:** 24px height (digital), 10mm (print)
- **Clear space:** Minimum 50% of logo height on all sides
- **On dark backgrounds:** Gold (#F4B70F) or White (#FFFFFF) logo
- **On light backgrounds:** Black (#0A0A0A) logo (rare — dark mode first)
- **Never:** Stretch, rotate, add effects, change colors outside brand palette, place on busy backgrounds

### 2.3 Logo File Format Requirements
| Usage | Format | Background |
|-------|--------|------------|
| Web / UI | SVG (preferred), PNG | Transparent |
| Favicon | ICO, PNG (16/32/180px) | Black #0A0A0A |
| Social Media | PNG @2x | Black #0A0A0A |
| Print | PDF, EPS, SVG | Transparent |
| Email | PNG @2x, 200px max width | Transparent |

---

## 3. Color System

### 3.1 Primary Palette

| Role | Name | Hex | RGB | Usage |
|------|------|-----|-----|-------|
| **Primary** | Black | `#0A0A0A` | 10, 10, 10 | Backgrounds, base surfaces |
| **Brand** | Gold | `#F4B70F` | 244, 183, 15 | CTAs, brand marks, highlights |
| **Surface** | Charcoal | `#1A1A2E` | 26, 26, 46 | Cards, elevated surfaces, panels |
| **Accent** | Teal | `#00D4AA` | 0, 212, 170 | Success states, positive values, accents |

### 3.2 Semantic Colors

| Role | Hex | Usage |
|------|-----|-------|
| Success / Profit | `#00D4AA` | Positive P&L, confirmations, up trends |
| Warning / Alert | `#F4B70F` | Caution, pending states, alerts |
| Danger / Loss | `#FF4757` | Errors, negative P&L, down trends |
| Info | `#3B82F6` | Informational, links, help |

### 3.3 WCAG AA Accessibility — Contrast Ratios

| Foreground | Background | Ratio | AA Pass | Usage |
|-----------|------------|-------|---------|-------|
| White `#FFF` | Black `#0A0A0A` | **19.6:1** | ✅ AAA | Primary text |
| Gold `#F4B70F` | Black `#0A0A0A` | **9.2:1** | ✅ AAA | Brand text, headings |
| Teal `#00D4AA` | Black `#0A0A0A` | **10.8:1** | ✅ AAA | Accent text |
| White `#FFF` | Charcoal `#1A1A2E` | **15.1:1** | ✅ AAA | Text on cards |
| Gold `#F4B70F` | Charcoal `#1A1A2E` | **7.1:1** | ✅ AA | Brand text on cards |
| Danger `#FF4757` | Black `#0A0A0A` | **4.9:1** | ✅ AA | Error text |
| Secondary `#B8B8CC` | Black `#0A0A0A` | **10.2:1** | ✅ AAA | Secondary text |
| Tertiary `#5A5A80` | Black `#0A0A0A` | **3.6:1** | ⚠️ AA Large | Tertiary / disabled only |

> **Rule:** All text must meet **WCAG AA minimum (4.5:1)** for normal text and **3:1** for large text (18px+ or 14px bold).
> Tertiary text (#5A5A80) should *only* be used for decorative labels, timestamps, or non-critical UI elements.

### 3.4 Color Hierarchy Rules

1. **Black (#0A0A0A)** → All backgrounds, root surface. *"The void from which alpha emerges."*
2. **Gold (#F4B70F)** → Use sparingly. Only for: brand marks, primary CTAs, key metrics, active states. *Maximum 15% of any screen.*
3. **Charcoal (#1A1A2E)** → Cards, panels, input fields, modal overlays. Creates elevation.
4. **Teal (#00D4AA)** → Positive financial states (profit, up trend), secondary accent. Never for navigation.
5. **Danger (#FF4757)** → Loss, errors, destructive actions only. Never decorative.

---

## 4. Typography

### 4.1 Font Families

| Role | Font | Weight | Source |
|------|------|--------|--------|
| UI / Body / Headings | **Inter** | 300–900 | Google Fonts |
| Code / Monospace / Data | **JetBrains Mono** | 400–700 | Google Fonts |

### 4.2 Type Scale (Major Third — 1.250 ratio)

| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| `display` | 76.3px | 900 Black | 1.0 | Hero headings (landing page) |
| `h1` | 61px | 800 ExtraBold | 1.15 | Page titles |
| `h2` | 48.8px | 700 Bold | 1.15 | Section headings |
| `h3` | 39px | 700 Bold | 1.3 | Sub-sections |
| `h4` | 31.3px | 600 SemiBold | 1.3 | Card headers |
| `h5` | 25px | 600 SemiBold | 1.3 | Widget titles |
| `h6` | 20px | 500 Medium | 1.3 | Label headers |
| `body-lg` | 18px | 400 Regular | 1.625 | Leading paragraphs |
| `body` | 16px | 400 Regular | 1.5 | Default body copy |
| `body-sm` | 13.3px | 400 Regular | 1.5 | Secondary text |
| `caption` | 11.1px | 500 Medium | 1.5 | Timestamps, labels |
| `overline` | 11.1px | 600 SemiBold | 1.5 | Category labels (UPPERCASE) |
| `code` | 13.3px | 400 Regular | 1.625 | Inline code, data values |

### 4.3 Typography Rules

1. **Headings:** Always Inter. Letter-spacing: -0.025em for h1–h3, 0 for h4–h6
2. **Body:** Inter Regular. Max line width: 65–80 characters for readability
3. **Code/Data:** JetBrains Mono. Use tabular-nums for number alignment in tables
4. **Financial amounts:** JetBrains Mono + tabular-nums, right-aligned
5. **ALL CAPS:** Only for overline labels and badges. Never for headings or body text

---

## 5. Spacing System

**Base unit: 4px grid**

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | 4px | Inline element gaps, icon padding |
| `space-2` | 8px | Tight component padding |
| `space-3` | 12px | Input padding, small gaps |
| `space-4` | 16px | Default component padding |
| `space-6` | 24px | Card padding, section gaps |
| `space-8` | 32px | Between components |
| `space-12` | 48px | Between sections |
| `space-16` | 64px | Page section spacing |
| `space-24` | 96px | Major section spacing |

**Rule:** All spacing values must be divisible by 4.

---

## 6. Component Tokens

### Border Radius
| Token | Value | Usage |
|-------|-------|-------|
| `radius-sm` | 4px | Badges, tags, small elements |
| `radius-md` | 8px | Buttons, inputs, cards |
| `radius-lg` | 12px | Large cards, panels |
| `radius-xl` | 16px | Modals, feature cards |
| `radius-full` | 9999px | Pills, avatars, toggles |

### Shadows & Elevation
| Level | Usage | Shadow |
|-------|-------|--------|
| Base (0) | Page background | None |
| Raised (1) | Cards, panels | `0 2px 4px rgba(0,0,0,0.4)` |
| Overlay (2) | Dropdowns, popovers | `0 4px 8px rgba(0,0,0,0.4)` |
| Modal (3) | Modals, drawers | `0 8px 24px rgba(0,0,0,0.5)` |
| Toast (4) | Notifications | `0 16px 48px rgba(0,0,0,0.6)` |

### Brand Shadows
| Type | Usage |
|------|-------|
| Gold glow | Primary CTA hover: `0 4px 24px rgba(244,183,15,0.20)` |
| Teal glow | Success states: `0 4px 24px rgba(0,212,170,0.20)` |
| Danger glow | Error states: `0 4px 24px rgba(255,71,87,0.20)` |

---

## 7. Glassmorphism

ShadowAlpha uses glassmorphism for premium overlay elements:

```css
/* Standard Glass */
background: rgba(26, 26, 46, 0.40);
backdrop-filter: blur(16px);
border: 1px solid rgba(255, 255, 255, 0.06);

/* Heavy Glass (modals, important overlays) */
background: rgba(26, 26, 46, 0.70);
backdrop-filter: blur(32px);
border: 1px solid rgba(255, 255, 255, 0.08);
```

**Usage:** Navigation bars, modal backgrounds, floating action bars, tooltip backgrounds

---

## 8. Motion & Animation

| Animation | Duration | Easing | Usage |
|-----------|----------|--------|-------|
| Fade in | 300ms | ease-out | Page loads, reveals |
| Fade in + up | 400ms | ease-out | Cards appearing, list items |
| Hover lift | 200ms | default | Card hovers, buttons |
| Gold pulse | 2s infinite | — | CTA attention, live indicators |
| Terminal cursor | 1s step-end | — | Code blocks, terminal UI |
| Shimmer | 1.5s infinite | — | Loading skeletons |

**Rules:**
1. No animation longer than 500ms (except infinite loops)
2. `prefers-reduced-motion` must disable all non-essential animations
3. Use `will-change` for GPU-accelerated animations
4. Never animate on page load — use intersection observer

---

## 9. Implementation Reference

The complete CSS design system is available at:
→ `brand/design-system.css`

Import in your root stylesheet:
```css
@import './brand/design-system.css';
```

All tokens are defined as CSS custom properties on `:root` and can be used with `var(--token-name)`.

---

*"Every pixel tells the story of elite financial intelligence."*
