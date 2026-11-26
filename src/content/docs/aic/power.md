---
title: AIC power
description: How AIC power works in Arknights Endfield, from the PAC and Thermal Banks to batteries and pylons.
appliesTo: "Arknights: Endfield, global service, Version 1.7; facility and recipe data from game data 1.7"
caveat: A blueprint places facilities, not power. Every facility it adds draws from the region's grid, and only Thermal Banks fed with Originium Ore or batteries raise the grid's output.
lastVerified: 2026-11-26
effectiveDate: 2026-11-25
aliases:
  - 集成工業電力
  - 集成工业电力
  - 集成工業の電力
  - 통합 공업 전력
sources:
  - title: warfarin.wiki, in-game tutorial Thermal Bank (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_power_sta
  - title: warfarin.wiki, in-game tutorial Backup Power (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_backup_power
  - title: "warfarin.wiki, in-game tutorial Protocol Automation-Core: Power Reserves Depletion (game data 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_zero_power
  - title: "warfarin.wiki, in-game tutorials Relay Tower: Power Transmission and Relay Tower: Power Supply (game data 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_power_link
  - title: "warfarin.wiki, in-game tutorials Electric Pylon: Power Supply and Electric Pylon: Power Transmission (game data 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_hub_plink
  - title: warfarin.wiki, in-game tutorial Blueprint (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_blueprint
  - title: warfarin.wiki, Packaging Unit (game data 1.7)
    url: https://warfarin.wiki/en/facilities/tools_assebling_mc_1
  - title: warfarin.wiki, Thermal Bank (game data 1.7)
    url: https://warfarin.wiki/en/facilities/power_station_1
  - title: warfarin.wiki, Xiranite Pylon (game data 1.7)
    url: https://warfarin.wiki/en/facilities/power_diffuser_2
  - title: warfarin.wiki, Xiranite Relay (game data 1.7)
    url: https://warfarin.wiki/en/facilities/power_pole_3
  - title: warfarin.wiki, Facilities (game data 1.7)
    url: https://warfarin.wiki/en/facilities
  - title: Endfield Talos Wiki, Thermal Bank
    url: https://endfield.wiki.gg/wiki/Thermal_Bank
  - title: Endfield Talos Wiki, Automated Industry Complex
    url: https://endfield.wiki.gg/wiki/Automated_Industry_Complex
  - title: Endfield Talos Wiki, Facility/Power
    url: https://endfield.wiki.gg/wiki/Facility/Power
  - title: Endfield Talos Wiki, Blueprint
    url: https://endfield.wiki.gg/wiki/Blueprint
  - title: Old Deep Water Dies, by Rising Tide It is Denied Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/8907
  - title: Sketches of Lost Heirlooms Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/0758
  - title: Sketches of Lost Heirlooms Version DEV Comm
    url: https://endfield.gryphline.com/en-us/news/9577
  - title: Homecoming Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/5200
  - title: Sanctuary of Ink Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/9560
  - title: "Fuel table FactoryFuelItemTable (game data 1.7): HC Wuling Battery"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFuelItemTable.json
  - title: "Recipe table FactoryMachineCraftTable (game data 1.7): HC Wuling Battery"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryMachineCraftTable.json
---

## Why a factory runs out of power

A factory runs out of power when its facilities draw more than the region's grid generates. The grid's source is the Protocol Automation-Core (PAC), and Thermal Banks raise its output only while they burn Originium Ore or batteries. When demand stays above output, the PAC's power reserve drains; at zero, Backup Power can keep everything running for 30 minutes, then the region has a power outage. A blueprint adds facilities and their power use at once, but no generation.

## Why a factory is out of power after placing a blueprint

| Cause | Explanation |
| --- | --- |
| Demand rose | Each facility draws its power use from the grid (see Power use by facility). A blueprint places a preset layout of many facilities in one action. |
| Output did not rise | The PAC is the only source of the grid. Every region starts with 200 power; more comes only from Thermal Banks connected to the grid and fed fuel. |
| A facility is outside a pylon's range | Most facilities work only inside the supply radius of an Electric Pylon connected to the grid. Pylons in a Core AIC Area join the grid on their own. |
| Part of the blueprint is not built | Facilities you did not have are placed as an Unconstructed Set and become real facilities only when you submit the missing ones. |

To fix it, build more Thermal Banks and feed them, or switch facilities off. In top view mode, bulk actions switch many facilities off at once.

## What a blueprint brings and what it does not

| A blueprint brings | A blueprint does not bring |
| --- | --- |
| The facilities and their arrangement, placed in a Core AIC Area | Power: every facility in it draws from the grid of the region where it is placed |
| Facilities from your stock, including stock held in other regions | Facilities you lack: they stay an Unconstructed Set until submitted |
| The connection state of conduits (since Version 1.4) and the Multi-Clog Auto-Fix setting of the Expanded Crucible (since Version 1.3) | The PAC or a Sub-PAC, which cannot be part of a blueprint |

A blueprint is at most 50 by 50 tiles. A blueprint with a facility that has a regional limit, such as Forge of the Sky, cannot be placed if it would pass that limit, even as an unconstructed facility.

## Backup Power

| Rule | Value |
| --- | --- |
| Added | Version 1.3 |
| Becomes available | When the PAC's power reserve is at zero and generation is below consumption |
| Effect | All AIC facilities of the region keep running as normal |
| Duration | 30 minutes |
| Cooldown | 12 hours after it ends |
| Auto-activation | On by default when a region loses power while you are online; can be switched off and Backup Power started by hand |

If generation is still too low when the 30 minutes end, the region goes into a power outage.

## Thermal Bank fuel

A Thermal Bank must be connected to the grid to work, and turns Originium Ore or batteries into power.

| Fuel | Burn time per item | Power while burning | Items per hour |
| --- | --- | --- | --- |
| Originium Ore | 8 s | 50 | 450 |
| LC Valley Battery | 40 s | 220 | 90 |
| SC Valley Battery | 40 s | 420 | 90 |
| HC Valley Battery | 40 s | 1100 | 90 |
| LC Wuling Battery | 40 s | 1600 | 90 |
| SC Wuling Battery | 40 s | 3200 | 90 |
| HC Wuling Battery | 40 s | 6400 | 90 |

## Battery recipes

All six batteries are made in the Packaging Unit (power use 20). Each recipe gives 1 battery in 10 seconds. HC Wuling Battery came with game data 1.7.

| Battery | Inputs | Time | Output |
| --- | --- | --- | --- |
| LC Valley Battery | Amethyst Part ×5, Originium Powder ×10 | 10 s | 1 |
| SC Valley Battery | Ferrium Part ×10, Originium Powder ×15 | 10 s | 1 |
| HC Valley Battery | Steel Part ×10, Dense Originium Powder ×15 | 10 s | 1 |
| LC Wuling Battery | Xiranite ×5, Dense Originium Powder ×15 | 10 s | 1 |
| SC Wuling Battery | Xircon ×5, Dense Originium Powder ×20 | 10 s | 1 |
| HC Wuling Battery | Equiranite ×5, Dense Originium Powder ×20 | 10 s | 1 |

### Inputs of the Wuling batteries

| Input | Facility | Recipe |
| --- | --- | --- |
| Originium Powder | Shredding Unit | Originium Ore ×1 to Originium Powder ×1, 2 s |
| Dense Originium Powder | Grinding Unit | Originium Powder ×2 and Sandleaf Powder ×1 to Dense Originium Powder ×1, 2 s |
| Xiranite | Forge of the Sky | Carbon ×1 and Clean Water ×1 to Xiranite ×1, 2 s; or Stabilized Carbon ×2 and Clean Water ×1 to Xiranite ×1, 2 s |
| Xiranite | Solid-Gas Transmuting Unit | Xiragen ×1 to Xiranite ×1, 2 s |
| Xircon | Reactor Crucible or Expanded Crucible | Xircon Effluent ×2 and Ferrium Powder ×1 to Xircon ×1 and Sewage ×1, 2 s |

## Power transmission

The PAC is the origin of the grid. Every power facility in a region must link back to it, through Relay Towers or pylons.

| Facility | Region | Role | Distance |
| --- | --- | --- | --- |
| Relay Tower | Any | Carries power to other Relay Towers, Electric Pylons and Electric Nexuses. Outside a Core AIC Area it powers no facilities until an AIC Factory Plan technology lets it supply a small area. | Connects within 80 m; since Version 1.1 the wire stays connected up to 100 m (was 90 m) |
| Electric Pylon | Any | Powers all facilities in its supply radius once it is on the grid. A researched technology also lets it carry power, for spots where a Relay Tower does not fit. | Carries power 30 m after research; since Version 1.1 the wire stays connected up to 50 m (was 40 m) |
| Xiranite Relay | Wuling only | Carries power and supplies nearby facilities | Connects on its own to the PAC and any Xiranite power facility within 80 m; inside a Core AIC Area to the PAC at any distance |
| Xiranite Pylon | Wuling only | Supplies facilities in range and carries power over short distances | Connects on its own to the PAC and Xiranite Relays within 80 m, to Xiranite Pylons and other power facilities within 30 m; inside a Core AIC Area to the PAC at any distance |

Since Version 1.3, Xiranite Pylons and Relays inside a Core AIC Area can connect to Xiranite facilities outside it. A Sub-PAC powers the Electric Pylons in its own Core AIC Area.

## Power use by facility

| Power use | Facilities |
| --- | --- |
| 100 | Expanded Crucible |
| 50 | Waste Treatment Unit, Grinding Unit, Reactor Crucible, Forge of the Sky, Purification Unit, Fluid-Gas Transmuting Unit, Solid-Gas Transmuting Unit, Gas Reactor Globe |
| 20 | Acid Resistant Pump Mk II, Fitting Unit, Planting Unit, Filling Unit, Packaging Unit, Separating Unit |
| 10 | Electric Mining Rig Mk II, Fluid Pump, Moulding Unit, Seed-Picking Unit, Gearing Unit, Sprinkler, Fluid Supply Unit |
| 5 | Electric Mining Rig, Protocol Stash, Refining Unit, Shredding Unit, Zipline Pylon, Zipline Tower |
| 0, must be on the grid | Electric Pylon, Xiranite Pylon, Relay Tower, Xiranite Relay, Thermal Bank |
| No grid needed | Portable Originium Rig, Hydro Mining Rig, Gas Extractor, Gas Dispersing Unit, Depot Loader, Depot Unloader, Depot Bus Port, Depot Bus Section, Fluid Tank, Gas Tank, Conduit Inlet, Conduit Outlet |

Batteries are also bought by outposts for Stock Bills: see [Regional Development](/aic/regional-development/).
