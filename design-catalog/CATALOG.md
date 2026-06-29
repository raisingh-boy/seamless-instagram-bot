# SEAMLESS Design Catalog

Created: 2026-06-02 · Session: Reference Nastya Analysis
Inspiration: Pinterest moodboard + @seamless.mrp Instagram + Swiss/Brutalist/Bauhaus research
Photo credit: @andrey_berezkin (SEAMLESS Nextcloud)
All designs: 1080×1350px · HTML/CSS · Playwright render

---

## Design Index

### #1 — Split Text/Photo (Product)
- **Style:** Minimalist, raw/industrial
- **Fonts:** Courier Prime (400/700)
- **BG:** #f8f8f8 · Text: #1a1a1a, #555
- **Techniques:** Split layout (text top, photo bottom), slide number circle, italic CTA
- **File:** test_nastya_slide.html

### #2 — Full-Photo Overlay
- **Style:** Atmospheric, dark gradient
- **Fonts:** IBM Plex Mono (400), Courier Prime (400/italic)
- **BG:** Dark photo overlay (linear-gradient 0.65→0.05)
- **Techniques:** Full-bleed photo, gradient overlay, white text on dark
- **File:** test_nastya_var2.html

### #3 — Editorial Quote (Centered)
- **Style:** Minimalist editorial, air-heavy
- **Fonts:** Courier Prime (400/700/italic)
- **BG:** #fafaf8 · Accent: #d4c8b8 (earth)
- **Techniques:** Centered quote, large type, thin line divider, accent circle
- **File:** test_nastya_var3.html

### #4 — Asymmetric Split
- **Style:** Editorial, large-number
- **Fonts:** IBM Plex Mono (300), Courier Prime (700/400)
- **BG:** #fafaf8 (text) / earth gradient (photo)
- **Techniques:** 45/55 split, giant watermark number, mono label, divider line
- **File:** test_nastya_var4.html

### #5 — Magazine Editorial (3-col)
- **Style:** Swiss magazine spread
- **Fonts:** IBM Plex Mono (400/600), Courier Prime (700)
- **BG:** #ffffff · Vertical accent line, 3-column bottom grid
- **Techniques:** 12-grid, vertical sidebar text, horizontal+vertical mix, 3-col footer
- **File:** test_nastya_var5.html

### #6 — Deconstructed Moodboard
- **Style:** Art-gallery, quotable
- **Fonts:** Courier Prime (700), IBM Plex Mono (300/400)
- **BG:** #f8f6f2 · Number watermark #e8e4de · Accent: #d4ccc0
- **Techniques:** Giant watermark number, dot+label header, vertical accent line, corner hairlines
- **File:** test_nastya_var6.html

### #7 — Swiss Editorial (12-grid)
- **Style:** International Typographic Style, structured
- **Fonts:** IBM Plex Mono (300/500), Courier Prime (400), Inter (400)
- **BG:** #ffffff · Watermark #f5f5f3
- **Techniques:** 12-column grid, 80px margins, 24px gutters, asymmetric hero+image, vertical accent
- **File:** test_nastya_var7.html

### #8 — Brutalist Raw
- **Style:** Anti-aesthetic, raw, visible grid
- **Fonts:** IBM Plex Mono (600), Courier Prime (400)
- **BG:** #f0ece4 · Raw borders #111 · Circle #ddd5c8
- **Techniques:** Visible grid lines, raw structural borders, strikethrough text, brutalist circle
- **File:** test_nastya_var8.html

### #9 — Bauhaus Geometric
- **Style:** Bauhaus, primary colors, geometric
- **Fonts:** IBM Plex Mono (300/500/700), Courier Prime (400/italic)
- **BG:** #fdfcf8 · Circle: #c23b22 · Triangle: #1a3a5c · Rect: #d4a017
- **Techniques:** Geometric shapes (circle/triangle/rectangle), horizontal line, info blocks
- **File:** test_nastya_var9.html

### #10 — Ethereal Frosted Glass
- **Style:** Ethereal, soft-focus, atmospheric
- **Fonts:** IBM Plex Mono (500), Courier Prime (400/italic)
- **BG:** #f5f2ed · Glass: rgba(255,255,255,0.55)
- **Techniques:** Backdrop-filter blur (20px), radial gradient atmosphere, frosted glass panel, hairline
- **File:** test_nastya_var10.html

### #11 — Full Photo + Stroke + Mixed Weights
- **Style:** Bold editorial, luxury
- **Fonts:** Playfair Display (400italic/900), IBM Plex Mono (300), Space Mono (400)
- **Photo:** SEAMLESS (7O0A0074.jpg)
- **Techniques:** -webkit-text-stroke, dramatic letter-spacing (12px), mixed weights in one line
- **File:** test_photo_real1.html

