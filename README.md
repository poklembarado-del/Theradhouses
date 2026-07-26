# theradhouses.eu

The website for **theradhouses.eu**, served from this repository via GitHub Pages.

Plain static HTML/CSS — no build step, no framework, no dependencies. Every push to
`main` is published automatically by
[`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml).

```
index.html                     home page
404.html                       not-found page (GitHub Pages serves this automatically)
assets/styles.css              all styling
assets/favicon.svg             favicon
CNAME                          custom domain — GitHub Pages reads this file
robots.txt, sitemap.xml        search engines
.nojekyll                      publish files as-is, skip Jekyll processing
```

> The current home page is a placeholder ("the site is being built") and the contact
> address `hello@theradhouses.eu` is a stand-in. Replace both with the real content
> and address.

## Local preview

No tooling needed — open `index.html` in a browser. To preview with correct
absolute paths (`/assets/...`):

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Go-live checklist

Two halves: turn on Pages here on GitHub, and point DNS at it from Hostcreators.
Do the GitHub half first — the DNS half is what takes time to propagate.

### 0. Make sure `main` exists

The repository was empty before this commit, so GitHub made the branch this work
landed on the default branch — there is no `main` yet, and the deploy workflow only
triggers on pushes to `main`. Fix it either way:

- **Settings → General → Default branch → rename** the current default to `main`, or
- create `main` from this branch and set it as the default.

Until then, the site can still be published by running the workflow by hand from the
**Actions** tab (**Deploy site to GitHub Pages → Run workflow**).

### 1. Enable GitHub Pages (one-time, in this repo)

1. **Settings → Pages → Build and deployment → Source: GitHub Actions.**
   Not "Deploy from a branch" — the workflow in this repo uses the Actions source.
2. Push to `main` (or run the workflow manually from the **Actions** tab). Once it
   goes green the site is live at `https://poklembarado-del.github.io/Theradhouses/`.
3. **Settings → Pages → Custom domain** should already read `theradhouses.eu`,
   picked up from the `CNAME` file. If it's blank, type it in and press Save.
4. Leave **Enforce HTTPS** unchecked for now — GitHub greys it out until DNS
   resolves and it has issued a certificate. Come back and tick it in step 3 below.

### 2. Point DNS at GitHub (at Hostcreators)

Log in to Hostcreators and open the DNS / nameserver management for
`theradhouses.eu` (in a DirectAdmin or cPanel panel this is usually "DNS
Management" or "DNS Zone Editor"; in their own customer portal, look for
"Domains → theradhouses.eu → DNS").

This only works if the domain uses **Hostcreators' own nameservers**. If the
nameservers were delegated elsewhere, make these records there instead.

**Apex domain `theradhouses.eu` — four A records** (host/name field: `@`, or blank,
or `theradhouses.eu.` depending on the panel):

| Type | Name | Value           | TTL  |
| ---- | ---- | --------------- | ---- |
| A    | @    | 185.199.108.153 | 3600 |
| A    | @    | 185.199.109.153 | 3600 |
| A    | @    | 185.199.110.153 | 3600 |
| A    | @    | 185.199.111.153 | 3600 |

**Optional but recommended — four AAAA records** for IPv6:

| Type | Name | Value               | TTL  |
| ---- | ---- | ------------------- | ---- |
| AAAA | @    | 2606:50c0:8000::153 | 3600 |
| AAAA | @    | 2606:50c0:8001::153 | 3600 |
| AAAA | @    | 2606:50c0:8002::153 | 3600 |
| AAAA | @    | 2606:50c0:8003::153 | 3600 |

**`www` subdomain — one CNAME:**

| Type  | Name | Value                        | TTL  |
| ----- | ---- | ---------------------------- | ---- |
| CNAME | www  | poklembarado-del.github.io.  | 3600 |

(Note the trailing dot; some panels want it, some add it for you. GitHub then
redirects `www.theradhouses.eu` → `theradhouses.eu` because `CNAME` holds the apex.)

**Delete any conflicting records first:** a pre-existing `A`/`AAAA` on `@`, a
`CNAME` on `www`, or a parking/redirect record pointing at a Hostcreators holding
page. Two sets of A records on the apex will make the site load intermittently.

Leave `MX` and `TXT` records alone — those are email and domain verification, and
GitHub Pages doesn't touch them. **GitHub Pages does not host email**; if mail for
`@theradhouses.eu` runs at Hostcreators it keeps working unchanged.

The IPs above were verified against GitHub's live DNS. If a record is ever
rejected, cross-check the current list at
<https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site>.

### 3. Verify, then force HTTPS

DNS usually takes 15–60 minutes and can take up to 24 hours. Check with:

```bash
dig +short theradhouses.eu          # expect the four 185.199.x.153 addresses
dig +short www.theradhouses.eu      # expect poklembarado-del.github.io.
curl -sI https://theradhouses.eu    # expect HTTP/2 200
```

Then go back to **Settings → Pages** and tick **Enforce HTTPS**. GitHub issues a
free Let's Encrypt certificate once DNS checks out; if the checkbox is still
greyed out, DNS hasn't fully propagated — wait and revisit.

## Deploying changes

Push to `main`. The workflow rebuilds and publishes within about a minute; watch it
in the **Actions** tab. Never delete the `CNAME` file — removing it unsets the
custom domain in the Pages settings and the site drops back to the `github.io` URL.
