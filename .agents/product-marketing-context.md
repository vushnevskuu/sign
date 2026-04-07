# Product Marketing Context — Air Sign

*Last updated: 2026-04-06*

## Product Overview

**One-liner:** Sign PDFs and images in the browser using your webcam and hand tracking — no upload until you export.

**What it does:** Air Sign runs entirely in the user’s browser: open a PDF or image, draw a signature in the air with hand gestures, confirm with gestures, drag the signature onto the document, and export. Hand tracking uses the device camera; the document stays local until the user chooses to download a signed file.

**Product category:** Browser-based PDF signing, e-signature tools, privacy-first document tools, webcam / computer-vision utilities.

**Product type:** Client-side web app (static hosting) + optional Python demos for finger tracking.

**Business model:** Freemium in-browser (first signature free; additional slots via low-friction payment / Stripe when enabled). Open source on GitHub.

## Target Audience

**Target companies:** Less primary — product is prosumer / individual-first. Secondary: freelancers, micro-businesses, educators, developers evaluating hand-tracking UX.

**Decision-makers:** Individual users who need a quick signed PDF without installing desktop e-sign software; privacy-conscious signers; tech-curious early adopters.

**Primary use case:** “I need to put my signature on this PDF right now, on this machine, without sending the file to a server.”

**Jobs to be done:**

- Sign a PDF or image quickly without account friction.
- Avoid uploading sensitive documents to third-party clouds.
- Try a novel, gesture-based signing experience (demo / wow factor).

**Use cases:**

- One-off contracts, forms, scans.
- Personal documents where privacy matters.
- Demos of in-browser MediaPipe / hand-tracking (developer audience).

## Personas

| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| Privacy-focused signer | Local processing, no cloud | Distrust of upload-based tools | File stays on device until export |
| Casual user | Speed, no install | Complexity of enterprise e-sign | Works in modern browser with webcam |
| Builder / developer | How it works, OSS | Reusable patterns for CV in browser | Clear repo, MIT-friendly stack, GitHub presence |

## Problems & Pain Points

**Core problem:** Traditional e-sign flows often require accounts, uploads, or installed apps — and feel heavy for a single signature.

**Why alternatives fall short:**

- Cloud-first signers: require trust and upload of full documents.
- Desktop tools: install friction and OS lock-in.
- Mobile-only flows: poor fit for laptop users with a webcam.

**What it costs them:** Time (signup, onboarding), anxiety (data residency), or money (subscriptions for rare use).

**Emotional tension:** “Is this document safe?” and “I just need this done once.”

## Competitive Landscape

**Direct:** Browser PDF viewers with draw tools — often lack air / gesture signing and guided confirm flow.

**Secondary:** DocuSign, Adobe Acrobat Sign, Dropbox Sign — strong for compliance and workflows; overkill for quick local signing and imply cloud processing.

**Indirect:** Print → sign → scan; tablet + stylus apps — different hardware, not “webcam in air.”

**How each falls short for our ICP:** Either too enterprise-heavy, upload-dependent, or not gesture / webcam-native.

## Differentiation

**Key differentiators:**

- Hand-tracked signature in free space, confirmed with gestures.
- Processing in the browser; privacy story is real, not marketing-only.
- Open source; attributable creator (GitHub + LinkedIn).

**How we do it differently:** MediaPipe (or equivalent) in the client, explicit export step, minimal server surface for the static app.

**Why that’s better:** Lower trust bar for sensitive one-offs; memorable UX; hackable for developers.

**Why customers choose us:** Speed + novelty + privacy narrative + no mandatory account for first use.

## Objections

| Objection | Response |
|-----------|----------|
| “Is this legally binding?” | We don’t provide legal advice; users should follow jurisdiction and document requirements. Position as practical signing aid, not a compliance suite. |
| “I don’t have a webcam / don’t want camera on.” | Honest: product requires a camera for the air-sign path; point to traditional upload/sign tools as alternative. |
| “Is my PDF uploaded?” | No — processing is in-browser until you export; link to README / privacy explanation. |
| “Why pay for more slots?” | Optional; supports continued development; first signature free to try the full flow. |

**Anti-persona:** Organizations needing audit trails, multi-party workflow, or regulated e-IDAS/QES-level guarantees.

## Switching Dynamics

**Push:** Fatigue with SaaS accounts; fear of data on unknown servers; desire for instant try.

**Pull:** Try in 30 seconds; tactile “magic” of air signing; open code.

**Habit:** Default tool is whatever employer bought (DocuSign, etc.).

**Anxiety:** Camera permissions; “is this a toy?” — counter with privacy facts and export control.

## Customer Language

**How they describe the problem:**

- “Sign this PDF without uploading it.”
- “Quick signature in the browser.”
- “Webcam hand tracking signature.”

**How they describe us (desired):**

- “Air Sign — sign in the air, stays on your device.”
- “Browser PDF signer with gestures.”

**Words to use:** browser, webcam, hand tracking, private, local, export, PDF, signature, open source, free first signature.

**Words to avoid overusing:** “AI” without clarity (prefer hand tracking / computer vision where accurate); “enterprise” unless targeting that segment.

**Glossary:**

| Term | Meaning |
|------|---------|
| Air Sign | Product name; signing gesture in space in front of webcam |
| Hand tracking | Detecting hand pose in video to drive cursor / stroke |
| Export | User-initiated download of signed PDF |

## Brand Voice

**Tone:** Calm, precise, slightly retro / craft (typewriter aesthetic) — not hypey.

**Style:** Short sentences; lead with privacy and control; English primary for global GitHub and SEO.

**Personality:** Minimal, trustworthy, maker-built, engineering-literate.

## Proof Points

**Metrics:** (Fill as available — e.g. GitHub stars, demo completions.)

**Customers:** Individual users and developers; no enterprise logo wall required for positioning.

**Testimonials:** (Add when available.)

**Value themes:**

| Theme | Proof |
|-------|-------|
| Privacy | Client-side processing until export |
| Simplicity | No install for web app |
| Openness | Public GitHub repo |

## Goals

**Business goal:** Grow qualified traffic and GitHub visibility; convert try → signature → optional paid slot.

**Conversion action:** Open app, complete first signature, star/fork repo (secondary).

**Current metrics:** (Add Analytics / Plausible later if installed.)

## Primary URLs & Creator (for consistency across SEO and schema)

- **Live app:** https://sign-pink-one.vercel.app/
- **Signer:** https://sign-pink-one.vercel.app/app.html
- **Repository:** https://github.com/vushnevskuu/sign
- **Creator:** Alexey Vishnevsky — https://www.linkedin.com/in/vushnevskuu
