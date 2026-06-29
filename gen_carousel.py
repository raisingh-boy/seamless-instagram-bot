#!/usr/bin/env python3
"""
SEAMLESS Carousel Generator — exact design from gen_carousel_19.py
7 slides, 1080×1350px, rich HTML text formatting.

Design:
- 1080×1350, photo background center-cropped
- Gradient overlay (alpha 0→100, starts at 52%)
- Inter fonts: Black(64px), Bold(26-28px), Regular(26px)
- Gold accent line (60×3px) above title
- Slide counter top-right (18px)
- "SEAMLESS" left / "@seamless_research" right bottom (12px)
- HTML styling: <b>, <span style="color:#d4a373">, <br>
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
GRADIENT_START = int(H * 0.52)  # 52% from top
MARGIN_X = 80
CONTENT_TOP = H - 700


def _get_font(name, size):
    return ImageFont.truetype(name, size)


def _center_crop(img, target_w, target_h):
    iw, ih = img.size
    target_ratio = target_w / target_h
    img_ratio = iw / ih
    if img_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        offset = (iw - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, ih))
    else:
        new_h = int(iw / target_ratio)
        offset = (ih - new_h) // 2
        img = img.crop((0, offset, iw, offset + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)


def _parse_line(html_line):
    """Parse a line of HTML into segments with styles."""
    segments = []
    plain = html_line
    plain = re.sub(r'<br\s*/?>', '', plain)
    
    # Simple HTML tag parsing
    pos = 0
    current_style = {"bold": False, "color": WHITE, "font_size": 26, "font": FONT_REGULAR}
    
    while pos < len(html_line):
        tag_match = re.search(r'<(/?)(\w+)([^>]*)>', html_line[pos:])
        if not tag_match:
            text = html_line[pos:]
            if text.strip():
                segments.append((text, current_style.copy()))
            break
        
        before = html_line[pos:pos + tag_match.start()]
        if before.strip():
            segments.append((before, current_style.copy()))
        
        slash, tag, attrs = tag_match.group(1), tag_match.group(2), tag_match.group(3)
        
        if tag == 'b' or tag == 'strong':
            if slash:
                current_style["bold"] = False
                current_style["font"] = FONT_REGULAR
                current_style["font_size"] = 26
            else:
                current_style["bold"] = True
                current_style["font"] = FONT_BOLD
                current_style["font_size"] = 26
        
        elif tag == 'span':
            color_match = re.search(r'color:\s*#([0-9a-fA-F]{6})', attrs)
            size_match = re.search(r'font-size:\s*(\d+)', attrs)
            if color_match:
                hex_color = color_match.group(1)
                current_style["color"] = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            if size_match:
                size = int(size_match.group(1))
                current_style["font_size"] = size
                if "bold" in attrs.lower() or "<b>" in html_line[max(0, pos-20):pos]:
                    current_style["font"] = FONT_BOLD
                else:
                    current_style["font"] = FONT_REGULAR
        
        elif tag == '/span':
            # Reset to defaults
            current_style["bold"] = False
            current_style["color"] = WHITE
            current_style["font_size"] = 26
            current_style["font"] = FONT_REGULAR
        
        pos += tag_match.end()
    
    return segments


def generate_slide(photo: Image.Image, title_html: str, body_lines: list, 
                   slide_no: int = None, total: int = None,
                   output_path: str = None) -> str:
    """Generate one carousel slide. Returns file path."""
    
    # Background
    bg = _center_crop(photo, W, H)
    
    # Gradient overlay
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for i in range(GRADIENT_START, H):
        alpha = int(OVERLAY_ALPHA * ((i - GRADIENT_START) / (H - GRADIENT_START)))
        overlay_draw.line([(0, i), (W, i)], fill=(0, 0, 0, alpha))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGBA")
    draw = ImageDraw.Draw(bg)
    
    # Gold accent line
    draw.rounded_rectangle(
        [MARGIN_X, CONTENT_TOP, MARGIN_X + 60, CONTENT_TOP + 3],
        radius=2, fill=GOLD
    )
    
    # Title
    title_clean = title_html.replace("<br>", "\n").replace("&amp;", "&")
    title_font = _get_font(FONT_BLACK, 64)
    title_y = CONTENT_TOP + 30
    
    for tline in title_clean.split("\n"):
        tclean = re.sub(r'<[^>]+>', '', tline).strip()
        is_gold = 'gold' in title_html.lower() or '#d4a373' in title_html
        if is_gold:
            # Parse gold text in title
            segs = _parse_line(title_html)
            segs = [(s[0], s[1]) for s in segs if s[0].strip()]
            for seg_text, seg_style in segs:
                seg_text = re.sub(r'<[^>]+>', '', seg_text)
                seg_font = _get_font(seg_style["font"] if seg_style.get("font_name") else FONT_BLACK, seg_style.get("font_size", 64))
                c = seg_style.get("color", WHITE)
                draw.text((MARGIN_X + (0 if segs.index((seg_text, seg_style)) == 0 else draw.textbbox((0,0), segs[0][0], font=seg_font)[2]), title_y), 
                         seg_text, font=seg_font, fill=c)
            title_y += title_font.getbbox(tclean)[3] + 8
            continue
        
        draw.text((MARGIN_X, title_y), tclean, font=title_font, fill=GOLD if '#d4a373' in title_html else WHITE)
        title_y += title_font.getbbox(tclean)[3] + 8
    
    # Body text
    body_y = title_y + 24
    body_font = _get_font(FONT_REGULAR, 26)
    
    for line in body_lines:
        clean = line.strip()
        if not clean:
            body_y += 16
            continue
        
        # Determine styling from HTML tags
        is_bold = "<b>" in line
        is_gold = "#d4a373" in line
        is_small = 'font-size:22px' in line or 'font-size:16px' in line
        
        if is_small:
            f = _get_font(FONT_REGULAR, 22)
            c = DARK_GRAY
        elif is_bold:
            f = _get_font(FONT_BOLD, 26)
            c = WHITE
        elif is_gold:
            f = _get_font(FONT_BOLD, 28)
            c = GOLD
        elif "#2a9d8f" in line:
            f = _get_font(FONT_BOLD, 26)
            c = TEAL
        else:
            f = body_font
            c = LIGHT_GRAY
        
        clean = re.sub(r'<[^>]+>', '', clean)
        clean = clean.replace("&amp;", "&").strip()
        
        # Word wrap
        words = clean.split()
        current = ""
        for word in words:
            test = current + " " + word if current else word
            tw = f.getbbox(test)[2]
            if tw < W - MARGIN_X * 2:
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
        num_font = _get_font(FONT_BOLD, 18)
        num_text = f"{slide_no}/{total}"
        nb = draw.textbbox((0, 0), num_text, font=num_font)
        draw.text((W - MARGIN_X - (nb[2] - nb[0]), 40), num_text, font=num_font, fill=DARK_GRAY)
    
    # Bottom bar
    bottom_font = _get_font(FONT_REGULAR, 12)
    draw.text((MARGIN_X, H - 30), "SEAMLESS", font=bottom_font, fill=DARK_GRAY)
    br = draw.textbbox((0, 0), "@seamless_research", font=bottom_font)
    draw.text((W - MARGIN_X - (br[2] - br[0]), H - 30), "@seamless_research", font=bottom_font, fill=DARK_GRAY)
    
    # Save
    if output_path:
        bg.convert("RGB").save(output_path, "PNG")
    else:
        out_dir = "/tmp/carousel"
        os.makedirs(out_dir, exist_ok=True)
        output_path = os.path.join(out_dir, f"slide_{slide_no:02d}.png")
        bg.convert("RGB").save(output_path, "PNG")
    
    return output_path


def preprocess_photo(photo_path: str, output_path: str = None) -> str:
    """Center-crop a raw photo to 1080×1350 and save."""
    img = Image.open(photo_path).convert("RGB")
    cropped = _center_crop(img, W, H)
    if output_path is None:
        output_path = photo_path.replace(".jpg", "_ready_1080x1350.jpg").replace(".jpeg", "_ready_1080x1350.jpg")
    cropped.save(output_path, quality=95)
    return output_path


def generate_carousel(photo_path: str, slides: list[dict], 
                      output_dir: str = "/tmp/carousel") -> list[str]:
    """
    Generate a full 7-slide carousel matching SEAMLESS design.
    
    Args:
        photo_path: Path to background photo (RAW, will be cropped)
        slides: List of 7 dicts with keys:
            - title: str (with HTML: <br>, <span style="color:#d4a373">)
            - body: list[str] (each line with HTML tags)
        output_dir: Output directory
    
    Returns:
        List of 7 file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Preprocess photo once
    ready_path = os.path.join(output_dir, "bg_ready.jpg")
    photo = Image.open(photo_path).convert("RGB")
    photo = _center_crop(photo, W, H)
    photo.save(ready_path, quality=95)
    
    paths = []
    total = len(slides)
    for i, slide in enumerate(slides, 1):
        out_path = os.path.join(output_dir, f"slide_{i:02d}.png")
        generate_slide(
            photo=photo,
            title_html=slide.get("title", ""),
            body_lines=slide.get("body", []),
            slide_no=i,
            total=total,
            output_path=out_path
        )
        paths.append(out_path)
        sz = os.path.getsize(out_path)
        print(f"  Slide {i}/{total}: {out_path} ({sz//1024} KB)")
    
    return paths


