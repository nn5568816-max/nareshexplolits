#!/usr/bin/env python3
"""
NARESH EXPLOITS | Portfolio  (Python version)

Generates index.html from the data below and serves it locally.

Usage:
    python portfolio.py              # build index.html and open http://localhost:8000
    python portfolio.py --build      # only build index.html
    python portfolio.py --port 9000  # use another port

Put hacker.jpg (your photo) and app.apk (your app) in the same folder.
"""

import argparse
import functools
import http.server
import socketserver
import webbrowser
from html import escape
from pathlib import Path

# ============================================================
# 1. YOUR DATA  (edit only this section)
# ============================================================

SITE = {
    "name": "NARESH EXPLOITS",
    "short_name": "NARESH",
    "tagline": "Cyber Security Learner & fingerprint osint based in India.",
    "footer_tagline": "Cyber Security Learner • Frontend Developer",
    "bio": (
        "I'm NARESH Exploits — a OSINT and cybersecurity learner "
        "interested in Linux, network security and web technologies."
    ),
    "location": "India",
    "email": "naresh@example.com",
    "photo": "hacker.jpg",
    "year": 2026,
    # Your WhatsApp number with country code, digits only (e.g. 919876543210)
    "whatsapp_number": "91xxxxxxxxxxx",
}

SOCIAL = [
    {
        "label": "WhatsApp",
        "icon": "fa-brands fa-whatsapp",
        "url": "https://whatsapp.com/channel/0029VbChMkL3gvWUmdoLeT0U",
        "cta": "Chat with me →",
        "css": "whatsapp-link",
    },
    {
        "label": "Telegram",
        "icon": "fa-brands fa-telegram",
        "url": "https://t.me/+Xrok4xEFCHc5N2M1",
        "cta": "Message me →",
        "css": "telegram-link",
    },
]

STATS = [
    ("GRADUATED", "2026"),
    ("COMPLETED PROJECTS", "1+"),
    ("PROJECTS", "1+"),
]

SKILLS = [
    {
        "name": "Kali Linux",
        "level": "Advanced",
        "url": "https://www.kali.org",
        "icon": "fa-brands fa-linux",
        "css": "kali-icon",
    },
    {
        "name": "Nmap",
        "level": "Advanced",
        "url": "https://nmap.org",
        "icon": "fa-solid fa-network-wired",
        "css": "nmap-icon",
    },
]

PROJECTS = [
    {
        "title": "My Web Project",
        "description": "A personal web project developed using modern frontend technologies.",
        "icon": "fa-solid fa-globe",
        "theme": "theme-blue",
        "url": "#",
    },
    {
        "title": "Security Dashboard",
        "description": "My own cybersecurity learning and security analysis dashboard.",
        "icon": "fa-solid fa-shield-halved",
        "theme": "theme-purple",
        "url": "#",
    },
    {
        "title": "My Own Project",
        "description": "A custom project created and developed by NARESH EXPLOITS.",
        "icon": "fa-solid fa-code",
        "theme": "theme-cyan",
        "url": "#",
    },
]

APP = {
    "name": "chatGpt",
    "description": (
        "An Android app I built and maintain, packed with OSINT and "
        "networking tools for security learners."
    ),
    "size": "20 MB",
    "version": "v1.0",
    "file": "app.apk",
}

NAV = [
    ("#home", "fa-solid fa-house"),
    ("#skills", "fa-solid fa-terminal"),
    ("#projects", "fa-solid fa-code"),
    ("#app", "fa-solid fa-mobile-screen-button"),
    ("#contact", "fa-regular fa-envelope"),
]

# ============================================================
# 2. CSS
# ============================================================

CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
:root{--pink:#ff416c;--orange:#ffb347;--blue:#36d1dc;--purple:#7f00ff;--cyan:#00c9a7;--darkblue:#4776e6}
body{font-family:Georgia,"Times New Roman",serif;background:#fff;color:#111;transition:.4s}
a{color:inherit;text-decoration:none}

/* NAVBAR */
.navbar{position:fixed;bottom:25px;left:50%;transform:translateX(-50%);width:min(500px,92%);height:65px;
 background:rgba(255,255,255,.95);backdrop-filter:blur(15px);border-radius:40px;border:1px solid #ddd;
 display:flex;align-items:center;justify-content:space-around;box-shadow:0 10px 35px rgba(0,0,0,.15);z-index:999}
.logo{font-size:14px;font-weight:bold;background:linear-gradient(90deg,var(--pink),var(--purple),var(--blue));
 -webkit-background-clip:text;background-clip:text;color:transparent}
.nav-icon{font-size:20px;cursor:pointer;transition:.3s}
.nav-icon:hover{transform:translateY(-4px) scale(1.15);color:var(--purple)}

/* HERO */
.hero{max-width:1100px;margin:auto;padding:40px 25px 70px}
.hero-title{text-align:center;font-size:25px;line-height:1.5;margin-bottom:65px}
.hero-title strong{background:linear-gradient(90deg,var(--pink),var(--orange),var(--blue),var(--purple));
 background-size:300% 300%;-webkit-background-clip:text;background-clip:text;color:transparent;
 animation:gradientMove 6s ease infinite}
@keyframes gradientMove{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.hero-grid{display:grid;grid-template-columns:1fr 280px 1fr;gap:40px;align-items:center}
.side-title{font-size:10px;letter-spacing:1px;font-weight:bold;color:var(--purple);margin-bottom:15px}
.side-text{font-size:15px;line-height:1.6}
.contact-info{margin-top:50px}

/* PROFILE */
.profile-wrapper{text-align:center}
.profile-frame{width:175px;height:255px;margin:auto;padding:10px;border:3px solid transparent;border-radius:100px;
 background:linear-gradient(#fff,#fff) padding-box,linear-gradient(135deg,var(--pink),var(--purple),var(--blue)) border-box;
 box-shadow:0 10px 35px rgba(127,0,255,.2)}
.profile-frame img{width:100%;height:100%;object-fit:cover;border-radius:90px;background:#111}

/* SOCIAL */
.social{display:flex;justify-content:center;gap:28px;margin-top:25px}
.social a{text-align:center;color:#777;transition:.3s}
.social i{display:block;font-size:25px;margin-bottom:6px;transition:.3s}
.social span{font-size:9px}
.social a:nth-child(1) i{color:#25D366}
.social a:nth-child(2) i{color:#229ED9}
.social a:hover{transform:translateY(-5px)}
.social a:hover i{transform:scale(1.2)}

/* STATS */
.stats{text-align:right}
.stat{margin-bottom:40px}
.stat-label{font-size:10px;color:var(--purple);margin-bottom:10px;font-weight:bold}
.stat-number{font-size:21px;font-weight:bold}

/* SECTION */
section{max-width:1050px;margin:auto;padding:75px 25px;border-top:1px solid #aaa}
.section-title{text-align:center;font-size:27px;margin-bottom:8px}
.section-subtitle{text-align:center;color:var(--blue);font-size:12px;font-weight:bold;letter-spacing:1px;
 text-transform:uppercase;margin-bottom:45px}

/* SKILLS */
.skills-container{max-width:550px;margin:auto}
.experience-title{text-align:center;font-size:15px;font-weight:bold;color:var(--purple);margin-bottom:35px}
.skills-grid{display:grid;grid-template-columns:repeat(2,160px);justify-content:center;gap:50px}
.skill{text-align:center}
.skill-icon{width:95px;height:95px;margin:auto;border-radius:50%;display:flex;align-items:center;
 justify-content:center;color:#fff;font-size:42px;box-shadow:0 10px 25px rgba(0,0,0,.18);transition:.35s}
.kali-icon{background:linear-gradient(135deg,#557cff,#7f00ff)}
.nmap-icon{background:linear-gradient(135deg,#00c9a7,#36d1dc)}
.skill:hover .skill-icon{transform:translateY(-8px) scale(1.1) rotate(3deg)}
.skill-name{margin-top:15px;font-size:15px;font-weight:bold}
.skill-level{margin-top:6px;font-size:11px;font-weight:bold;color:var(--cyan)}

/* PROJECTS */
.projects{max-width:900px;margin:auto}
.projects-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.project-card{border:1px solid #ddd;border-radius:17px;overflow:hidden;background:#fff;transition:.35s}
.project-card:hover{transform:translateY(-8px);box-shadow:0 15px 35px rgba(0,0,0,.15)}
.project-image{height:155px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:40px}
.project-image.theme-blue{background:linear-gradient(135deg,var(--blue),var(--darkblue))}
.project-image.theme-purple{background:linear-gradient(135deg,var(--purple),var(--pink))}
.project-image.theme-cyan{background:linear-gradient(135deg,var(--cyan),var(--orange))}
.project-content{padding:20px}
.project-title{font-size:17px;margin-bottom:10px}
.project-description{color:#777;font-size:12px;line-height:1.6;margin-bottom:17px}
.project-button{display:inline-block;padding:8px 16px;border:1px solid var(--purple);border-radius:20px;
 color:var(--purple);font-size:11px;font-weight:bold;transition:.3s}
.project-button:hover{color:#fff;border-color:transparent;background:linear-gradient(90deg,var(--purple),var(--blue))}

/* MY APP */
.app-container{max-width:560px;margin:auto}
.app-card{display:flex;align-items:center;gap:24px;border:1px solid #ddd;border-radius:22px;padding:26px;
 background:#fff;transition:.35s}
.app-card:hover{transform:translateY(-6px);box-shadow:0 15px 35px rgba(0,0,0,.15)}
.app-icon{flex-shrink:0;width:85px;height:85px;border-radius:22px;display:flex;align-items:center;
 justify-content:center;color:#fff;font-size:36px;background:linear-gradient(135deg,var(--purple),var(--pink));
 box-shadow:0 10px 25px rgba(127,0,255,.25)}
.app-info{flex:1}
.app-name{font-size:17px;margin-bottom:8px}
.app-description{color:#777;font-size:12px;line-height:1.6;margin-bottom:14px}
.app-meta{display:flex;gap:16px;align-items:center;margin-bottom:16px;font-size:11px;font-weight:bold;color:var(--cyan)}
.app-meta i{margin-right:5px}
.app-version{color:#999}
.app-actions{display:flex;gap:12px;flex-wrap:wrap}
.install-button{display:inline-flex;align-items:center;gap:8px;padding:9px 18px;border-radius:20px;border:none;
 color:#fff;font-size:11px;font-weight:bold;background:linear-gradient(90deg,var(--purple),var(--blue));
 transition:.3s;cursor:pointer}
.install-button:hover{transform:translateY(-3px);box-shadow:0 10px 20px rgba(127,0,255,.3)}
.delete-button{display:inline-flex;align-items:center;gap:8px;padding:9px 18px;border-radius:20px;
 border:1px solid var(--pink);color:var(--pink);background:transparent;font-size:11px;font-weight:bold;
 font-family:inherit;cursor:pointer;transition:.3s}
.delete-button:hover{color:#fff;border-color:transparent;background:var(--pink)}
.app-card.removed{opacity:0;transform:scale(.95);pointer-events:none}
.app-empty{text-align:center;color:#999;font-size:13px;display:none;padding:20px;border:1px dashed #ccc;border-radius:20px}
.app-empty.visible{display:block}

/* CONTACT */
.contact-section{max-width:950px}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:70px}
.contact-left h3,.contact-right h3{font-size:17px;color:var(--purple);margin-bottom:25px}
.contact-item{margin-bottom:25px}
.contact-label{font-size:12px;color:#999;margin-bottom:7px}
.contact-value{font-size:15px}
.whatsapp-link{display:inline-flex;align-items:center;gap:10px;color:#25D366;font-weight:bold}
.whatsapp-link i{font-size:21px}
.telegram-link{display:inline-flex;align-items:center;gap:10px;color:#229ED9;font-weight:bold}
.telegram-link i{font-size:21px}

/* FORM */
.form-group{position:relative;margin-bottom:30px}
.form-group input,.form-group textarea{width:100%;padding:17px 23px;border:2px solid var(--blue);
 border-radius:35px;outline:none;font-family:inherit;font-size:14px;background:transparent}
.form-group textarea{height:145px;border-radius:25px;resize:vertical}
.form-group input:focus,.form-group textarea:focus{border-color:var(--purple)}
.form-group label{position:absolute;top:-8px;left:23px;padding:0 7px;background:#fff;font-size:11px;
 font-weight:bold;color:var(--purple)}
.send-button{border:none;background:none;cursor:pointer;font-family:inherit;font-size:18px;font-weight:bold;
 color:var(--purple);transition:.3s}
.send-button:hover{transform:translateX(7px);color:var(--pink)}

/* FOOTER */
footer{border-top:1px solid #aaa;text-align:center;padding:80px 20px 120px}
footer h2{font-size:29px;margin-bottom:12px;background:linear-gradient(90deg,var(--pink),var(--purple),var(--blue));
 -webkit-background-clip:text;background-clip:text;color:transparent}
footer p{color:#777;margin-bottom:25px}
.copyright{color:#aaa;font-size:11px;margin-top:25px}

/* DARK MODE */
body.dark{background:#080812;color:#f5f5f5}
body.dark .navbar{background:rgba(15,15,30,.95);border-color:#333}
body.dark .hero-title,body.dark .section-title,body.dark .stat-number,body.dark .skill-name,body.dark .app-name{color:#fff}
body.dark .project-card,body.dark .app-card{background:#111122;border-color:#333}
body.dark .project-description,body.dark .app-description{color:#aaa}
body.dark .app-empty{border-color:#333;color:#777}
body.dark .form-group input,body.dark .form-group textarea{color:#fff}
body.dark .form-group label{background:#080812}
body.dark .profile-frame{background:linear-gradient(#080812,#080812) padding-box,
 linear-gradient(135deg,var(--pink),var(--purple),var(--blue)) border-box}

/* MOBILE */
@media(max-width:750px){
 .hero{padding-top:30px}
 .hero-title{font-size:20px;margin-bottom:45px}
 .hero-grid{grid-template-columns:1fr;text-align:center}
 .profile-wrapper{order:-1}
 .stats{text-align:center;display:flex;justify-content:space-around;gap:15px}
 .stat{margin-bottom:0}
 .contact-info{margin-top:30px}
 .skills-grid{grid-template-columns:repeat(2,130px);gap:35px}
 .projects-grid{grid-template-columns:1fr}
 .app-card{flex-direction:column;text-align:center}
 .app-actions{justify-content:center}
 .contact-grid{grid-template-columns:1fr;gap:45px}
 section{padding:55px 20px}
}
@media(max-width:400px){
 .stats{flex-direction:column;gap:25px}
 .skills-grid{grid-template-columns:1fr 1fr;gap:20px}
 .navbar{width:95%}
}

/* ICON ANIMATION */
.kali-icon i,.nmap-icon i{animation:iconFloat 3s ease-in-out infinite}
@keyframes iconFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
"""

# ============================================================
# 3. JAVASCRIPT  (dark mode, delete app, WhatsApp form)
#    __WA_NUMBER__ is replaced from SITE["whatsapp_number"]
# ============================================================

JS = r"""
/* DARK MODE */
const themeButton = document.getElementById("themeButton");
themeButton.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    const icon = themeButton.querySelector("i");
    icon.className = document.body.classList.contains("dark")
        ? "fa-regular fa-sun"
        : "fa-regular fa-moon";
});

/* MY APP - DELETE */
const appCard = document.getElementById("appCard");
const appEmpty = document.getElementById("appEmpty");
document.getElementById("deleteAppBtn").addEventListener("click", () => {
    if (!confirm("Delete this app from your portfolio?")) return;
    appCard.classList.add("removed");
    setTimeout(() => {
        appCard.style.display = "none";
        appEmpty.classList.add("visible");
    }, 350);
});

/* WHATSAPP CONTACT FORM */
document.getElementById("contactForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;
    const whatsappNumber = "__WA_NUMBER__";
    const text = `Hello __SITE_NAME__!\n\nName: ${name}\n\nEmail: ${email}\n\nMessage:\n${message}`;
    window.open(`https://wa.me/${whatsappNumber}?text=${encodeURIComponent(text)}`, "_blank");
});
"""

# ============================================================
# 4. HTML BUILDERS
# ============================================================


def e(value):
    """Escape text for safe HTML output."""
    return escape(str(value), quote=True)


def social_icons():
    items = "".join(
        f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">'
        f'<i class="{e(s["icon"])}"></i><span>{e(s["label"])}</span></a>'
        for s in SOCIAL
    )
    return f'<div class="social">{items}</div>'


def hero():
    stats = "".join(
        f'<div class="stat"><div class="stat-label">{e(label)}</div>'
        f'<div class="stat-number">{e(number)}</div></div>'
        for label, number in STATS
    )
    return f"""
<header class="hero" id="home">
  <h1 class="hero-title">Hi, I'm <strong>{e(SITE["name"])}</strong><br>{e(SITE["tagline"])}</h1>
  <div class="hero-grid">
    <div>
      <div class="side-title">BIOGRAPHY</div>
      <p class="side-text">{e(SITE["bio"])}</p>
      <div class="contact-info">
        <div class="side-title">CONTACT</div>
        <p class="side-text">{e(SITE["location"])}<br>{e(SITE["email"])}</p>
      </div>
    </div>
    <div class="profile-wrapper">
      <div class="profile-frame"><img src="{e(SITE["photo"])}" alt="{e(SITE["name"])}"></div>
      {social_icons()}
    </div>
    <div class="stats">{stats}</div>
  </div>
</header>"""


def skills():
    cards = "".join(
        f"""
      <div class="skill">
        <a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer" class="skill-icon {e(s["css"])}">
          <i class="{e(s["icon"])}"></i>
        </a>
        <div class="skill-name">{e(s["name"])}</div>
        <div class="skill-level">{e(s["level"])}</div>
      </div>"""
        for s in SKILLS
    )
    return f"""
<section id="skills">
  <h2 class="section-title">Skills</h2>
  <p class="section-subtitle">Cyber Security Tools</p>
  <div class="skills-container">
    <div class="experience-title">{{ }} Security &amp; Networking</div>
    <div class="skills-grid">{cards}
    </div>
  </div>
</section>"""


def projects():
    cards = "".join(
        f"""
      <div class="project-card">
        <div class="project-image {e(p["theme"])}"><i class="{e(p["icon"])}"></i></div>
        <div class="project-content">
          <h3 class="project-title">{e(p["title"])}</h3>
          <p class="project-description">{e(p["description"])}</p>
          <a href="{e(p["url"])}" class="project-button">View Project →</a>
        </div>
      </div>"""
        for p in PROJECTS
    )
    return f"""
<section id="projects">
  <h2 class="section-title">Projects</h2>
  <p class="section-subtitle">My Own Projects</p>
  <div class="projects">
    <div class="projects-grid">{cards}
    </div>
  </div>
</section>"""


def app_section():
    return f"""
<section id="app">
  <h2 class="section-title">My App</h2>
  <p class="section-subtitle">Download My Own App</p>
  <div class="app-container">
    <div class="app-card" id="appCard">
      <div class="app-icon"><i class="fa-solid fa-mobile-screen-button"></i></div>
      <div class="app-info">
        <h3 class="app-name">{e(APP["name"])}</h3>
        <p class="app-description">{e(APP["description"])}</p>
        <div class="app-meta">
          <span><i class="fa-solid fa-hard-drive"></i>{e(APP["size"])}</span>
          <span class="app-version">{e(APP["version"])}</span>
        </div>
        <div class="app-actions">
          <a href="{e(APP["file"])}" download class="install-button" id="installBtn">
            <i class="fa-solid fa-download"></i> Install
          </a>
          <button class="delete-button" id="deleteAppBtn" type="button">
            <i class="fa-solid fa-trash"></i> Delete
          </button>
        </div>
      </div>
    </div>
    <div class="app-empty" id="appEmpty">No app uploaded yet.</div>
  </div>
</section>"""


def contact():
    links = "".join(
        f"""
      <div class="contact-item">
        <div class="contact-label">{e(s["label"])}</div>
        <a class="{e(s["css"])}" href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">
          <i class="{e(s["icon"])}"></i> {e(s["cta"])}
        </a>
      </div>"""
        for s in SOCIAL
    )
    return f"""
<section class="contact-section" id="contact">
  <h2 class="section-title">Contact Me</h2>
  <p class="section-subtitle">Get In Touch</p>
  <div class="contact-grid">
    <div class="contact-left">
      <h3><i class="fa-regular fa-comment"></i> Text me</h3>
      <div class="contact-item">
        <div class="contact-label">Email</div>
        <div class="contact-value">{e(SITE["email"])}</div>
      </div>{links}
    </div>
    <div class="contact-right">
      <h3><i class="fa-regular fa-paper-plane"></i> Have a query for me?</h3>
      <form id="contactForm">
        <div class="form-group">
          <label>Name</label>
          <input type="text" id="name" placeholder="Your name" required>
        </div>
        <div class="form-group">
          <label>Email</label>
          <input type="email" id="email" placeholder="Your email" required>
        </div>
        <div class="form-group">
          <label>Message</label>
          <textarea id="message" placeholder="Ask me something?" required></textarea>
        </div>
        <button class="send-button" type="submit">Send ↗</button>
      </form>
    </div>
  </div>
</section>"""


def footer():
    return f"""
<footer>
  <h2>{e(SITE["name"])}</h2>
  <p>{e(SITE["footer_tagline"])}</p>
  {social_icons()}
  <div class="copyright">© {e(SITE["year"])} {e(SITE["name"])}. All Rights Reserved.</div>
</footer>"""


def navbar():
    icons = "".join(
        f'<a href="{href}" class="nav-icon"><i class="{icon}"></i></a>' for href, icon in NAV
    )
    return f"""
<nav class="navbar">
  <a href="#home" class="logo">{e(SITE["short_name"])}</a>
  {icons}
  <button class="nav-icon" id="themeButton" style="border:none;background:none;">
    <i class="fa-regular fa-moon"></i>
  </button>
</nav>"""


def build_page():
    js = JS.replace("__WA_NUMBER__", SITE["whatsapp_number"]).replace(
        "__SITE_NAME__", SITE["name"]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(SITE["name"])} | Portfolio</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<style>{CSS}</style>
</head>
<body>
{hero()}
{skills()}
{projects()}
{app_section()}
{contact()}
{footer()}
{navbar()}
<script>{js}</script>
</body>
</html>
"""


# ============================================================
# 5. BUILD + SERVE
# ============================================================


def main():
    parser = argparse.ArgumentParser(description="Build and serve the portfolio.")
    parser.add_argument("--build", action="store_true", help="only write index.html")
    parser.add_argument("--port", type=int, default=8000, help="port (default 8000)")
    args = parser.parse_args()

    folder = Path(__file__).resolve().parent
    out = folder / "index.html"
    out.write_text(build_page(), encoding="utf-8")
    print(f"Built {out}")

    if args.build:
        return

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(folder))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", args.port), handler) as server:
        url = f"http://localhost:{args.port}"
        print(f"Serving at {url}  (Ctrl+C to stop)")
        webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()