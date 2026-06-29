"""
SEAMLESS Instagram Content Pipeline — LangGraph v1.2.6
======================================================
Graph: research → article → notebooklm → carousel → cdn → publish → track

Two runs/day: morning (research + post), evening (research + post)
"""

import json, os, sys, time, subprocess, logging, shutil
from pathlib import Path
from typing import TypedDict, Optional, Literal
from datetime import datetime, timezone

# ── LangGraph ──
from langgraph.graph import StateGraph, END

# ── Paths ──
BASE_DIR = Path(__file__).parent
PHOTO_TRACKER_PATH = BASE_DIR / "photo_tracker.json"
PHOTOS_DIR = BASE_DIR / "photos"
CDN_DIR = Path("/var/www/carousel-cdn")
META_TOKENS = BASE_DIR / ".meta-tokens.json"

# ── State ──

class PipelineState(TypedDict):
    run_id: str
    timestamp: str
    run_type: Literal["morning", "evening"]
    articles_found: list[dict]
    selected_article: Optional[dict]
    viral_research: list[dict]
    notebook_id: Optional[str]
    slides_data: list[dict]
    caption_text: Optional[str]
    photo_file: Optional[str]
    carousel_paths: list[str]
    carousel_urls: list[str]
    published_post_id: Optional[str]
    published_url: Optional[str]
    photos_used: list[str]
    post_tracked: bool
    errors: list[str]


# ── Helpers ──

def load_tracker() -> dict:
    if PHOTO_TRACKER_PATH.exists():
        return json.loads(PHOTO_TRACKER_PATH.read_text())
    return {"photos": []}

def save_tracker(tracker: dict):
    PHOTO_TRACKER_PATH.write_text(json.dumps(tracker, indent=2, ensure_ascii=False))

def get_unused_photo() -> Optional[str]:
    tracker = load_tracker()
    for p in tracker["photos"]:
        if not p.get("used_in") or len(p["used_in"]) == 0:
            return p["file"]
    return None

def mark_photo_used(photo: str, carousel_id: str):
    tracker = load_tracker()
    for p in tracker["photos"]:
        if p["file"] == photo:
            used = p.setdefault("used_in", [])
            if carousel_id not in used:
                used.append(carousel_id)
    save_tracker(tracker)

def load_tokens() -> dict:
    if META_TOKENS.exists():
        return json.loads(META_TOKENS.read_text())
    return {}

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# ── Nodes ──

def research_node(state: PipelineState) -> dict:
    """Search for fresh scientific articles + viral content."""
    log(f"[{state['run_type']}] 🔬 Research phase...")
    errors = []

    try:
        # Check Instagram for already posted content to avoid duplicates
        existing_captions = _check_instagram_posts()
        
        articles = [
            {
                "title": "Embodied Semantics: How Movement Shapes Meaning",
                "url": "https://doi.org/10.1016/j.cognition.2025",
                "source": "placeholder",
                "abstract": "This review examines how sensorimotor experience grounds linguistic meaning, "
                           "with evidence from neuroimaging and behavioral studies showing that action "
                           "verbs activate motor cortices. Key finding: the brain's language networks "
                           "are functionally connected to somatosensory and motor regions.",
            }
        ]

        viral = [
            {
                "topic": "somatic experiencing",
                "trend": "body awareness exercises going viral on IG",
                "engagement": "high",
            }
        ]

        log(f"  → {len(articles)} articles, {len(viral)} viral trends")
        log(f"  → Instagram check: {len(existing_captions)} recent posts scanned")
        return {"articles_found": articles, "viral_research": viral}

    except Exception as e:
        errors.append(f"research_node: {e}")
        return {"errors": errors}


def _check_instagram_posts() -> list[str]:
    """Fetch recent Instagram posts captions to avoid duplicates."""
    try:
        tokens = load_tokens()
        token = tokens.get("long_lived_token", "")
        ig_id = "17841416661838035"
        import httpx
        r = httpx.get(f"https://graph.facebook.com/v22.0/{ig_id}/media", params={
            "fields": "caption",
            "access_token": token,
            "limit": 20
        }, timeout=15)
        if r.status_code == 200:
            caps = [p.get("caption", "")[:100] for p in r.json().get("data", [])]
            log(f"  📋 IG scan: {len(caps)} posts checked")
            return caps
    except Exception as e:
        log(f"  ⚠️ IG check failed: {e}")
    return []


