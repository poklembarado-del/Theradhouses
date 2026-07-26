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

### 2. Point DNS at GitHub

**Current state of the domain (checked against the live `.eu` registry):
`theradhouses.eu` is not delegated at all — it returns `NXDOMAIN`, and the only
thing answering for it is the registry's own `si.dns.eu`.** No nameservers are
set, so there is no zone, no records, and no mail routing to preserve. Nothing
below can break an existing service.

GitHub Pages is not a DNS host — it has no nameservers to hand out. It needs `A`
and `CNAME` **records**, which have to live in a DNS zone somewhere. So the first
question is where that zone will be.

#### 2a. Where the zone lives

Hostcreators' panel exposes only four nameserver fields (`ns1`–`ns4`). That is the
registrar half of the job: it decides *who* answers DNS for the domain, not *what*
they answer. Two ways forward.

**Path A — keep DNS at Hostcreators.** They do run their own nameservers. Fill the
four fields with:

```
ns1.hostcreators.eu
ns2.hostcreators.eu
ns3.hostcreators.eu
ns4.hostcreators.eu
```

Save, then look for a **DNS / zone editor** in the panel. If one appears, create
the records in 2b there and you are done — no third party involved. Many
registrars only unlock the zone editor once the domain points at their own
nameservers, so this is worth trying first. If no editor appears (common when the
domain was bought without a hosting package), ask their support whether DNS
management is included — and if it isn't, take path B.

**Path B — delegate DNS to a free DNS host.** Put *their* nameservers in the
`ns1`–`ns4` fields instead, then create the records in 2b in that provider's panel.
Any of these work; pick one:

| Provider | Nameservers to enter | Notes |
| --- | --- | --- |
| **Cloudflare** (recommended) | the two it assigns you, e.g. `dana.ns.cloudflare.com` / `rex.ns.cloudflare.com` | Free. Best UI and docs. Add the domain at dash.cloudflare.com and it tells you your exact pair — they are per-account, don't copy the example. Leave `ns3`/`ns4` blank. |
| **deSEC** | `ns1.desec.io`, `ns2.desec.org` | Free, EU non-profit, DNSSEC on by default. Good fit for a `.eu` domain if you'd rather keep DNS in Europe. Leave `ns3`/`ns4` blank. |
| **Hurricane Electric** | `ns1.he.net` … `ns5.he.net` | Free, no frills, and fills all four fields exactly. |

Only two nameservers is completely normal — leaving `ns3`/`ns4` empty is fine.

> **If you use Cloudflare**, set the records to **DNS only** (grey cloud, not
> orange) at first. GitHub cannot validate the domain or issue its certificate
> through Cloudflare's proxy, and proxying with SSL/TLS mode "Flexible" causes a
> redirect loop. Once the site is live on HTTPS you may switch the proxy on,
> provided SSL/TLS mode is **Full (strict)**.

#### 2b. The records to create

Whichever panel you land in, create these.

**Filling in the "Host" / "Name" field.** It takes the part of the name to the left
of the domain, not the whole thing: `@` means the domain itself
(`theradhouses.eu`), and `www` means `www.theradhouses.eu` — the panel appends the
domain for you. Check which convention this panel uses by looking at the `SOA`/`NS`
rows it created automatically: if their Host column reads `@` or is blank, use `@`;
if it reads `theradhouses.eu.` with a trailing dot, this panel wants fully-qualified
names, so enter `theradhouses.eu.` and `www.theradhouses.eu.` instead.

Do not type `theradhouses.eu` without a trailing dot into a Host field that appends
the domain — that silently creates `theradhouses.eu.theradhouses.eu`, which resolves
nowhere and looks correct in the records table. `@` is the safer choice when unsure.

Each A record is its own row: four rows, all with Host `@`, one IP each.

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

**Delete any conflicting records the panel creates for you:** some hosts drop in a
default `A` record on `@` pointing at a parking page, or a `CNAME` on `www`. Two
sets of A records on the apex will make the site load intermittently.

**GitHub Pages does not host email.** The domain has no `MX` records today, so
nothing breaks — but it also means `hello@theradhouses.eu` will not receive mail
until you set up a mailbox somewhere and add its `MX` (and `SPF`/`DKIM` `TXT`)
records in whichever zone you chose above. That is separate from the website.

The IPs above were verified against GitHub's live DNS. If a record is ever
rejected, cross-check the current list at
<https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site>.

### 3. Verify, then force HTTPS

DNS usually takes 15–60 minutes and can take up to 24 hours. Check with:

```bash
dig +short NS theradhouses.eu       # expect the nameservers you entered — check this first
dig +short theradhouses.eu          # expect the four 185.199.x.153 addresses
dig +short www.theradhouses.eu      # expect poklembarado-del.github.io.
curl -sI https://theradhouses.eu    # expect HTTP/2 200
```

Work through those in order. If the `NS` line is empty the delegation hasn't taken
effect yet and the rest cannot possibly work — that's the registrar half (step 2a),
and it is the part that has never been set for this domain. Only once `NS` answers
does it make sense to debug the `A` records (step 2b).

Then go back to **Settings → Pages** and tick **Enforce HTTPS**. GitHub issues a
free Let's Encrypt certificate once DNS checks out; if the checkbox is still
greyed out, DNS hasn't fully propagated — wait and revisit.

## Deploying changes

Push to `main`. The workflow rebuilds and publishes within about a minute; watch it
in the **Actions** tab. Never delete the `CNAME` file — removing it unsets the
custom domain in the Pages settings and the site drops back to the `github.io` URL.
