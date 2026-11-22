---
title: "Dijiang"
description: "Dijiang, the base ship of Arknights: Endfield: its rooms, operator assignments, mood, and base skills by room."
appliesTo: "Arknights: Endfield, global service, Version 1.6; tutorials and base skills from game data 1.6"
caveat: "An assigned operator loses mood over time; at zero mood they leave to rest in the Central Ring and give no effect until their mood is full again. Base skills unlock at promotions, so an operator below Promotion I has none."
lastVerified: 2026-11-22
effectiveDate: 2026-11-22
aliases:
  - "帝江號"
  - "帝江号"
sources:
  - title: "In-game tutorials on Dijiang, WikiTutorialPageTable (game data 1.6)"
    url: https://github.com/rmxlinux/EndfieldData/blob/d847759f71d4549aba4727b3b0ac1a1ad0e37742/TableCfg/WikiTutorialPageTable.json
  - title: "rmxlinux/EndfieldData, game tables (1.6, 2026-11-05)"
    url: https://github.com/rmxlinux/EndfieldData/tree/d847759f71d4549aba4727b3b0ac1a1ad0e37742/TableCfg
---

Dijiang is the Endministrator's ship and the base of Arknights: Endfield. Operators assigned to its rooms make progression materials, grow plants, fungi and minerals, collect clues and build trust while the player is elsewhere. Each room needs at least one operator to work, and every operator assigned raises its output. 33 of the 34 operators have base skills that add to one room; the Endministrator has none.

## Rooms

| Room | What it does | Base skills that work there |
| --- | --- | --- |
| Control Nexus | Manages the whole ship and every room's assignments. Its level decides how many rooms can be built and how far they can be upgraded. Operators assigned here gain trust over time, also while the player is away. | Mood recovery of all operators |
| MFG Cabin | Makes operator and weapon progression materials over time from a chosen MFG Plan. Each item takes part of the room's MFG Load, which caps how many can be queued. | Slower mood drop in the room; Weapon EXP materials, faster; Operator EXP materials, faster |
| Growth Chamber | Grows materials for promotions, skill upgrades and weapon tuning. Growing needs seed materials, extracted from existing materials, which uses those up. | Slower mood drop in the room; Rare minerals, faster; Vitrified plants, faster; Fungal matter, faster |
| Reception Room | Operators here collect clues and earn credits over time. A full set of clue types starts a Clue Exchange; clues can be given to and received from friends. | Slower mood drop in the room; Chance of one clue; Clue collection, faster |

## Mood, shifts and upgrades

- Operators assigned to a working room lose mood over time. At zero mood an operator goes to the Central Ring to rest and gives no assignment effect; at full mood they return to the room by themselves.
- Each room can hold two shifts of operators, A and B. Shifts can be switched by hand or rotated on a schedule.
- Leveling up the Control Nexus opens more space for new rooms and raises the level cap of some rooms. An upgraded room holds more operators and unlocks more production. Building and upgrading take Aerospace Materials, gathered regularly from Recycling Stations across Talos-II.
- Credits come from clue collection, Clue Exchange, Production Assists in friends' rooms and delivery jobs for friends.

## Base skills by room

Which operators to assign to each room. Each base skill has two levels, unlocked at promotions; the second replaces the first. A clue skill does not stack with another of the same kind. Each operator's page lists their base skills under Base skills.

### Control Nexus

| Effect | Operator | Skill | First level | Second level |
| --- | --- | --- | --- | --- |
| Mood recovery of all operators | [Da Pan](/operators/da-pan/) | Worldly Wisdom | +12%, Promotion II | +16%, Promotion IV |
| Mood recovery of all operators | [Fluorite](/operators/fluorite/) | Reader of Emotions | +12%, Promotion II | +16%, Promotion IV |
| Mood recovery of all operators | [Lifeng](/operators/lifeng/) | Youthful Ambition | +12%, Promotion I | +16%, Promotion III |
| Mood recovery of all operators | [Liino](/operators/liino/) | Stage Vibe That Lingers | +12%, Promotion II | +16%, Promotion IV |
| Mood recovery of all operators | [Snowshine](/operators/snowshine/) | Happy-Go-Lucky | +12%, Promotion II | +16%, Promotion IV |
| Mood recovery of all operators | [Alesh](/operators/alesh/) | Casual Angling | +8%, Promotion I | +12%, Promotion III |
| Mood recovery of all operators | [Avywenna](/operators/avywenna/) | Residence Advisor | +8%, Promotion I | +12%, Promotion III |
| Mood recovery of all operators | [Catcher](/operators/catcher/) | Silent Caretaker | +8%, Promotion I | +12%, Promotion III |
| Mood recovery of all operators | [Estella](/operators/estella/) | Fragmented Rest | +8%, Promotion I | +12%, Promotion III |
| Mood recovery of all operators | [Perlica](/operators/perlica/) | Supervisor | +8%, Promotion I | +12%, Promotion III |

