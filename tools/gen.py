#!/usr/bin/env python3
"""Generates the A4-sheet CV variants (v2-v4, v6-v9) from shared data.
v1 and v5 are hand-written and left untouched."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Backups")          # all variants
LIVE = ("v3-dark-terminal.html", os.path.join(ROOT, "index.html"))   # the chosen one, published at the root

# ------------------------------------------------------------------ DATA
NAME = "Sergio de Jesús Sánchez Robles"
ROLE = "Senior Software Engineer · Tech Lead"
TAG = "Backend &amp; Full-Stack · Game Development · AI-Assisted Engineering"

PROFILE = ("Software developer with <b><span data-years>15</span> years of experience</b> across the gaming, media, and enterprise sectors, "
           "collaborating with major global companies. As an <b>AI enthusiast</b>, I actively leverage AI-assisted tools in my "
           "daily workflow to optimize backend development and accelerate project delivery. I am a rapid learner, highly "
           "adaptable to new technology stacks. Having previously <b>led teams of up to six people</b>, I consistently deliver "
           "high-quality, scalable software solutions on time and within budget.")

STEAM = "https://store.steampowered.com/app/2493180/The_Lullaby_of_Life/"
YT_VR = "https://www.youtube.com/watch?v=dyOfO0sYyp8&amp;t=446s"
YT_REEL = "https://www.youtube.com/watch?v=PWaarVatoEU"

def ext(href, text):
    return f'<a href="{href}" target="_blank" rel="noopener noreferrer">{text}</a>'

JOBS = [
    dict(role="Senior Software Engineer / Tech Lead", co="Wizeline", period="Feb 2020 — Present", frm="2020-02", to=None, inds=["News", "Media &amp; Entertainment", "Retail", "Cybersecurity"], loc="Guadalajara, México", cur=True, pts=[
        '<b>Global News Industry:</b> Engineered new features and resolved production issues in a high-velocity environment. Leveraged AI tooling to accelerate development cycles and enhance code quality. <span class="stack">Tech: .NET, AWS, PostgreSQL, Claude Code.</span>',
        '<b>Media &amp; Entertainment Industry:</b> Directed a team of 5 engineers as Tech Lead, designing and implementing customized, scalable software solutions for internal stakeholders. <span class="stack">Tech: Java, Spring, Node.js, AWS, PostgreSQL.</span>',
        '<b>Enterprise Retail Industry:</b> Architected backend services for a complex audit system. Designed relational databases, implemented microservices, and built migration services for long-running data imports. <span class="stack">Tech: Java, Spring, MariaDB.</span>',
        '<b>Cybersecurity startup:</b> Spearheaded the full-stack development of an MVP as a contingent engineer to successfully launch the initial platform. <span class="stack">Tech: Python, React.</span>',
    ]),
    dict(role="Lead Programmer", co="1 Simple Idea", period="Jul 2019 — Feb 2020", frm="2019-07", to="2020-02", inds=["Gaming · Mobile"], loc="Guadalajara, México", cur=False, pts=[
        'Led a small programming team in the development of a mobile iOS game, taking ownership of the <b>core game architecture</b>.',
        'Architected and implemented an Inversion of Control (IoC), Dependency Injection (DI), and a robust event-driven system.',
        'Accelerated the development cycle and reduced bug rates by establishing a modular paradigm, which significantly decreased art asset integration time for art teams.',
        f'Released on <b>Apple Arcade</b>, now on Steam: {ext(STEAM, "The Lullaby of Life")}.',
    ]),
    dict(role="Senior Programmer", co="Virtually Live", period="Feb 2017 — Jan 2020", frm="2017-02", to="2020-01", inds=["Gaming · VR"], loc="Málaga, Spain", cur=False, pts=[
        'Developed <b>racing games</b> for HTC Vive, Oculus, and Gear VR platforms.',
        'Engineered a core abstraction layer for game modules, encompassing VR controllers, Social APIs, and database access, utilizing JSON for configuration management.',
        'Ported the VR title to iOS by developing core gameplay mechanics in C# and architecting the supporting backend RESTful services with Python, Django, and Go.',
        f'Contributed to the successful release of the iOS adaptation ({ext(YT_VR, "gameplay")}).',
    ]),
    dict(role="Software Engineer", co="Intel", period="Feb 2015 — Feb 2017", frm="2015-02", to="2017-02", inds=["Semiconductors"], loc="Guadalajara, México", cur=False, pts=[
        'Engineered <b>APIs in Ruby</b> to support hardware validation teams and streamline testing workflows.',
        'Created automation tools and scripts to synchronize API deployments with client environments across multiple global Intel sites.',
        'Leveraged Ruby metaprogramming to parse XML-formatted design documents and dynamically generate executable files.',
    ]),
    dict(role="3D &amp; Online Programmer", co="Gameloft", period="May 2011 — Jan 2015", frm="2011-05", to="2015-01", inds=["Gaming · Mobile"], loc="Guadalajara, México", cur=False, pts=[
        'Programmed 3D games and internal development tools using portable <b>C++, Java, and Objective-C</b> to ensure seamless cross-platform compatibility across Android and iOS.',
        'Integrated proprietary REST-based online services into multiple Android titles.',
        'Contributed to the development and release of major mobile titles, including <b>The Oregon Trail: American Settler</b> and <b>9mm</b>.',
    ]),
    dict(role="Game Developer", co="Kaxan Games", period="Aug 2009 — May 2011", frm="2009-08", to="2011-05", inds=["Gaming · Mobile &amp; Console"], loc="Guadalajara, México", cur=False, pts=[
        'Developed and published <b>over five mobile games</b> for iPhone and iPad utilizing C# and Unity3D.',
        'Contributed as an additional programmer to a released <b>Nintendo Wii</b> title.',
        f'Showcased development work in a demo reel of five released iOS games ({ext(YT_REEL, "gameplay")}).',
    ]),
]

CORE = [("C# / .NET", 5), ("Java / Spring", 5), ("Python / FastAPI", 4), ("JavaScript / Node.js / React", 4),
        ("AWS", 4), ("SQL / Postgres", 5), ("System Design", 5)]
LEVEL = {5: ("Expert", "100%"), 4: ("Advanced", "80%"), 3: ("Proficient", "60%")}
TECH = ["C#", ".NET", "Java", "Spring", "C/C++", "Python", "FastAPI", "Ruby", "JavaScript", "Node.js", "React", "AWS",
        "PostgreSQL", "Microservices", "RESTful APIs", "Unit Testing", "OOP", "Unity3D", "Git", "Full-Stack"]
AI_TEXT = "AI-assisted tools in my daily workflow to optimize backend development and accelerate project delivery."
AI_CHIPS = ["Claude Code", "opencode", "Codex"]
TITLES = [
    f'<b>The Lullaby of Life</b> — Apple Arcade &amp; {ext(STEAM, "Steam")}',
    f'<b>VR racing games</b> — HTC Vive, Oculus, Gear VR &amp; {ext(YT_VR, "iOS")}',
    '<b>The Oregon Trail: American Settler</b>, <b>9mm</b> — Gameloft',
    f'<b>5+ iOS games</b> &amp; a Nintendo Wii title — {ext(YT_REEL, "demo reel")}',
]
EDU = [("Master in Computer Science", "Universidad Autónoma de Guadalajara · Aug 2018"),
       ("Computer Science", "Universidad de Guadalajara · Dec 2010")]
STATS = [('<span data-years>15</span>', "+", "Years building software"), ("3", "", "Industries: gaming, media &amp; enterprise"), ("6", "", "Engineers led as Tech Lead")]

ICON = {
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "in": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.01M11 17v-4a2 2 0 0 1 4 0v4"/></svg>',
    "gh": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M9 19c-4.5 1.5-4.5-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/></svg>',
    "ai": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M6 6l2 2M16 16l2 2M18 6l-2 2M8 16l-2 2"/><circle cx="12" cy="12" r="3.5"/></svg>',
}
CONTACT = [
    ("pin", "Zapopan, Jalisco, México", None),
    ("phone", "+52 1 33 1799 1812", "tel:+5213317991812"),
    ("mail", "sergioj.sanchezr@gmail.com", "mailto:sergioj.sanchezr@gmail.com"),
    ("in", "linkedin.com/in/sergiojsanchez", "https://www.linkedin.com/in/sergiojsanchez/"),
    ("gh", "github.com/sergiowero", "https://github.com/sergiowero"),
]

# ------------------------------------------------------------------ BLOCKS
def contact_html():
    out = []
    for ic, text, href in CONTACT:
        inner = f'<a href="{href}"{" target=\"_blank\" rel=\"noopener noreferrer\"" if href and href.startswith("http") else ""}>{text}</a>' if href else text
        out.append(f'<div class="cline">{ICON[ic]}{inner}</div>')
    return "\n".join(out)

def core_html():
    # one markup, many looks: each version shows the bar (.sk-track), the dots (.sk-dots), the word or the percent
    out = []
    for name, lvl in CORE:
        word, pct = LEVEL[lvl]
        dots = "".join('<i class="on"></i>' if i < lvl else '<i></i>' for i in range(5))
        out.append(f'<div class="cskill" data-lvl="{lvl}"><div class="sk-top"><span class="sk-name">{name}</span>'
                   f'<span class="sk-word">{word}</span><span class="sk-pct">{pct}</span></div>'
                   f'<div class="sk-track"><div class="sk-fill" style="width:{pct}"></div></div><div class="sk-dots">{dots}</div></div>')
    return "\n".join(out)

def chips_html(items, cls="dchip"):
    return '<div class="dchips">' + "".join(f'<span class="{cls}">{s}</span>' for s in items) + '</div>'

def ai_html(with_icon=True):
    ic = ICON["ai"] if with_icon else ""
    return (f'<div class="ai"><div class="h">{ic}AI-Assisted Dev</div><p>{AI_TEXT}</p>{chips_html(AI_CHIPS)}</div>')

def titles_html():
    return "\n".join(f'<div class="award">{t}</div>' for t in TITLES)

def edu_html():
    return "\n".join(f'<div class="edu"><div class="d">{d}</div><div class="m">{m}</div></div>' for d, m in EDU)

BEST_STAT = '<div class="stat best"><div class="n">.NET · Spring · Python · Node.js</div><div class="l">Best skills</div></div>'

def stats_html():
    return '<div class="stats">' + "".join(
        f'<div class="stat"><div class="n">{n}<span class="u">{u}</span></div><div class="l">{l}</div></div>' for n, u, l in STATS) + BEST_STAT + '</div>'

def profile_html():
    return f'<p class="profile">{PROFILE}</p>'

def experience_html():
    out = ['<div class="tl">']
    for j in JOBS:
        out.append(f'<div class="job{" cur" if j["cur"] else ""}">')
        out.append(f'<div class="job-head"><div class="r">{j["role"]} · <span class="c">{j["co"]}</span></div><div class="p" data-from="{j["frm"]}"{f' data-to="{j["to"]}"' if j["to"] else ""}>{j["period"]}</div></div>')
        inds = "".join(f'<span class="ind">{i}</span>' for i in j["inds"])
        out.append(f'<div class="loc">{j["loc"]}<span class="inds">{inds}</span></div>')
        out.append('<ul class="pts">' + "".join(f'<li>{p}</li>' for p in j["pts"]) + '</ul>')
        out.append('</div>')
    out.append('</div>')
    return "\n".join(out)

FIT_JS = """<script>
/* Years of experience, computed from the year I started working */
(function(){
  var START_YEAR=2010;
  var years=new Date().getFullYear()-START_YEAR;
  document.querySelectorAll('[data-years]').forEach(function(el){el.textContent=years;});
})();
/* Job dates rendered from data-from / data-to (YYYY-MM; no data-to = present): "Feb 2020 — Present · 6 yrs 8 mos" */
(function(){
  var M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  function ym(s){var p=s.split('-');return {y:+p[0],m:+p[1]};}
  function label(d){return M[d.m-1]+' '+d.y;}
  var now=new Date(), nowS=now.getFullYear()+'-'+(now.getMonth()+1);
  document.querySelectorAll('[data-from]').forEach(function(el){
    var toAttr=el.getAttribute('data-to');
    var a=ym(el.getAttribute('data-from')), b=ym(toAttr||nowS);
    var months=(b.y-a.y)*12+(b.m-a.m)+1; // inclusive count, like LinkedIn
    var y=Math.floor(months/12), m=months%12, parts=[];
    if(y) parts.push(y+(y===1?' yr':' yrs'));
    if(m) parts.push(m+(m===1?' mo':' mos'));
    el.textContent=label(a)+' \u2014 '+(toAttr?label(b):'Present');
    var d=document.createElement('span'); d.className='dur'; d.textContent=' \u00b7 '+parts.join(' ');
    el.appendChild(d);
  });
})();
/* Fits the A4 sheet to the available width: grows on wide screens (up to 1.5x)
   and shrinks on narrow ones so there is never horizontal scroll. Not applied when printing. */