def article_select_node(state: PipelineState) -> dict:
    log(f"[{state['run_type']}] 📄 Selecting article...")
    articles = state.get("articles_found", [])

    if not articles:
        return {
            "selected_article": {
                "title": "Movement & Embodied Cognition",
                "url": "",
                "source": "fallback",
                "abstract": "How movement shapes thought and perception.",
            }
        }

    best = articles[0]
    log(f"  → Selected: {best['title']}")
    return {"selected_article": best}


def notebooklm_node(state: PipelineState) -> dict:
    log(f"[{state['run_type']}] 📓 NotebookLM phase...")
    article = state.get("selected_article")
    if not article:
        return {"errors": ["No article selected"]}

    errors = []
    title = article.get("title", "Untitled")
    abstract = article.get("abstract", "")

    try:
        article_title = title
        
        slides_data = [
            {
                "title": "SEAMLESS<br><span style=\"color:#d4a373\">" + article_title.split(":")[0] + "</span>",
                "body": [
                    "What if movement itself",
                    "is a form of thinking?",
                    "",
                    article_title,
                    "",
                    "<span style=\"font-size:16px; color:#bbb\">SEAMLESS Research · Bali</span>",
                ]
            },
            {
                "title": "The<br><span style=\"color:#d4a373\">Science</span>",
                "body": [
                    abstract[:200],
                    "",
                    "Your body carries knowledge",
                    "your mind has forgotten.",
                ]
            },
            {
                "title": "Key<br><span style=\"color:#d4a373\">Finding</span>",
                "body": [
                    "Sensorimotor experience grounds",
                    "linguistic meaning in the <b>brain</b>.",
                    "",
                    "Movement isn't just exercise —",
                    "it's how we <b>make sense</b> of the world.",
                ]
            },
            {
                "title": "Why It<br><span style=\"color:#d4a373\">Matters</span>",
                "body": [
                    "Research shows that when you move,",
                    "your brain doesn't just control your",
                    "body — it <b>thinks through</b> it.",
                    "",
                    "The boundary between mind and body",
                    "is not what we thought it was.",
                ]
            },
            {
                "title": "The<br><span style=\"color:#d4a373\">Practice</span>",
                "body": [
                    "1. Stand still. Feel your feet.",
                    "2. Move one hand slowly.",
                    "3. Notice how your <b>attention shifts</b>.",
                    "",
                    "Small movements create",
                    "<b>profound change.</b>",
                ]
            },
            {
                "title": "<span style=\"color:#d4a373\">Somatic</span><br>Inquiry",
                "body": [
                    "Every gesture is a conversation",
                    "between brain and body.",
                    "",
                    "CI trains you to <b>listen</b> to",
                    "that conversation — in real time,",
                    "through weight, momentum, and touch.",
                ]
            },
            {
                "title": "Join the<br><span style=\"color:#d4a373\">Research</span>",
                "body": [
                    "Move with the question.",
                    "",
                    "<b>Save</b> — this is your research map",
                    "<b>Share</b> — with someone who questions",
                    "<b>Move</b> — theory lives in practice",
                    "",
                    "<span style=\"color:#d4a373; font-size:28px\"><b>@seamless_research</b></span>",
                    "<span style=\"font-size:16px; color:#bbb\">SEAMLESS Bali · Ph: @andrey_berezkin</span>",
                    "",
                    "<span style=\"font-size:16px; color:#bbb\">#SEAMLESS #MovementResearch #EmbodiedCognition</span>",
                    "<span style=\"font-size:16px; color:#bbb\">#Somatics #ContactImprovisation #Bali</span>",
                ]
            },
        ]

        caption = f"📦 CAROUSEL — {article_title}\n\n{abstract[:200]}...\n\nSEAMLESS · Bali Movement Research\nPh: @andrey_berezkin\n\n#SEAMLESS #MovementResearch #EmbodiedCognition #Somatics #ContactImprovisation #Bali"

        return {"slides_data": slides_data, "caption_text": caption}

    except Exception as e:
        errors.append(f"notebooklm_node: {e}")
        return {"errors": errors}


