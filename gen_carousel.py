#!/usr/bin/env python3
"""
Generic carousel generator — 7 slides, 1080×1350px.
Takes: photo path + list of 7 text blocks → outputs 7 PNG files.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (30, 30, 30)
GOLD = (212, 163, 115)
W, H = 1080, 1350

FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "fonts", "inter")
FONT_BLACK = os.path.join(FONT_DIR, "Inter-Black.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "Inter-Bold.ttf")
FONT_REGULAR = os.path.join(FONT_DIR, "Inter-Regular.ttf")

# Fallback font if Inter not available
for fp in [FONT_BLACK, FONT_BOLD, FONT_REGULAR]:
    if not os.path.exists(fp):
        FONT_BLACK = FONT_BOLD = FONT_REGULAR = None
        break


def get_font(size, bold=False):
    if FONT_BOLD and bold:
        return ImageFont.truetype(FONT_BOLD, size)
    elif FONT_REGULAR:
        return ImageFont.truetype(FONT_REGULAR, size)
    return ImageFont.load_default()


def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = f"{current} {w}".strip()
        bbox = font.getbbox(test)
        tw = bbox[2] - bbox[0]
        if tw <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def make_slide(photo: Image.Image, title: str, body_text: str, slide_no: int, total: int = 7,
               output_dir: str = "/tmp/carousel") -> str:
    """Generate one carousel slide. Returns output file path."""
    os.makedirs(output_dir, exist_ok=True)

    # Resize photo to fill background
    bg = photo.copy().convert("RGB")
    iw, ih = bg.size
    target_ratio = W / H
    img_ratio = iw / ih
    if img_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        offset = (iw - new_w) // 2
        bg = bg.crop((offset, 0, offset + new_w, ih))
    else:
        new_h = int(iw / target_ratio)
        offset = (ih - new_h) // 2
        bg = bg.crop((0, offset, iw, offset + new_h))
    bg = bg.resize((W, H), Image.LANCZOS)

    # Create overlay
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Dark gradient overlay at bottom
    gradient_start = int(H * 0.48)
    for i in range(gradient_start, H):
        alpha = int(140 * ((i - gradient_start) / (H - gradient_start)))
        draw.line([(0, i), (W, i)], fill=(0, 0, 0, alpha))

    # Title
    margin = 60
    content_top = H - 680

    if title:
        t_font = get_font(56, bold=True)
        draw.text((margin, content_top), title, fill=GOLD, font=t_font)
        content_top += 80

    # Body text
    b_font = get_font(26)
    max_w = W - margin * 2

    lines = []
    for paragraph in body_text.split("\n"):
        p_lines = wrap_text(paragraph.strip(), b_font, max_w)
        lines.extend(p_lines)

    line_h = 38
    y = content_top
    for line in lines[:12]:  # max 12 lines
        draw.text((margin, y), line, fill=WHITE, font=b_font)
        y += line_h

    # Slide counter
    if total > 1:
        s_font = get_font(18)
        counter_text = f"{slide_no} / {total}"
        bb = s_font.getbbox(counter_text)
        cw = bb[2] - bb[0]
        draw.text((W - margin - cw, H - 40), counter_text, fill=(200, 200, 200), font=s_font)

    # Composite
    result = Image.alpha_composite(bg.convert("RGBA"), canvas)

    out_path = os.path.join(output_dir, f"slide_{slide_no:02d}.png")
    result.convert("RGB").save(out_path, quality=95)
    return out_path


def generate_carousel(photo_path: str, slides: list[dict], output_dir: str = "/tmp/carousel") -> list[str]:
    """
    Generate a full carousel.
    
    Args:
        photo_path: Path to background photo
        slides: List of dicts with 'title' and 'body' keys (exactly 7)
        output_dir: Output directory
    
    Returns:
        List of 7 file paths
    """
    photo = Image.open(photo_path)
    total = len(slides)
    paths = []

    for i, slide in enumerate(slides, 1):
        path = make_slide(photo, slide.get("title", ""), slide.get("body", ""), i, total, output_dir)
        paths.append(path)
        print(f"  Slide {i}/{total}: {path}")

    return paths


if __name__ == "__main__":
    # Test
    test_photo = sys.argv[1] if len(sys.argv) > 1 else "/root/.openclaw-instagram/workspace/photos/7O0A2612.jpg"
    test_slides = [
        {"title": "SEAMLESS", "body": "Research meets movement"},
        {"title": "", "body": "Your body carries knowledge\nthat your mind has forgotten."},
        {"title": "The Science", "body": "Embodied cognition shows movement shapes thought."},
        {"title": "", "body": "Every gesture is a conversation\nbetween brain and body."},
        {"title": "Practice", "body": "Start with awareness.\nNotice how you hold tension."},
        {"title": "", "body": "Small shifts create\nprofound change."},
        {"title": "Join Us", "body": "SEAMLESS Movement Research\nBali — Contact Improvisation\n\n@seamless_research"},
    ]
    paths = generate_carousel(test_photo, test_slides)
    print(f"\n✅ Generated {len(paths)} slides")
    for p in paths:
        print(f"  {p}")