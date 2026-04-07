# SEO: ключи, интенты, FAQ

Цель — находимость по **проблеме** (подписать PDF в браузере) и по **механике** (webcam, hand tracking, gesture sign).

## Кластеры запросов (английский — основной для GitHub Pages)

### Высокий приоритет (информационный + инструмент)

| Ключ / формулировка | Интент | Куда вести |
|---------------------|--------|------------|
| sign pdf in browser without uploading | решение проблемы | `/` + блок про privacy |
| webcam signature pdf | инструмент | `/`, `/app.html` |
| hand tracking signature browser | тех. аудитория | README, `/` |
| draw signature in air webcam | демо / wow | лендинг + видео |
| client side pdf sign javascript | разработчики | README, GitHub topics |
| mediapipe hands signature demo | разработчики | README |
| free pdf signer browser | коммерческий альтернативный | лендинг (честно: freemium) |
| private pdf signature local | privacy | hero + meta description |

### Средний приоритет

- browser pdf signature no account  
- sign pdf offline browser (уточнять: нужен интернет для загрузки страницы, обработка локальная)  
- alternative to docusign for personal use  
- electronic signature without cloud  

### Русский (вторичный)

- подписать пдф в браузере  
- подпись веб камера  
- подпись жестом pdf  

Имеет смысл завести отдельную RU-страницу или пост только если готовы поддерживать язык в UI.

## Meta title / description (рекомендации)

Уже заданы на `index.html` / `app.html`. Для экспериментов в GSC можно ротировать description вокруг трёх крючков: **local / webcam / no upload**.

**Title (≤60 символов):**  
`Air Sign — Sign PDFs in Your Browser (Webcam Hand Tracking)`

**Description (≤155):**  
`Draw your signature in the air with your webcam. Hand tracking runs in your browser — your PDF stays on your device until you export. First signature free.`

## FAQ (для людей и для расширения Schema на сайте)

1. **Does Air Sign upload my PDF to a server?**  
   Processing happens in your browser. The file is not sent to our servers for signing; you export when ready.

2. **Do I need an account?**  
   No account required to try. Optional paid slots may apply after free uses (see app messaging).

3. **Does it work without a webcam?**  
   The air-signature flow needs a camera. Without it, use another signing method.

4. **Which browsers are supported?**  
   Modern Chromium-based browsers and recent Safari/Firefox with WebGL and camera access — always state “requires modern browser” in support copy.

5. **Is it legally binding?**  
   Air Sign does not provide legal advice. Requirements vary by country and document type.

6. **Who built it?**  
   Alexey Vishnevsky — links: GitHub `vushnevskuu`, LinkedIn in repo and site footer.

## Технический SEO (чеклист)

- [x] Canonical на `index.html` и `app.html`
- [x] `WebApplication` JSON-LD
- [ ] **Google Search Console** — основной префикс: `https://sign-pink-one.vercel.app` (и опционально зеркало `https://vushnevskuu.github.io/sign/`)
- [x] `sitemap.xml` / `robots.txt` (абсолютные URL на Vercel)
- [ ] `robots.txt` разрешающий индексацию публичных путей
- [ ] Стабильный **og:image** (абсолютный URL постера демо)

## AI-поиск (AEO)

Фразы в стиле ответа LLM (добавить в README и на лендинг естественным текстом):

- “Air Sign is a browser-based tool that lets you sign PDFs using webcam hand tracking; files stay on your device until export.”
- “It is not a full replacement for enterprise e-signature platforms that provide audit trails and compliance workflows.”