### #12 — Photo Right + Italic Serif + Rotated Strip
- **Style:** Romantic editorial, literary
- **Fonts:** Playfair Display (400italic), Space Mono (400), IBM Plex Mono (400)
- **Photo:** SEAMLESS (7O0A2300.jpg)
- **Techniques:** 52/48 split, rotated credit strip (90deg), giant watermark number, golden accent
- **File:** test_photo_real2.html

### #13 — Multi-Direction + Framed Photo
- **Style:** Avant-garde editorial, 3-axis typography
- **Fonts:** Playfair Display (900), Space Mono (400), IBM Plex Mono (400), Courier Prime (400italic)
- **Photo:** SEAMLESS (7O0A2300.jpg)
- **Techniques:** All 3 text directions simultaneously, photo frame (2px border), gold accent line
- **File:** test_photo_real3.html

---

## Font Library
| Font | Type | Weights | Use Case |
|------|------|---------|----------|
| Courier Prime | Monospace serif | 400, 700, 400italic | Body, labels, raw aesthetic |
| IBM Plex Mono | Monospace sans | 200, 300, 400, 500, 600, 700 | Labels, headers, ultrawide spacing |
| Playfair Display | Serif | 400, 400italic, 700, 900 | Headlines, editorial, luxury |
| Space Mono | Monospace | 400, 700 | Labels, tech feel |
| Inter | Sans-serif | 300, 400, 500, 600 | UI, readability |
| Anton | Display sans | 400 | Impact headlines |

## Technique Library
- `writing-mode: vertical-rl` — text top→bottom
- `transform: rotate(-90deg)` — text bottom→up
- `-webkit-text-stroke` — outlined text
- `letter-spacing: 4-12px` — wide spacing
- `backdrop-filter: blur(20px)` — frosted glass
- `mix-blend-mode` — photo/text blending
- `filter: blur()` — soft focus
- `linear-gradient` — overlay/gradient
- 12-column CSS Grid
- Watermark giant numbers
- Visible grid lines (Brutalist)
- Clip-path geometric shapes (Bauhaus)
- Asymmetric split layouts
- Hairline dividers

### #14 — Dark Mode + Glitch + Neon
- **Style:** Aggressive, cyberpunk, dark editorial
- **Fonts:** Syne (800), Space Mono (400/700)
- **BG:** #0a0a0a · Accent: #ff3366, #3366ff
- **Techniques:** text-shadow glitch (dual offset), neon gradient line, data blocks, vertical color strip
- **File:** test_dark_glitch.html

### #15 — Collage / Mixed Media
- **Style:** Organic, art-school, mixed media
- **Fonts:** DM Serif Display (400), Space Grotesk (500), JetBrains Mono (400)
- **BG:** #fffbf5 · Shapes: #ff6b35, #004e89
- **Techniques:** Organic blob shapes (border-radius %), photo fragment + shadow, bottom info bar, dot cluster
- **File:** test_collage.html

### #16 — Gig Poster / Diagonal Slash
- **Style:** Concert poster, bold, punk-luxe
- **Fonts:** Syncopate (700), DM Mono (400)
- **BG:** #f7f3e8 · Slash: #1a1a2e, #e94560
- **Techniques:** Diagonal background slash (linear-gradient 155deg), large uppercase typography, ring border, footer band
- **File:** test_poster.html

### #17 — Memphis / 80s Postmodern
- **Style:** Playful, retro, geometric
- **Fonts:** Instrument Serif (italic), JetBrains Mono (400), Inter (700)
- **BG:** #e8e2d5 · Accents: #ff6b6b, #4ecdc4, #ffe66d, #1a535c
- **Techniques:** Repeating-linear-gradient squiggle, triangle, dotted circle, zigzag pattern, highlight text (inline background), circular photo + offset shadow
- **File:** test_memphis.html

---

## Research Sources (2026-06-02)
- Swiss Style: zekagraphic.com, docs.mew.design, Poster House
- Brutalism: zekagraphic.com, reallygooddesigns.com, nat.io
- Bauhaus: putracetol.com, illustrarch.com, weandthecolor.com
- Carousel Rules: colorkuler.com, morphica.studio, getdraft.io
- Font Pairing: ym-graphix.com (one hero + one support rule), caroubolt.com
- Open Source: Open Carrusel (Hainrixz), Carousel Generator (FranciscoMoretti), Insta Carousel (Schlomoh)

## Font Pairing Rules (from research)
- One expressive font (headlines) + one calm font (details)
- 2-3 stable pairings for entire feed
- 60-30-10 color distribution
- Test at small sizes (zoom out — if headline fails, change it)
- Whitespace is what turns "nice font" into premium design
