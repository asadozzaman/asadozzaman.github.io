"""Build a portable static portfolio using only Python's standard library."""
import html
import json
from pathlib import Path
import shutil
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
data = json.loads((ROOT / 'content/site.json').read_text())
e = html.escape
BASE = data['site_url'].rstrip('/')

def link(url, label, cls=''):
    return f'<a href="{e(url, quote=True)}" class="{e(cls)}">{e(label)}</a>'

def layout(title, description, body, path='', prefix=''):
    home = prefix or './'
    full_title = title + ' | ' + data['name'] if title else data['name'] + ' — ' + data['focus']
    canonical = BASE + '/' + path
    favicon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#142b25"/><text x="32" y="42" text-anchor="middle" font-family="Arial,sans-serif" font-size="28" font-weight="bold" fill="#d6f582">MA</text></svg>'
    structured = {'@context':'https://schema.org', '@type':'Person', 'name':data['name'], 'url':BASE+'/', 'jobTitle':data['role'], 'sameAs':[data['github'],data['linkedin']], 'worksFor':{'@type':'Organization','name':data['employer']}}
    structured_json = json.dumps(structured).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(full_title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#142b25"><meta name="referrer" content="strict-origin-when-cross-origin"><link rel="canonical" href="{e(canonical)}"><meta property="og:type" content="website"><meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{e(canonical)}"><meta name="twitter:card" content="summary"><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{quote(favicon, safe='')}"><link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/site.js" defer></script><script type="application/ld+json">{structured_json}</script><noscript><style>.site-nav{{display:flex!important}}@media(max-width:760px){{.site-nav{{padding-bottom:16px}}}}</style></noscript></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{home}" aria-label="Md. Asadozzaman home"><span class="monogram" aria-hidden="true">MA</span><span>Md. Asadozzaman</span></a><button class="menu-button" data-menu aria-expanded="false" aria-controls="site-nav" hidden>Menu</button><nav class="site-nav" id="site-nav" aria-label="Main navigation"><a href="{home}#work">Work</a><a href="{home}#about">About</a><a href="{home}#writing">Writing</a><a class="contact-link" href="{home}#contact">Get in touch</a></nav></div></header>
<main id="main">{body}</main><footer class="site-footer"><div class="wrap footer-inner"><p>© 2026 {e(data['name'])}. Personal portfolio · Views are my own.</p><div class="footer-links">{link(data['github'],'GitHub')}{link(data['linkedin'],'LinkedIn')}{link(prefix+'privacy/','Privacy')}</div></div></footer></body></html>'''

def contact():
    return f'''<section class="contact-section" id="contact"><div class="wrap contact-inner"><div><p class="eyebrow">LET’S CONNECT</p><h2>Good engineering starts<br>with a clear question.</h2><p>I welcome thoughtful conversations about AI engineering, research, and professional collaboration.</p></div><div class="contact-details">{link('mailto:'+data['email'],data['email'],'email')}<p>A short written introduction is a good place to start.</p><div class="contact-socials">{link(data['linkedin'],'LinkedIn')}{link(data['github'],'GitHub')}</div></div></div></section>'''

def card(p):
    visual = ''
    if p['slug'] == 'video-analytics':
        visual = '''<div class="project-visual video"><div class="run-diagram" aria-label="Video pipeline: frames, YOLO detection, ByteTrack tracking, then MP4, JSON and CSV outputs"><p class="meta">PIPELINE / STRUCTURED OUTPUTS</p><div class="run-row"><span>Frames</span><span>YOLO</span><span>ByteTrack</span></div><div class="run-output"><span>MP4</span><span>JSON</span><span>CSV</span></div></div></div>'''
    elif p['slug'] == 'cvat-roundtrip':
        visual = '<div class="project-visual"><img src="assets/evidence_frame_010.jpg" width="640" height="360" loading="lazy" alt="Synthetic CVAT frame 10 with its re-imported rectangle annotation"></div>'
    tags = ''.join('<span>'+e(t)+'</span>' for t in p['tags'])
    links = (link(p['detail'],'Read case study') if p['detail'] else '') + link(p['repository'],'View repository')
    return f'''<article class="project {'compact' if not visual else ''}" data-category="{p['category']}">{visual}<div class="project-body"><div class="project-topline"><span class="meta">{e(p['label'])}</span><span class="index">/{p['number']}</span></div><h3>{e(p['title'])}</h3><p class="project-name">{e(p['name'])}</p><p class="project-summary">{e(p['summary'])}</p><div class="tags">{tags}</div><div class="project-evidence"><strong>{e(p['evidence'])}</strong><small>{e(p['status'])} · {e(p['boundary'])}</small></div><div class="project-links">{links}</div></div></article>'''

def home():
    expertise=''.join(f'''<article class="expertise"><p class="expertise-number">0{i+1}</p><h3>{e(x['title'])}</h3><p>{e(x['description'])}</p><p class="tools">{e(x['tools'])}</p></article>''' for i,x in enumerate(data['expertise']))
    reading=''.join(f'''<article class="reading-item"><p class="meta">{e(x['type'])}</p><h3>{e(x['title'])}</h3><p>{e(x['description'])}</p>{link(x['url'],x['action'])}</article>''' for x in data['reading'])
    return f'''<div class="wrap"><section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow">SENIOR AI ENGINEER / {e(data['location'])}</p><h1 id="hero-title">Computer vision.<br><span>Built beyond<br>the model.</span></h1><p><span class="intro-name">I’m {e(data['name'])}.</span>{e(data['intro'])}</p><div class="actions"><a class="button primary" href="#work">Explore my work</a>{link(data['github'],'GitHub profile','button secondary')}</div><p class="current-role">Currently contributing at<strong>{e(data['employer'])} · {e(data['role'])}</strong></p></div><div class="hero-art"><div class="meta"><span>ENGINEERING PERSPECTIVE</span><span>01 / 03</span></div><div class="pipeline"><div class="pipeline-step"><span>01</span><div><b>See clearly.</b><small>Detection · tracking · annotation</small></div></div><div class="pipeline-step is-highlight"><span>02</span><div><b>Verify what matters.</b><small>Frame alignment · evidence · evaluation</small></div></div><div class="pipeline-step"><span>03</span><div><b>Build the whole system.</b><small>APIs · workflows · cloud infrastructure</small></div></div></div><div class="hero-art-footer"><span>A model is the beginning.</span><a href="#work">Inspect the engineering</a></div></div></section><div class="scope-strip"><span class="label">ACROSS THE STACK</span><span>Computer Vision</span><span>Evaluation</span><span>Backend Engineering</span><span>Cloud & MLOps</span></div><section class="section" id="work"><div class="section-heading"><div><p class="eyebrow">01 / SELECTED WORK</p><h2>Built to be inspected.</h2></div><p>Public projects with a clear problem, an implementation to explore, and evidence you can follow.</p></div><div class="filters" data-filters role="group" aria-label="Filter projects" hidden><button data-filter="all" aria-pressed="true">All work</button><button data-filter="vision" aria-pressed="false">Computer Vision</button><button data-filter="systems" aria-pressed="false">AI applications</button></div><p class="sr-only" data-filter-status aria-live="polite">4 projects shown</p><div class="project-grid">{''.join(card(p) for p in data['projects'])}</div><p class="section-note">Each project is presented at its actual stage. Recorded experiments and application prototypes are distinguished from production deployments.</p></section></div>
<section class="about-band section" id="about"><div class="wrap about-grid"><div><p class="eyebrow">02 / ABOUT</p><h2>Models, software,<br>and the space<br>between them.</h2><div class="experience" style="margin-top:35px"><small>{e(data['employment_period'])} · Remote</small><h3>{e(data['role'])}</h3><span>{e(data['employer'])}</span><p>{e(data['experience'])}</p></div></div><div class="about-side"><p class="about-lead">I’m interested in the engineering that turns a promising model into something people can actually use.</p><p>That means looking beyond inference: how data enters a system, how outputs are checked, and how another engineer can understand what happened.</p><div class="principles"><div class="principle"><b>01</b><p><strong>Make results inspectable.</strong><br>Keep configuration, artifacts, and limitations close to the code.</p></div><div class="principle"><b>02</b><p><strong>Measure the complete workflow.</strong><br>Model speed and application performance answer different questions.</p></div><div class="principle"><b>03</b><p><strong>Work across boundaries.</strong><br>Connect computer vision, backend systems, and cloud delivery.</p></div></div></div></div></section>
<div class="wrap"><section class="section" id="expertise"><div class="section-heading"><div><p class="eyebrow">03 / TECHNICAL FOCUS</p><h2>Depth in vision.<br>Range across systems.</h2></div></div><div class="expertise-grid">{expertise}</div></section><section class="section writing" id="writing"><div class="section-heading"><div><p class="eyebrow">04 / NOTES & ACTIVITY</p><h2>Thinking in public.</h2></div><p>Design notes, recorded experiments, and professional perspectives on applied AI.</p></div><div class="reading-grid">{reading}</div></section></div>{contact()}'''

def detail(p):
    article=(ROOT/'templates'/f"{p['slug']}.html").read_text()
    body=f'''<div class="wrap"><header class="detail-hero"><p class="breadcrumb"><a href="../../#work">Selected work</a> / {e(p['name'])}</p><p class="eyebrow">CASE STUDY {p['number']} / {e(p['label'])}</p><h1>{e(p['title'])}</h1><p class="lead">{e(p['summary'])}</p><dl class="detail-meta"><div><dt>Project</dt><dd>{e(p['name'])}</dd></div><div><dt>Status</dt><dd>{e(p['status'])}</dd></div><div><dt>Source</dt><dd>{link(p['repository'],'Public repository')}</dd></div></dl></header><div class="article-layout"><nav class="article-nav" aria-label="On this page"><a href="#problem">The problem</a><a href="#implementation">Implementation</a><a href="#evidence">Evidence & limits</a><a href="#next">What comes next</a></nav><article class="article-body">{article}</article></div></div>{contact()}'''
    return layout(p['name'],p['summary'],body,p['detail'],'../../')

def write(path, content):
    target=OUT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(content,encoding='utf-8')

OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
write('index.html',layout('',data['intro'],home()))
paths=['']
for p in data['projects']:
    if p['detail']:
        write(p['detail']+'index.html',detail(p))
        paths.append(p['detail'])
privacy='''<div class="wrap privacy"><p class="eyebrow">SITE INFORMATION</p><h1>Privacy & contact.</h1><p>This personal portfolio does not use analytics, advertising trackers, cookies, a contact form, or a visitor database. Fonts and images are served with the site.</p><h2>Hosting and external links</h2><p>GitHub Pages hosts this website and may process technical request information under GitHub’s privacy practices. Links to GitHub and LinkedIn take you to those services, which have their own policies.</p><h2>Getting in touch</h2><p>Email links open your chosen email application. Messages are sent only when you choose to send them. Please do not send confidential employer or client information in an initial message.</p><h2>Professional context</h2><p>This is Md. Asadozzaman’s personal portfolio. It is not an official website or endorsement of Tau Research Limited. Project demonstrations and opinions are presented in a personal capacity.</p><p><a href="../#contact">Contact details</a> · <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy statement</a></p></div>'''
write('privacy/index.html',layout('Privacy','Privacy and professional context for this personal portfolio.',privacy,'privacy/','../'))
paths.append('privacy/')
write('404.html',layout('Page not found','This page could not be found.',f'<section class="wrap not-found"><p class="eyebrow">404 / PAGE NOT FOUND</p><h1>Let’s get you back<br>to the work.</h1><p>This page may have moved.</p><div class="actions">{link(BASE+"/","Return home","button primary")}</div></section>','404.html',BASE+'/'))
write('.nojekyll','')
write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+'/'+p+'</loc></url>' for p in paths)+'</urlset>\n')
print(f'Built {len(paths)+1} HTML pages in {OUT}')
