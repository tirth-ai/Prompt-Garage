from flask import Flask, render_template_string, request, jsonify, send_from_directory
import os, base64, mimetypes, json, re

app = Flask(__name__)

# ── Developer password to unlock upload buttons ───────────────────────────────
DEV_PASSWORD = "tirth11"   # ← change this to whatever you want
# ─────────────────────────────────────────────────────────────────────────────

PROMPTS = [
    {
        "id":          "challenger",
        "title":       "Dodge Challenger Dyno Run",
        "description": 'A matte black Dodge Challenger with gold alloys, flames bursting from exhaust, number plate "TIRTH 11".',
        "prompt": (
            'Cinematic shot of a matte black Dodge Challenger on a dyno run, '
            'gold alloy wheels gleaming under neon lights, orange and blue flames '
            'erupting from dual exhausts, custom number plate reading "TIRTH 11", '
            'dramatic studio lighting, smoke swirling on concrete floor, '
            'photorealistic, 8K, hyperdetailed.'
        ),
    },
    {
        "id":          "desert_car",
        "title":       "Neon Desert Muscle Car",
        "description": "A classic muscle car parked in a neon-lit desert at midnight.",
        "prompt": (
            'Classic American muscle car parked on cracked desert highway at midnight, '
            'surrounded by towering glowing neon signs, reflections of purple and cyan '
            'light on the polished hood, Milky Way overhead, cinematic wide angle lens, '
            'photorealistic, ultra HD, 8K.'
        ),
    },
    {
        "id":          "garage_king",
        "title":       "Garage King",
        "description": "A lone mechanic silhouetted in a golden-lit garage surrounded by exotic cars.",
        "prompt": (
            'Silhouette of a mechanic standing in a vast industrial garage filled with '
            'exotic supercars, golden hour light streaming through floor-to-ceiling windows, '
            'oil-stained concrete floor reflecting the light, dramatic god rays, '
            'cinematic composition, hyperrealistic, 8K.'
        ),
    },
    {
        "id":          "hellcat",
        "title":       "Hellcat Storm Chase",
        "description": "A Dodge Hellcat racing ahead of a tornado on an empty highway.",
        "prompt": (
            'Dodge Hellcat Widebody in blood red racing at 200mph on an empty midwest '
            'highway, monstrous tornado forming on the horizon, storm clouds lit by '
            'lightning, motion blur on wheels, dust and debris flying, dramatic '
            'low-angle shot, photorealistic, cinematic, 8K.'
        ),
    },
]

IMG_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "images")
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts_data.json")
os.makedirs(IMG_DIR, exist_ok=True)