### MFG Cabin

| Effect | Operator | Skill | First level | Second level |
| --- | --- | --- | --- | --- |
| Operator EXP materials, faster | [Argent Flow](/operators/argent-flow/) | Axiom of Combat | +20%, Promotion I | +30%, Promotion III |
| Operator EXP materials, faster | [Camille](/operators/camille/) | Agaš'mekanaz's Manual | +20%, Promotion II | +30%, Promotion IV |
| Operator EXP materials, faster | [Ember](/operators/ember/) | Special Northern Training | +20%, Promotion I | +30%, Promotion III |
| Operator EXP materials, faster | [Laevatain](/operators/laevatain/) | Memory Crucible | +20%, Promotion I | +30%, Promotion III |
| Operator EXP materials, faster | [Purrchena](/operators/purrchena/) | Desserts for the Debrief | +20%, Promotion II | +30%, Promotion IV |
| Operator EXP materials, faster | [Zhuang Fangyi](/operators/zhuang-fangyi/) | Tianshi Chi Meditation | +20%, Promotion II | +30%, Promotion IV |
| Operator EXP materials, faster | [Wulfgard](/operators/wulfgard/) | Pack Techniques | +10%, Promotion I | +20%, Promotion III |
| Operator EXP materials, faster | [Xaihi](/operators/xaihi/) | Standardized Scripting | +10%, Promotion I | +20%, Promotion III |
| Weapon EXP materials, faster | [Gilberta](/operators/gilberta/) | Messengerial Arms Mastery | +20%, Promotion II | +30%, Promotion IV |
| Weapon EXP materials, faster | [Perlica](/operators/perlica/) | Protocol Redistribution | +20%, Promotion II | +30%, Promotion IV |
| Weapon EXP materials, faster | [Pogranichnik](/operators/pogranichnik/) | Hone the Weapons | +20%, Promotion I | +30%, Promotion III |
| Weapon EXP materials, faster | [Antal](/operators/antal/) | Experimental Arts Unit | +10%, Promotion I | +20%, Promotion III |
| Weapon EXP materials, faster | [Arclight](/operators/arclight/) | Blade of the Wildlands | +10%, Promotion I | +20%, Promotion III |
| Weapon EXP materials, faster | [Chen Qianyu](/operators/chen-qianyu/) | Blade Critique | +10%, Promotion I | +20%, Promotion III |
| Slower mood drop in the room | [Argent Flow](/operators/argent-flow/) | Tools of Momentum | −14%, Promotion II | −18%, Promotion IV |
| Slower mood drop in the room | [Gilberta](/operators/gilberta/) | Messengerial Processing | −14%, Promotion I | −18%, Promotion III |
| Slower mood drop in the room | [Laevatain](/operators/laevatain/) | Undying Flames | −14%, Promotion II | −18%, Promotion IV |
| Slower mood drop in the room | [Pogranichnik](/operators/pogranichnik/) | Morale Boost | −14%, Promotion II | −18%, Promotion IV |
| Slower mood drop in the room | [Zhuang Fangyi](/operators/zhuang-fangyi/) | Viceroy Experience | −14%, Promotion I | −18%, Promotion III |
| Slower mood drop in the room | [Akekuri](/operators/akekuri/) | Coffee or Tea | −10%, Promotion I | −14%, Promotion III |
| Slower mood drop in the room | [Snowshine](/operators/snowshine/) | Rescuer's Perseverance | −10%, Promotion I | −14%, Promotion III |

### Growth Chamber

