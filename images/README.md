# Photography

Drop the photographs here. Every striped block on the website is a placeholder waiting for one
of the files below.

Right now the site draws those blocks in CSS rather than loading images, so nothing is broken
while the folder is empty — the page just looks unfinished. Once the real photos are in here,
swap each placeholder `<div class="ph ...">` in `web/index.html` and `web/en/index.html` for an
`<img>` tag pointing at the matching file.

---

## Shot list

Eight photographs carry the entire site. Shoot them in one session.

| # | Filename | Aspect | Where it appears | What it needs to be |
|---|---|---|---|---|
| 1 | `hero-exterior.webp` | **4:3** | Homepage hero — the first thing anyone sees | The whole house at golden hour, three-quarter angle so you read both the long side and the end. Lights on inside, doors open. This is the single most important image on the site. |
| 2 | `model-lipa-20.webp` | **1:1** | LIPA 20 card | The 20 m² unit as a garden studio. If it doesn't exist yet, shoot the show house tight so it reads smaller. |
| 3 | `model-lipa-25.webp` | **1:1** | LIPA 25 card (the flagship) | Clean straight-on exterior of the show house. Square crop, house centred. |
| 4 | `model-lipa-25-offgrid.webp` | **1:1** | LIPA 25 Off-Grid card | Same house, angled to show the **solar panels on the roof**. The panels are the product here — make them unmissable. |
| 5 | `model-lipa-40.webp` | **1:1** | LIPA 40 card | The larger unit. A render is acceptable *only* for this one, and label it as such. |
| 6 | `interior-evening.webp` | **16:9** | "Don't trust the catalogue, sleep in it" | Inside, lamps on, dusk through the windows. **Put people in it** — someone cooking, someone reading. Every competitor shoots empty rooms; a used room is the differentiator. |
| 7 | `timber-detail.webp` | **16:9** | "Timber frame, not sandwich panel" | Close on a frame junction, visible joinery and grain. This is the picture that proves the quality claim to an engineer-minded buyer. |
| 8 | `location.webp` | **16:9** | Contact section | The house in its landscape — trees, hills, context. Sells the life, not the box. A drone shot works well. |

### Also needed

| Filename | Size | Purpose |
|---|---|---|
| `og-image.jpg` | **1200 × 630** | The thumbnail when the site is shared on Facebook, WhatsApp or LinkedIn. Usually a crop of #1 with the logo. Referenced in the `og:image` meta tag on both pages. |

---

## Specifications

- **Format: WebP.** 25–35% smaller than JPEG at the same quality. Keep a JPEG fallback only if
  you need one for something else.
- **Under 200 KB each.** Page speed is a Google ranking factor, and this site's main technical
  advantage is that it loads nothing else. Don't spend that advantage on a 4 MB hero image.
  [Squoosh.app](https://squoosh.app) does the conversion and compression in the browser, free.
- **Long edge 1600 px** is plenty. Nothing on the page displays wider than 1140 px.
- **Lowercase filenames, hyphens, no spaces or diacritics.** Web servers are case-sensitive;
  `Hero-Exterior.WEBP` and `hero-exterior.webp` are different files and one of them will 404.

## Swapping a placeholder for a real photo

Replace this:

```html
<div class="ph ph-hero" data-label="..." role="img" aria-label="Vzorový dom LIPA 25, exteriér"></div>
```

with this:

```html
<img src="/images/hero-exterior.webp" width="1600" height="1200"
     alt="Vzorový dom LIPA 25 pri západe slnka, drevená fasáda a terasa"
     class="ph-img" loading="lazy">
```

Three things that matter and are easy to skip:

- **`alt` text is SEO, not accessibility box-ticking.** Describe what's actually in the frame, in
  the page's language — Slovak on `index.html`, English on `en/index.html`. Google reads it.
- **Keep `width` and `height`** so the browser reserves the space before the image loads. Without
  them the page jumps as images arrive, which hurts Cumulative Layout Shift — a Core Web Vital.
- **Drop `loading="lazy"` on the hero image only.** It's above the fold; lazy-loading it makes the
  page feel slower, not faster. Every other image should keep it.

---

## Why this matters more than it looks

The business plan puts €600–900 against one professional shoot, and calls it the highest-return
money in the launch. That isn't a design opinion — the whole competitive position is *"we have a
real finished house and they're selling you renders."* That argument only lands if the
photographs are visibly of a real house that real people live in.

Budget half a day. Golden hour for the exteriors, blue hour for the lit interior.
