# Portfolio maintenance

## Review before changing

When the owner says **review everything**, perform a read-only review of the full website, linked public evidence, content freshness, accessibility, responsive layout, and technical health. Present an update list describing each proposed change, why it matters, and any missing evidence. Wait for the owner's confirmation before modifying or publishing the proposed changes. An explicit instruction to implement an approved list authorizes those changes.

## Editorial boundaries

- Maintain an accurate, positive description of the owner's current role at Tau Research Limited.
- Do not add job-seeking or availability claims without explicit authorization.
- Do not publish private employer/client information, internal architecture, infrastructure identifiers, source code, data, screenshots, or proprietary assets.
- Public availability alone does not establish ownership or permission to reuse material.
- Do not imply employer endorsement of personal projects or opinions.
- Every numerical result needs a linked source and a clear experiment boundary.
- Never invent achievements, certifications, testimonials, clients, awards, leadership titles, or production-readiness claims.
- Use only approved public contact information. Do not add private contact details.

## Architecture

- `content/site.json`: identity, contact links, experience, project summaries, expertise, reading links, canonical origin.
- `templates/`: detailed case-study content.
- `assets/`: stylesheet, progressive-enhancement JavaScript, and approved evidence images.
- `scripts/build.py`: dependency-free static generator.
- `docs/`: generated GitHub Pages output. Rebuild; do not hand-edit generated pages.
- No database, secrets, tokens, tracking, or third-party embeds are needed.

Run `python3 scripts/build.py`, `python3 scripts/validate.py`, and `node --check assets/site.js` before publishing. Review the changed content. Commit source and regenerated output together. GitHub Pages publishes `main` / `docs`.

For a custom domain, change `site_url`, rebuild, configure the verified domain in GitHub Pages, and follow current GitHub documentation for DNS and HTTPS. Do not claim a domain is connected before verifying it.
