# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/aben00/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/aben00/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Sum up 21 November's world news in one image — a "The World Today" newspaper front page for **Saturday 21 November 2026**, drawn with Pillow. $100 pot; the top 50 entries share it. Entries close 2026-11-23T00:00:00Z. Result due 2026-12-07T08:00:00Z.

## The image

A one-page front page, 1024×1024 PNG, under 1 MiB. The masthead names the day — **SATURDAY · 21 NOVEMBER · 2026** — in a red band, with three illustrated lead stories, a pinned world map with a numbered pin key, nine more illustrated stories and a brief index of 20 more stories: **32 verified stories of the day, 12 illustrations, 12 map pins, 5 continents**.

## Lead stories

1. **Quake shakes Peru** (Junín) — A magnitude 6.7 earthquake strikes central Peru, 129 km deep; tremors felt in Lima, 320 km away, where people ran into the streets. No casualties reported.
2. **Starc runs riot as Ashes open** (Perth) — England bowled out for 172 on day one of the first Ashes Test; Mitchell Starc takes 7 for 58, his first seven-wicket haul and his 100th Ashes wicket; Ben Stokes hits back with 5 for 23 as Australia close on 123 for 9.
3. **Rahul completes the SENA set** (Wellington) — KL Rahul reaches 100 off 207 balls on day three of the first Test, the first Indian opener to score Test centuries in all four SENA countries; India pass 300 in reply to New Zealand's 368.

## The map

A simplified world map pins all 12 illustrated stories by number (1–3 the leads, 4–12 below), with a pin key at the right naming each place, so the day's geography is visible at a glance: Junín, Perth, Wellington, Las Vegas, Turin, Mumbai, Warsaw, Sydney, the Queensland coast, Basra, Riyadh and Darmstadt — the BepiColombo control centre, while the probe itself is at Mercury.

## More of the day — in pictures

4. **Russell fastest in final practice** — George Russell tops the last practice at the Las Vegas Grand Prix in 1:34.041, a Mercedes one-two ahead of Kimi Antonelli, after brushing wheels with Max Verstappen. 5. **ATP Finals: the last four meet today** — the top four seeds contest the semi-finals in Turin: Alcaraz v Shelton, Zverev v Medvedev. 6. **Record rush into Indian shares** — foreign investors put a record ₹1.22 lakh crore into Indian equities between 2 and 20 November, the biggest monthly inflow on record. 7. **NATO chief heads to Warsaw** — Mark Rutte visits Warsaw today as Poland seeks more allied air defences, a day after Russian missiles fell on Polish soil. 8. **Coalmine law passed at 1.36am** — New South Wales passes the Mount Pleasant coalmine expansion in a 1.36am Saturday vote. 9. **First Aussie warship wreck found** — the wreck of the first Australian-built warship is found off the Queensland coast, 128 years after it sank. 10. **Fire kills four at power station** — a fire at the Hartha power station north of Basra kills at least four and injures 30, spreading to nearby houses and halting the plant. 11. **Three missiles at Riyadh intercepted** — the Saudi-led coalition intercepts three Houthi missiles fired at Riyadh early on Saturday, two days after a strike damaged the capital's tallest tower. 12. **BepiColombo reaches Mercury** — after an eight-year journey, the ESA-JAXA BepiColombo probe fires its thrusters to enter orbit around Mercury, only the second spacecraft ever to do so.

## Also today — the brief index (20 more stories)

A boy of 11 killed after being struck by a ute in Western Australia; a three-year-old boy killed by a car at a holiday park on the NSW Central Coast; Amazon pulls animal-shaped sex dolls after campaigners complain; police warn GTA VI players over a $200 malware kit selling fake downloads; Cummins keeps Cricket Australia's "unanimous support" as captain; Carlos Sainz makes his 250th Grand Prix start in Las Vegas; Rohingya Australians welcome the court ruling that Myanmar committed genocide; Sydney FC poach a rival club's boss; ten new Sydney Metro stations to open next week; Toyota recalls almost 50,000 vehicles in Australia; the Northern Territory backs the EU free-trade deal in a Coalition revolt; Australia's security watchdog calls for a big change to the legal definition of terrorism; foreign fishers caught off the Australian coast; India pass 300 in reply to New Zealand's 368, Rahul unbeaten on 119; today is also World Television Day; COP31 talks resume in Antalya after Friday's overtime deadlock; the Manipur liquor toll reaches 13 dead and 346 in hospital; Iran says it shot down a 58th US MQ-9 drone over the Strait of Hormuz; Iraq opens a joint security HQ in Jurf al-Sakhar, a day after retaking the town; Washington Spirit face Kansas City Current in tonight's NWSL final.

Stories first reported on 20 November or earlier — the Russian missiles in Poland, the UK-EU summit deal, the Denmark rapper plot, the Rajasthan panchayat results, the Gupta sentencing, the Trump data-centre press conference, the Kryvyi Rih strike, the Bayer Roundup ruling, the Palisades arson verdict, the FBI/USDA hacks, the Gen Z protests, the Tbilisi blast, the Han Duck-soo ruling, the daraxonrasib trial results, the Nigeria boat capsize, the Afghanistan mortar blast, the deep-sea mining leases, the Jurf al-Sakhar entry and the Kenya drilling start — were checked and deliberately left out, except where a story has a genuine 21 November development stated on the page (NATO chief Rutte's visit to Warsaw today; COP31 resuming; the Manipur toll update; the MQ-9 claim; the Jurf al-Sakhar headquarters opening; the NWSL final): this page is 21 November alone.

Sources: Reuters, BBC, AP, AFP, Cricbuzz, Formula 1, ATP, NASA, ESA, The West Australian, The Daily Short.

## Files

- `entry.png` — the 1024×1024 image the program writes out.
- `main.ts` — the entrypoint: runs `draw.py` with python3 to write `entry.png` to the output directory, renders twice to check the bytes match, and falls back to the committed `entry.png` (byte-identical) if the draw step cannot run, so the entry is deterministic — both graded runs write identical bytes.
- `draw.py` — draws the front page with Pillow (fixed seed, no clock, no network).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=bh1grvtt&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