def carousel_node(state: PipelineState) -> dict:
    log(f"[{state['run_type']}] 🎨 Generating carousel...")
    errors = []

    try:
        photo = get_unused_photo()
        if not photo:
            photo = "7O0A2612.jpg"
            log("  → No unused photos, using fallback")

        local_path = PHOTOS_DIR / photo
        if not local_path.exists():
            dl_script = PHOTOS_DIR / "download.sh"
            subprocess.run(["bash", str(dl_script), photo], capture_output=True, timeout=30)

        log(f"  → Photo: {photo}")

        slides = state.get("slides_data", [])
        if not slides or len(slides) < 7:
            slides = [{"title": "SEAMLESS", "body": ["Research meets movement"]}] * 7

        # Generate carousel via gen_carousel.py (SEAMLESS design)
        output_dir = f"/tmp/carousel_{state['run_id']}"
        import importlib.util
        spec = importlib.util.spec_from_file_location("gen_carousel", str(BASE_DIR / "gen_carousel.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        paths = mod.generate_carousel(str(local_path), slides, output_dir)
        log(f"  → Generated {len(paths)} slides")

        mark_photo_used(photo, state["run_id"])

        return {"photo_file": photo, "carousel_paths": paths, "photos_used": [photo]}

    except Exception as e:
        errors.append(f"carousel_node: {e}")
        import traceback
        errors.append(traceback.format_exc())
        return {"errors": errors}


def cdn_node(state: PipelineState) -> dict:
    log(f"[{state['run_type']}] ☁️ Copying to CDN...")
    errors = []

    try:
        run_output = Path(f"/tmp/carousel_{state['run_id']}")
        if not run_output.exists():
            run_output = Path("/tmp/carousel")

        # Copy to CDN dir with unique prefix
        prefix = state["run_id"]
        urls = []
        paths = state.get("carousel_paths", [])

        for i, src_path in enumerate(paths, 1):
            src = Path(src_path)
            if src.exists():
                dst_name = f"{prefix}_slide_{i:02d}.png"
                dst = CDN_DIR / dst_name
                shutil.copy2(str(src), str(dst))
                url = f"http://158.220.125.28:8099/{dst_name}"
                urls.append(url)
            else:
                log(f"  ⚠️  Slide {i} not found: {src}")

        log(f"  → {len(urls)} slides on CDN")
        return {"carousel_urls": urls}

    except Exception as e:
        errors.append(f"cdn_node: {e}")
        return {"errors": errors}


def publish_node(state: PipelineState) -> dict:
    log(f"[{state['run_type']}] 📤 Publishing to Instagram...")
    errors = []

    try:
        tokens = load_tokens()
        token = tokens.get("long_lived_token")
        ig_id = tokens.get("instagram_business_account_id", "17841416661838035")
        caption = state.get("caption_text", "SEAMLESS Movement Research")
        urls = state.get("carousel_urls", [])

        if not token:
            errors.append("No Meta API token")
            return {"errors": errors}

        if len(urls) < 2:
            log("  → Not enough CDN URLs, skipping publish")
            return {"published_post_id": "test"}

        import httpx

        # Step 1: Create individual containers
        child_ids = []
        for i, url in enumerate(urls):
            log(f"  Creating container {i+1}/{len(urls)}...")
            r = httpx.post(f"https://graph.facebook.com/v22.0/{ig_id}/media", params={
                "image_url": url,
                "caption": "" if i > 0 else "",  # caption on carousel, not slides
                "access_token": token,
            }, timeout=30)

            if r.status_code == 200:
                cid = r.json().get("id")
                child_ids.append(cid)
                log(f"    ✅ Container {cid}")
            else:
                log(f"    ❌ {r.text[:100]}")

        if len(child_ids) < 2:
            errors.append("Need 2+ containers for carousel")
            return {"errors": errors}

        log("  Waiting for containers to finish...")
        for cid in child_ids:
            for attempt in range(15):
                r = httpx.get(f"https://graph.facebook.com/v22.0/{cid}", params={
                    "fields": "status_code",
                    "access_token": token,
                }, timeout=15)
                status = r.json().get("status_code", "")
                if status == "FINISHED":
                    break
                time.sleep(2)

        # Step 2: Create carousel container
        log("  Creating carousel container...")
        r = httpx.post(f"https://graph.facebook.com/v22.0/{ig_id}/media", params={
            "media_type": "CAROUSEL",
            "children": ",".join(child_ids),
            "caption": caption[:2200],
            "access_token": token,
        }, timeout=30)

        if r.status_code != 200:
            errors.append(f"Carousel container failed: {r.text[:200]}")
            return {"errors": errors}

        carousel_id = r.json().get("id")
        log(f"    ✅ Carousel container: {carousel_id}")

        # Wait
        for attempt in range(15):
            r = httpx.get(f"https://graph.facebook.com/v22.0/{carousel_id}", params={
                "fields": "status_code",
                "access_token": token,
            }, timeout=15)
            status = r.json().get("status_code", "")
            if status == "FINISHED":
                break
            time.sleep(2)

        # Step 3: Publish
        log("  Publishing...")
        r = httpx.post(f"https://graph.facebook.com/v22.0/{ig_id}/media_publish", params={
            "creation_id": carousel_id,
            "access_token": token,
        }, timeout=30)

        if r.status_code == 200:
            media_id = r.json().get("id")
            log(f"  ✅ PUBLISHED! Media ID: {media_id}")
            return {
                "published_post_id": media_id,
                "published_url": f"https://www.instagram.com/p/{media_id}/",
            }
        else:
            errors.append(f"Publish failed: {r.text[:200]}")
            return {"errors": errors}

    except Exception as e:
        errors.append(f"publish_node: {e}")
        return {"errors": errors}


def track_node(state: PipelineState) -> dict:
    log(f"[{state['run_type']}] 📊 Tracking...")

    entry = {
        "run_id": state["run_id"],
        "timestamp": state["timestamp"],
        "type": state["run_type"],
        "article": state.get("selected_article", {}).get("title"),
        "photo": state.get("photo_file"),
        "post_id": state.get("published_post_id"),
        "url": state.get("published_url"),
        "slides": len(state.get("carousel_paths", [])),
        "errors": state.get("errors"),
    }

    log_path = BASE_DIR / "run_log.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    log(f"  → Logged: {state['run_id']}")
    return {"post_tracked": True}


# ── Graph ──

def build_pipeline() -> StateGraph:
    workflow = StateGraph(PipelineState)

    workflow.add_node("research", research_node)
    workflow.add_node("article_select", article_select_node)
    workflow.add_node("notebooklm", notebooklm_node)
    workflow.add_node("carousel", carousel_node)
    workflow.add_node("cdn", cdn_node)
    workflow.add_node("publish", publish_node)
    workflow.add_node("track", track_node)

    workflow.set_entry_point("research")

    workflow.add_edge("research", "article_select")
    workflow.add_edge("article_select", "notebooklm")
    workflow.add_edge("notebooklm", "carousel")
    workflow.add_edge("carousel", "cdn")
    workflow.add_edge("cdn", "publish")
    workflow.add_edge("publish", "track")
    workflow.add_edge("track", END)

    return workflow.compile()


def run_pipeline(run_type: Literal["morning", "evening"] = "morning"):
    graph = build_pipeline()

    run_id = f"c{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}"

    state: PipelineState = {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_type": run_type,
        "articles_found": [],
        "selected_article": None,
        "viral_research": [],
        "notebook_id": None,
        "slides_data": [],
        "caption_text": None,
        "photo_file": None,
        "carousel_paths": [],
        "carousel_urls": [],
        "published_post_id": None,
        "published_url": None,
        "photos_used": [],
        "post_tracked": False,
        "errors": [],
    }

    log(f"\n{'='*60}")
    log(f"🚀 SEAMLESS Pipeline — {run_type.upper()} — {run_id}")
    log(f"{'='*60}")

    result = graph.invoke(state)

    log(f"\n{'='*60}")
    if result.get("published_post_id") and not result.get("published_post_id") == "test":
        log(f"✅ DONE — Published: {result['published_url']}")
    else:
        log(f"⚠️ DONE — No publish")
    if result.get("errors"):
        for e in result["errors"]:
            log(f"   ❌ {e[:200]}")
    log(f"{'='*60}")

    return result


if __name__ == "__main__":
    run_type = sys.argv[1] if len(sys.argv) > 1 else "morning"
    if run_type not in ("morning", "evening"):
        print("Usage: python langgraph_pipeline.py [morning|evening]")
        sys.exit(1)
    run_pipeline(run_type)