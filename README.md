# Air Sign

**Sign PDFs and images in your browser using your webcam.** Hand tracking runs locally: your document stays on your device until you **export**. First signature free; optional paid slots in the app.

**[Try Air Sign →](https://sign-jade-two.vercel.app/app.html)** · **[Live site](https://sign-jade-two.vercel.app/)** · **Author:** [Alexey Vishnevsky](https://www.linkedin.com/in/vushnevskuu)

*Canonical URLs (SEO) point here.* **Mirror:** [GitHub Pages](https://vushnevskuu.github.io/sign/) — same build if Pages is enabled.

---

## Why Air Sign

- **Privacy-first flow** — signing happens in the browser; we’re not taking your PDF to a server to apply the signature.
- **No install** for the web app — modern browser + webcam.
- **Gesture UX** — draw in the air, confirm, drag the signature, download.

Air Sign is **not** a full enterprise e-signature platform (audit trails, legal compliance packages). It’s built for quick, local-first signing and for developers curious about hand tracking + PDFs.

---

## Quick start (web)

Open **[the app](https://sign-jade-two.vercel.app/app.html)** or clone and run locally:

```bash
git clone https://github.com/vushnevskuu/sign.git
cd sign
npm install
npm start
```

Then open http://localhost:3000/app.html and allow camera access.

---

## Python finger tracker (desktop demo)

Tracks one finger via webcam (MediaPipe Hands). Useful for local experiments; the **recommended** flow for most users is the browser app above.

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements-python.txt
python finger_tracker.py
```

| Key | Action |
|-----|--------|
| **Q** | Quit |
| **C** | Clear canvas (desktop) |

### CLI options

| Flag | Description |
|------|-------------|
| `-f`, `--finger` | Landmark id: 4, 8, 12, 16, 20 (default **8** — index) |
| `-s`, `--smooth` | Smoothing window (default 5; `0` = off) |
| `-r`, `--record` | Record trajectory to file |
| `-c`, `--camera` | Camera index (default 0) |

### MediaPipe model

`hand_landmarker.task` should sit next to the script. If missing:

```bash
curl -sL "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" -o hand_landmarker.task
```

### Local web server (camera in browser)

```bash
python serve.py
```

Open http://localhost:8765 — camera access is in the **browser**, not on the server.

---

## Deploy

- **GitHub Pages:** `static/` is the source; `npm run build` copies to `public/` for Vercel (see `vercel.json`).

---

## Marketing & positioning

Product and SEO context for humans and AI agents lives in:

- **[`.agents/product-marketing-context.md`](.agents/product-marketing-context.md)** — positioning, ICP, objections (template from [Marketing Skills](https://github.com/coreyhaines31/marketingskills))
- **[`marketing/`](marketing/)** — keywords, messaging, GitHub About text, content ideas

---

## На русском

**Air Sign** — подпись PDF (и изображений) в браузере с помощью веб-камеры и отслеживания руки. Обработка идёт у тебя в браузере; файл не нужно загружать на сервер **для самого процесса подписи** — ты экспортируешь результат, когда готов.

- **Демо в браузере:** https://sign-jade-two.vercel.app/app.html  
- **Маркетинг и SEO-заметки:** папка [`marketing/`](marketing/)
