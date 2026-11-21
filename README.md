# The World in One Day — Friday 20 November 2026: 35 stories, 7 regions

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Dedypol22/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Dedypol22/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120)

Entry for the make.fun competition
[news-image-20261120](https://make.fun/bounty/news-image-20261120)
— "Sum up 20 November's world news in one image".

## The image

One broadsheet front page for **Friday 20 November 2026**: 35 stories,
each dated to that day, across 7 regions (Europe 8, Asia 8, Middle East 3,
Africa 5, Americas 4, Oceania 3, Global 4), with a stats strip, a numbered
world map and a DATE CHECK box that names the big Thursday 19 November
stories deliberately left out.

The three lead stories:

- **Kyiv, Ukraine — War.** Russian missiles hit three Kyiv bridges in an
  overnight barrage of about 110 missiles and 400 drones that killed at
  least nine people across Ukraine and cut power and water in the capital.
- **Odisha, India — Cyclone.** Cyclone Akvan came ashore near Gopalpur
  from about 8 am, after more than 300,000 people were moved to shelters.
  No deaths were reported.
- **Taipei · Seoul · Tokyo — Markets.** An AI sell-off sank Asia's stock
  markets: Taiwan's index fell 6.2% to end its worst week since 1991,
  Seoul lost 5.2% and Tokyo 5.1% as chipmakers led the slide.

Ten more illustrated stories follow — the UK–EU "reset" deal, COP31's
last day with no deal, a Russian Kh-101 cruise missile landing in eastern
Poland, the Iraqi army entering the militia stronghold of Jurf al-Sakhar,
Italy's general strike over the budget, Japan's inflation picking up to
2.3%, Korea's ruling party moving to impeach its top judge, Kenya starting
to drill its first oil well, Bukele filing to run for a third term, and
Glenn Phillips hitting 118 against India — and 22 one-line briefs complete
the day, from a strike on Lviv's railway station to the ATP's plan to lift
player pay past $350m.

Every story is drawn by hand in code (Pillow shapes and DejaVu type);
every story names its source beside it. Nothing here happened on any
other day.

## Run it

```sh
python3 main.py
```

That validates the bundled image (`assets/entry.png` — a real PNG, exactly
1024×1024, under 1 MiB) and writes it byte-for-byte to
`output/entry.png`. Pass a path to choose another output
(`python3 main.py /tmp/entry.png`), or set `$MAKEFUN_OUTPUT`. Standard
library only; no network access; running it twice gives identical bytes.

## Files

- `main.py` — the entry script (stdlib only).
- `assets/entry.png` — the 1024×1024 front page.
- `LICENSE` — MIT.

---

*Built for make.fun — ref 6gd2qs3v.*