(function(){
  var sheet=document.querySelector('.sheet');
  if(!sheet) return;
  var MAX=1.5;
  function fit(){
    if(window.matchMedia&&window.matchMedia('print').matches){sheet.style.zoom='';return;}
    sheet.style.zoom='1';
    var natW=sheet.offsetWidth;
    var body=sheet.parentElement, cs=getComputedStyle(body);
    var avail=body.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
    var scale=avail/natW;
    if(scale>MAX) scale=MAX;
    sheet.style.zoom=scale;
  }
  fit();
  window.addEventListener('resize',fit);
  window.addEventListener('load',fit);
  if(window.matchMedia){
    var mq=window.matchMedia('print');
    if(mq.addEventListener) mq.addEventListener('change',fit);
    else if(mq.addListener) mq.addListener(fit);
  }
})();
</script>"""

BASE_CSS = """*{margin:0;padding:0;box-sizing:border-box;}
  html{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  @page{size:A4;margin:0;}
  a{text-decoration:none;color:inherit;}
  .sheet{width:210mm;min-height:297mm;margin:0 auto;position:relative;overflow:hidden;}
  .cline svg,.ai .h svg{width:13px;height:13px;flex:none;}
  .p .dur{font-weight:400;opacity:.85;}
  .sk-top{display:flex;justify-content:space-between;align-items:baseline;gap:6px;}
  .stat.best{flex:1.35;}
  .stat.best .n{font-size:10.5px;line-height:1.25;letter-spacing:0;}
  .inds{display:inline-flex;flex-wrap:wrap;gap:3px;margin-left:6px;vertical-align:middle;}
  .ind{display:inline-block;font-size:7.3px;line-height:1.35;padding:1px 6px;border-radius:3px;font-weight:600;white-space:nowrap;}
  .sk-pct,.sk-dots{display:none;}
  @media screen{
    body{min-height:100vh;display:flex;justify-content:center;align-items:flex-start;padding:clamp(12px,3vw,44px);}
    .sheet{flex:none;box-shadow:0 30px 80px -22px rgba(0,0,0,.6),0 10px 26px rgba(0,0,0,.35);border-radius:14px;}
  }
  /* site header, embedded as the top strip of the sheet (visual only for now) */
  .site-nav{display:flex;align-items:center;justify-content:flex-end;gap:8px;padding:7px 12mm;color:var(--nav-fg);font-family:var(--nav-font,inherit);}
  .site-nav .tabs{display:flex;gap:2px;}
  .site-nav .tab{padding:4px 7px;border-radius:6px;font-size:8.4px;font-weight:500;color:var(--nav-muted);cursor:default;user-select:none;letter-spacing:.2px;white-space:nowrap;}
  .site-nav .tab.active{background:var(--nav-active-bg);color:var(--nav-active-fg);font-weight:700;}
  .site-nav .grp{display:flex;align-items:center;gap:1px;}
  .site-nav .grp .tab{padding:4px 6px;cursor:pointer;}
  .site-nav .grp .slash{color:var(--nav-muted);font-size:8.6px;opacity:.6;padding:0 1px;}
  .site-nav .grp .tab svg{width:10px;height:10px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;vertical-align:-1.5px;margin-right:3px;}
  @media print{.sheet{zoom:1 !important;box-shadow:none !important;border-radius:0 !important;} .site-nav{display:none;}}"""

FLAG_MX = '<svg viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M8.7 5v14M15.3 5v14"/><circle cx="12" cy="12" r="1.6"/></svg>'
FLAG_US = '<svg viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 12h20M11 8.5h11M11 15.5H2M2 12v7"/><path d="M2 12h9V5"/></svg>'
NAV_HTML = """<header class="site-nav" aria-label="Site sections (visual only)">
  <nav class="tabs">
    <span class="tab">About me</span>
    <span class="tab active" aria-current="page">Resume / CV</span>
    <span class="tab">Extended History</span>
    <span class="tab">Blog</span>
  </nav>
  <div class="grp lang" aria-label="Language (visual only)"><span class="tab" data-lang="es">$FLAG_ES$ES</span><span class="slash">/</span><span class="tab active" data-lang="en">$FLAG_EN$EN</span></div>
  <div class="grp theme" aria-label="Theme"><span class="tab$DARK$" data-set-theme="dark"><svg viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>Dark</span><span class="slash">/</span><span class="tab$LIGHT$" data-set-theme="light"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>Light</span></div>
</header>"""

def page(title, fonts, css, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>{title}</title>
<meta name="description" content="Sergio de Jesús Sánchez Robles — Senior Software Engineer / Tech Lead. 15 years across gaming, media and enterprise.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
<style>
  {BASE_CSS}
{css}
</style>
</head>
<body>
{body}
{FIT_JS}
</body>
</html>
"""

def fill(tpl):
    return (tpl.replace("$CONTACT$", contact_html()).replace("$CORE$", core_html())
            .replace("$TECH$", chips_html(TECH)).replace("$AI$", ai_html()).replace("$AI_NOICON$", ai_html(False))
            .replace("$TITLES$", titles_html()).replace("$EDU$", edu_html()).replace("$STATS$", stats_html())
            .replace("$PROFILE$", profile_html()).replace("$EXP$", experience_html())
            .replace("$NAV$", NAV_HTML).replace("$NAME$", NAME).replace("$ROLE$", ROLE).replace("$TAG$", TAG))

VERSIONS = {}

# =================================================================== v2 EDITORIAL SERIF (A4)
VERSIONS["v2-editorial-serif.html"] = dict(
    nav="--nav-bg:#f2ede3;--nav-line:#dcd5c7;--nav-fg:#1c1a17;--nav-muted:#8a847a;--nav-active-bg:#b8321f;--nav-active-fg:#fff;",
    title="Sergio Sanchez CV",
    fonts="family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600",
    css="""
  :root{--paper:#faf7f1;--ink:#1c1a17;--body:#4a463f;--muted:#8a847a;--line:#dcd5c7;--accent:#b8321f;--accent-soft:#f3dcd6;}
  body{font-family:'Inter',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:var(--paper);}
  .serif{font-family:'Fraunces','Iowan Old Style',Georgia,serif;}
  .sheet{background:var(--paper);padding:12mm 13mm 8mm;display:flex;flex-direction:column;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#3b2a25 0%,#1f1613 50%,#120d0b 100%);}}

  .site-nav{margin:-12mm -13mm 7mm;padding-left:13mm;padding-right:13mm;}
  .top{display:flex;justify-content:space-between;align-items:flex-end;gap:10mm;border-bottom:1.5px solid var(--ink);padding-bottom:8px;}
  .kicker{font-size:8px;letter-spacing:2.2px;text-transform:uppercase;color:var(--accent);font-weight:600;margin-bottom:6px;}
  .name{font-family:'Fraunces',Georgia,serif;font-size:31px;font-weight:600;letter-spacing:-.8px;line-height:1;color:var(--ink);}
  .name em{font-style:italic;font-weight:400;color:var(--accent);}
  .tag{font-size:9px;color:var(--muted);margin-top:6px;}
  .contact{display:grid;gap:4px;flex:none;}
  .cline{display:flex;align-items:center;gap:6px;font-size:8.6px;color:var(--body);}
  .cline svg{stroke:var(--accent);width:11px;height:11px;}

  .stats{display:flex;margin:6px 0 8px;border-bottom:1px solid var(--line);}
  .stat{flex:1;padding:6px 10px 8px 0;border-right:1px solid var(--line);margin-right:10px;}
  .stat:last-child{border-right:0;margin-right:0;}
  .stat .n{font-family:'Fraunces',Georgia,serif;font-size:22px;font-weight:600;color:var(--ink);line-height:1;letter-spacing:-.5px;}
  .stat .n .u{color:var(--accent);}
  .stat .l{font-size:7.6px;text-transform:uppercase;letter-spacing:1.1px;color:var(--muted);margin-top:4px;font-weight:500;}

  .cols{display:flex;gap:8mm;flex:1;}
  .main{flex:1 1 auto;min-width:0;}
  .aside{flex:0 0 52mm;}
  h2.sh{font-size:8.6px;letter-spacing:2px;text-transform:uppercase;color:var(--ink);font-weight:600;margin-bottom:7px;display:flex;align-items:center;gap:8px;}
  h2.sh::after{content:"";flex:1;height:1px;background:var(--line);}
  section{margin-bottom:9px;}

  .profile{font-size:9.6px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--ink);font-weight:600;}

  .job{display:grid;grid-template-columns:1fr;padding:5px 0 3px;border-top:1px solid var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-family:'Fraunces',Georgia,serif;font-size:12px;font-weight:600;color:var(--ink);}
  .job .c{color:var(--accent);font-style:italic;font-weight:400;}
  .job .p{font-size:8.2px;color:var(--muted);font-weight:500;white-space:nowrap;flex:none;}
  .job.cur .p::after{content:"· Current";color:var(--accent);margin-left:4px;font-weight:600;}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"—";position:absolute;left:0;color:var(--accent);}
  .ind{font-size:6.8px;letter-spacing:1px;text-transform:uppercase;font-weight:600;color:var(--accent);border:1px solid var(--accent-soft);background:#fff;border-radius:2px;padding:1px 5px;}
  ul.pts li b{color:var(--ink);font-weight:600;}
  ul.pts li a{color:var(--accent);font-weight:600;}
  .stack{color:var(--muted);}

  .cskill{padding:3px 0 5px;}
  .sk-top{font-size:9.3px;color:var(--ink);}
  .sk-word{font-family:'Fraunces',Georgia,serif;font-style:italic;color:var(--accent);font-size:8.6px;}
  .sk-track{height:1px;background:var(--line);margin-top:5px;}
  .sk-fill{height:2px;margin-top:-.5px;background:var(--ink);position:relative;}
  .sk-fill::after{content:"";position:absolute;right:-2px;top:-2px;width:6px;height:6px;border-radius:50%;background:var(--accent);}
  .ai{background:var(--ink);color:var(--paper);padding:10px 11px;border-radius:3px;}
  .ai .h{font-size:8px;letter-spacing:1.6px;text-transform:uppercase;color:var(--accent);font-weight:600;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:var(--accent);}
  .ai p{font-size:8.8px;line-height:1.45;color:#d9d3c7;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:500;padding:2px 7px;border-radius:20px;border:1px solid var(--line);color:var(--ink);background:#fff;}
  .ai .dchip{background:transparent;border-color:rgba(255,255,255,.3);color:var(--paper);}
  .award{font-size:8.8px;color:var(--body);padding:3px 0;border-bottom:1px dotted var(--line);line-height:1.35;}
  .award:last-child{border-bottom:0;}
  .award b{color:var(--ink);font-weight:600;}
  .award a{color:var(--accent);}
  .edu{padding:3px 0;border-bottom:1px dotted var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-family:'Fraunces',Georgia,serif;font-size:10.5px;font-weight:600;color:var(--ink);}
  .edu .m{font-size:8.4px;color:var(--muted);}
  .foot{margin-top:auto;padding-top:6px;border-top:1px solid var(--line);font-size:7.6px;color:var(--muted);display:flex;justify-content:space-between;}
""",
    body="""<div class="sheet">
  $NAV$
  <header class="top">
    <div>
      <div class="kicker">$ROLE$ · Zapopan, México</div>
      <div class="name">Sergio de Jesús Sánchez <em>Robles</em></div>
      <div class="tag">$TAG$</div>
    </div>
    <div class="contact">$CONTACT$</div>
  </header>
  $STATS$
  <div class="cols">
    <main class="main">
      <section><h2 class="sh">Profile</h2>$PROFILE$</section>
      <section><h2 class="sh">Experience</h2>$EXP$</section>
    </main>
    <aside class="aside">
      <section>$AI$</section>
      <section><h2 class="sh">Core Skills</h2>$CORE$</section>
      <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
      <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
      <section><h2 class="sh">Education</h2>$EDU$</section>
    </aside>
  </div>
  <div class="foot"><span>$NAME$</span><span>sergiowero.github.io</span></div>
</div>""")

# =================================================================== v3 DARK TERMINAL (A4)
VERSIONS["v3-dark-terminal.html"] = dict(
    theme="dark", flags=True,
    nav="--nav-bg:#10161d;--nav-line:#1f2a35;--nav-fg:#d6dde6;--nav-muted:#7d8a99;--nav-active-bg:#3ddc84;--nav-active-fg:#06130c;--nav-font:'JetBrains Mono',Menlo,monospace;",
    title="Sergio Sanchez CV",
    extra_js="""<script>
/* Dark / light toggle from the header; the choice is remembered in localStorage */
(function(){
  var KEY='cv-theme';
  function apply(t){
    if(t==='light') document.documentElement.setAttribute('data-theme','light'); else document.documentElement.removeAttribute('data-theme');
    document.querySelectorAll('[data-set-theme]').forEach(function(el){el.classList.toggle('active',el.getAttribute('data-set-theme')===(t==='light'?'light':'dark'));});
  }
  var saved=null; try{saved=localStorage.getItem(KEY);}catch(e){}
  apply(saved||'dark');
  document.querySelectorAll('[data-set-theme]').forEach(function(el){
    el.addEventListener('click',function(){var t=el.getAttribute('data-set-theme');apply(t);try{localStorage.setItem(KEY,t);}catch(e){}});
  });
})();
</script>
<script>
/* ASCII skill bars sized to fill the column: [████████░░] with as many cells as fit */
(function(){
  function draw(){
    document.querySelectorAll('.sk-dots').forEach(function(el){
      var lvl=+el.parentElement.getAttribute('data-lvl')||0;
      var probe=document.createElement('span'); probe.textContent='██████████'; probe.style.cssText='position:absolute;visibility:hidden;white-space:pre;font:inherit;';
      el.appendChild(probe); var cw=probe.getBoundingClientRect().width/10; probe.remove();
      var w=el.getBoundingClientRect().width;   // same (zoomed) units as the probe
      if(!cw||!w) return;
      var n=Math.min(80,Math.floor(w/cw)-2), f=Math.round(n*lvl/5);
      if(n<3) return;
      el.className='sk-dots ascii';
      el.innerHTML='<span class="b">[</span><span class="f">'+'█'.repeat(f)+'</span><span class="e">'+'░'.repeat(n-f)+'</span><span class="b">]</span>';
    });
  }
  draw();
  window.addEventListener('load',draw);
  // the web font can arrive after `load`; redraw whenever a font finishes loading so the cell count matches its metrics
  if(document.fonts){ document.fonts.ready.then(draw); document.fonts.addEventListener('loadingdone',draw); }
  setTimeout(draw,1500); setTimeout(draw,4000);
})();
</script>
<script>
/* Typewriter effect on the name (skipped when the user prefers reduced motion or when printing) */
(function(){
  var el=document.getElementById('typed'); if(!el) return;
  var full=el.textContent;
  if(window.matchMedia&&(window.matchMedia('(prefers-reduced-motion: reduce)').matches||window.matchMedia('print').matches)) return;
  el.textContent=''; var i=0;
  (function tick(){ if(i<=full.length){ el.textContent=full.slice(0,i++); setTimeout(tick,i<8?90:45);} })();
})();
</script>""",
    fonts="family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700",
    css="""
  :root{--bg:#0b0f14;--panel:#141b23;--line:#1f2a35;--text:#d6dde6;--muted:#7d8a99;--green:#3ddc84;--cyan:#4cc9f0;--amber:#ffb454;--pink:#ff6b9d;--fg:#fff;--body-text:var(--body-text);--empty:var(--empty);}
  /* light mode (toggled from the header) */
  :root[data-theme="light"]{--bg:#f6f8fa;--panel:#fff;--line:#d0d7de;--text:#1f2328;--muted:#6e7781;--green:#1a7f37;--cyan:#0969da;--amber:#9a6700;--pink:#bf3989;--fg:#0b1220;--body-text:#3d444d;--empty:#d8dee4;
    --nav-fg:#1f2328;--nav-muted:#6e7781;--nav-active-bg:#1a7f37;--nav-active-fg:#fff;}
  @media screen{:root[data-theme="light"] body{background:radial-gradient(900px 500px at 50% -10%,#e6ecf2 0%,#cfd8e1 55%,#bcc7d2 100%);}}
  body{font-family:'Inter',system-ui,sans-serif;color:var(--text);font-size:10px;line-height:1.5;background:var(--bg);}
  .mono{font-family:'JetBrains Mono',Menlo,Consolas,monospace;}
  .sheet{background:var(--bg);padding:11mm 12mm 4mm;display:flex;flex-direction:column;
    background-image:radial-gradient(500px 260px at 90% -5%,rgba(76,201,240,.10),transparent 60%),radial-gradient(420px 220px at 0% 8%,rgba(61,220,132,.09),transparent 60%);}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#0f1f1a 0%,#070a0d 55%,#000 100%);} .sheet{border:1px solid var(--line);}}

  .site-nav{margin:-11mm -12mm 6mm;}
  .prompt{font-size:8.6px;color:var(--muted);}
  .prompt .g{color:var(--green);} .prompt .c{color:var(--cyan);} .prompt .f{color:var(--amber);}
  .name{font-size:29px;font-weight:700;letter-spacing:-1px;line-height:1;color:var(--fg);margin-top:5px;}
  .name .cur{display:inline-block;width:.45em;height:.9em;background:var(--green);vertical-align:-.08em;margin-left:3px;animation:blink 1s steps(1) infinite;}
  @keyframes blink{50%{opacity:0;}}
  @media print{.name .cur{animation:none;}}
  .sub{font-size:9px;color:var(--muted);margin-top:5px;}
  .sub .hl{color:var(--amber);}
  .top{display:flex;justify-content:space-between;align-items:flex-end;gap:8mm;}
  .contact{display:grid;gap:3px;flex:none;}
  .cline{display:flex;align-items:center;gap:6px;font-size:8.4px;color:var(--muted);}
  .cline a{color:var(--text);}
  .cline svg{stroke:var(--green);width:11px;height:11px;}

  .stats{display:flex;gap:6px;margin:5px 0 5px;}
  .stat{flex:1;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:5px 8px;}
  .stat .n{font-family:'JetBrains Mono',monospace;font-size:18px;font-weight:700;color:var(--fg);line-height:1;}
  .stat .n .u{color:var(--green);}
  .stat .l{font-size:7.8px;color:var(--muted);margin-top:3px;}

  .cols{display:flex;gap:7mm;flex:1;}
  .main{flex:1 1 auto;min-width:0;}
  .aside{flex:0 0 54mm;}
  h2.sh{font-family:'JetBrains Mono',monospace;font-size:8.6px;color:var(--muted);font-weight:500;margin-bottom:6px;}
  h2.sh::before{content:"➜ ~ ";color:var(--green);}
  h2.sh::after{content:"";}
  section{margin-bottom:8px;}

  .profile{font-size:9.5px;line-height:1.5;color:var(--body-text);}
  .profile b{color:var(--fg);font-weight:600;}

  .job{padding:6px 0 4px;border-top:1px dashed var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:600;color:var(--fg);}
  .job .c{color:var(--cyan);}
  .job .p{font-family:'JetBrains Mono',monospace;font-size:7.8px;color:var(--muted);white-space:nowrap;flex:none;}
  .job.cur .p{color:var(--green);}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:12px;margin-bottom:2.5px;line-height:1.35;font-size:9.1px;color:var(--body-text);}
  .ind{font-family:'JetBrains Mono',monospace;font-size:7.4px;font-weight:700;color:var(--cyan);background:rgba(76,201,240,.12);border:1px solid rgba(76,201,240,.45);padding:1px 6px;border-radius:4px;}
  .ind::before{content:"#";color:rgba(76,201,240,.6);margin-right:1px;}
  ul.pts li::before{content:">";position:absolute;left:0;color:var(--green);font-family:'JetBrains Mono',monospace;font-weight:700;}
  ul.pts li b{color:var(--fg);font-weight:600;}
  ul.pts li a{color:var(--cyan);}
  .stack{color:var(--muted);}

  .cskill{padding:2px 0 3px;}
  .sk-top{font-size:9px;color:var(--text);font-weight:500;}
  .sk-word,.sk-track{display:none;}
  .sk-pct{display:inline;font-family:'JetBrains Mono',monospace;font-size:8.4px;color:var(--green);}
  .sk-dots{display:block;font-family:'JetBrains Mono',monospace;font-size:8.6px;line-height:1.25;margin-top:1px;white-space:nowrap;overflow:hidden;}
  .sk-dots::before{content:"[";color:var(--muted);} .sk-dots::after{content:"]";color:var(--muted);}
  .sk-dots i::before{content:"░░";color:var(--empty);} .sk-dots i.on::before{content:"██";color:var(--green);}
  .sk-dots.ascii::before,.sk-dots.ascii::after{content:none;}
  .sk-dots .b{color:var(--muted);} .sk-dots .f{color:var(--green);} .sk-dots .e{color:var(--empty);}
  .ai{background:linear-gradient(160deg,rgba(61,220,132,.10),rgba(76,201,240,.07));border:1px solid rgba(61,220,132,.35);border-radius:9px;padding:9px 10px;}
  .ai .h{font-family:'JetBrains Mono',monospace;font-size:8.4px;color:var(--green);margin-bottom:4px;display:flex;align-items:center;gap:6px;}
  .ai .h::before{content:"// ";color:var(--muted);}
  .ai .h svg{display:none;}
  .ai p{font-size:8.8px;color:var(--body-text);line-height:1.45;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-family:'JetBrains Mono',monospace;font-size:7.6px;padding:2px 6px;border-radius:4px;background:var(--panel);border:1px solid var(--line);color:var(--text);}
  .ai .dchip{border-color:rgba(61,220,132,.4);color:var(--green);background:transparent;}
  .award{font-size:8.7px;color:var(--body-text);padding:2.5px 0;border-bottom:1px dashed var(--line);line-height:1.35;}
  .award:last-child{border-bottom:0;}
  .award b{color:var(--fg);font-weight:600;}
  .award a{color:var(--cyan);}
  .edu{padding:3px 0;border-bottom:1px dashed var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.5px;font-weight:600;color:var(--fg);}
  .edu .m{font-size:8.2px;color:var(--muted);}
  .foot{margin-top:auto;padding-top:5px;border-top:1px solid var(--line);font-family:'JetBrains Mono',monospace;font-size:7.6px;color:var(--muted);display:flex;justify-content:space-between;}
  .foot .g{color:var(--green);}
""",
    body="""<div class="sheet">
  $NAV$
  <header class="top">
    <div>
      <div class="prompt mono"><span class="g">sergio</span>@<span class="c">sergiowero.github.io</span>:~$ cat <span class="f">cv.md</span></div>
      <div class="name"><span id="typed">$NAME$</span><span class="cur"></span></div>
      <div class="sub mono">Senior Software Engineer <span class="hl">/</span> Tech Lead <span class="hl">/</span> Backend &amp; Full-Stack <span class="hl">/</span> Game Dev <span class="hl">/</span> AI-Assisted</div>
    </div>
    <div class="contact">$CONTACT$</div>
  </header>
  $STATS$
  <div class="cols">
    <main class="main">
      <section><h2 class="sh">cat profile.md</h2>$PROFILE$</section>
      <section><h2 class="sh">cat experience.log</h2>$EXP$</section>
    </main>
    <aside class="aside">
      <section>$AI$</section>
      <section><h2 class="sh">ls core-skills/</h2>$CORE$</section>
      <section><h2 class="sh">ls tech/</h2>$TECH$</section>
      <section><h2 class="sh">cat shipped.txt</h2>$TITLES$</section>
      <section><h2 class="sh">cat education.txt</h2>$EDU$</section>
    </aside>
  </div>
  <div class="foot"><span><span class="g">➜</span> exit 0 · $NAME$</span><span>sergiowero.github.io</span></div>
</div>""")

# =================================================================== v4 BENTO GRID (A4)
VERSIONS["v4-bento-grid.html"] = dict(
    nav="--nav-bg:#fff;--nav-line:#e6e8ef;--nav-fg:#0f1222;--nav-muted:#7c8196;--nav-active-bg:#2f5bff;--nav-active-fg:#fff;",
    title="Sergio Sanchez CV",
    fonts="family=Plus+Jakarta+Sans:wght@400;500;600;700;800",
    css="""
  :root{--bg:#f3f4f8;--card:#fff;--ink:#0f1222;--body:#3f4458;--muted:#7c8196;--line:#e6e8ef;--blue:#2f5bff;--blue-soft:#e8edff;--orange:#ff7a1a;--mint:#12b886;--mint-soft:#e3f8f0;--violet:#7c4dff;--violet-soft:#efe9ff;}
  body{font-family:'Plus Jakarta Sans',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:var(--bg);}
  .sheet{background:var(--bg);padding:7mm;display:grid;grid-template-columns:1fr 54mm;grid-auto-rows:min-content;gap:6px;align-content:start;
    background-image:radial-gradient(500px 300px at 5% -5%,rgba(47,91,255,.10),transparent 60%),radial-gradient(400px 240px at 100% 0%,rgba(255,122,26,.10),transparent 60%);}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#2a3a8a 0%,#151a3a 50%,#0b0d1e 100%);}}
  .site-nav{grid-column:1/-1;margin:-7mm -7mm 0;padding-left:7mm;padding-right:7mm;}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:9px 11px;}
  .span2{grid-column:1/-1;}
  .stack-col{display:grid;gap:6px;align-content:start;}
  h2.sh{font-size:7.8px;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);font-weight:700;margin-bottom:6px;display:flex;align-items:center;gap:6px;}
  h2.sh::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--blue);}
  .c-or h2.sh::before{background:var(--orange);} .c-mint h2.sh::before{background:var(--mint);} .c-vio h2.sh::before{background:var(--violet);}

  .hero{background:linear-gradient(135deg,#101635 0%,#1a2352 60%,#2f5bff 140%);color:#fff;border:0;position:relative;overflow:hidden;display:flex;justify-content:space-between;gap:8mm;align-items:flex-end;padding:12px 14px;}
  .hero::after{content:"";position:absolute;right:-60px;top:-60px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(255,122,26,.55),transparent 65%);}
  .hero>*{position:relative;z-index:1;}
  .mono{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,var(--orange),#ffb066);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;color:#fff;margin-bottom:8px;}
  .name{font-size:26px;font-weight:800;letter-spacing:-.8px;line-height:1.02;}
  .role{font-size:9.5px;color:#c9d2ff;margin-top:5px;font-weight:500;}
  .role b{color:#ffb066;font-weight:700;}
  .contact{display:grid;gap:3px;flex:none;}
  .cline{display:flex;align-items:center;gap:6px;font-size:8.2px;color:#c9d2ff;}
  .cline svg{stroke:#ffb066;width:11px;height:11px;}

  .stats{display:grid;grid-template-columns:1fr 1fr 1fr 1.3fr;gap:6px;grid-column:1/-1;}
  .stat{border-radius:12px;padding:8px 11px;display:flex;align-items:baseline;gap:8px;}
  .stat:nth-child(1){background:var(--blue-soft);} .stat:nth-child(1) .n{color:var(--blue);}
  .stat:nth-child(2){background:var(--mint-soft);} .stat:nth-child(2) .n{color:var(--mint);}
  .stat:nth-child(3){background:var(--violet-soft);} .stat:nth-child(3) .n{color:var(--violet);}
  .stat.best{background:#fff0e4;flex-direction:column;align-items:flex-start;gap:2px;} .stat.best .n{color:var(--orange);}
  .stat .n{font-size:20px;font-weight:800;letter-spacing:-1px;line-height:1;}
  .stat .n .u{color:var(--orange);}
  .stat .l{font-size:8px;color:var(--muted);font-weight:600;line-height:1.2;}

  .profile{font-size:9.4px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--ink);font-weight:700;}

  .job{padding:4px 0 3px;border-top:1px solid var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:10.8px;font-weight:700;color:var(--ink);letter-spacing:-.1px;}
  .job .c{color:var(--blue);}
  .job .p{font-size:7.8px;color:var(--muted);font-weight:700;white-space:nowrap;flex:none;background:var(--bg);padding:1px 6px;border-radius:5px;}
  .job.cur .p{background:var(--mint-soft);color:var(--mint);}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9px;}
  .ind{border-radius:20px;background:var(--blue-soft);color:var(--blue);}
  .ind:nth-child(4n+2){background:var(--mint-soft);color:var(--mint);} .ind:nth-child(4n+3){background:var(--violet-soft);color:var(--violet);} .ind:nth-child(4n){background:#fff0e4;color:var(--orange);}
  ul.pts li::before{content:"";position:absolute;left:0;top:5.5px;width:4px;height:4px;border-radius:1px;background:var(--orange);transform:rotate(45deg);}
  ul.pts li b{color:var(--ink);font-weight:700;}
  ul.pts li a{color:var(--blue);font-weight:600;}
  .stack{color:var(--muted);}

  .ai{background:linear-gradient(135deg,var(--orange) 0%,#ff9a4a 100%);color:#fff;border-radius:12px;padding:9px 11px;}
  .ai .h{font-size:7.8px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;color:rgba(255,255,255,.9);margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:#fff;}
  .ai p{font-size:8.8px;line-height:1.45;font-weight:500;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:600;padding:2px 7px;border-radius:20px;background:var(--bg);color:var(--ink);border:1px solid var(--line);}
  .ai .dchip{background:rgba(255,255,255,.18);border-color:rgba(255,255,255,.35);color:#fff;}
  .cskill{padding:2.5px 0 4px;}
  .sk-top{align-items:center;font-size:9.2px;font-weight:600;color:var(--ink);}
  .sk-word{display:none;}
  .sk-pct{display:inline;font-size:7.4px;font-weight:700;color:var(--blue);background:var(--blue-soft);padding:1px 6px;border-radius:20px;}
  .sk-track{height:6px;border-radius:6px;background:var(--bg);margin-top:3px;overflow:hidden;}
  .sk-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--blue),var(--violet));}
  .award{font-size:8.6px;color:var(--body);background:var(--bg);border-radius:8px;padding:5px 8px;margin-bottom:4px;line-height:1.35;}
  .award:last-child{margin-bottom:0;}
  .award b{color:var(--ink);font-weight:700;}
  .award a{color:var(--blue);font-weight:600;}
  .edu{padding:3px 0;border-bottom:1px solid var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.4px;font-weight:700;color:var(--ink);}
  .edu .m{font-size:8.2px;color:var(--muted);}
""",
    body="""<div class="sheet">
  $NAV$
  <header class="card hero span2">
    <div>
      <div class="mono">SS</div>
      <div class="name">$NAME$</div>
      <div class="role">$ROLE$ · <b>AI-Assisted Engineering</b> · Zapopan, México</div>
    </div>
    <div class="contact">$CONTACT$</div>
  </header>
  $STATS$
  <main class="stack-col">
    <section class="card"><h2 class="sh">About</h2>$PROFILE$</section>
    <section class="card"><h2 class="sh">Experience</h2>$EXP$</section>
  </main>
  <aside class="stack-col">
    <section class="ai"><div class="h">AI-Assisted Dev</div><p>$AI_TEXT$</p>$AI_CHIPS$</section>
    <section class="card"><h2 class="sh">Core Skills</h2>$CORE$</section>
    <section class="card c-vio"><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
    <section class="card c-or"><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
    <section class="card c-mint"><h2 class="sh">Education</h2>$EDU$</section>
  </aside>
</div>""")

# =================================================================== v6 SPLIT PANEL (A4, sidebar right)
VERSIONS["v6-split-panel.html"] = dict(
    nav="--nav-bg:transparent;--nav-line:transparent;--nav-fg:#161616;--nav-muted:#8a8a85;--nav-active-bg:#c8f135;--nav-active-fg:#111;",
    title="Sergio Sanchez CV",
    fonts="family=Space+Grotesk:wght@400;500;600;700",
    css="""
  :root{--char:#151515;--paper:#f6f5f0;--ink:#161616;--body:#444;--muted:#8a8a85;--line:#e2e0d8;--lime:#c8f135;--lime-dark:#6f8c00;--on-dark:#f2f2ee;--on-dark-mute:#9c9c95;}
  body{font-family:'Space Grotesk',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:var(--paper);}
  .sheet{background:var(--paper);display:flex;flex-direction:column;}
  .cols{display:flex;flex:1;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#2a2f14 0%,#141510 50%,#0a0a08 100%);}}
  .main{flex:1 1 auto;min-width:0;padding:7mm 9mm 6mm 12mm;}
  .panel{flex:0 0 64mm;background:var(--char);color:var(--on-dark);padding:7mm 8mm 6mm;position:relative;overflow:hidden;}
  .panel::before{content:"";position:absolute;left:-90px;bottom:-90px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(200,241,53,.22),transparent 65%);pointer-events:none;}
  .panel>*{position:relative;z-index:1;}

  .site-nav{padding:0;margin:0 0 4mm;}
  .badge{display:inline-flex;align-items:center;gap:6px;font-size:8px;letter-spacing:1.6px;text-transform:uppercase;color:var(--lime-dark);font-weight:600;}
  .badge i{width:7px;height:7px;border-radius:50%;background:var(--lime);box-shadow:0 0 0 3px rgba(200,241,53,.3);}
  .name{font-size:36px;font-weight:700;letter-spacing:-1.8px;line-height:.95;color:var(--ink);margin-top:8px;}
  .name span{color:var(--lime-dark);}
  .tag{font-size:9px;color:var(--muted);margin-top:6px;}

  .stats{display:flex;gap:7px;margin:8px 0 8px;}
  .stat{flex:1;background:#fff;border:1px solid var(--line);border-radius:10px;padding:6px 10px;}
  .stat .n{font-size:19px;font-weight:700;letter-spacing:-1px;line-height:1;color:var(--ink);}
  .stat .n .u{color:var(--lime-dark);}
  .stat .l{font-size:7.8px;color:var(--muted);margin-top:3px;}

  h2.sh{font-size:8.4px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);font-weight:600;margin-bottom:7px;display:flex;align-items:center;gap:7px;}
  h2.sh::before{content:"";width:7px;height:7px;background:var(--lime);border-radius:2px;}
  .panel h2.sh{color:var(--on-dark-mute);}
  section{margin-bottom:9px;}
  .panel section{margin-bottom:12px;}

  .profile{font-size:10px;line-height:1.5;color:var(--ink);font-weight:500;}
  .profile b{font-weight:600;background:linear-gradient(transparent 62%,var(--lime) 62%);}

  .job{padding:4px 0 3px;border-top:1px dashed var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:600;color:var(--ink);letter-spacing:-.2px;}
  .job .c{color:var(--lime-dark);}
  .job .p{font-size:8px;color:var(--muted);font-weight:500;white-space:nowrap;flex:none;}
  .job.cur .p{background:var(--lime);color:#111;padding:1px 6px;border-radius:3px;font-weight:600;}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"";position:absolute;left:0;top:5.5px;width:5px;height:5px;background:var(--lime);border-radius:1px;}
  .ind{border:1px solid var(--ink);color:var(--ink);border-radius:999px;background:transparent;font-weight:500;}
  ul.pts li b{color:var(--ink);font-weight:600;}
  ul.pts li a{color:var(--lime-dark);font-weight:600;}
  .stack{color:var(--muted);}

  .cline{display:flex;align-items:center;gap:7px;font-size:8.6px;color:var(--on-dark-mute);margin-bottom:5px;}
  .cline a{color:var(--on-dark);}
  .cline svg{stroke:var(--lime);}
  .cskill{padding:3px 0;display:flex;align-items:center;justify-content:space-between;gap:8px;}
  .sk-top{font-size:9.4px;color:#fff;font-weight:500;}
  .sk-word,.sk-track{display:none;}
  .sk-dots{display:flex;gap:3px;flex:none;}
  .sk-dots i{width:8px;height:8px;border:1px solid rgba(200,241,53,.45);border-radius:1px;}
  .sk-dots i.on{background:var(--lime);border-color:var(--lime);}
  .ai{border:1px solid rgba(200,241,53,.4);border-radius:9px;padding:9px 10px;background:rgba(200,241,53,.06);}
  .ai .h{font-size:8px;letter-spacing:1.6px;text-transform:uppercase;color:var(--lime);font-weight:600;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:var(--lime);}
  .ai p{font-size:8.6px;color:var(--on-dark-mute);line-height:1.45;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.6px;font-weight:500;padding:2px 7px;border-radius:20px;border:1px solid rgba(255,255,255,.2);color:var(--on-dark);}
  .ai .dchip{border-color:rgba(200,241,53,.5);color:var(--lime);}
  .award{font-size:8.6px;color:var(--on-dark-mute);padding:2.5px 0;line-height:1.35;border-bottom:1px dotted rgba(255,255,255,.14);}
  .award:last-child{border-bottom:0;}
  .award b{color:#fff;font-weight:600;}
  .award a{color:var(--lime);}
  .edu{padding:3px 0;border-bottom:1px dotted rgba(255,255,255,.14);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.4px;font-weight:600;color:#fff;}
  .edu .m{font-size:8.2px;color:var(--on-dark-mute);}
""",
    body="""<div class="sheet">
  <div class="cols">
  <main class="main">
    $NAV$
    <div class="badge"><i></i>$ROLE$</div>
    <div class="name">Sergio de Jesús<br>Sánchez Robles<span>.</span></div>
    <div class="tag">$TAG$ · Zapopan, México</div>
    $STATS$
    <section><h2 class="sh">About</h2>$PROFILE$</section>
    <section><h2 class="sh">Experience</h2>$EXP$</section>
  </main>
  <aside class="panel">
    <section><h2 class="sh">Contact</h2>$CONTACT$</section>
    <section>$AI$</section>
    <section><h2 class="sh">Core Skills</h2>$CORE$</section>
    <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
    <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
    <section><h2 class="sh">Education</h2>$EDU$</section>
  </aside>
  </div>
</div>""")

# =================================================================== v7 SWISS BLACK / YELLOW (A4, new)
VERSIONS["v7-swiss-yellow.html"] = dict(
    nav="--nav-bg:#fff;--nav-line:#111;--nav-fg:#111;--nav-muted:#7a7a7a;--nav-active-bg:#ffd500;--nav-active-fg:#111;",
    title="Sergio Sanchez CV",
    fonts="family=Archivo:wght@400;500;600;700;800;900",
    css="""
  :root{--ink:#111;--body:#3a3a3a;--muted:#7a7a7a;--line:#e3e3e3;--rail:#f4f4f4;--yellow:#ffd500;}
  body{font-family:'Archivo',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:#fff;}
  .sheet{background:#fff;display:flex;flex-direction:column;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#3a3a3a 0%,#1a1a1a 50%,#0a0a0a 100%);}}

  .head{padding:7mm 12mm 0;}
  .head .in{display:flex;justify-content:space-between;align-items:flex-end;gap:8mm;padding-bottom:9px;border-bottom:4px solid var(--ink);}
  .kicker{display:inline-block;background:var(--yellow);color:var(--ink);font-size:8px;font-weight:800;letter-spacing:1.8px;text-transform:uppercase;padding:2px 7px;margin-bottom:8px;}
  .name{font-size:34px;font-weight:900;letter-spacing:-1.6px;line-height:.95;color:var(--ink);text-transform:uppercase;}
  .tag{font-size:9px;color:var(--muted);margin-top:6px;font-weight:500;}
  .contact{display:grid;gap:3px;flex:none;text-align:right;}
  .cline{display:flex;align-items:center;justify-content:flex-end;gap:6px;font-size:8.4px;color:var(--ink);font-weight:500;}
  .cline svg{stroke:var(--ink);width:11px;height:11px;order:2;}

  .stats{display:flex;background:var(--ink);color:#fff;margin:0 12mm;}
  .stat{flex:1;padding:7px 12px;border-right:1px solid rgba(255,255,255,.15);display:flex;align-items:baseline;gap:8px;}
  .stat:last-child{border-right:0;}
  .stat .n{font-size:20px;font-weight:900;letter-spacing:-1px;line-height:1;}
  .stat.best{flex-direction:column;align-items:flex-start;gap:2px;} .stat.best .n{color:var(--yellow);}
  .stat .n .u{color:var(--yellow);}
  .stat .l{font-size:7.6px;text-transform:uppercase;letter-spacing:1px;color:#bdbdbd;font-weight:600;line-height:1.2;}

  .cols{display:flex;flex:1;margin-top:7mm;}
  .rail{flex:0 0 58mm;background:var(--rail);padding:7mm 7mm 8mm 12mm;}
  .main{flex:1 1 auto;min-width:0;padding:0 12mm 8mm 8mm;}
  h2.sh{font-size:8.4px;letter-spacing:2px;text-transform:uppercase;color:var(--ink);font-weight:800;margin-bottom:6px;padding-bottom:3px;border-bottom:2px solid var(--ink);}
  section{margin-bottom:8px;}

  .profile{font-size:9.6px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--ink);font-weight:700;background:linear-gradient(transparent 60%,var(--yellow) 60%);}

  .job{padding:4px 0 3px;border-top:1px solid var(--line);}
  .job:first-child{border-top:0;padding-top:0;}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:800;color:var(--ink);letter-spacing:-.2px;}
  .job .c{font-weight:600;color:var(--ink);background:linear-gradient(transparent 60%,var(--yellow) 60%);}
  .job .p{font-size:8px;color:var(--muted);font-weight:700;white-space:nowrap;flex:none;letter-spacing:.3px;}
  .job.cur .p{color:var(--ink);}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"";position:absolute;left:0;top:6px;width:5px;height:2px;background:var(--ink);}
  .ind{background:var(--yellow);color:var(--ink);border-radius:0;text-transform:uppercase;letter-spacing:.6px;font-size:6.8px;font-weight:800;}
  ul.pts li b{color:var(--ink);font-weight:700;}
  ul.pts li a{color:var(--ink);font-weight:700;text-decoration:underline;text-decoration-color:var(--yellow);text-decoration-thickness:2px;}
  .stack{color:var(--muted);}

  .cskill{padding:1.5px 0 2.5px;}
  .sk-top{font-size:8.6px;font-weight:800;color:var(--ink);text-transform:uppercase;letter-spacing:.3px;line-height:1.3;}
  .sk-word{font-weight:500;text-transform:none;letter-spacing:0;color:var(--muted);font-size:8.2px;}
  .sk-track{height:5px;background:#e3e3e3;margin-top:2px;}
  .sk-fill{height:100%;background:var(--ink);position:relative;}
  .sk-fill::after{content:"";position:absolute;right:0;top:0;width:6px;height:100%;background:var(--yellow);}
  .ai{background:var(--ink);color:#fff;padding:10px 11px;}
  .ai .h{font-size:8px;letter-spacing:1.8px;text-transform:uppercase;color:var(--yellow);font-weight:800;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:var(--yellow);}
  .ai p{font-size:8.8px;line-height:1.45;color:#cfcfcf;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:700;padding:2px 7px;border:1.5px solid var(--ink);color:var(--ink);background:#fff;}
  .ai .dchip{background:var(--yellow);border-color:var(--yellow);color:var(--ink);}
  .award{font-size:8.7px;color:var(--body);padding:2.5px 0;border-bottom:1px solid var(--line);line-height:1.35;}
  .award:last-child{border-bottom:0;}
  .award b{color:var(--ink);font-weight:700;}
  .award a{color:var(--ink);font-weight:700;text-decoration:underline;text-decoration-color:var(--yellow);text-decoration-thickness:2px;}
  .edu{padding:3px 0;border-bottom:1px solid var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.5px;font-weight:800;color:var(--ink);}
  .edu .m{font-size:8.2px;color:var(--muted);}
""",
    body="""<div class="sheet">
  $NAV$
  <header class="head">
    <div class="in">
      <div>
        <div class="kicker">$ROLE$</div>
        <div class="name">Sergio de Jesús<br>Sánchez Robles</div>
        <div class="tag">$TAG$ · Zapopan, México</div>
      </div>
      <div class="contact">$CONTACT$</div>
    </div>
  </header>
  $STATS$
  <div class="cols">
    <aside class="rail">
      <section>$AI$</section>
      <section><h2 class="sh">Core Skills</h2>$CORE$</section>
      <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
      <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
      <section><h2 class="sh">Education</h2>$EDU$</section>
    </aside>
    <main class="main">
      <section><h2 class="sh">Profile</h2>$PROFILE$</section>
      <section><h2 class="sh">Experience</h2>$EXP$</section>
    </main>
  </div>
</div>""")

# =================================================================== v8 CORPORATE NAVY / EMERALD (A4, new)
VERSIONS["v8-navy-emerald.html"] = dict(
    nav="--nav-bg:transparent;--nav-line:transparent;--nav-fg:#0b2545;--nav-muted:#7a8595;--nav-active-bg:#13a97a;--nav-active-fg:#fff;",
    title="Sergio Sanchez CV",
    fonts="family=IBM+Plex+Sans:wght@400;500;600;700",
    css="""
  :root{--navy:#0b2545;--navy-2:#13315c;--ink:#0b2545;--body:#3b4656;--muted:#7a8595;--line:#dfe5ee;--side:#eef2f7;--em:#13a97a;--em-soft:#dff5ec;}
  body{font-family:'IBM Plex Sans',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:#fff;}
  .sheet{background:#fff;display:flex;flex-direction:column;}
  .cols{display:flex;flex:1;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#1b4f8a 0%,#0b2545 50%,#061426 100%);}}
  .side{flex:0 0 60mm;background:var(--side);padding:7mm 7mm 8mm 10mm;border-right:1px solid var(--line);}
  .main{flex:1 1 auto;min-width:0;padding:7mm 11mm 8mm 9mm;}

  .mono{width:40px;height:40px;border-radius:10px;background:var(--navy);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;margin-bottom:12px;position:relative;}
  .mono::after{content:"";position:absolute;right:-4px;bottom:-4px;width:12px;height:12px;border-radius:50%;background:var(--em);border:2px solid var(--side);}
  h2.sh{font-size:8.4px;letter-spacing:1.8px;text-transform:uppercase;color:var(--navy);font-weight:700;margin-bottom:7px;display:flex;align-items:center;gap:7px;}
  h2.sh::before{content:"";width:12px;height:3px;background:var(--em);border-radius:2px;}
  section{margin-bottom:10px;}

  .cline{display:flex;align-items:center;gap:7px;font-size:8.6px;color:var(--body);margin-bottom:5px;}
  .cline svg{stroke:var(--em);}
  .cskill{padding:3px 0;border-bottom:1px solid var(--line);display:flex;align-items:flex-end;justify-content:space-between;gap:8px;}
  .cskill:last-child{border-bottom:0;}
  .sk-top{font-size:9.3px;color:var(--ink);font-weight:500;}
  .sk-word,.sk-track{display:none;}
  .sk-dots{display:flex;gap:2px;align-items:flex-end;height:11px;flex:none;}
  .sk-dots i{width:5px;background:var(--line);border-radius:1px;}
  .sk-dots i:nth-child(1){height:3px;} .sk-dots i:nth-child(2){height:5px;} .sk-dots i:nth-child(3){height:7px;} .sk-dots i:nth-child(4){height:9px;} .sk-dots i:nth-child(5){height:11px;}
  .sk-dots i.on{background:var(--em);}
  .ai{background:var(--navy);color:#fff;border-radius:9px;padding:10px 11px;}
  .ai .h{font-size:8px;letter-spacing:1.5px;text-transform:uppercase;color:#8fe3c5;font-weight:700;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:#8fe3c5;}
  .ai p{font-size:8.8px;line-height:1.45;color:#c8d3e3;margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:600;padding:2px 7px;border-radius:5px;background:#fff;border:1px solid var(--line);color:var(--navy);}
  .ai .dchip{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.25);color:#fff;}
  .award{font-size:8.7px;color:var(--body);padding:2.5px 0 2.5px 10px;position:relative;line-height:1.35;}
  .award::before{content:"";position:absolute;left:0;top:7px;width:4px;height:4px;border-radius:50%;background:var(--em);}
  .award b{color:var(--ink);font-weight:600;}
  .award a{color:var(--em);font-weight:600;}
  .edu{padding:3px 0;border-bottom:1px solid var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.5px;font-weight:600;color:var(--ink);}
  .edu .m{font-size:8.2px;color:var(--muted);}

  .site-nav{padding:0;margin:0 0 4mm;}
  .kicker{font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--em);font-weight:700;margin-bottom:6px;}
  .name{font-size:29px;font-weight:700;letter-spacing:-.8px;line-height:1;color:var(--navy);}
  .role{font-size:12px;font-weight:600;color:var(--navy-2);margin-top:6px;}
  .tag{font-size:9px;color:var(--muted);margin-top:3px;}
  .stats{display:flex;gap:8px;margin:11px 0 11px;}
  .stat{flex:1;border:1px solid var(--line);border-left:3px solid var(--em);border-radius:8px;padding:6px 10px;}
  .stat .n{font-size:19px;font-weight:700;color:var(--navy);line-height:1;letter-spacing:-.5px;}
  .stat .n .u{color:var(--em);}
  .stat .l{font-size:7.8px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;font-weight:600;margin-top:3px;line-height:1.2;}
  .profile{font-size:9.6px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--navy);font-weight:600;}

  .tl{position:relative;padding-left:16px;}
  .tl::before{content:"";position:absolute;left:4px;top:4px;bottom:4px;width:2px;background:var(--line);}
  .job{position:relative;margin-bottom:6px;}
  .job::before{content:"";position:absolute;left:-16px;top:3px;width:10px;height:10px;border-radius:50%;background:#fff;border:2.5px solid var(--em);}
  .job.cur::before{background:var(--em);box-shadow:0 0 0 3px var(--em-soft);}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:700;color:var(--navy);}
  .job .c{color:var(--em);font-weight:600;}
  .job .p{font-size:8.2px;color:var(--muted);font-weight:600;white-space:nowrap;flex:none;}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"";position:absolute;left:0;top:6px;width:4px;height:4px;border-radius:50%;background:var(--navy);}
  .ind{background:var(--em-soft);color:#0f7a58;border-radius:4px;}
  ul.pts li b{color:var(--navy);font-weight:600;}
  ul.pts li a{color:var(--em);font-weight:600;}
  .stack{color:var(--muted);}
""",
    body="""<div class="sheet">
  <div class="cols">
  <aside class="side">
    <div class="mono">SS</div>
    <section><h2 class="sh">Contact</h2>$CONTACT$</section>
    <section><h2 class="sh">Core Skills</h2>$CORE$</section>
    <section>$AI$</section>
    <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
    <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
    <section><h2 class="sh">Education</h2>$EDU$</section>
  </aside>
  <main class="main">
    $NAV$
    <div class="kicker">Curriculum Vitae · 2026</div>
    <div class="name">$NAME$</div>
    <div class="role">$ROLE$</div>
    <div class="tag">$TAG$</div>
    $STATS$
    <section><h2 class="sh">Profile</h2>$PROFILE$</section>
    <section><h2 class="sh">Experience</h2>$EXP$</section>
  </main>
  </div>
</div>""")

# =================================================================== v9 GRADIENT HERO PURPLE→PINK (A4, new)
VERSIONS["v9-gradient-hero.html"] = dict(
    nav="--nav-bg:transparent;--nav-line:transparent;--nav-fg:#fff;--nav-muted:rgba(255,255,255,.75);--nav-active-bg:#fff;--nav-active-fg:#5b21b6;",
    title="Sergio Sanchez CV",
    fonts="family=Sora:wght@400;500;600;700;800",
    css="""
  :root{--p1:#5b21b6;--p2:#ec4899;--ink:#1e1b2e;--body:#463f5c;--muted:#8b85a3;--line:#ebe7f3;--tint:#f7f4fc;}
  body{font-family:'Sora',system-ui,sans-serif;color:var(--body);font-size:10px;line-height:1.5;background:#fff;}
  .sheet{background:#fff;display:flex;flex-direction:column;}
  @media screen{body{background:radial-gradient(900px 500px at 50% -10%,#4c1d95 0%,#2a1052 50%,#120726 100%);}}

  .band{background:linear-gradient(120deg,var(--p1) 0%,#9333ea 55%,var(--p2) 100%);color:#fff;padding:6mm 12mm 8mm;position:relative;overflow:hidden;}
  .band::before{content:"";position:absolute;right:-30mm;top:-45mm;width:90mm;height:90mm;border-radius:50%;background:rgba(255,255,255,.08);}
  .band::after{content:"";position:absolute;left:40%;bottom:-40mm;width:60mm;height:60mm;border-radius:50%;background:rgba(255,255,255,.06);}
  .band .in{position:relative;z-index:1;display:flex;justify-content:space-between;align-items:flex-end;gap:8mm;}
  .band .site-nav{position:relative;z-index:1;padding:0;margin:0 0 3mm;}
  .kicker{font-size:8px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.8);font-weight:600;margin-bottom:6px;}
  .name{font-size:28px;font-weight:800;letter-spacing:-.9px;line-height:1.02;}
  .role{font-size:11px;font-weight:600;margin-top:6px;}
  .tag{font-size:8.8px;color:rgba(255,255,255,.8);margin-top:3px;}
  .contact{display:grid;gap:3px;flex:none;}
  .cline{display:flex;align-items:center;gap:6px;font-size:8.2px;color:rgba(255,255,255,.9);background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);padding:2px 8px 2px 6px;border-radius:20px;width:fit-content;}
  .cline svg{stroke:#fff;width:10px;height:10px;}
  .stats{position:relative;z-index:1;display:flex;gap:7px;margin-top:8px;}
  .stat{flex:1;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);border-radius:10px;padding:6px 10px;backdrop-filter:blur(4px);display:flex;align-items:baseline;gap:8px;}
  .stat .n{font-size:19px;font-weight:800;line-height:1;letter-spacing:-.5px;}
  .stat.best{flex-direction:column;align-items:flex-start;gap:2px;}
  .stat .n .u{color:#fbcfe8;}
  .stat .l{font-size:7.6px;text-transform:uppercase;letter-spacing:.8px;color:rgba(255,255,255,.85);font-weight:600;line-height:1.2;}

  .cols{display:flex;gap:8mm;padding:5mm 12mm 7mm;flex:1;}
  .main{flex:1 1 auto;min-width:0;}
  .aside{flex:0 0 55mm;}
  h2.sh{font-size:8.4px;letter-spacing:1.8px;text-transform:uppercase;font-weight:700;margin-bottom:7px;display:flex;align-items:center;gap:7px;
    background:linear-gradient(90deg,var(--p1),var(--p2));-webkit-background-clip:text;background-clip:text;color:transparent;}
  h2.sh::after{content:"";flex:1;height:1px;background:var(--line);}
  section{margin-bottom:9px;}

  .profile{font-size:9.6px;line-height:1.5;color:var(--body);}
  .profile b{color:var(--ink);font-weight:600;}

  .tl{position:relative;padding-left:16px;}
  .tl::before{content:"";position:absolute;left:4px;top:4px;bottom:4px;width:2px;border-radius:2px;background:linear-gradient(180deg,var(--p1),var(--p2),var(--line));}
  .job{position:relative;margin-bottom:6px;}
  .job::before{content:"";position:absolute;left:-16px;top:3px;width:10px;height:10px;border-radius:50%;background:#fff;border:2.5px solid var(--p2);}
  .job.cur::before{background:linear-gradient(135deg,var(--p1),var(--p2));border-color:transparent;box-shadow:0 0 0 3px rgba(236,72,153,.18);}
  .job-head{display:flex;justify-content:space-between;align-items:baseline;gap:8px;}
  .job .r{font-size:11px;font-weight:700;color:var(--ink);}
  .job .c{color:var(--p1);font-weight:600;}
  .job .p{font-size:8px;color:var(--muted);font-weight:600;white-space:nowrap;flex:none;}
  .job .loc{font-size:8.2px;color:var(--muted);}
  ul.pts{list-style:none;margin-top:2px;}
  ul.pts li{position:relative;padding-left:11px;margin-bottom:1px;line-height:1.32;font-size:9.1px;}
  ul.pts li::before{content:"";position:absolute;left:0;top:6px;width:4px;height:4px;border-radius:1px;background:var(--p2);transform:rotate(45deg);}
  .ind{background:var(--tint);color:var(--p1);border:1px solid #e3d9f7;border-radius:20px;}
  ul.pts li b{color:var(--ink);font-weight:600;}
  ul.pts li a{color:var(--p1);font-weight:600;}
  .stack{color:var(--muted);}

  .cskill{padding:2.5px 6px 5px 0;}
  .sk-top{font-size:9.2px;font-weight:600;color:var(--ink);}
  .sk-word{font-size:8px;color:var(--muted);font-weight:500;}
  .sk-track{height:4px;border-radius:4px;background:var(--line);margin-top:5px;}
  .sk-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--p1),var(--p2));position:relative;}
  .sk-fill::after{content:"";position:absolute;right:-4px;top:-3px;width:10px;height:10px;border-radius:50%;background:#fff;border:2.5px solid var(--p2);box-shadow:0 0 0 3px rgba(236,72,153,.18);}
  .ai{background:var(--tint);border:1px solid var(--line);border-radius:10px;padding:10px 11px;position:relative;overflow:hidden;}
  .ai::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,var(--p1),var(--p2));}
  .ai .h{font-size:8px;letter-spacing:1.5px;text-transform:uppercase;color:var(--p1);font-weight:700;margin-bottom:5px;display:flex;align-items:center;gap:6px;}
  .ai .h svg{stroke:var(--p2);}
  .ai p{font-size:8.8px;line-height:1.45;color:var(--body);margin-bottom:6px;}
  .dchips{display:flex;flex-wrap:wrap;gap:4px;}
  .dchip{font-size:7.8px;font-weight:600;padding:2px 7px;border-radius:20px;background:var(--tint);border:1px solid var(--line);color:var(--ink);}
  .ai .dchip{background:linear-gradient(90deg,var(--p1),var(--p2));border-color:transparent;color:#fff;}
  .award{font-size:8.7px;color:var(--body);padding:2.5px 0;border-bottom:1px solid var(--line);line-height:1.35;}
  .award:last-child{border-bottom:0;}
  .award b{color:var(--ink);font-weight:600;}
  .award a{color:var(--p2);font-weight:600;}
  .edu{padding:3px 0;border-bottom:1px solid var(--line);}
  .edu:last-child{border-bottom:0;}
  .edu .d{font-size:9.5px;font-weight:700;color:var(--ink);}
  .edu .m{font-size:8.2px;color:var(--muted);}
""",
    body="""<div class="sheet">
  <header class="band">
    $NAV$
    <div class="in">
      <div>
        <div class="kicker">Curriculum Vitae · 2026</div>
        <div class="name">$NAME$</div>
        <div class="role">$ROLE$</div>
        <div class="tag">$TAG$ · Zapopan, México</div>
      </div>
      <div class="contact">$CONTACT$</div>
    </div>
    $STATS$
  </header>
  <div class="cols">
    <main class="main">
      <section><h2 class="sh">Profile</h2>$PROFILE$</section>
      <section><h2 class="sh">Experience</h2>$EXP$</section>
    </main>
    <aside class="aside">
      <section>$AI$</section>
      <section><h2 class="sh">Core Skills</h2>$CORE$</section>
      <section><h2 class="sh">Tech &amp; Tools</h2>$TECH$</section>
      <section><h2 class="sh">Shipped Titles</h2>$TITLES$</section>
      <section><h2 class="sh">Education</h2>$EDU$</section>
    </aside>
  </div>
</div>""")

# ------------------------------------------------------------------ BUILD
if __name__ == "__main__":
    for fname, v in VERSIONS.items():
        body = fill(v["body"]).replace("$AI_TEXT$", AI_TEXT).replace("$AI_CHIPS$", chips_html(AI_CHIPS))
        dark = v.get("theme") == "dark"
        body = body.replace("$DARK$", " active" if dark else "").replace("$LIGHT$", "" if dark else " active")
        flags = v.get("flags", False)   # outline flag icons on ES / EN (v3 only)
        body = body.replace("$FLAG_ES$", FLAG_MX if flags else "").replace("$FLAG_EN$", FLAG_US if flags else "")
        css = "  :root{" + v["nav"] + "}\n" + v["css"]
        html = page(v["title"], v["fonts"], css, body + "\n" + v.get("extra_js", ""))
        path = os.path.join(OUT, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"wrote {fname} ({len(html)//1024} KB)")
        if fname == LIVE[0]:
            with open(LIVE[1], "w", encoding="utf-8") as f:
                f.write(html)
            print(f"wrote index.html (from {fname})")
