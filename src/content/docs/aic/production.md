---
title: Production and logistics
description: How AIC facilities in Arknights Endfield take inputs, run recipes and pass items by belt, pipe and depot.
appliesTo: "Arknights: Endfield, global service, Version 1.6; facility and recipe data from game data 1.6"
caveat: Transport belts can be placed only inside a Core AIC Area. Facilities placed outside it use the region's Protocol Capacity, and when that is used up no more facilities can be placed in the region.
lastVerified: 2026-11-22
effectiveDate: 2026-10-15
aliases:
  - 生產與物流
  - 生产与物流
sources:
  - title: "Recipe table FactoryMachineCraftTable (game data 1.6): recipe counts"
    url: https://github.com/rmxlinux/EndfieldData/blob/d847759f71d4549aba4727b3b0ac1a1ad0e37742/TableCfg/FactoryMachineCraftTable.json
  - title: "warfarin.wiki, in-game tutorials Facility: Processing and Facility: Production Formulas (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_formula
  - title: warfarin.wiki, in-game tutorial Input and Output Ports (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_port
  - title: "warfarin.wiki, in-game tutorial Transport Belt: Placement Restrictions (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_belt
  - title: warfarin.wiki, in-game tutorials Splitter, Converger and Belt Bridge (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_splitter
  - title: warfarin.wiki, in-game tutorial Pipeline (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_pipe
  - title: warfarin.wiki, in-game tutorial Depot Bus (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_usb_loader_unloader
  - title: warfarin.wiki, in-game tutorial Protocol Capacity and Restrictions (game data 1.6)
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_bandwidth
  - title: warfarin.wiki, Facilities (game data 1.6)
    url: https://warfarin.wiki/en/facilities
  - title: warfarin.wiki, Protocol Stash (game data 1.6)
    url: https://warfarin.wiki/en/facilities/storager_1
  - title: warfarin.wiki, Expanded Crucible (game data 1.6)
    url: https://warfarin.wiki/en/facilities/mix_pool_2
  - title: Endfield Talos Wiki, Automated Industry Complex
    url: https://endfield.wiki.gg/wiki/Automated_Industry_Complex
  - title: At the Wake of Spring Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/0751
  - title: Sketches of Lost Heirlooms Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/0758
  - title: Homecoming Version Update Notes
    url: https://endfield.gryphline.com/en-us/news/5200
---

A production facility turns inputs into outputs by recipe (production formula). It runs one recipe at a time and starts as soon as the items in it match one of its recipes. Items reach it by transport belt from other facilities or from the depot, fluids by pipe, and products leave by belt toward the next facility, a Depot Loader or a Protocol Stash.

## How a facility takes inputs and gives outputs

- The PAC, the Sub-PAC and most production facilities have input ports and output ports. A belt from an output port moves items out; a belt into an input port moves items in.
- The PAC and Sub-PAC ports are connected to the region's depot: choose an item on an output port and it unloads that item from the depot. Other facilities' ports reach only their own storage.
- You can also drag items from the Backpack or depot into a facility by hand and take the products back.
- A facility's panel shows input ports and incoming materials on the left, output ports and outgoing products on the right.
- When a facility is clogged, it stops loading and unloading, and the panel shows a warning.
- In Wuling some facilities have a fluid mode with fluid ports for pipes; switching mode changes the recipes the facility can run. Since Version 1.4 the mode can be chosen before placing the facility.

## Logistics units

| Unit | What it does | Limits |
| --- | --- | --- |
| Transport belt | Moves items between facilities | Core AIC Area only; must start from a facility or a placed belt |
| Belt Bridge | Lets one belt cross another without mixing them | |
| Splitter | Splits one belt evenly into up to 3 | |
| Converger | Merges up to 3 belts into one | |
| Pipeline | Carries fluids between fluid ports | Length limit per section; a pipe support at the end starts the next section |
| Conduit Inlet and Conduit Outlet | Carry fluids underground between a matching pair | 300 m in a straight line since Version 1.4 (was 200 m) |
| Depot Bus Port and Depot Bus Section | The Depot Bus: the port is its origin, sections extend it | Port anywhere in the Core AIC Area; sections connect to the port or an active section |
| Depot Unloader | Sends a chosen depot item out onto a belt | Placed right next to the Depot Bus |
| Depot Loader | Stores items that arrive by belt in the depot | Placed right next to the Depot Bus |
| Protocol Stash | Holds items and, when powered, teleports them to the depot; often the end of a line | Power use 5 |
| Fluid Tank and Gas Tank | Store fluids and gases | |

## Protocol Capacity

Every region has its own Protocol Capacity. Placing facilities outside the Core AIC Area uses it up, and each kind of facility uses a different amount. When a region's capacity is used up, no more facilities can be placed there. A higher Regional Development Level raises the limits: see [Regional Development](/aic/regional-development/).

## What each production facility makes

Power use is in power units; the grid is explained on [AIC power](/aic/power/). Every recipe, sorted by product, is on [Recipes by product](/aic/recipes/).

| Facility | Power | Recipes | What it makes |
| --- | --- | --- | --- |
| Refining Unit | 5 | 26 | Metal blocks (Ferrium, Cuprium, Steel), Amethyst and Cryston Fiber, Carbon, Origocrust |
| Shredding Unit | 5 | 18 | Powders from ores and plants, such as Originium Powder, Ferrium Powder, Sandleaf Powder, Flour, Sugar |
| Fitting Unit | 20 | 7 | Parts from metal blocks and fibers, such as Ferrium Part, Steel Part, Amethyst Part, Cuprium Part |
| Moulding Unit | 10 | 7 | Bottles and canisters |
| Planting Unit | 20 | 6 | Plants from seeds |
| Seed-Picking Unit | 10 | 19 | Seeds and cuttings from crops |
| Gearing Unit | 10 | 7 | Gear components |
| Filling Unit | 20 | 84 | Fills bottles and canisters with fluids or gases; also Buck Capsules, Canned Citrome and bottled drinks |
| Packaging Unit | 20 | 11 | All five batteries, Industrial Explosive, Jincao drinks, Yazhen Syringes, Separator Core |
| Grinding Unit | 50 | 7 | Dense and ground powders |
| Reactor Crucible | 50 | 11 | Solutions, Xircon, Hetonite, Liquid Xiranite, feed and seed oil |
| Expanded Crucible | 100 | 11 | The same 11 recipes as the Reactor Crucible, with more ports and several reactions at once |
| Forge of the Sky | 50 | 4 | Xiranite, Heavy Xiranite and Bumper-Rich |
| Purification Unit | 50 | 6 | Purer gases and solutions |
| Separating Unit | 20 | 74 | Empties filled bottles and canisters, giving back the container and the fluid or gas in it |
| Fluid-Gas Transmuting Unit | 50 | 12 | Turns fluids into gases and back; runs on a steady input of Liquid Xiranite |
| Solid-Gas Transmuting Unit | 50 | 10 | Turns solids into gases and back; runs on a steady input of Xiragen |
| Gas Reactor Globe | 50 | 1 | Pyrrolite Gas |

The Water Treatment Unit (power use 50) processes Sewage, and Xircon Effluent and Inert Xircon Effluent at lower efficiency.

## Full recipes of the facilities with few recipes

| Facility | Inputs | Output | Time |
| --- | --- | --- | --- |
| Gas Reactor Globe | Hetonite Gas ×2, Xiragen ×1 | Pyrrolite Gas ×1 | 2 s |
| Forge of the Sky | Xiranite ×10, Xircon Effluent ×5 | Heavy Xiranite ×1 | 10 s |
| Forge of the Sky | Burdo-Muck ×1, Liquid Xiranite ×1 | Bumper-Rich ×1 | 2 s |
| Forge of the Sky | Stabilized Carbon ×2, Clean Water ×1 | Xiranite ×1 | 2 s |
| Forge of the Sky | Carbon ×1, Clean Water ×1 | Xiranite ×1 | 2 s |
| Planting Unit | Buckflower Seed ×1 | Buckflower ×1 | 2 s |
| Planting Unit | Sandleaf Seed ×1 | Sandleaf ×1 | 2 s |
| Planting Unit | Jincao Seed ×1, Clean Water ×1 | Jincao ×2 | 2 s |
| Planting Unit | Aketine Seed ×1 | Aketine ×1 | 2 s |
| Planting Unit | Yazhen Seeds ×1, Clean Water ×1 | Yazhen ×2 | 2 s |
| Planting Unit | Citrome Seed ×1 | Citrome ×1 | 2 s |
| Grinding Unit | Originium Powder ×2, Sandleaf Powder ×1 | Dense Originium Powder ×1 | 2 s |
| Grinding Unit | Ferrium Powder ×2, Sandleaf Powder ×1 | Dense Ferrium Powder ×1 | 2 s |
| Grinding Unit | Carbon Powder ×2, Sandleaf Powder ×1 | Dense Carbon Powder ×1 | 2 s |
| Grinding Unit | Origocrust Powder ×2, Sandleaf Powder ×1 | Dense Origocrust Powder ×1 | 2 s |
| Grinding Unit | Amethyst Powder ×2, Sandleaf Powder ×1 | Cryston Powder ×1 | 2 s |
| Grinding Unit | Citrome Powder ×2, Sandleaf Powder ×1 | Ground Citrome Powder ×1 | 2 s |
| Grinding Unit | Buckflower Powder ×2, Sandleaf Powder ×1 | Ground Buckflower Powder ×1 | 2 s |
| Gearing Unit | Origocrust ×10, Ferrium ×10 | Ferrium Component ×1 | 10 s |
| Gearing Unit | Origocrust ×5, Amethyst Fiber ×5 | Amethyst Component ×1 | 10 s |
| Gearing Unit | Packed Origocrust ×10, Cryston Fiber ×10 | Cryston Component ×1 | 10 s |
| Gearing Unit | Packed Origocrust ×10, Xiranite ×10 | Xiranite Component ×1 | 10 s |
| Gearing Unit | Cuprium Part ×10, Xiranite ×10 | Cuprium Component ×1 | 10 s |
| Gearing Unit | Hetonite Part ×2, Heavy Xiranite ×2 | Hetonite Component ×1 | 10 s |
| Gearing Unit | Pyrrolite Part ×1, Heavy Xiranite ×2 | Pyrrolite Component ×1 | 10 s |

The battery recipes of the Packaging Unit are on [AIC power](/aic/power/).

## Expanded Crucible: Multi-Clog Auto-Fix

Since Version 1.3, when an Expanded Crucible runs several recipes and all of them are clogged, it empties its cache so that reactions continue. The option is on by default and is saved with a blueprint.

## Resourcing facilities

| Facility | Mines or pumps | Power |
| --- | --- | --- |
| Portable Originium Rig | Originium Ore; runs on the Originium it mines | None |
| Electric Mining Rig | Originium Ore and Amethyst Ore | 5 |
| Electric Mining Rig Mk II | Ferrium Ore and other minerals | 10 |
| Hydro Mining Rig | Cuprium Ore and other ores; driven by Clean Water | None |
| Fluid Pump | Fluids | 10 |
| Acid Resistant Pump Mk II | Fluids, corrosive liquids included | 20 |
| Gas Extractor | Inergen and other gases | None |
