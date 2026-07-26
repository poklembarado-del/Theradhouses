# LIPA — website

The LIPA small-timber-homes website: a static, bilingual, zero-dependency site.
Slovak at `/`, English at `/en/`.

Migrated from the `web/` directory of [wallacewain/Tiny-houses](https://github.com/wallacewain/Tiny-houses),
which also holds the market research, business plan and financial model behind it.

## Layout

```
index.html      Slovak homepage
en/index.html   English homepage
assets/         style.css, site.js
images/         photography (webp) + camera originals
robots.txt
sitemap.xml
```

The site lives at the repository root so that its absolute asset paths
(`/assets/style.css`, `/images/…`) resolve without configuration — publish the
repository root and it works.

## Run it locally

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

Because the pages use absolute paths, serve from the repository root rather than
opening `index.html` from the filesystem.

## What's in it

- **Zero dependencies.** No CDN fonts, no frameworks, nothing external.
- **SEO-complete.** hreflang across both languages, canonical URLs, Open Graph,
  and JSON-LD for `Organization`, `LocalBusiness`, `Product` and `FAQPage`.
- **Responsive and theme-aware**, light and dark, with an interactive rental ROI
  calculator and real photography of the show house.
- **Accessible** — skip link, landmarks, labelled form fields, keyboard-operable
  navigation.

## Deploying

Any static host works, and these are free with automatic HTTPS: Netlify, Vercel,
Cloudflare Pages, GitHub Pages. Publish the repository root.

## Before it goes live

1. **Point the domain.** Every canonical URL, hreflang tag, Open Graph URL and
   sitemap entry currently says `https://lipahouse.sk`. If the site ships under a
   different domain, those need updating in `index.html`, `en/index.html`,
   `sitemap.xml` and `robots.txt`.
2. **Fill in the real contact details** — phone, email, IČO/DIČ in the footer.
3. **Wire up the contact form.** The markup is ready; point `action` at Formspree,
   Netlify Forms or your own endpoint.
4. **Check the prices** against the financial model in the source repository
   before publishing them.
5. **Reshoot two gaps.** Still missing: a daylight exterior showing the house in
   its landscape, and clean retakes of the two interiors where the photographer
   is visible in a mirror.

`images/README.md` carries the full shot list and image specifications. The
`IMG-*.jpg` files are the untouched camera originals kept alongside the optimised
WebP versions the site actually loads; they can be pruned if the repository needs
to stay small.