def load_prompts():
    """Load prompts from JSON file, fall back to hardcoded PROMPTS list."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return PROMPTS

def save_prompts(data):
    """Persist prompts list to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def slugify(text):
    """Convert title to a safe id string."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')[:40]

def get_image_url(prompt_id):
    for ext in ["jpg", "jpeg", "png", "webp"]:
        path = os.path.join(IMG_DIR, f"{prompt_id}.{ext}")
        if os.path.exists(path):
            return f"/static/images/{prompt_id}.{ext}"
    return None

@app.route("/static/images/<filename>")
def serve_image(filename):
    return send_from_directory(IMG_DIR, filename)

@app.route("/api/upload/<prompt_id>", methods=["POST"])
def upload_image(prompt_id):
    valid_ids = [p["id"] for p in load_prompts()]
    if prompt_id not in valid_ids:
        return jsonify({"ok": False, "error": "Invalid prompt ID"}), 400

    if "file" not in request.files:
        return jsonify({"ok": False, "error": "No file"}), 400

    file = request.files["file"]
    ext  = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ["jpg", "jpeg", "png", "webp"]:
        return jsonify({"ok": False, "error": "Only jpg/png/webp allowed"}), 400

    # Remove old images for this prompt
    for old_ext in ["jpg", "jpeg", "png", "webp"]:
        old = os.path.join(IMG_DIR, f"{prompt_id}.{old_ext}")
        if os.path.exists(old):
            os.remove(old)

    save_path = os.path.join(IMG_DIR, f"{prompt_id}.{ext}")
    file.save(save_path)
    return jsonify({"ok": True, "url": f"/static/images/{prompt_id}.{ext}"})

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tirth's Prompt Garage</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --cyan:     #00f5ff;
      --cyan-dim: rgba(0,245,255,0.15);
      --blue:     #0080ff;
      --bg:       #020810;
      --surface:  #071525;
      --surface2: #0a1e35;
      --text:     #c8e8ff;
      --muted:    #8ec8e8;
      --border:   rgba(0,245,255,0.18);
      --green:    #00ff88;
      --red:      #ff3a5c;
    }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Exo 2', sans-serif;
      background: var(--bg); color: var(--text);
      min-height: 100vh; overflow-x: hidden; cursor: crosshair;
    }
    body::before {
      content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
      background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,128,255,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(123,47,255,0.1) 0%, transparent 60%);
    }
    body::after {
      content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
      background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,245,255,0.012) 2px, rgba(0,245,255,0.012) 4px);
      animation: scan 8s linear infinite;
    }
    @keyframes scan { from{background-position:0 0} to{background-position:0 100vh} }
    #particles { position: fixed; inset: 0; z-index: 0; pointer-events: none; display: block; }

    /* ── Manage Panel ── */
    #manage-panel {
      display: none;
      position: fixed; inset: 0; z-index: 800;
      background: rgba(2,8,16,0.97);
      backdrop-filter: blur(12px);
      overflow-y: auto;
      padding: 40px 24px 80px;
    }
    #manage-panel.open { display: block; animation: lbIn .3s ease; }

    .mp-header {
      display: flex; align-items: center; justify-content: space-between;
      border-bottom: 1px solid var(--border); padding-bottom: 18px; margin-bottom: 28px;
      max-width: 860px; margin-left: auto; margin-right: auto;
    }
    .mp-header h2 {
      font-family: 'Orbitron', sans-serif; font-size: 1rem;
      letter-spacing: 4px; color: var(--cyan); text-transform: uppercase;
    }
    .mp-close {
      font-family: 'Orbitron', sans-serif; font-size: .6rem; letter-spacing: 2px;
      color: var(--muted); cursor: pointer; border: 1px solid var(--border);
      padding: 6px 14px; background: transparent; transition: all .3s;
    }
    .mp-close:hover { color: var(--cyan); border-color: var(--cyan); }

    .mp-body { max-width: 860px; margin: 0 auto; }

    /* Add form */
    .mp-form {
      background: var(--surface); border: 1px solid var(--border);
      padding: 24px; margin-bottom: 32px;
    }
    .mp-form h3 {
      font-family: 'Orbitron', sans-serif; font-size: .7rem; letter-spacing: 3px;
      color: var(--cyan); margin-bottom: 18px; text-transform: uppercase;
    }
    .mp-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
    .mp-row.full { grid-template-columns: 1fr; }
    .mp-field { display: flex; flex-direction: column; gap: 6px; }
    .mp-field label {
      font-family: 'Orbitron', sans-serif; font-size: .52rem; letter-spacing: 2px;
      color: var(--muted); text-transform: uppercase;
    }
    .mp-field input, .mp-field textarea {
      background: var(--bg); border: 1px solid rgba(0,245,255,0.2);
      color: var(--text); font-family: 'Exo 2', sans-serif; font-size: .9rem;
      padding: 10px 12px; outline: none; resize: vertical;
      transition: border-color .3s;
    }
    .mp-field input:focus, .mp-field textarea:focus {
      border-color: var(--cyan); box-shadow: 0 0 8px rgba(0,245,255,0.12);
    }
    .mp-field textarea { min-height: 90px; }
    .mp-btn {
      font-family: 'Orbitron', sans-serif; font-size: .6rem; letter-spacing: 2px;
      text-transform: uppercase; padding: 10px 24px; cursor: pointer;
      border: 1px solid var(--cyan); background: transparent; color: var(--cyan);
      transition: all .3s; margin-top: 8px; position: relative; overflow: hidden;
    }
    .mp-btn::before {
      content: ''; position: absolute; inset: 0;
      background: linear-gradient(90deg, var(--blue), var(--cyan));
      opacity: 0; transition: opacity .3s; z-index: 0;
    }
    .mp-btn:hover::before { opacity: 1; }
    .mp-btn:hover { color: #000; }
    .mp-btn span { position: relative; z-index: 1; }
    .mp-btn.danger { border-color: var(--red); color: var(--red); }
    .mp-btn.danger::before { background: var(--red); }
    .mp-btn.danger:hover { color: #fff; }

    /* Prompt list */
    .mp-list { display: flex; flex-direction: column; gap: 14px; }
    .mp-item {
      background: var(--surface); border: 1px solid var(--border);
      padding: 18px 20px; display: flex; align-items: flex-start;
      gap: 16px; transition: border-color .3s;
    }
    .mp-item:hover { border-color: rgba(0,245,255,0.3); }
    .mp-item-thumb {
      width: 72px; height: 56px; flex-shrink: 0;
      object-fit: cover; border: 1px solid var(--border);
      background: var(--bg);
    }
    .mp-item-thumb-placeholder {
      width: 72px; height: 56px; flex-shrink: 0;
      background: var(--bg); border: 1px solid var(--border);
      display: flex; align-items: center; justify-content: center;
      font-size: .5rem; color: rgba(0,245,255,0.25);
      font-family: 'Orbitron', sans-serif; letter-spacing: 1px;
    }
    .mp-item-info { flex: 1; min-width: 0; }
    .mp-item-title {
      font-family: 'Orbitron', sans-serif; font-size: .75rem;
      letter-spacing: 2px; color: var(--cyan); margin-bottom: 5px;
      text-transform: uppercase;
    }
    .mp-item-desc { font-size: .82rem; color: var(--muted); line-height: 1.5; }
    .mp-item-actions { display: flex; gap: 8px; flex-shrink: 0; align-items: center; }

    .mp-msg {
      font-family: 'Orbitron', sans-serif; font-size: .55rem; letter-spacing: 2px;
      padding: 8px 0; text-transform: uppercase; min-height: 22px;
    }

    /* ── Dev login bar (hidden by default) ── */
    #dev-bar {
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 500;
      background: rgba(2,8,16,0.97);
      border-top: 1px solid rgba(0,245,255,0.2);
      padding: 10px 20px;
      display: flex; align-items: center; gap: 12px;
      transform: translateY(100%);
      transition: transform .35s cubic-bezier(.23,1,.32,1);
    }
    #dev-bar.open { transform: translateY(0); }
    #dev-bar label {
      font-family: 'Orbitron', sans-serif; font-size: .55rem;
      letter-spacing: 3px; color: var(--cyan); text-transform: uppercase;
    }
    #dev-bar input {
      background: var(--surface); border: 1px solid var(--border);
      color: var(--cyan); font-family: 'Orbitron', sans-serif;
      font-size: .65rem; letter-spacing: 2px;
      padding: 6px 12px; outline: none; width: 180px;
    }
    #dev-bar input:focus { border-color: var(--cyan); box-shadow: 0 0 8px var(--cyan-dim); }
    #dev-bar button {
      background: transparent; border: 1px solid var(--cyan);
      color: var(--cyan); font-family: 'Orbitron', sans-serif;
      font-size: .55rem; letter-spacing: 2px; text-transform: uppercase;
      padding: 6px 16px; cursor: pointer; transition: all .3s;
    }
    #dev-bar button:hover { background: var(--cyan); color: #000; }
    #dev-status { font-family: 'Orbitron', sans-serif; font-size: .55rem; letter-spacing: 2px; }

    /* floating manage button — visible only in dev mode */
    #dev-manage-float {
      display: none;
      position: fixed; bottom: 24px; right: 24px; z-index: 502;
      font-family: 'Orbitron', sans-serif; font-size: .6rem;
      letter-spacing: 2px; text-transform: uppercase;
      padding: 12px 20px;
      background: rgba(2,8,16,0.95);
      border: 1px solid var(--cyan);
      color: var(--cyan);
      cursor: pointer;
      box-shadow: 0 0 20px rgba(0,245,255,0.25);
      transition: all .3s;
      animation: borderPulse 2s ease-in-out infinite;
    }
    #dev-manage-float:hover {
      background: var(--cyan); color: #000;
      box-shadow: 0 0 30px rgba(0,245,255,0.5);
    }

    /* secret trigger — tiny dot bottom-right corner */
    #dev-trigger {
      position: fixed; bottom: 8px; right: 12px; z-index: 501;
      width: 10px; height: 10px; border-radius: 50%;
      background: rgba(0,245,255,0.15);
      cursor: pointer; transition: background .3s;
      border: 1px solid rgba(0,245,255,0.2);
    }
    #dev-trigger:hover { background: rgba(0,245,255,0.5); box-shadow: 0 0 8px var(--cyan); }

    /* ── Header ── */
    header {
      position: relative; z-index: 10;
      padding: 50px 24px 36px; text-align: center;
      background: linear-gradient(180deg, rgba(0,20,50,0.9) 0%, transparent 100%);
      border-bottom: 1px solid var(--border);
    }
    header::after {
      content: ''; position: absolute; bottom: -1px; left: 0; right: 0; height: 1px;
      background: linear-gradient(90deg, transparent, var(--cyan) 30%, var(--blue) 70%, transparent);
      animation: borderPulse 3s ease-in-out infinite;
    }
    @keyframes borderPulse { 0%,100%{opacity:.4} 50%{opacity:1} }
    .logo-wrap { display: inline-block; position: relative; }
    .logo-wrap::before, .logo-wrap::after {
      content: ''; position: absolute; top: 50%; width: 60px; height: 1px;
      background: linear-gradient(90deg, transparent, var(--cyan)); transform: translateY(-50%);
    }
    .logo-wrap::before { right: 100%; margin-right: 16px; }
    .logo-wrap::after  { left: 100%; margin-left: 16px; background: linear-gradient(90deg, var(--cyan), transparent); }
    header h1 {
      font-family: 'Orbitron', sans-serif; font-weight: 900;
      font-size: clamp(1.8rem, 5vw, 3.4rem); letter-spacing: 6px; text-transform: uppercase;
      background: linear-gradient(90deg, var(--cyan) 0%, #fff 40%, var(--blue) 70%, var(--cyan) 100%);
      background-size: 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      animation: titleFlow 5s linear infinite;
      filter: drop-shadow(0 0 20px rgba(0,245,255,0.4));
    }
    @keyframes titleFlow { 0%{background-position:0% center} 100%{background-position:300% center} }
    .tagline { font-size:.75rem; letter-spacing:5px; color:var(--muted); text-transform:uppercase; margin-top:8px; font-weight:300; }
    nav { margin-top:24px; display:flex; justify-content:center; gap:8px; }
    nav a {
      font-family:'Orbitron',sans-serif; font-size:.65rem; letter-spacing:3px; text-transform:uppercase;
      color:var(--muted); padding:8px 20px; border:1px solid rgba(0,245,255,0.28);
      text-decoration:none; transition:all .3s; position:relative; overflow:hidden;
    }
    nav a::before {
      content:''; position:absolute; inset:0; background:var(--cyan-dim);
      transform:scaleX(0); transform-origin:left; transition:transform .3s; z-index:0;
    }
    nav a:hover::before { transform:scaleX(1); }
    nav a:hover { color:var(--cyan); border-color:var(--cyan); box-shadow:0 0 12px var(--cyan-dim); }
    nav a span { position:relative; z-index:1; }

    .section-label {
      position:relative; z-index:2; text-align:center; padding:48px 0 8px;
      font-family:'Orbitron',sans-serif; font-size:.65rem; letter-spacing:6px;
      color:var(--cyan); opacity:.9; text-transform:uppercase;
    }

    /* ── Gallery ── */
    #gallery {
      position:relative; z-index:2; display:flex; flex-wrap:wrap;
      justify-content:center; gap:28px; padding:24px 24px 56px;
    }

    /* ── Card ── */
    .card {
      background: linear-gradient(135deg, rgba(7,21,37,0.95), rgba(5,14,26,0.98));
      border: 1px solid var(--border); border-radius: 2px;
      width: 310px; position: relative; overflow: hidden;
      transition: box-shadow .35s;
      /* base state — hidden, pushed back */
      opacity: 0;
      transform: translateY(40px) scale(0.93);
      transition: transform .55s cubic-bezier(0.22,1,0.36,1),
                  opacity  .55s cubic-bezier(0.22,1,0.36,1),
                  box-shadow .4s ease,
                  border-color .3s ease;
    }
    /* popped in — visible & at normal position */
    .card.pop-in {
      opacity: 1;
      transform: translateY(0px) scale(1);
    }
    /* popped out — scrolled past, shrink back */
    .card.pop-out {
      opacity: 0;
      transform: translateY(-30px) scale(0.93);
      transition: transform .45s cubic-bezier(0.64,0,0.78,0),
                  opacity  .45s cubic-bezier(0.64,0,0.78,0),
                  box-shadow .4s ease,
                  border-color .3s ease;
    }
    .card::before, .card::after { content:''; position:absolute; width:14px; height:14px; z-index:2; }
    .card::before { top:-1px; left:-1px; border-top:2px solid var(--cyan); border-left:2px solid var(--cyan); }
    .card::after  { bottom:-1px; right:-1px; border-bottom:2px solid var(--cyan); border-right:2px solid var(--cyan); }
    .card.pop-in:hover {
      transform: translateY(-8px) scale(1.015);
      border-color: rgba(0,245,255,0.5);
      box-shadow: 0 0 0 1px rgba(0,245,255,0.22), 0 24px 48px rgba(0,245,255,0.12), 0 0 40px rgba(0,245,255,0.08);
    }

    /* ── Image area ── */
    .card-img-wrap {
      width:100%; height:190px; overflow:hidden;
      position:relative; border-bottom:1px solid var(--border);
      background: var(--surface); cursor: zoom-in;
    }
    .card-img-wrap img {
      width:100%; height:100%; object-fit:cover; display:block;
      transition: transform .5s cubic-bezier(.23,1,.32,1), filter .5s;
      filter: brightness(0.85) saturate(1.1);
    }
    .card:hover .card-img-wrap img { transform:scale(1.07); filter:brightness(1) saturate(1.3); }

    .card-img-wrap::after {
      content:''; position:absolute; inset:0; pointer-events:none; z-index:1;
      background: linear-gradient(180deg, transparent 55%, rgba(0,245,255,0.06) 80%, rgba(0,10,20,0.6) 100%);
    }
    .card-img-placeholder {
      width:100%; height:190px; display:flex; flex-direction:column;
      align-items:center; justify-content:center; gap:10px;
      background:linear-gradient(135deg, #050e1a, #071525);
      border-bottom:1px solid var(--border);
      color:rgba(0,245,255,0.3); font-family:'Orbitron',sans-serif;
      font-size:.55rem; letter-spacing:3px; text-transform:uppercase;
    }
    .card-img-placeholder svg { opacity:0.25; }

    .img-badge {
      position:absolute; top:10px; right:10px; z-index:4;
      font-family:'Orbitron',sans-serif; font-size:.5rem; letter-spacing:2px;
      color:var(--cyan); border:1px solid rgba(0,245,255,0.4);
      padding:3px 8px; background:rgba(2,8,16,0.7); text-transform:uppercase;
    }

    /* ── Dev upload overlay (hidden unless dev mode) ── */
    .upload-overlay {
      display: none;
      position: absolute; top: 0; left: 0;
      width: 100%; height: 190px;
      background: rgba(0,10,20,0.85);
      z-index: 10;
      align-items: center; justify-content: center; flex-direction: column; gap: 10px;
      border-bottom: 1px solid rgba(0,245,255,0.3);
    }
    .dev-mode .upload-overlay { display: flex; }

    .upload-overlay label {
      font-family: 'Orbitron', sans-serif; font-size: .58rem;
      letter-spacing: 2px; color: var(--cyan); text-transform: uppercase;
      border: 1px dashed rgba(0,245,255,0.4); padding: 10px 18px;
      cursor: pointer; transition: all .3s; text-align: center; line-height: 1.8;
    }
    .upload-overlay label:hover { border-color: var(--cyan); background: var(--cyan-dim); }
    .upload-overlay input[type=file] { display: none; }

    .upload-status {
      font-family: 'Orbitron', sans-serif; font-size: .5rem;
      letter-spacing: 2px; text-transform: uppercase;
      color: var(--muted); min-height: 16px;
    }

    /* ── Card body ── */
    .card-body { padding:22px 22px 18px; position:relative; }
    .card-num {
      font-family:'Orbitron',sans-serif; font-size:2.8rem; font-weight:900;
      color:rgba(0,245,255,0.22); position:absolute; top:6px; right:12px;
      line-height:1; user-select:none; letter-spacing:-2px;
    }
    .card-status {
      font-family:'Orbitron',sans-serif; font-size:.58rem; letter-spacing:3px;
      color:var(--cyan); opacity:.85; margin-bottom:10px;
      display:flex; align-items:center; gap:6px;
    }
    .card-status::before {
      content:''; display:inline-block; width:6px; height:6px;
      border-radius:50%; background:var(--cyan); box-shadow:0 0 6px var(--cyan);
      animation:blink 2s ease infinite;
    }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }
    .card h2 {
      font-family:'Orbitron',sans-serif; font-size:1rem; font-weight:700;
      letter-spacing:1.5px; color:#fff; margin-bottom:10px;
      text-shadow:0 0 20px rgba(0,245,255,0.3); text-transform:uppercase;
    }
    .card p { font-size:.88rem; color:var(--muted); line-height:1.65; margin-bottom:20px; font-weight:300; }
    .preview-hint {
      font-family:'Orbitron',sans-serif; font-size:.52rem; letter-spacing:2px;
      color:rgba(0,245,255,0.5); text-align:center; margin-bottom:12px; text-transform:uppercase;
    }
    .copy-btn {
      display:block; width:100%; padding:11px 0; background:transparent;
      border:1px solid rgba(0,245,255,0.25); color:var(--cyan);
      font-family:'Orbitron',sans-serif; font-size:.6rem; letter-spacing:3px;
      text-transform:uppercase; cursor:pointer; position:relative; overflow:hidden; transition:all .3s;
    }
    .copy-btn::before {
      content:''; position:absolute; inset:0;
      background:linear-gradient(90deg, var(--blue), var(--cyan));
      opacity:0; transition:opacity .3s; z-index:0;
    }
    .copy-btn:hover::before { opacity:1; }
    .copy-btn:hover { color:#000; border-color:var(--cyan); box-shadow:0 0 20px rgba(0,245,255,0.3); }
    .copy-btn span { position:relative; z-index:1; }
    .copy-btn.ok { border-color:var(--green); color:var(--green); }

    /* ── Lightbox ── */
    #lightbox {
      display:none; position:fixed; inset:0; z-index:1000;
      background:rgba(2,8,16,0.96); align-items:center; justify-content:center;
      flex-direction:column; gap:20px; backdrop-filter:blur(10px); cursor:zoom-out;
    }
    #lightbox.open { display:flex; animation:lbIn .3s ease; }
    @keyframes lbIn { from{opacity:0;transform:scale(.95)} to{opacity:1;transform:scale(1)} }
    #lightbox img {
      max-width:90vw; max-height:78vh;
      border:1px solid rgba(0,245,255,0.3);
      box-shadow:0 0 60px rgba(0,245,255,0.15), 0 0 120px rgba(0,128,255,0.1);
      border-radius:2px; object-fit:contain;
    }
    #lightbox-title {
      font-family:'Orbitron',sans-serif; font-size:.8rem;
      letter-spacing:4px; color:var(--cyan); text-transform:uppercase;
    }
    #lightbox-close {
      position:absolute; top:20px; right:28px;
      font-family:'Orbitron',sans-serif; font-size:.7rem; letter-spacing:2px;
      color:var(--muted); cursor:pointer; border:1px solid var(--border);
      padding:6px 14px; background:transparent; transition:all .3s;
    }
    #lightbox-close:hover { color:var(--cyan); border-color:var(--cyan); }

    /* ── Toast ── */
    #toast {
      position:fixed; bottom:56px; left:50%;
      transform:translateX(-50%) translateY(20px);
      background:rgba(0,20,40,0.95); border:1px solid var(--cyan);
      color:var(--cyan); padding:12px 32px;
      font-family:'Orbitron',sans-serif; font-size:.6rem; letter-spacing:3px;
      text-transform:uppercase; box-shadow:0 0 30px rgba(0,245,255,0.25);
      opacity:0; transition:opacity .3s,transform .3s; pointer-events:none; z-index:999;
    }
    #toast.show { opacity:1; transform:translateX(-50%) translateY(0); }

    /* ── Info sections ── */
    .info-section {
      position:relative; z-index:2; max-width:640px; margin:0 auto;
      padding:44px 28px; border-top:1px solid rgba(0,245,255,0.06);
    }
    .info-section h2 {
      font-family:'Orbitron',sans-serif; font-size:1.1rem; font-weight:700;
      letter-spacing:4px; color:var(--cyan); margin-bottom:16px;
      text-transform:uppercase; text-shadow:0 0 20px rgba(0,245,255,0.4);
    }
    .info-section p { color:var(--muted); font-size:.95rem; line-height:1.75; margin-bottom:8px; font-weight:300; }
    .info-section a { color:var(--cyan); text-decoration:none; }
    .info-section a:hover { text-shadow:0 0 8px var(--cyan); }
    footer {
      position:relative; z-index:2; background:rgba(2,8,16,0.95);
      border-top:1px solid rgba(0,245,255,0.08); text-align:center;
      padding:24px; margin-top:40px; font-family:'Orbitron',sans-serif;
      font-size:.55rem; letter-spacing:4px; color:rgba(0,245,255,0.55); text-transform:uppercase;
    }
  </style>
</head>
<body>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <canvas id="particles"></canvas>

  <header>
    <div class="logo-wrap"><h1>Tirth's Prompt Garage</h1></div>
    <p class="tagline">AI · Cinematic · Hyperdetailed</p>
    <nav>
      <a href="#gallery"><span>Prompts</span></a>
      <a href="#about"><span>About</span></a>
      <a href="#contact"><span>Contact</span></a>
    </nav>
  </header>

  <div class="section-label">// Prompt Database</div>

  <section id="gallery">
    {% for idx, item in prompts %}
    <div class="card" id="card-{{ item.id }}" style="animation-delay:{{ idx * 0.15 }}s; --float-delay:{{ idx * 0.7 }}s">

      <!-- Upload overlay (only visible in dev mode) -->
      <div class="upload-overlay">
        <label for="file-{{ item.id }}">
          ⬆ Upload AI Preview<br>jpg / png / webp
          <input type="file" id="file-{{ item.id }}" accept=".jpg,.jpeg,.png,.webp"
                 onchange="uploadImage('{{ item.id }}', this)">
        </label>
        <div class="upload-status" id="status-{{ item.id }}"></div>
      </div>

      {% if item.image_url %}
        <div class="card-img-wrap" onclick="openLightbox('{{ item.image_url }}', '{{ item.title }}')">
          <span class="img-badge">AI Preview</span>
          <img src="{{ item.image_url }}" alt="{{ item.title }}" loading="lazy" id="img-{{ item.id }}">
        </div>
      {% else %}
        <div class="card-img-placeholder" id="placeholder-{{ item.id }}">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
            <rect x="3" y="3" width="18" height="18" rx="1"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <polyline points="21,15 16,10 5,21"/>
          </svg>
          No preview yet
        </div>
      {% endif %}

      <div class="card-body">
        <div class="card-num">{{ "%02d" % (idx+1) }}</div>
        <div class="card-status">Active Prompt</div>
        <h2>{{ item.title }}</h2>
        <p>{{ item.description }}</p>
        {% if item.image_url %}<p class="preview-hint">↑ Click image to expand</p>{% endif %}
        <button class="copy-btn" data-prompt="{{ item.prompt }}"
                onclick="copyPrompt(this); event.stopPropagation();">
          <span>[ Copy Prompt ]</span>
        </button>
      </div>
    </div>
    {% endfor %}
  </section>

  <section id="about" class="info-section">
    <h2>// About</h2>
    <p>I'm Tirth — a Prompt Engineer and Python Developer building at the intersection of artificial intelligence and creative technology.</p>
    <p>I specialise in crafting high-precision, cinematic AI prompts that transform ideas into stunning visual outputs. Every prompt I engineer is a deliberate, layered instruction — designed to push AI image and video models to their fullest potential.</p>
    <p>Beyond prompting, I build intelligent tools and automation systems in Python that streamline creative workflows and bring AI-powered products to life.</p>
    <p>This garage is my creative lab — a curated collection of my finest prompts, built for creators, developers, and visionaries who demand more from AI.</p>
  </section>
  <section id="contact" class="info-section">
    <h2>// Contact</h2>
    <p>Email: <a href="mailto:pateltirth6088@gmail.com">pateltirth6088@gmail.com</a></p>
  </section>
  <footer>© 2026 Tirth's Prompt Garage &nbsp;·&nbsp; All systems operational</footer>

  <!-- Manage Panel -->
  <div id="manage-panel">
    <div class="mp-header">
      <h2>// Prompt Manager</h2>
      <button class="mp-close" onclick="closeManage()">[ Close ]</button>
    </div>
    <div class="mp-body">

      <!-- Add new prompt form -->
      <div class="mp-form">
        <h3>+ Add New Prompt</h3>
        <div class="mp-row">
          <div class="mp-field">
            <label>Title</label>
            <input type="text" id="np-title" placeholder="e.g. Neon City Racer">
          </div>
          <div class="mp-field">
            <label>Short Description</label>
            <input type="text" id="np-desc" placeholder="One line summary">
          </div>
        </div>
        <div class="mp-row full">
          <div class="mp-field">
            <label>Full Prompt</label>
            <textarea id="np-prompt" placeholder="Paste your full AI prompt here..."></textarea>
          </div>
        </div>
        <button class="mp-btn" onclick="addPrompt()"><span>[ Add Prompt ]</span></button>
        <div class="mp-msg" id="add-msg"></div>
      </div>

      <!-- Existing prompts list -->
      <div class="mp-list" id="mp-list"></div>

    </div>
  </div>

  <!-- Edit modal -->
  <div id="edit-modal" style="display:none;position:fixed;inset:0;z-index:900;background:rgba(2,8,16,0.97);display:none;align-items:center;justify-content:center;">
    <div style="background:var(--surface);border:1px solid var(--border);padding:28px;width:90%;max-width:560px;">
      <h3 style="font-family:Orbitron,sans-serif;font-size:.7rem;letter-spacing:3px;color:var(--cyan);margin-bottom:18px;text-transform:uppercase;">// Edit Prompt</h3>
      <input type="hidden" id="edit-id">
      <div class="mp-field" style="margin-bottom:12px">
        <label>Title</label><input type="text" id="edit-title">
      </div>
      <div class="mp-field" style="margin-bottom:12px">
        <label>Description</label><input type="text" id="edit-desc">
      </div>
      <div class="mp-field" style="margin-bottom:16px">
        <label>Prompt</label><textarea id="edit-prompt" style="min-height:110px"></textarea>
      </div>
      <div style="display:flex;gap:10px;">
        <button class="mp-btn" onclick="saveEdit()"><span>[ Save ]</span></button>
        <button class="mp-btn danger" onclick="closeEdit()"><span>[ Cancel ]</span></button>
      </div>
      <div class="mp-msg" id="edit-msg"></div>
    </div>
  </div>

  <!-- Lightbox -->
  <div id="lightbox" onclick="closeLightbox()">
    <button id="lightbox-close" onclick="closeLightbox()">[ Close ]</button>
    <div id="lightbox-title"></div>
    <img id="lightbox-img" src="" alt="">
  </div>

  <div id="toast"></div>

  <!-- Secret dev trigger dot — bottom right corner -->
  <div id="dev-trigger" title="" onclick="toggleDevBar()"></div>
  <button id="dev-manage-float" onclick="openManage()">⚙ Manage Prompts</button>

  <!-- Dev bar — slides up from bottom -->
  <div id="dev-bar">
    <label>Dev Password</label>
    <input type="password" id="dev-pass" placeholder="Enter password" onkeydown="if(event.key==='Enter') devLogin()">
    <button onclick="devLogin()">Unlock</button>
    <button id="dev-lock-btn" style="display:none;border-color:var(--red);color:var(--red)" onclick="devLogout()">Lock</button>
    <button id="dev-manage-btn" style="display:none;" onclick="openManage()" class="mp-btn"><span>[ Manage Prompts ]</span></button>
    <span id="dev-status"></span>
  </div>

  <script>
    /* ══════════════════════════════════════════════════════
       SOUND ENGINE — Web Audio API, no files needed
       All sounds synthesised from scratch in the browser
    ══════════════════════════════════════════════════════ */
    const SFX = (() => {
      let ctx = null;

      function getCtx() {
        if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
        if (ctx.state === 'suspended') ctx.resume();
        return ctx;
      }

      /* master gain so nothing clips */
      function masterGain(ac, vol=0.4) {
        const g = ac.createGain();
        g.gain.setValueAtTime(vol, ac.currentTime);
        g.connect(ac.destination);
        return g;
      }

      /* ── Utility: quick envelope ── */
      function env(param, ac, attack, sustain, release, peak=1) {
        const t = ac.currentTime;
        param.setValueAtTime(0, t);
        param.linearRampToValueAtTime(peak, t + attack);
        param.setValueAtTime(peak, t + attack + sustain);
        param.exponentialRampToValueAtTime(0.0001, t + attack + sustain + release);
      }

      return {



        /* ⚡ Button hover — electric flicker */
        hover() {
          const ac = getCtx(), mg = masterGain(ac, 0.12);
          const buf = ac.createBuffer(1, ac.sampleRate*0.06, ac.sampleRate);
          const data = buf.getChannelData(0);
          for(let i=0;i<data.length;i++) data[i] = (Math.random()*2-1) * Math.pow(1-i/data.length,2);
          const src = ac.createBufferSource();
          src.buffer = buf;
          const filt = ac.createBiquadFilter();
          filt.type = 'bandpass'; filt.frequency.value = 3200; filt.Q.value = 1.5;
          const gain = ac.createGain();
          env(gain.gain, ac, 0.001, 0.02, 0.04, 1);
          src.connect(filt); filt.connect(gain); gain.connect(mg);
          src.start();
        },

        /* 📋 Copy prompt — satisfying sci-fi confirm */
        copy() {
          const ac = getCtx(), mg = masterGain(ac, 0.28);
          /* two-tone beep: low then high */
          [0, 0.07].forEach((delay, i) => {
            const osc  = ac.createOscillator();
            const gain = ac.createGain();
            osc.type = 'square';
            osc.frequency.setValueAtTime(i===0 ? 440 : 880, ac.currentTime+delay);
            env(gain.gain, ac, 0.002, 0.05, 0.10, 0.6);
            const filt = ac.createBiquadFilter();
            filt.type = 'lowpass'; filt.frequency.value = 1800;
            osc.connect(filt); filt.connect(gain); gain.connect(mg);
            osc.start(ac.currentTime+delay);
            osc.stop(ac.currentTime+delay+0.18);
          });
          /* trailing shimmer */
          const noise = ac.createBuffer(1, ac.sampleRate*0.3, ac.sampleRate);
          const nd = noise.getChannelData(0);
          for(let i=0;i<nd.length;i++) nd[i]=(Math.random()*2-1)*Math.pow(1-i/nd.length,1.5);
          const ns = ac.createBufferSource(); ns.buffer = noise;
          const nf = ac.createBiquadFilter(); nf.type='highpass'; nf.frequency.value=4000;
          const ng = ac.createGain(); ng.gain.setValueAtTime(0.15, ac.currentTime+0.12);
          ng.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime+0.4);
          ns.connect(nf); nf.connect(ng); ng.connect(mg);
          ns.start(ac.currentTime+0.12);
        },

        /* 🔓 Dev unlock — power-up sweep */
        unlock() {
          const ac = getCtx(), mg = masterGain(ac, 0.35);
          const osc = ac.createOscillator();
          const gain = ac.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(120, ac.currentTime);
          osc.frequency.exponentialRampToValueAtTime(1400, ac.currentTime+0.4);
          env(gain.gain, ac, 0.005, 0.2, 0.25, 0.5);
          const filt = ac.createBiquadFilter();
          filt.type='lowpass'; filt.frequency.setValueAtTime(400, ac.currentTime);
          filt.frequency.exponentialRampToValueAtTime(3000, ac.currentTime+0.4);
          osc.connect(filt); filt.connect(gain); gain.connect(mg);
          osc.start(); osc.stop(ac.currentTime+0.65);
        },

        /* 🔒 Dev lock — power-down sweep */
        lock() {
          const ac = getCtx(), mg = masterGain(ac, 0.28);
          const osc = ac.createOscillator();
          const gain = ac.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(1200, ac.currentTime);
          osc.frequency.exponentialRampToValueAtTime(80, ac.currentTime+0.35);
          env(gain.gain, ac, 0.005, 0.15, 0.20, 0.45);
          const filt = ac.createBiquadFilter();
          filt.type='lowpass'; filt.frequency.setValueAtTime(3000, ac.currentTime);
          filt.frequency.exponentialRampToValueAtTime(200, ac.currentTime+0.35);
          osc.connect(filt); filt.connect(gain); gain.connect(mg);
          osc.start(); osc.stop(ac.currentTime+0.55);
        },

        /* 🖼️ Lightbox open — deep thud + shimmer */
        open() {
          const ac = getCtx(), mg = masterGain(ac, 0.32);
          /* thud */
          const osc = ac.createOscillator();
          const g1  = ac.createGain();
          osc.type='sine'; osc.frequency.setValueAtTime(180, ac.currentTime);
          osc.frequency.exponentialRampToValueAtTime(40, ac.currentTime+0.18);
          env(g1.gain, ac, 0.002, 0.06, 0.18, 0.8);
          osc.connect(g1); g1.connect(mg); osc.start(); osc.stop(ac.currentTime+0.28);
          /* shimmer */
          const osc2 = ac.createOscillator();
          const g2   = ac.createGain();
          osc2.type='sine'; osc2.frequency.setValueAtTime(1200, ac.currentTime+0.05);
          osc2.frequency.linearRampToValueAtTime(2400, ac.currentTime+0.22);
          env(g2.gain, ac, 0.005, 0.05, 0.20, 0.3);
          osc2.connect(g2); g2.connect(mg);
          osc2.start(ac.currentTime+0.05); osc2.stop(ac.currentTime+0.35);
        },

        /* ❌ Lightbox close — soft click */
        close() {
          const ac = getCtx(), mg = masterGain(ac, 0.20);
          const osc = ac.createOscillator();
          const gain = ac.createGain();
          osc.type='triangle'; osc.frequency.setValueAtTime(600, ac.currentTime);
          osc.frequency.exponentialRampToValueAtTime(200, ac.currentTime+0.08);
          env(gain.gain, ac, 0.001, 0.01, 0.10, 0.6);
          osc.connect(gain); gain.connect(mg);
          osc.start(); osc.stop(ac.currentTime+0.14);
        },

        /* ⬆️ Upload success — rising chime */
        upload() {
          const ac = getCtx(), mg = masterGain(ac, 0.30);
          [0, 0.10, 0.20].forEach((delay, i) => {
            const freqs = [523, 659, 784];
            const osc   = ac.createOscillator();
            const gain  = ac.createGain();
            osc.type='sine'; osc.frequency.value=freqs[i];
            env(gain.gain, ac, 0.005, 0.08, 0.25, 0.5);
            osc.connect(gain); gain.connect(mg);
            osc.start(ac.currentTime+delay);
            osc.stop(ac.currentTime+delay+0.35);
          });
        },

        /* ✗ Error — harsh buzz */
        error() {
          const ac = getCtx(), mg = masterGain(ac, 0.22);
          const osc = ac.createOscillator();
          const gain = ac.createGain();
          osc.type='sawtooth'; osc.frequency.value=120;
          env(gain.gain, ac, 0.002, 0.12, 0.12, 0.5);
          const filt = ac.createBiquadFilter(); filt.type='lowpass'; filt.frequency.value=600;
          osc.connect(filt); filt.connect(gain); gain.connect(mg);
          osc.start(); osc.stop(ac.currentTime+0.28);
        },

        /* 🖱️ Nav link click — crisp tap */
        tap() {
          const ac = getCtx(), mg = masterGain(ac, 0.18);
          const buf = ac.createBuffer(1, ac.sampleRate*0.04, ac.sampleRate);
          const d = buf.getChannelData(0);
          for(let i=0;i<d.length;i++) d[i]=(Math.random()*2-1)*Math.pow(1-i/d.length,3);
          const src = ac.createBufferSource(); src.buffer=buf;
          const filt = ac.createBiquadFilter(); filt.type='bandpass'; filt.frequency.value=2000; filt.Q.value=2;
          const gain = ac.createGain(); gain.gain.value=1;
          src.connect(filt); filt.connect(gain); gain.connect(mg);
          src.start();
        },

      };
    })();

    /* attach hover sound to all interactive elements */
    document.querySelectorAll('button, nav a, .copy-btn, .card').forEach(el => {
      el.addEventListener('mouseenter', () => SFX.hover());
    });
    /* nav tap */
    document.querySelectorAll('nav a').forEach(el => el.addEventListener('click', () => SFX.tap()));

    /* ── Dev mode ── */
    let devMode = false;
    function toggleDevBar() {
      document.getElementById('dev-bar').classList.toggle('open');
    }
    function devLogin() {
      const pw = document.getElementById('dev-pass').value;
      fetch('/api/devcheck', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({password: pw})
      }).then(r => r.json()).then(d => {
        if (d.ok) {
          devMode = true;
          document.body.classList.add('dev-mode');
          document.getElementById('dev-status').textContent = '✓ Dev Mode Active';
          document.getElementById('dev-status').style.color = 'var(--green)';
          document.getElementById('dev-lock-btn').style.display = '';
          document.getElementById('dev-manage-btn').style.display = '';
          document.getElementById('dev-manage-float').style.display = 'block';
          document.getElementById('dev-bar').classList.remove('open');
          showToast('▶ Dev mode unlocked', 'green'); SFX.unlock();
        } else {
          document.getElementById('dev-status').textContent = '✗ Wrong password'; SFX.error();
          document.getElementById('dev-status').style.color = 'var(--red)';
        }
      });
    }
    function devLogout() {
      devMode = false;
      document.body.classList.remove('dev-mode');
      document.getElementById('dev-status').textContent = '';
      document.getElementById('dev-lock-btn').style.display = 'none';
      document.getElementById('dev-manage-btn').style.display = 'none';
      document.getElementById('dev-manage-float').style.display = 'none';
      document.getElementById('dev-pass').value = '';
      showToast('▶ Dev mode locked'); SFX.lock();
    }

    /* ── Upload image ── */
    function uploadImage(promptId, input) {
      if (!input.files.length) return;
      const file   = input.files[0];
      const status = document.getElementById('status-' + promptId);
      status.style.color = 'var(--muted)';
      status.textContent = 'Uploading...';

      const fd = new FormData();
      fd.append('file', file);

      fetch('/api/upload/' + promptId, { method: 'POST', body: fd })
        .then(r => r.json())
        .then(d => {
          if (d.ok) {
            status.style.color = 'var(--green)';
            status.textContent = '✓ Uploaded!'; SFX.upload();

            // Update image live without page reload
            const wrap = document.querySelector('#card-' + promptId + ' .card-img-wrap');
            const placeholder = document.getElementById('placeholder-' + promptId);
            const ts = '?t=' + Date.now();

            if (wrap) {
              // Card already has an image — just update src
              document.getElementById('img-' + promptId).src = d.url + ts;
            } else if (placeholder) {
              // Replace placeholder with real image wrap
              const newWrap = document.createElement('div');
              newWrap.className = 'card-img-wrap';
              newWrap.onclick = () => openLightbox(d.url, document.querySelector('#card-' + promptId + ' h2').textContent);
              newWrap.innerHTML = `
                <span class="img-badge">AI Preview</span>
                <img src="${d.url + ts}" id="img-${promptId}" alt="" style="width:100%;height:100%;object-fit:cover;display:block;filter:brightness(0.85) saturate(1.1)">
                <div style="position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,transparent 60%,rgba(0,245,255,0.08) 80%,rgba(0,10,20,0.55) 100%)"></div>
              `;
              placeholder.replaceWith(newWrap);
            }
            setTimeout(() => { status.textContent = ''; }, 3000);
          } else {
            status.style.color = 'var(--red)';
            status.textContent = '✗ ' + d.error; SFX.error();
          }
        });
    }

    /* ── Lightbox ── */
    function openLightbox(src, title) {
      if (document.body.classList.contains('dev-mode')) return; // don't open while uploading
      document.getElementById('lightbox-img').src = src;
      document.getElementById('lightbox-title').textContent = title;
      SFX.open(); document.getElementById('lightbox').classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function closeLightbox() {
      SFX.close(); document.getElementById('lightbox').classList.remove('open');
      document.body.style.overflow = '';
    }
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });

    /* ── Copy ── */
    function copyPrompt(btn) {
      const text = btn.dataset.prompt, label = btn.querySelector('span');
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.resolve(legacyCopy(text)))
        .then(() => {
          btn.classList.add('ok'); label.textContent = '[ ✓ Copied! ]';
          SFX.copy(); showToast('▶ Prompt copied to buffer');
          setTimeout(() => { btn.classList.remove('ok'); label.textContent = '[ Copy Prompt ]'; }, 2200);
        });
    }
    function legacyCopy(text) {
      const ta = Object.assign(document.createElement('textarea'), {value:text, style:'position:fixed;opacity:0'});
      document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
    }
    function showToast(msg, color) {
      const t = document.getElementById('toast');
      t.textContent = msg || '';
      t.style.borderColor = color === 'green' ? 'var(--green)' : 'var(--cyan)';
      t.style.color       = color === 'green' ? 'var(--green)' : 'var(--cyan)';
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2600);
    }


    /* ── Manage Panel JS ── */
    function openManage() {
      document.getElementById('manage-panel').classList.add('open');
      document.body.style.overflow = 'hidden';
      loadMpList();
    }
    function closeManage() {
      document.getElementById('manage-panel').classList.remove('open');
      document.body.style.overflow = '';
    }
    function closeEdit() {
      document.getElementById('edit-modal').style.display = 'none';
    }

    function loadMpList() {
      fetch('/api/prompts').then(r=>r.json()).then(prompts => {
        const list = document.getElementById('mp-list');
        if (!prompts.length) { list.innerHTML = '<div style="color:var(--muted);font-family:Orbitron,sans-serif;font-size:.6rem;letter-spacing:2px;">No prompts yet</div>'; return; }
        list.innerHTML = prompts.map((p,i) => {
          const imgSrc = p.image_url || '';
          const thumb  = imgSrc
            ? `<img class="mp-item-thumb" src="${imgSrc}" alt="">`
            : `<div class="mp-item-thumb-placeholder">No IMG</div>`;
          return `
          <div class="mp-item" id="mp-item-${p.id}">
            ${thumb}
            <div class="mp-item-info">
              <div class="mp-item-title">${String(i+1).padStart(2,'0')} — ${p.title}</div>
              <div class="mp-item-desc">${p.description || p.prompt.slice(0,80)}...</div>
            </div>
            <div class="mp-item-actions">
              <button class="mp-btn" onclick="openEdit('${p.id}','${encodeURIComponent(p.title)}','${encodeURIComponent(p.description||'')}','${encodeURIComponent(p.prompt)}')"><span>Edit</span></button>
              <button class="mp-btn danger" onclick="deletePrompt('${p.id}')"><span>Delete</span></button>
            </div>
          </div>`;
        }).join('');
      });
    }

    function addPrompt() {
      const title = document.getElementById('np-title').value.trim();
      const desc  = document.getElementById('np-desc').value.trim();
      const prompt= document.getElementById('np-prompt').value.trim();
      const msg   = document.getElementById('add-msg');
      if (!title || !prompt) { msg.style.color='var(--red)'; msg.textContent='✗ Title and prompt are required'; return; }
      const pw = document.getElementById('dev-pass').value;
      fetch('/api/prompts/add', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({password:pw, title, description:desc, prompt})
      }).then(r=>r.json()).then(d => {
        if (d.ok) {
          msg.style.color='var(--green)'; msg.textContent='✓ Prompt added! Refresh to see it on the page.';
          document.getElementById('np-title').value='';
          document.getElementById('np-desc').value='';
          document.getElementById('np-prompt').value='';
          loadMpList(); SFX.upload();
        } else { msg.style.color='var(--red)'; msg.textContent='✗ '+d.error; SFX.error(); }
      });
    }

    function openEdit(id, title, desc, prompt) {
      document.getElementById('edit-id').value    = id;
      document.getElementById('edit-title').value = decodeURIComponent(title);
      document.getElementById('edit-desc').value  = decodeURIComponent(desc);
      document.getElementById('edit-prompt').value= decodeURIComponent(prompt);
      document.getElementById('edit-modal').style.display = 'flex';
      document.getElementById('edit-msg').textContent = '';
    }

    function saveEdit() {
      const id    = document.getElementById('edit-id').value;
      const title = document.getElementById('edit-title').value.trim();
      const desc  = document.getElementById('edit-desc').value.trim();
      const prompt= document.getElementById('edit-prompt').value.trim();
      const msg   = document.getElementById('edit-msg');
      const pw    = document.getElementById('dev-pass').value;
      fetch('/api/prompts/edit', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({password:pw, id, title, description:desc, prompt})
      }).then(r=>r.json()).then(d => {
        if (d.ok) {
          msg.style.color='var(--green)'; msg.textContent='✓ Saved! Refresh to see changes.';
          loadMpList(); SFX.upload();
          setTimeout(() => closeEdit(), 1200);
        } else { msg.style.color='var(--red)'; msg.textContent='✗ '+d.error; SFX.error(); }
      });
    }

    function deletePrompt(id) {
      if (!confirm('Delete this prompt? This cannot be undone.')) return;
      const pw = document.getElementById('dev-pass').value;
      fetch('/api/prompts/delete', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({password:pw, id})
      }).then(r=>r.json()).then(d => {
        if (d.ok) {
          document.getElementById('mp-item-'+id)?.remove();
          showToast('▶ Prompt deleted'); SFX.lock();
        } else { showToast('✗ '+d.error); SFX.error(); }
      });
    }

        /* ── Scroll Pop Animation ── */
    (function() {
      const cards = document.querySelectorAll('.card');

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          const card = entry.target;
          const ratio = entry.intersectionRatio;

          if (entry.isIntersecting && ratio > 0.15) {
            /* card scrolled into view — pop out toward viewer */
            card.classList.remove('pop-out');
            card.classList.add('pop-in');
          } else if (!entry.isIntersecting) {
            /* card scrolled out of view — determine direction */
            const rect = entry.boundingClientRect;
            card.classList.remove('pop-in');
            if (rect.top < 0) {
              /* scrolled past upward — shrink back up */
              card.classList.add('pop-out');
            } else {
              /* below viewport — reset to pre-pop state */
              card.classList.remove('pop-out');
            }
          }
        });
      }, {
        threshold: [0, 0.15, 0.5, 1.0],
        rootMargin: '0px 0px -60px 0px'  /* trigger slightly before fully visible */
      });

      /* stagger each card's transition delay so row pops in sequentially */
      cards.forEach((card, i) => {
        const col = i % 3;   /* assumes up to 3 columns */
        card.style.transitionDelay = (col * 0.08) + 's';
        observer.observe(card);
      });
    })();

        /* ── Neon City Skyline ── */
    (function() {
      const THREE = window.THREE;

      const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('particles'), antialias: true, alpha: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;

      const scene  = new THREE.Scene();
      scene.fog    = new THREE.Fog(0x020810, 30, 75);

      const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 120);
      camera.position.set(0, 3.2, 16);
      camera.lookAt(0, 2, 0);

      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth/window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      });

      let mouseX = 0, mouseY = 0;
      window.addEventListener('mousemove', e => {
        mouseX =  (e.clientX/window.innerWidth  - 0.5)*2;
        mouseY = -(e.clientY/window.innerHeight - 0.5)*2;
      });

      /* ── Lights ── */
      scene.add(new THREE.AmbientLight(0x020810, 3));
      const moonLight = new THREE.DirectionalLight(0x001a33, 1.8);
      moonLight.position.set(-3, 10, 5);
      moonLight.castShadow = true;
      scene.add(moonLight);

      /* searchlight — follows cursor */
      const searchLight = new THREE.SpotLight(0x00f5ff, 0, 70, Math.PI*0.055, 0.45, 1.0);
      searchLight.position.set(0, 24, 6);
      searchLight.castShadow = false;
      scene.add(searchLight);
      scene.add(searchLight.target);

      /* ground glow */
      const groundGlow = new THREE.PointLight(0x001830, 2, 12);
      groundGlow.position.set(0, 0.3, 0);
      scene.add(groundGlow);

      /* ── GROUND — wet dark street ── */
      const ground = new THREE.Mesh(
        new THREE.PlaneGeometry(160, 50),
        new THREE.MeshStandardMaterial({ color:0x010608, roughness:0.04, metalness:0.95 })
      );
      ground.rotation.x = -Math.PI/2;
      ground.receiveShadow = true;
      scene.add(ground);

      /* street centre line */
      const centreLine = new THREE.Mesh(
        new THREE.PlaneGeometry(160, 0.06),
        new THREE.MeshBasicMaterial({ color:0x002233, transparent:true, opacity:0.7 })
      );
      centreLine.rotation.x = -Math.PI/2;
      centreLine.position.y = 0.01;
      scene.add(centreLine);

      /* ── BUILDING COLOUR — only ONE palette, dim body + bright windows ── */
      const BODY_COL = 0x020c14;       /* almost black, very faint blue tint */
      const WIN_COL  = 0x44ddff;       /* bright light blue — ALL windows same */
      const ROOF_COL = 0x00ccff;       /* roof edge glow */
      const EDGE_COL = 0x003344;       /* vertical edge lines — barely visible */

      const windows = [];

      /* ── BUILDING FACTORY ── */
      function makeBuilding(x, z, w, d, h) {
        const g = new THREE.Group();

        /* body — very dark, barely visible */
        const body = new THREE.Mesh(
          new THREE.BoxGeometry(w, h, d),
          new THREE.MeshStandardMaterial({
            color:    BODY_COL,
            emissive: 0x001122,
            emissiveIntensity: 0.08,
            roughness: 0.3,
            metalness: 0.8,
          })
        );
        body.position.y = h/2;
        body.castShadow = true;
        g.add(body);

        /* thin roof glow strip */
        const roof = new THREE.Mesh(
          new THREE.BoxGeometry(w + 0.04, 0.045, d + 0.04),
          new THREE.MeshBasicMaterial({ color: ROOF_COL, transparent:true, opacity:0.8 })
        );
        roof.position.y = h + 0.02;
        g.add(roof);

        /* 4 corner edge strips — barely visible dark blue */
        [[-w/2, -d/2],[w/2,-d/2],[-w/2,d/2],[w/2,d/2]].forEach(([ex,ez]) => {
          const e = new THREE.Mesh(
            new THREE.BoxGeometry(0.03, h, 0.03),
            new THREE.MeshBasicMaterial({ color:EDGE_COL, transparent:true, opacity:0.35 })
          );
          e.position.set(ex, h/2, ez);
          g.add(e);
        });

        /* ── WINDOWS — bright light blue, grid layout ── */
        const cols = Math.max(1, Math.floor(w / 0.52));
        const rows = Math.max(1, Math.floor(h / 0.68));
        const winW = 0.20, winH = 0.25;

        for (let r = 0; r < rows; r++) {
          for (let c = 0; c < cols; c++) {
            if (Math.random() < 0.14) continue;   /* ~14% dark */

            const wx = x - w/2 + (c+0.5)*(w/cols);
            const wy = 0.55 + r*(h/rows) + (h/rows)*0.1;
            const wz = z + d/2 + 0.015;

            const wMat = new THREE.MeshBasicMaterial({
              color: WIN_COL,
              transparent: true,
              opacity: 0.75 + Math.random()*0.25,
            });
            const win = new THREE.Mesh(new THREE.PlaneGeometry(winW, winH), wMat);
            win.position.set(wx, wy, wz);
            win.userData = {
              base:        wMat.opacity,
              flickerSpd:  Math.random()*2.5 + 0.4,
              flickerPhs:  Math.random()*Math.PI*2,
              offChance:   0.0008 + Math.random()*0.001,
              off:         false,
              offTimer:    0,
            };
            scene.add(win);
            windows.push(win);

            /* back face windows */
            if (Math.random() > 0.45) {
              const wb = win.clone();
              wb.position.z = z - d/2 - 0.015;
              wb.rotation.y = Math.PI;
              scene.add(wb);
              windows.push(wb);
            }
          }
        }

        /* window glow reflection on ground */
        const refl = new THREE.Mesh(
          new THREE.PlaneGeometry(w*0.7, 1.8),
          new THREE.MeshBasicMaterial({ color:0x003344, transparent:true, opacity:0.07 })
        );
        refl.rotation.x = -Math.PI/2;
        refl.position.set(x, 0.01, z + d/2 + 0.9);
        scene.add(refl);

        g.position.set(x, 0, z);
        scene.add(g);
      }

      /* ── CITY LAYOUT — 3 depth layers, all varied heights ── */

      /* back layer — tallest skyscrapers */
      for (let i = -10; i <= 10; i++) {
        /* varied heights: mix of supertall, tall, medium */
        const roll = Math.random();
        const h    = roll < 0.2 ? 14+Math.random()*8      /* supertall 14-22 */
                   : roll < 0.5 ? 9 +Math.random()*5      /* tall      9-14  */
                   :               5 +Math.random()*4;     /* medium    5-9   */
        const w = 1.1 + Math.random()*1.6;
        makeBuilding(i*2.7 + (Math.random()-0.5)*0.7, -18, w, 0.9, h);
      }

      /* mid layer */
      for (let i = -9; i <= 9; i++) {
        const roll = Math.random();
        const h    = roll < 0.15 ? 11+Math.random()*7
                   : roll < 0.5  ? 6 +Math.random()*5
                   :                3 +Math.random()*3;
        const w = 0.9 + Math.random()*2.0;
        makeBuilding(i*2.3 + (Math.random()-0.5)*0.5, -10, w, 1.1, h);
      }

      /* front layer — shorter, close to camera */
      for (let i = -8; i <= 8; i++) {
        const roll = Math.random();
        const h    = roll < 0.2 ? 7+Math.random()*5
                   : roll < 0.6 ? 3+Math.random()*4
                   :               1.5+Math.random()*1.5;
        const w = 0.7 + Math.random()*1.7;
        makeBuilding(i*1.9 + (Math.random()-0.5)*0.4, -4, w, 1.3, h);
      }

      /* ── ANTENNA / SPIRE on tallest buildings ── */
      /* add thin spires to some taller-looking spots */
      [-7,-2,3,8].forEach(xi => {
        const h = 3 + Math.random()*4;
        const spire = new THREE.Mesh(
          new THREE.CylinderGeometry(0.015, 0.04, h, 5),
          new THREE.MeshBasicMaterial({ color:0x002233 })
        );
        spire.position.set(xi*2.7 + (Math.random()-0.5)*1.5, 18+Math.random()*4 + h/2, -18);
        scene.add(spire);
        /* blinking light on top */
        const blink = new THREE.Mesh(
          new THREE.SphereGeometry(0.05, 6, 6),
          new THREE.MeshBasicMaterial({ color:0x00f5ff, transparent:true, opacity:0.9 })
        );
        blink.position.set(spire.position.x, spire.position.y + h/2, spire.position.z);
        blink.userData = { phase: Math.random()*Math.PI*2, spd: Math.random()*2+1 };
        scene.add(blink);
        windows.push(blink);   /* reuse flicker logic */
      });

      /* ── FLYING VEHICLES — same cyan colour ── */
      const vehicles = [];
      for (let i = 0; i < 20; i++) {
        const v = new THREE.Group();
        const body = new THREE.Mesh(
          new THREE.BoxGeometry(0.22, 0.06, 0.10),
          new THREE.MeshBasicMaterial({ color:0x001a26 })
        );
        v.add(body);
        /* headlights */
        [0.12, -0.12].forEach(ox => {
          const hl = new THREE.Mesh(
            new THREE.SphereGeometry(0.025,6,6),
            new THREE.MeshBasicMaterial({ color:WIN_COL })
          );
          hl.position.set(0.12, 0, ox);
          v.add(hl);
        });
        const lane = 1.2 + Math.random()*5.5;
        const zv   = -3 - Math.random()*22;
        v.position.set((Math.random()-0.5)*36, lane, zv);
        scene.add(v);
        vehicles.push({
          mesh:  v,
          speed: (0.04 + Math.random()*0.07) * (Math.random()<0.5?1:-1),
          lane,  zv,
        });
      }

      /* ── RAIN ── */
      const RAIN = 1400;
      const rPos = new Float32Array(RAIN*3);
      const rSpd = new Float32Array(RAIN);
      for (let i = 0; i < RAIN; i++) {
        rPos[i*3]   = (Math.random()-0.5)*52;
        rPos[i*3+1] = Math.random()*26;
        rPos[i*3+2] = (Math.random()-0.5)*35 - 12;
        rSpd[i]     = 0.14 + Math.random()*0.10;
      }
      const rGeo = new THREE.BufferGeometry();
      rGeo.setAttribute('position', new THREE.BufferAttribute(rPos,3));
      const rMat = new THREE.PointsMaterial({ color:0x001a28, size:0.04, transparent:true, opacity:0.3 });
      scene.add(new THREE.Points(rGeo, rMat));

      /* ── SEARCHLIGHT CONE visual ── */
      const coneGeo = new THREE.ConeGeometry(0.15, 1, 14, 1, true);
      const coneMat = new THREE.MeshBasicMaterial({ color:0x00f5ff, transparent:true, opacity:0.05, side:THREE.DoubleSide });
      const coneMesh = new THREE.Mesh(coneGeo, coneMat);
      scene.add(coneMesh);

      /* ── Main loop ── */
      let t = 0;
      function animate() {
        requestAnimationFrame(animate);
        t += 0.013;

        /* searchlight */
        const slX = mouseX * 13;
        const slY = mouseY * 5 + 1.5;
        searchLight.target.position.set(slX, slY, -10);
        searchLight.target.updateMatrixWorld();
        searchLight.intensity = 28 + Math.sin(t*1.2)*3;

        /* cone */
        const dx = slX - searchLight.position.x;
        const dy = slY - searchLight.position.y;
        const dz = -10  - searchLight.position.z;
        const dl = Math.sqrt(dx*dx+dy*dy+dz*dz);
        coneMesh.position.set(
          searchLight.position.x + dx/dl*9,
          searchLight.position.y + dy/dl*9,
          searchLight.position.z + dz/dl*9
        );
        coneMesh.lookAt(slX, slY, -10);
        coneMesh.rotateX(Math.PI/2);
        coneMesh.scale.y = dl*0.28;

        /* window flicker */
        windows.forEach(w => {
          const u = w.userData;
          if (!u.flickerSpd) return;
          if (u.off) {
            u.offTimer--;
            if (u.offTimer <= 0) { u.off = false; }
            w.material.opacity = 0;
            return;
          }
          if (Math.random() < u.offChance) { u.off = true; u.offTimer = 8+Math.floor(Math.random()*25); return; }
          const flicker = 0.55 + 0.45*Math.sin(t*u.flickerSpd + u.flickerPhs);
          w.material.opacity = (u.base || 0.8) * flicker;
        });

        /* vehicles */
        vehicles.forEach(v => {
          v.mesh.position.x += v.speed;
          if (v.mesh.position.x >  20) v.mesh.position.x = -20;
          if (v.mesh.position.x < -20) v.mesh.position.x =  20;
          v.mesh.position.y = v.lane + Math.sin(t*0.7 + v.zv)*0.12;
        });

        /* rain */
        const rpa = rGeo.attributes.position;
        for (let i = 0; i < RAIN; i++) {
          let ry = rpa.getY(i) - rSpd[i];
          if (ry < 0) {
            ry = 26;
            rpa.setX(i,(Math.random()-0.5)*52);
            rpa.setZ(i,(Math.random()-0.5)*35-12);
          }
          rpa.setY(i, ry);
        }
        rpa.needsUpdate = true;

        /* subtle camera drift */
        camera.position.x += (mouseX*0.55 - camera.position.x)*0.012;
        camera.position.y += (3.2 + mouseY*0.35 - camera.position.y)*0.012;
        camera.lookAt(mouseX*0.25, 2 + mouseY*0.18, 0);

        renderer.render(scene, camera);
      }
      animate();
    })();
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    enriched = []
    for item in load_prompts():
        enriched.append({**item, "image_url": get_image_url(item["id"]) or ""})
    return render_template_string(PAGE, prompts=list(enumerate(enriched)))


@app.route("/api/prompts", methods=["GET"])
def get_prompts():
    items = load_prompts()
    for item in items:
        item['image_url'] = get_image_url(item['id']) or ''
    return jsonify(items)

@app.route("/api/prompts/add", methods=["POST"])
def add_prompt():
    data  = request.get_json()
    if data.get("password") != DEV_PASSWORD:
        return jsonify({"ok": False, "error": "Unauthorized"}), 403
    title       = data.get("title", "").strip()
    description = data.get("description", "").strip()
    prompt      = data.get("prompt", "").strip()
    if not title or not prompt:
        return jsonify({"ok": False, "error": "Title and prompt required"}), 400
    prompts = load_prompts()
    pid = slugify(title)
    # ensure unique id
    existing_ids = [p["id"] for p in prompts]
    base_pid = pid
    counter  = 2
    while pid in existing_ids:
        pid = f"{base_pid}_{counter}"
        counter += 1
    prompts.append({"id": pid, "title": title, "description": description, "prompt": prompt})
    save_prompts(prompts)
    return jsonify({"ok": True, "id": pid})

@app.route("/api/prompts/edit", methods=["POST"])
def edit_prompt():
    data = request.get_json()
    if data.get("password") != DEV_PASSWORD:
        return jsonify({"ok": False, "error": "Unauthorized"}), 403
    pid = data.get("id")
    prompts = load_prompts()
    for p in prompts:
        if p["id"] == pid:
            if data.get("title"):       p["title"]       = data["title"].strip()
            if data.get("description") is not None: p["description"] = data["description"].strip()
            if data.get("prompt"):      p["prompt"]      = data["prompt"].strip()
            save_prompts(prompts)
            return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Not found"}), 404

@app.route("/api/prompts/delete", methods=["POST"])
def delete_prompt():
    data = request.get_json()
    if data.get("password") != DEV_PASSWORD:
        return jsonify({"ok": False, "error": "Unauthorized"}), 403
    pid     = data.get("id")
    prompts = load_prompts()
    new_list = [p for p in prompts if p["id"] != pid]
    if len(new_list) == len(prompts):
        return jsonify({"ok": False, "error": "Not found"}), 404
    # delete image too
    for ext in ["jpg","jpeg","png","webp"]:
        img = os.path.join(IMG_DIR, f"{pid}.{ext}")
        if os.path.exists(img): os.remove(img)
    save_prompts(new_list)
    return jsonify({"ok": True})

@app.route("/api/devcheck", methods=["POST"])
def devcheck():
    data = request.get_json()
    return jsonify({"ok": data.get("password") == DEV_PASSWORD})

if __name__ == "__main__":
    print("\n  ⚡  Tirth's Prompt Garage")
    print("  ──────────────────────────────────────────────")
    print("  Running at  →  http://127.0.0.1:5000")
    print(f"  Dev password  →  {DEV_PASSWORD}")
    print(f"  Images folder →  {IMG_DIR}\n")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