| Effect | Operator | Skill | First level | Second level |
| --- | --- | --- | --- | --- |
| Fungal matter, faster | [Mi Fu](/operators/mi-fu/) | Esoteric Tisane | +20%, Promotion II | +30%, Promotion IV |
| Fungal matter, faster | [Typhoeus](/operators/typhoeus/) | Life in the Spores | +20%, Promotion II | +30%, Promotion IV |
| Fungal matter, faster | [Yvonne](/operators/yvonne/) | Fungal Pigment Extraction | +20%, Promotion I | +30%, Promotion III |
| Fungal matter, faster | [Da Pan](/operators/da-pan/) | Chef of Forage and Game | +10%, Promotion I | +20%, Promotion III |
| Rare minerals, faster | [Arcane](/operators/arcane/) | Pluck the Mountain, Boil the Sea | +20%, Promotion I | +30%, Promotion III |
| Rare minerals, faster | [Chen Qianyu](/operators/chen-qianyu/) | Jadeworking | +20%, Promotion II | +30%, Promotion IV |
| Rare minerals, faster | [Typhoeus](/operators/typhoeus/) | Lithic Murmurs | +20%, Promotion I | +30%, Promotion III |
| Rare minerals, faster | [Wulfgard](/operators/wulfgard/) | Knack for the Wildlands | +20%, Promotion II | +30%, Promotion IV |
| Rare minerals, faster | [Fluorite](/operators/fluorite/) | Wildlands Trekker | +10%, Promotion I | +20%, Promotion III |
| Vitrified plants, faster | [Arcane](/operators/arcane/) | Botanophile | +20%, Promotion II | +30%, Promotion IV |
| Vitrified plants, faster | [Camille](/operators/camille/) | Hemo-Vitreography | +20%, Promotion I | +30%, Promotion III |
| Vitrified plants, faster | [Last Rite](/operators/last-rite/) | Cemetery Gardening | +20%, Promotion I | +30%, Promotion III |
| Vitrified plants, faster | [Tangtang](/operators/tangtang/) | River's Daughter | +20%, Promotion II | +30%, Promotion IV |
| Slower mood drop in the room | [Antal](/operators/antal/) | Pun-isher Studies | −14%, Promotion II | −18%, Promotion IV |
| Slower mood drop in the room | [Catcher](/operators/catcher/) | Grounded Approach | −14%, Promotion II | −18%, Promotion IV |
| Slower mood drop in the room | [Tangtang](/operators/tangtang/) | Supreme Chief | −14%, Promotion I | −18%, Promotion III |
| Slower mood drop in the room | [Yvonne](/operators/yvonne/) | Fashionista | −14%, Promotion II | −18%, Promotion IV |

### Reception Room

| Effect | Operator | Skill | First level | Second level |
| --- | --- | --- | --- | --- |
| Clue 1, UWST | [Alesh](/operators/alesh/) | Anglers' Intel Network | small rise, Promotion II | rise, Promotion IV |
| Clue 2, TGCC | [Avywenna](/operators/avywenna/) | Messenger's Secret | small rise, Promotion II | rise, Promotion IV |
| Clue 2, TGCC | [Purrchena](/operators/purrchena/) | Brand Ambassador | small rise, Promotion I | rise, Promotion III |
| Clue 3, HAS | [Lifeng](/operators/lifeng/) | Laddie Reliable | small rise, Promotion II | rise, Promotion IV |
| Clue 3, HAS | [Mi Fu](/operators/mi-fu/) | Secret Informants | small rise, Promotion I | rise, Promotion III |
| Clue 4, Order of Steel Oath | [Ember](/operators/ember/) | Keepers of the Banner | small rise, Promotion II | rise, Promotion IV |
| Clue 5, Cabal of Tranquility | [Xaihi](/operators/xaihi/) | Murmuring Session | small rise, Promotion II | rise, Promotion IV |
| Clue 6, Hannabit Circuit | [Arclight](/operators/arclight/) | Hanna Traditions | small rise, Promotion II | rise, Promotion IV |
| Clue 7, Seš'qa | [Last Rite](/operators/last-rite/) | Fame of the Royal Courts | small rise, Promotion II | rise, Promotion IV |
| Clue collection, faster | [Ardelia](/operators/ardelia/) | Tales of the Land | +20%, Promotion I | +30%, Promotion III |
| Clue collection, faster | [Estella](/operators/estella/) | Frequency Monitoring | +20%, Promotion II | +30%, Promotion IV |
| Clue collection, faster | [Rossi](/operators/rossi/) | Scent of the Hunt | +20%, Promotion II | +30%, Promotion IV |
| Clue collection, faster | [Si](/operators/si/) | Ware is the Geist | +20%, Promotion I | +30%, Promotion III |
| Slower mood drop in the room | [Akekuri](/operators/akekuri/) | Icebreaker | −14%, Promotion II | −18%, Promotion IV |
| Slower mood drop in the room | [Ardelia](/operators/ardelia/) | Mr. Dolly's Game | −14%, Promotion II | −18%, Promotion IV |
| Slower mood drop in the room | [Liino](/operators/liino/) | Idol Passion | −14%, Promotion I | −18%, Promotion III |
| Slower mood drop in the room | [Rossi](/operators/rossi/) | Clan Etiquette | −14%, Promotion I | −18%, Promotion III |
| Slower mood drop in the room | [Si](/operators/si/) | Ink Spirit Aide | −14%, Promotion II | −18%, Promotion IV |
