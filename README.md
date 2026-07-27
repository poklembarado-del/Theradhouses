# radhouses.eu

The Radhouses website — a static, bilingual, zero-dependency site served from this
repository via GitHub Pages. Slovak at `/`, English at `/en/`.

The site content originated in the `web/` directory of
[wallacewain/Tiny-houses](https://github.com/wallacewain/Tiny-houses), which also holds
the market research, business plan and financial model behind it. It was rebranded from
LIPA to Radhouses and repointed from `lipahouse.sk` to `radhouses.eu` on the way in.

```
index.html                  Slovak home page
en/index.html               English home page
404.html                    not-found page (Pages serves it automatically)
assets/style.css            all styling
assets/site.js              theme toggle, mobile nav, ROI calculator
assets/favicon.svg          favicon
images/                     photography (webp) + camera originals — see images/README.md
CNAME                       custom domain — GitHub Pages reads this file
scripts/check-dns.py        audits the live DNS setup
robots.txt, sitemap.xml     search engines
.nojekyll                   publish files as-is, skip Jekyll processing
```

No build step, no framework, no external requests. Every push to `main` is published by
[`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml).

## Local preview

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

Serve from the repository root rather than opening `index.html` from disk — the pages use
absolute paths (`/assets/…`, `/images/…`).

## Go-live checklist

### 1. Create `main`

The repository was empty before this work, so GitHub made a `claude/…` branch the default.
The deploy workflow only triggers on pushes to `main`. Either rename the default branch to
`main` under **Settings → General**, or create `main` from this branch and set it as default.

Until then the site can still be published by hand from the **Actions** tab
(**Deploy site to GitHub Pages → Run workflow**).

### 2. Enable Pages

This step has to be done by hand, once, by someone with admin on the repository. The
workflow cannot do it for you: creating a Pages site requires admin rights, and
`GITHUB_TOKEN` does not have them even with `pages: write`. Until it is done, every run
fails at `configure-pages` with *"Get Pages site failed … Not Found"*.

1. **Settings → Pages → Build and deployment → Source: GitHub Actions.** Not "Deploy from
   a branch" — this repo deploys through the workflow.
2. **Settings → Pages → Custom domain** should read `radhouses.eu`, picked up from `CNAME`.
3. Leave **Enforce HTTPS** unchecked until DNS resolves and GitHub has issued the
   certificate, then come back and tick it.

### 3. DNS

DNS is managed at Hostcreators. The apex records are in place and verified:

| Type | Host | Value |
| --- | --- | --- |
| A | *(blank)* | 185.199.108.153 |
| A | *(blank)* | 185.199.109.153 |
| A | *(blank)* | 185.199.110.153 |
| A | *(blank)* | 185.199.111.153 |
| AAAA | *(blank)* | 2606:50c0:8000::153 |
| AAAA | *(blank)* | 2606:50c0:8001::153 |
| AAAA | *(blank)* | 2606:50c0:8002::153 |
| AAAA | *(blank)* | 2606:50c0:8003::153 |
| CNAME | `www` | `poklembarado-del.github.io.` |

Notes on the Hostcreators panel: the **Host** field appears as "Guest" and the **A** record
type as "And" — both are machine-translation artefacts. The field appends `.radhouses.eu`
for you, so leave it blank for the apex and enter just `www` for the subdomain. Never type
the full domain in there or you get `radhouses.eu.radhouses.eu`.

Verify from outside the control panel:

```bash
python3 scripts/check-dns.py
```

It reads the zone directly from the authoritative nameservers and reports what is missing.
It exits non-zero while anything is wrong and needs no dependencies beyond Python 3.

Leave the `smtp`/`imap`/`pop3`/`ssh` CNAMEs, the `_autodiscover` SRV and the SPF/DMARC TXT
records alone — that is the mail setup, unrelated to Pages.

## Before it is really live

1. **Wire up the contact form.** Both forms post to
   `https://formspree.io/f/YOUR_FORM_ID` — replace that with a real endpoint from
   [formspree.io](https://formspree.io) and submissions will be emailed to the address you
   register. The `email` field is used as Reply-To.
2. **Fill in the real contact details** — phone, email, IČO/DIČ in the footer of both pages.
   They are currently zeroed placeholders.
3. **Check the prices** against the financial model in the source repository.
4. **Reshoot two photo gaps** — see [`images/README.md`](images/README.md).

## Deploying changes

Push to `main`; the workflow publishes within about a minute. Never delete `CNAME` —
removing it unsets the custom domain and the site drops back to the `github.io` URL.
