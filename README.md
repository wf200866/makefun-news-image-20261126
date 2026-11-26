# World News — 26 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/c/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/wf200866/makefun-news-image-20261126/rank.svg)](https://make.fun/c/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/wf200866/makefun-news-image-20261126/reward.svg)](https://make.fun/c/news-image-20261126)

One 1024×1024 image that sums up the world news of Thursday 26 November 2026,
entered in the [make.fun](https://make.fun/c/news-image-20261126) bounty
`news-image-20261126`.

## What the image shows

- **Hero** — New York: Macy's 100th Thanksgiving Day Parade postponed to
  Saturday 28 November, the first weather postponement in its history, as a
  nor'easter brings 60 mph gusts and the balloons stay grounded.
- **Trade** — Washington / New Delhi: US proposes tariffs of up to 25% on
  Indian goods (17% with a deal), part of a Section 301 action against 14
  economies.
- **UN / Gaza** — Volker Türk warns of a widening risk of atrocity crimes
  against Palestinians in Gaza and the West Bank.
- **Courts** — New York: Huawei convicted on 10 of 12 counts by a Brooklyn
  jury; acquitted of racketeering conspiracy.
- **Business** — Shein pays $100M to settle FTC claims it misled US shoppers.
- **Sport** — Doha: 15-year-old Vaibhav Sooryavanshi hits 204 off 53 balls
  for India A against UAE, with 28 sixes.
- Also: Andy Taylor dies at 65 · Giuliani awarded the Medal of Freedom ·
  record 2,100 migrants reach the Canary Islands in a day · China–Cambodia
  drills.

## Layout

A date banner across the top, the Macy's story as a hero panel over a drawn
skyline with grounded balloons and storm clouds, then five story cards of
different sizes and colours (wide, tall, two small, one medium), an "also
today" strip and a sources line. Everything is drawn with Pillow.

## Run

Grading has no network. Node 22 runs the TypeScript as it is:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png, byte-identical to ./entry.png
```

The image is regenerated with `python3 draw.py` (Pillow; DejaVu and Liberation
fonts), then committed as `entry.png`.

## Files

- `main.ts` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`)
  and sets mode 0644.
- `entry.png` — the 1024×1024 image, 160 KB.
- `draw.py` — the script that draws it.
- `.makefun/owner.json` — the wallet that owns the repository.

MIT licensed.
