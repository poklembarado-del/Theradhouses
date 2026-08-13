# Photography

The show-house photographs are shot, optimised and wired into both language pages.
This file records what each one is for, so replacements go in the right slot.

## In use

| Filename | Aspect | Where it appears |
| --- | --- | --- |
| `hero-exterior.webp` | 4:3 | Homepage hero — the first thing anyone sees |
| `model-20.webp` | 1:1 | Radhouses 20 card |
| `model-30.webp` | 1:1 | Radhouses 30 card |
| `model-39.webp` | 1:1 | Radhouses 39 card (the show house) |
| `interior-evening.webp` | 16:9 | "Don't trust the catalogue, sleep in it" |
| `timber-detail.webp` | 16:9 | "Timber frame, not sandwich panel" |
| `location.webp` | 16:9 | Contact section |
| `og-image.jpg` | 1200 × 630 | Share thumbnail — referenced in `og:image` on both pages |

`bedroom.webp` and `interior-wide.webp` are shot and optimised but not currently placed.

The `IMG-*.jpg` files are the untouched camera originals. Nothing references them; they
are kept so the WebPs can be re-derived, and can be deleted if the repo needs to be small.

## Still to shoot

1. A daylight exterior showing the house in its landscape.
2. Clean retakes of the two interiors where the photographer is visible in a mirror.

## Specifications

- **WebP**, 25–35% smaller than JPEG at the same quality. [Squoosh.app](https://squoosh.app)
  converts and compresses in the browser, free.
- **Under 200 KB each.** The site's main technical advantage is that it loads nothing
  external — don't spend it on a 4 MB hero.
- **Long edge 1600 px.** Nothing on the page displays wider than 1140 px.
- **Lowercase filenames, hyphens, no diacritics.** Servers are case-sensitive.

## Swapping in a new photo

Keep the existing `<img>` attributes and change only `src` and `alt`:

```html
<img src="/images/hero-exterior.webp" width="1600" height="1200"
     alt="Vzorový dom Radhouses 39 pri západe slnka, drevená fasáda a terasa"
     class="ph-img" loading="lazy">
```

- **`alt` text is SEO, not box-ticking.** Describe what is in the frame, in that page's
  language — Slovak in `index.html`, English in `en/index.html`.
- **Keep `width` and `height`** so the browser reserves space before the image loads;
  without them the page jumps, which hurts Cumulative Layout Shift.
- **The hero image has no `loading="lazy"`** — it is above the fold. Every other image
  should keep it.
