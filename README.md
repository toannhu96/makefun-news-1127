# makefun-news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/toannhu96/makefun-news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/toannhu96/makefun-news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One image that sums up the world's news of Friday 27 November 2026. The entry is
a Node 22 program: `main.ts` writes the finished front page to `/output/entry.png`
(1024x1024, under 1 MiB) and fails loudly rather than leaving a partial file when
any gate check does not hold. Two runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`tools/build.py` renders the page: it asserts that every text line fits its box
and that every text/background pair clears 4.5:1 contrast, so a layout that would
overflow or wash out fails the build instead of shipping.

## What the page says

The lead is labelled `STATEMENTS · UNVERIFIED`: Trump's statement that Putin is
ready for a deal and Zelensky's warning of a new Russian mass strike, each shown
as an attributed box with a footnote that neither is independently confirmed.
Cards: the Thanksgiving storm (70 mph), the EU budget summit (EUR 1.6tn), US
tariffs on 14 partners, and an ALLEGED North Korean pause in aid to Russia (a
claim by Ukrainian intelligence). A ticker adds the Bank of England and Lithuania
items. Sources: Reuters items as carried by The Standard (HK) morning recap and
SBS News, 27 Nov 2026.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
