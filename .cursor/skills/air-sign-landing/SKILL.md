---
name: air-sign-landing
description: >-
  Single-page English landing for the Air Sign webcam PDF signer (GitHub Pages
  static/). Covers SEO meta/JSON-LD, pricing copy (1 free + $1 extra), localStorage
  credit model, Stripe Payment Link placeholder, and deferring camera until Sign.
---

# Air Sign landing (static site)

## When to use

Editing `sign/static/index.html` or related static assets for the hand-tracking document signer deployed from the `static/` folder.

## Product facts

- App runs in the browser; **webcam required** (tested mindset: MacBook + Safari/Chrome).
- MediaPipe hand tracking; user draws signature in the air, confirms with gestures.
- Hosting: GitHub Pages uploads **only** `static/` (see `.github/workflows/deploy.yml`). No server-side API.

## Pricing model (client-only)

- **1 signature free** per browser (localStorage).
- **$1 for one additional signature** via Stripe Payment Link; success redirect should append `?paid=1` so the page grants one credit (client-side only — document limitation for static hosting).

## SEO checklist

- `lang="en"`, unique `<title>`, meta description, canonical URL (replace placeholder with real domain).
- Open Graph + Twitter Card meta.
- `application/ld+json` for `WebApplication`.
- Optional: `robots.txt`, `sitemap.xml` with absolute URLs after domain is known.

## UX rules

- Do **not** call `getUserMedia` until the user clicks **Sign** (privacy + clearer permissions).
- Primary CTA: start signing / use app. Secondary: pricing (`#pay` → “Buy another slot”).
- Paywall: two copy modes — **out of slots** vs **prepay** (user still has slots). If Stripe URL is empty, show “Checkout is not available” (no technical alerts to visitors).
- After `?paid=1`, show a short success toast and refresh credits + Sign button label (`Sign` vs `Unlock to sign — $1`).
- All user-visible strings on the page: **English only**.

## Code locations

- Main UI and logic: `static/index.html`.
- Default PDF path: resolved from `window.location` (works on Pages subpaths if trailing slash is correct).
