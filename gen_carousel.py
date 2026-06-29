#!/usr/bin/env python3
"""
SEAMLESS Carousel Generator — EXACT design from gen_carousel_19.py
7 slides, 1080×1350px, rich HTML text formatting.
"""

import os, re, shutil
from PIL import Image, ImageDraw, ImageFont

# ── Colors ──
WHITE = (255, 255, 255)
LIGHT_GRAY = (238, 238, 238)
DARK_GRAY = (119, 119, 119)
GOLD = (212, 163, 115)
TEAL = (42, 157, 143)

# ── Fonts ──
FONT_DIR = "/root/.openclaw-instagram/fonts/inter"
FONT_BLACK = os.path.join(FONT_DIR, "Inter-Black.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "Inter-Bold.ttf")
FONT_REGULAR = os.path.join(FONT_DIR, "Inter-Regular.ttf")

# ── Dimensions ──
W, H = 1080, 1350
OVERLAY_ALPHA = 100
GRADIENT_START = int(H * 0.52)
MARGIN_X = 80
CONTENT_TOP = H - 700
TITLE_SIZE = 64
BODY_SIZE = 26
SMALL_SIZE = 22
BOLD_SIZE = 26


def center_crop(img, target_w, target_h):
    iw, ih = img.size
    tr = target_w / target_h
    ir = iw / ih
    if ir > tr:
        new_w = int(ih * tr)
        off = (iw - new_w) // 2
        img = img.crop((off, 0, off + new_w, ih))
    else:
        new_h = int(iw / tr)
        off = (ih - new_h) // 2
        img = img.crop((0, off, iw, off + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)


def generate_slide(photo: Image.Image, title_html: str, body_lines: list,
                   slide_no: int = None, total: int = None,
                   output_path: str = None) -> str:
    """Generate one carousel slide — EXACT design."""

    # Background with gradient
    bg = center_crop(photo, W, H)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for i in range(GRADIENT_START, H):
        a = int(OVERLAY_ALPHA * ((i - GRADIENT_START) / (H - GRADIENT_START)))
        overlay_draw.line([(0, i), (W, i)], fill=(0, 0, 0, a))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGBA")
    draw = ImageDraw.Draw(bg)

    # Gold accent line (60×3px, rounded)
    draw.rounded_rectangle(
        [MARGIN_X, CONTENT_TOP, MARGIN_X + 60, CONTENT_TOP + 3],
        radius=2, fill=GOLD
    )

    # Title — EXACTLY as in gen_carousel_19.py
    title_clean = title_html.replace("<br>", "\n").replace("&amp;", "&")
    title_font = ImageFont.truetype(FONT_BLACK, TITLE_SIZE)
    title_y = CONTENT_TOP + 30

    for tline in title_clean.split("\n"):
        tclean = re.sub(r'<[^>]+>', '', tline).strip()
        is_gold = 'gold' in tline.lower() or '#d4a373' in tline
        tcolor = GOLD if is_gold else WHITE
        draw.text((MARGIN_X, title_y), tclean, font=title_font, fill=tcolor)
        title_y += title_font.getbbox(tclean)[3] + 8

    # Body text — EXACTLY as in gen_carousel_19.py
    body_y = title_y + 24
    body_font = ImageFont.truetype(FONT_REGULAR, BODY_SIZE)

    for line in body_lines:
        clean = line
        is_bold = "<b>" in line
        is_gold = "#d4a373" in line
        is_teal = "#2a9d8f" in line
        is_small = 'font-size:22px' in line or 'font-size:16px' in line

        clean = re.sub(r'<[^>]+>', '', clean)
        clean = clean.replace("&amp;", "&").strip()
        if not clean:
            body_y += 16
            continue

        if is_small:
            f = ImageFont.truetype(FONT_REGULAR, SMALL_SIZE)
            c = DARK_GRAY
        elif is_bold:
            f = ImageFont.truetype(FONT_BOLD, BOLD_SIZE)
            c = WHITE
        elif is_gold:
            f = ImageFont.truetype(FONT_BOLD, 28)
            c = GOLD
        elif is_teal:
            f = ImageFont.truetype(FONT_BOLD, BOLD_SIZE)
            c = TEAL
        else:
            f = body_font
            c = LIGHT_GRAY

        # Word wrap
        words = clean.split()
        current = ""
        for word in words:
            test = current + " " + word if current else word
            if f.getbbox(test)[2] < W - MARGIN_X * 2:
                current = test
            else:
                draw.text((MARGIN_X, body_y), current, font=f, fill=c)
                body_y += f.getbbox(current)[3] + 6
                current = word
        if current:
            draw.text((MARGIN_X, body_y), current, font=f, fill=c)
            body_y += f.getbbox(current)[3] + 6

    # Slide number
    if slide_no and total:
        num_font = ImageFont.truetype(FONT_BOLD, 18)
        num_text = f"{slide_no}/{total}"
        nb = draw.textbbox((0, 0), num_text, font=num_font)
        draw.text((W - MARGIN_X - (nb[2] - nb[0]), 40), num_text, font=num_font, fill=DARK_GRAY)

    # Bottom bar
    bottom_font = ImageFont.truetype(FONT_REGULAR, 12)
    draw.text((MARGIN_X, H - 30), "SEAMLESS", font=bottom_font, fill=DARK_GRAY)
    br = draw.textbbox((0, 0), "@seamless_research", font=bottom_font)
    draw.text((W - MARGIN_X - (br[2] - br[0]), H - 30), "@seamless_research", font=bottom_font, fill=DARK_GRAY)

    # Save
    if output_path is None:
        output_path = f"/tmp/carousel/slide_{slide_no:02d}.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    bg.convert("RGB").save(output_path, "PNG")
    return output_path


def generate_carousel(photo_path: str, slides: list[dict],
                      output_dir: str = "/tmp/carousel") -> list[str]:
    """Generate full 7-slide carousel. Returns file paths."""
    os.makedirs(output_dir, exist_ok=True)

    # Preprocess photo once
    photo = Image.open(photo_path).convert("RGB")

    paths = []
    total = len(slides)
    for i, slide in enumerate(slides, 1):
        out_path = os.path.join(output_dir, f"slide_{i:02d}.png")
        generate_slide(
            photo=photo,
            title_html=slide.get("title", ""),
            body_lines=slide.get("body", []),
            slide_no=i, total=total,
            output_path=out_path
        )
        paths.append(out_path)
        print(f"  Slide {i}/{total}: {out_path} ({os.path.getsize(out_path)//1024} KB)")

    return paths


if __name__ == "__main__":
    import sys
    test_photo = sys.argv[1] if len(sys.argv) > 1 else "/root/.openclaw-instagram/media/photos_approved/c19_ready_1080x1350.jpg"

    test_slides = [
        {"title": "SEAMLESS<br><span style=\"color:#d4a373\">Design Test</span>",
         "body": ["What if movement itself", "is a form of thinking?", "", "This is a test slide", "for the SEAMLESS pipeline."]},
        {"title": "The<br><span style=\"color:#d4a373\">Practice</span>",
         "body": ["1. Stand still. Feel your feet.", "2. Move one hand slowly.", "3. Notice your <b>attention shifts</b>."]},
        {"title": "Join the<br><span style=\"color:#d4a373\">Research</span>",
         "body": ["<b>Save</b> — research map", "<b>Share</b> — with movers", "<b>Move</b> — theory in practice", "", "<span style=\"color:#d4a373; font-size:28px\"><b>@seamless_research</b></span>", "<span style=\"font-size:16px; color:#bbb\">SEAMLESS Bali · Ph: @andrey_berezkin</span>"]},
    ]

    out = "/tmp/carousel_test_simple"
    if os.path.exists(out):
        shutil.rmtree(out)
    paths = generate_carousel(test_photo, test_slides, out)
    print(f"\n✅ {len(paths)} slides in {out}/")