if __name__ == "__main__":
    import sys
    
    test_photo = sys.argv[1] if len(sys.argv) > 1 else "/root/.openclaw-instagram/media/photos_approved/c19_ready_1080x1350.jpg"
    
    test_slides = [
        {
            "title": "SEAMLESS<br><span style=\"color:#d4a373\">Design Test</span>",
            "body": [
                "What if movement itself",
                "is a form of thinking?",
                "",
                "This is a test of the",
                "SEAMLESS carousel design",
                "pipeline.",
                "",
                "<span style=\"font-size:16px; color:#bbb\">SEAMLESS Bali · Ph: @andrey_berezkin</span>",
            ]
        },
        {
            "title": "Verbal Consent<br>Is <span style=\"color:#d4a373\">Not Enough</span>",
            "body": [
                "In CI, boundaries are negotiated",
                "in <b>milliseconds</b> — not minutes.",
                "",
                "A shift of weight, a change in tone,",
                "a micro-pause — these are consent signals",
                "that happen faster than language.",
            ]
        },
        {
            "title": "The Body Has<br><span style=\"color:#d4a373\">Three Boundary Systems</span>",
            "body": [
                "<span style=\"color:#d4a373\">1. Proprioceptive</span> — where am I in space?",
                "<span style=\"color:#d4a373\">2. Interoceptive</span> — what do I feel inside?",
                "<span style=\"color:#d4a373\">3. Relational</span> — quality of contact?",
                "",
                "Your body knows. <b>Instantly.</b>",
            ]
        },
        {
            "title": "CI as<br><span style=\"color:#d4a373\">Consent Training</span>",
            "body": [
                "CI is an embodied laboratory for consent:",
                "",
                "→ You learn to <b>enter and exit</b> contact",
                "→ You learn to <b>discern</b> invitation vs imposition",
                "→ You learn that <b>not-doing</b> is a valid choice",
                "",
                "<b>These are not just dance skills.</b>",
            ]
        },
        {
            "title": "The Neuroscience<br><span style=\"color:#d4a373\">of Agency</span>",
            "body": [
                "Research on sense of agency shows:",
                "",
                "→ Agency arises when your <b>prediction</b>",
                "  of movement matches sensory outcome",
                "→ When a partner overrides your impulse,",
                "  your brain registers a <b>prediction error</b>",
            ]
        },
        {
            "title": "From the Dance Floor<br><span style=\"color:#d4a373\">to Daily Life</span>",
            "body": [
                "What CI teaches about consent:",
                "",
                "→ <b>Listening</b> precedes action",
                "→ <b>Uncertainty</b> is creative, not threatening",
                "→ <b>No</b> is not rejection — it's information",
                "→ <b>Yes</b> can be partial, tentative, evolving",
            ]
        },
        {
            "title": "The Body<br><span style=\"color:#d4a373\">Knows First</span>",
            "body": [
                "Your body says yes or no",
                "before your mind formulates the word.",
                "",
                "CI trains you to <b>listen to that signal.</b>",
                "",
                "<span style=\"color:#d4a373; font-size:28px\"><b>@seamless_research</b></span>",
                "<span style=\"font-size:16px; color:#bbb\">SEAMLESS Bali · Ph: @andrey_berezkin</span>",
                "",
                "<span style=\"font-size:16px; color:#bbb\">#ConsentCulture #SEAMLESS #CI</span>",
            ]
        },
    ]
    
    output_dir = "/tmp/carousel_design_test"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    paths = generate_carousel(test_photo, test_slides, output_dir=output_dir)
    print(f"\n✅ Generated {len(paths)} slides in {output_dir}/")
    for p in paths:
        print(f"  {p}")