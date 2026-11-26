---
title: Arrays and Exclusion Zone Rebuilding
description: Arknights Endfield arrays give Cuprium and Xiranite L, T or E forms in Wuling for Exclusion Zone Rebuilding.
appliesTo: "Arknights: Endfield, global service, Version 1.7; array, recipe and rebuilding data from game data 1.7"
caveat: "Arrays stack only when they overlap completely: two arrays of one kind raise the tier, and an L-Array on a T-Array makes an E-Array only after the AIC technology L/T Stacking."
lastVerified: 2026-11-26
effectiveDate: 2026-11-25
aliases:
  - 陣列與重建禁區
  - 阵列与重建禁区
  - 陣と封鎖区域再建
  - 배열과 금지 구역 재건
  - Forge of Luminance
  - Forge of Equilibrium
  - 明晦爐
  - 平衡爐
sources:
  - title: Meeting You in the World o'Shrooms Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/0740
  - title: warfarin.wiki, in-game tutorial Forge of Luminance (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_ming
  - title: warfarin.wiki, in-game tutorial T-Array (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_hui
  - title: warfarin.wiki, in-game tutorial E-Array (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_heng
  - title: warfarin.wiki, in-game tutorial Bipolar Forge of Luminance (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_2
  - title: warfarin.wiki, in-game tutorial Forge of Equilibrium (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_balancer_1
  - title: warfarin.wiki, in-game tutorial Rebuilding Supply Port (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_wonder_supply_port_1
  - title: warfarin.wiki, in-game tutorial Efficient Lucidolite Production (game data 1.7)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_copper_bright_cube
  - title: "Array tables FactoryFormationTable, FactoryFormationLevelTable and FactoryFormationTransTable (game data 1.7): array kinds, tiers and infusion chances"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationTransTable.json
  - title: "Forge table FactoryFormationStakeTable (game data 1.7): Xiragen and array areas"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationStakeTable.json
  - title: "Facility table FactoryBuildingTable (game data 1.7): power use, ports and footprint"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryBuildingTable.json
  - title: "Recipe table FactoryMachineCraftTable (game data 1.7): Forge of Equilibrium and rebuilding materials"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryMachineCraftTable.json
  - title: "AIC Factory Plan table FacSTTNodeTable (game data 1.7): array technologies"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FacSTTNodeTable.json
  - title: "Rebuilding table WonderStageTable (game data 1.7): phases and materials"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/WonderStageTable.json
---

## Facilities

| Facility | Power use | Footprint | What it does |
| --- | --- | --- | --- |
| Forge of Luminance | — | 5 × 5 | Projects 1 array (L or T) in front of it |
| Bipolar Forge of Luminance | — | 5 × 5 | Projects 2 arrays, one in front and one to its side |
| Forge of Equilibrium | 50 | 5 × 5 | Combines the L and T forms of a material into a new one; 5 belt inputs and 5 outputs |
| Rebuilding Supply Port | — | 3 × 3 | Sends the rebuilding materials it takes to the Rebuilding Depot of the North Wuling Exclusion Zone |

All four are built only in Wuling. A Forge of Luminance needs no power: it is activated by a steady flow of Xiragen into its pipe port, at the same minimum flow rate as the Activation Port of the Solid-Gas Transmuting Unit. Each array covers an area of 5 × 5 at a fixed distance from the forge.

## Arrays

| Array | 繁體中文 | 簡體中文 | Made by | Turns Cuprium into | Turns Xiranite into |
| --- | --- | --- | --- | --- | --- |
| L-Array | 陣列·明 | 阵列·明 | A Forge of Luminance | L-Cuprium | Luminarite |
| T-Array | 陣列·晦 | 阵列·晦 | A Forge of Luminance, after Expansion: Turbid | T-Cuprium | Turbidarite |
| E-Array | 陣列·衡 | 阵列·衡 | An L-Array and a T-Array stacked completely, after L/T Stacking | Equprium | Equiranite |

An array acts on the Cuprium and Xiranite that transport belts carry through its area. At fixed intervals it infuses its property into them, and each infusion succeeds with the chance of the array's tier.

## Tiers and infusion chance

| Array | T1 | T2 | T3 | T4 |
| --- | --- | --- | --- | --- |
| L-Array | 20% | 40% | 60% | 100% |
| T-Array | 20% | 40% | 60% | 100% |
| E-Array | 40% | 80% | — | — |

Arrays of the same kind that overlap completely stack and raise the tier, up to T4: two L-Arrays stacked completely make an L-Array T2. Arrays that overlap only in part do not stack. The two arrays of a Bipolar Forge of Luminance stack with the two of a second one, and both rise a tier at once.

## Forge of Equilibrium recipes

| Inputs | Output | Time |
| --- | --- | --- |
| Luminarite ×5, Turbidarite ×5 | Heavy Xiranite ×2 | 10 s |
| L-Cuprium ×10, T-Cuprium ×10 | Hetonite ×5 | 10 s |
| Equiranite ×10, Equprium ×10 | Lucidolite ×5 | 10 s |

## Rebuilding materials

| Material | Facility | Inputs | Output | Time |
| --- | --- | --- | --- | --- |
| L-Cuprium Part | Fitting Unit | L-Cuprium ×1 | L-Cuprium Part ×1 | 2 s |
| T-Cuprium Part | Fitting Unit | T-Cuprium ×1 | T-Cuprium Part ×1 | 2 s |
| Lucidolite Part | Fitting Unit | Lucidolite ×1 | Lucidolite Part ×1 | 2 s |
| CuPKG Luminarite Component | Packaging Unit | L-Cuprium Part ×10, Luminarite ×5 | CuPKG Luminarite Component ×5 | 10 s |
| CuPKG Heavy IC | Packaging Unit | T-Cuprium Part ×15, Heavy Xiranite ×2 | CuPKG Heavy IC ×5 | 10 s |
| Lucidolite Energy Brick | Packaging Unit | Lucidolite Part ×5, Dense Originium Powder ×5 | Lucidolite Energy Brick ×5 | 10 s |

Lucidolite also comes from gas: a Gas Reactor Globe turns Equprium Gas ×1 and Equiragen ×1 into Clean Lucidolite Gas ×2, and a Solid-Gas Transmuting Unit turns Clean Lucidolite Gas ×2 into Lucidolite ×2. Equprium Gas and Equiragen are made from Equprium and Equiranite in the Solid-Gas Transmuting Unit.

## Exclusion Zone Rebuilding

| Phase | Materials taken |
| --- | --- |
| 1, Rebuilding: South | CuPKG Luminarite Component |
| 2, Rebuilding: North | CuPKG Luminarite Component, CuPKG Heavy IC |
| 3, Array Ignition | CuPKG Luminarite Component, CuPKG Heavy IC, Lucidolite Energy Brick |
| 4, Routine Maintenance | CuPKG Luminarite Component, CuPKG Heavy IC, Lucidolite Energy Brick |

The mode unlocks with the side mission Rebuilding a Home II. Phases 1 and 2 build a Tianshi Pillar Array in the south and then the north of the North Wuling Exclusion Zone, phase 3 ignites the two, and phase 4, the last, maintains them. Materials reach the Rebuilding Depot through Rebuilding Supply Ports; it holds up to 8,000 of each. The rebuilding raises Wuling's Regional Development (see [Regional Development](/aic/regional-development/)).

## AIC technologies

| Technology | Requires | AIC Plan | Unlocks | Opens with progress in |
| --- | --- | --- | --- | --- |
| Forge Ignition | — | Wuling AIC I | Forge of Luminance, L-Array | — |
| Rebuilding Supply | Forge Ignition | Wuling AIC I | Rebuilding Supply Port | Rebuilding a Home II |
| Expansion: Turbid | Rebuilding Supply | Wuling AIC II | T-Array | Rebuilding a Home II |
| L/T Equilibrium | Expansion: Turbid | Wuling AIC II | Forge of Equilibrium | Rebuilding a Home II |
| L/T Stacking | L/T Equilibrium | Wuling AIC III | E-Array | Rebuilding a Home III |
| Forge Bipolarity | L/T Stacking | Wuling AIC III | Bipolar Forge of Luminance | Rebuilding a Home III |

Researching a technology that unlocks a facility also gives two of that facility.
