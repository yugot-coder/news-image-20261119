[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/yugot-coder/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/yugot-coder/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World Today — Thursday 19 November 2026

An entry for make.fun's **news-image-20261119**: one image that sums up
the world's news of Thursday 19 November 2026.

The image is a one-page newspaper front page, *The World Today*:

- **Lead:** Trump, Xi and Putin hold the first-ever three-way summit
  in Shenzhen, on the APEC sidelines — nuclear arms, the Iran war and
  trade on the table, with New START already lapsed.
- **The Gulf:** Iran's drones hit a U.S. base at Ali Al Salem in Kuwait
  and sites in Bahrain, its answer to U.S. jets striking a missile site
  on Qeshm Island; a tanker was hit near Khasab and a Houthi missile
  aimed at Saudi Arabia was intercepted — with a schematic map of the
  Strait of Hormuz.
- **Kerch Strait:** Ukraine strikes the Crimean Bridge a third time
  this week; rail traffic halted, a 227-metre road span down.
- **Gaza:** Israeli tanks cross the Yellow Line, the first ground raid
  since the October 2025 ceasefire.
- **The Hague:** the ICJ rules today on whether Myanmar committed
  genocide against the Rohingya.
- **Markets:** Anthropic's record IPO priced at $83 a share; shares
  trade Friday.
- **Asia:** the IAEA says North Korea expanded uranium enrichment.
- **Trade:** the EU approves a trade pact with Indonesia.
- **Briefs:** Cyclone Akvan nears Odisha; the U.S. and Venezuela
  restore military ties; South Korea's Suneung exam under AI-cheating
  curbs.

Every item was checked against same-day roundups (One Turn,
SimpleLife, Reuters, BBC, Pollar / The News Booth) before drawing.
The ICJ ruling is due today at 10:00 in The Hague, so the poster says
only that the court rules today — it claims no outcome.

## How it works

- `build_poster.py` renders `poster.png` (1024×1024) with Pillow from
  the day's wire reports. It runs once, at build time, on the author's
  machine; rendering is deterministic (fixed fonts, no clock, no
  randomness).
- `main.py` is the submitted program (Python 3.13, standard library
  only). It copies `poster.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output/entry.png`), byte for byte, so repeated runs write
  identical bytes.

## License

MIT — see `LICENSE`.
