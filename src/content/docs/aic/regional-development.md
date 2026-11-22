---
title: Regional Development
description: Regional Development in Arknights Endfield covers outposts, Stock Bills, Depot Nodes and Regional Transfer.
appliesTo: "Arknights: Endfield, global service, Version 1.6; tutorial text from game data 1.6"
caveat: Regional Transfer unlocks by the Regional Development Level of the source region. Stockpile Transfer takes the goods out of the source depot; only Metastorage Transfer, unlocked at a higher level, leaves them there.
lastVerified: 2026-11-21
effectiveDate: 2026-10-15
aliases:
  - 地區建設
  - 地区建设
sources:
  - title: warfarin.wiki, in-game tutorial Regional Transfer (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_domain_transport
  - title: warfarin.wiki, in-game tutorial Regional Development System (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_domain
  - title: warfarin.wiki, in-game tutorial Outpost Supplies (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_settlement
  - title: warfarin.wiki, in-game tutorials Stock Redistribution and Elastic Goods (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_domain_shop_1
  - title: warfarin.wiki, in-game tutorials Depot Node, Pack Goods and Delivery Job Transfer (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_domain_depot_2
  - title: warfarin.wiki, in-game tutorials Regional Depot and Expansion Management System (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_map_storage
  - title: Endfield Talos Wiki, Regional Development
    url: https://endfield.wiki.gg/wiki/Regional_Development
  - title: Endfield Talos Wiki, Automated Industry Complex
    url: https://endfield.wiki.gg/wiki/Automated_Industry_Complex
  - title: Endfield Talos Wiki, Thermal Bank
    url: https://endfield.wiki.gg/wiki/Thermal_Bank
  - title: Endfield Talos Wiki, Outpost
    url: https://endfield.wiki.gg/wiki/Outpost
  - title: Endfield Talos Wiki, Stock Redistribution
    url: https://endfield.wiki.gg/wiki/Stock_Redistribution
  - title: Endfield Talos Wiki, Depot Node
    url: https://endfield.wiki.gg/wiki/Depot_Node
  - title: Old Deep Water Dies, by Rising Tide It is Denied Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/8907
  - title: At the Wake of Spring Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/0751
  - title: Sketches of Lost Heirlooms Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/0758
  - title: Homecoming Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/5200
  - title: Sanctuary of Ink Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/9560
  - title: Sanctuary of Ink Version DEV Comm
    url: https://endfield.gryphline.com/en-us/news/7014
---

Regional Development is the progress of each region, Valley IV and Wuling, measured by its Regional Development Level. The level rises with Regional Development Metric, earned by exploring and by supplying goods to outposts, and it unlocks functions such as Regional Transfer, raises ore yields and raises how many facilities can be placed. Outposts pay Stock Bills for AIC products; Stock Bills buy goods at Stock Redistribution and pay for upgrades of Depot Nodes, terminals and the Core AIC Area.

## Regional Transfer: moving goods from Wuling to Valley IV and back

Regional Transfer sends items from the depot of one region to the depot of another. It is set at the PAC, under Protocol Management. Each mode unlocks at a Regional Development Level of the source region:

| Mode | Source depot | Destination depot | Unlocks |
| --- | --- | --- | --- |
| Stockpile Transfer | Loses the goods sent | Gains the same amount | At a set level of the source region |
| Metastorage Transfer | Keeps its goods | Gains the goods | At a higher level of the source region |

Once a transfer is set, items move continuously, once every hour. With Valley IV as the source region:

| Valley IV level | Regional Transfer |
| --- | --- |
| 8 | Unlocked, total transfer value 800 |
| 9 | 900 |
| 10 | 1,000 |
| 11 | 1,200 |
| 12 | 1,500, and Metastorage Transfer unlocked |

Running a Valley IV Thermal Bank on Wuling batteries:

- Goods sent by Regional Transfer arrive in the Valley IV depot. From the depot, an output port of the PAC or a Sub-PAC, or a Depot Unloader, sends a chosen item onto a belt toward the Thermal Bank.
- LC and SC Wuling Battery are Thermal Bank fuels, at 1600 and 3200 power, each burning for 40 seconds: one Thermal Bank uses 90 batteries an hour.
- Both Wuling batteries are made in the Packaging Unit: recipes on [AIC power](/aic/power/).

## Outposts and Stock Bills

| Topic | Rule |
| --- | --- |
| What an outpost does | Once contact is made, Outpost Supplies opens: the outpost builds up Stock Bills over time, and you earn them by trading it the goods it needs |
| Limit | Stock Bills build up to a cap and stop there until you trade; when an outpost's Stock Bills run out, trading waits until they build up again |
| Prosperity | Trades earn Outpost Prosperity; enough of it raises the Prosperity Level, after which the outpost asks for more and better goods and pays more |
| Sub-PAC | Each outpost starts with a Sub-PAC |
| Liaison | An operator can be assigned as Liaison; a match of faction, hobby and expertise improves the outpost |
| Area defense | At the Early Warning Terminal; each cleared level raises Stock Bill build-up |

Valley Stock Bills are spent at Valley IV Stock Redistribution, Wuling Stock Bills at Wuling Stock Redistribution. Regional Stock Bills also pay for Core AIC Area upgrades at the AIC Steward, which make the area bigger.

Wuling has three outposts: Sky King Flats Construction Site (level cap raised in Versions 1.1 and 1.3), Cardiac Remediation Station (added in 1.2) and Xiranflow Cloudseeder Station (added in 1.4, Wuling - Yinglung Pass). Valley IV has three outposts as well.

Batteries that outposts buy:

| Battery | Price | Outposts that buy it |
| --- | --- | --- |
| LC Valley Battery | 30 Valley Stock Bills | 1 of 3 in Valley IV |
| SC Valley Battery | 30 Valley Stock Bills | 3 of 3 in Valley IV |
| HC Valley Battery | 70 Valley Stock Bills | 3 of 3 in Valley IV |
| LC Wuling Battery | 25 Wuling Stock Bills | 2 of 3 in Wuling |
| SC Wuling Battery | 54 Wuling Stock Bills | 3 of 3 in Wuling |

## Stock Redistribution and Elastic Goods

- Stock Redistribution sells items for Stock Bills at a discount. Adding Stock Redistributors or upgrading them unlocks more items.
- Items have stock limits, some refresh weekly, and terminals are upgraded with Stock Bills.
- Elastic Goods change price every day: buy low, sell high. Prices on a friend's ship differ from local prices, so you can sell your stock there. Elastic Goods open when the first terminal of a region reaches level 2.

## Depot Nodes and Pack and Deliver

- Unlocking and upgrading Depot Nodes raises the storage capacity of the regional depot. Valley IV has three nodes and Wuling two; the second Wuling node, in Wuling - Test Area, came in Version 1.2.
- Pack and Deliver: pack goods at a Depot Node, carry them from the Pick-Up Point to the Delivery Point, and earn Stock Bills. The goods should arrive intact, and zipline facilities make delivery faster and safer. There is a daily limit on accepted jobs. Upgraded nodes unlock more kinds of goods and bigger packages.
- A delivery job you accepted can be transferred to other players from the Mission screen. When another player completes it, both of you receive the same final fee.

Two sources disagree on a transferred job that is not finished in time. The in-game tutorial says both players still receive half the final fee in Stock Bills. The Version 1.6 DEV Comm says that since 1.6 a transferred job that nobody accepts within a set time is taken over and completed by other helpers.

## Regional Development Level

| Topic | Rule |
| --- | --- |
| How it rises | Regional Development Metric, from exploring, supplying goods to outposts, placing Mining Rigs on new mineral beds, upgrading outposts, Recycling Stations, Stock Redistribution Terminals, Depot Nodes and monitoring stations, and missions |
| What it raises | New functions, mineral ore yields and facility placement limits: per-area Protocol Capacity, Zipline Placement Limit, Combat Facility Limit and mineral purity |
| Example | Wuling City Protocol Capacity 200, then 250 at level 3, 300 at level 5 and 350 at level 7, its maximum |
| Level caps | Valley IV goes up to level 12. Every version from 1.1 to 1.6 raised the cap of Wuling |
| Overview | Since Version 1.3, Regional Overview on the Regional Development screen shows Stock Redistribution, Depot Nodes and their places on the map |

Protocol Capacity itself is explained on [Production and logistics](/aic/production/).
