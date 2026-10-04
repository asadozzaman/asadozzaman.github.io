# Md. Asadozzaman — professional portfolio

A personal portfolio focused on computer vision, evidence, and the software around AI models.

## Content

- Professional introduction and current experience
- Four selected public projects
- Video analytics and CVAT case studies with scoped evidence
- Interactive project filters and a CVAT source/annotation explorer
- Technical focus, public writing, and contact links

Read [AGENTS.md](AGENTS.md) before making changes. A request to “review everything” means review and propose an update list first; implementation requires the owner's confirmation.

## Maintain

Requires Python 3.10+ for the generator. No third-party Python packages or frontend dependencies are required.

```bash
python3 scripts/build.py
python3 scripts/validate.py
node --check assets/site.js
```

Edit `content/site.json` for structured content and `templates/` for case-study narratives. Styling and interactions live in `assets/`. The generator writes the public site to `docs/`; commit that output with its sources.

For a local preview:

```bash
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000`. All primary content and navigation remain available without JavaScript. Project filtering and the frame explorer progressively enhance the page.

## Publishing

GitHub Pages uses the `main` branch and `/docs` folder. The `.nojekyll` file keeps the output as plain static files. A validation workflow checks source/output consistency and local links on pushes and pull requests.

To connect a custom domain, update `site_url` in `content/site.json`, rebuild, and configure the domain and DNS using [GitHub's custom-domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site). Do not add a placeholder CNAME or purchase a domain automatically.

## Evidence and attribution

- Video analytics facts: [public README and run report](https://github.com/asadozzaman/production-video-analytics).
- CVAT facts and six synthetic-frame images: [public CVAT experiment](https://github.com/asadozzaman/cvat-video-annotation-roundtrip). These are recorded experimental assets, not client footage.
- Supporting project descriptions: their linked public READMEs.
- Professional context and contact links: the owner's confirmed information and public profiles.

No employer source code, customer data, employer imagery, or proprietary model weights are included. No analytics, tracking cookies, remote font requests, or embedded third-party feeds are used. This site does not assert that any prototype is production-certified.
