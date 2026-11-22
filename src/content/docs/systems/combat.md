---
title: Combat mechanics
description: "Combat mechanics of Arknights: Endfield: damage formula, elements, Arts Reactions, Physical Statuses, Stagger."
appliesTo: "Arknights: Endfield, global service, Version 1.6; terms and tutorials from game data 1.6; damage formulas from player tests in Version 1.0"
caveat: "Vulnerable (Vulnerability) is the stack that Physical Status hits build on an enemy, up to 4. It is not Susceptible (Susceptibility), the debuff that makes a target take more damage of one element."
lastVerified: 2026-11-22
aliases:
  - 戰鬥機制
  - 战斗机制
sources:
  - title: "rmxlinux/EndfieldData, game tables (1.6, 2026-11-05)"
    url: https://github.com/rmxlinux/EndfieldData/tree/d847759f71d4549aba4727b3b0ac1a1ad0e37742/TableCfg
  - title: "NGA forum guide 终末地数据机制导论 (player tests, Version 1.0)"
    url: https://bbs.nga.cn/read.php?tid=46094556
  - title: "warfarin.wiki, combat terms in game data 1.6"
    url: https://warfarin.wiki/en/operators/laevatain
  - title: "warfarin.wiki, tutorial Damage Type (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_dmg_type
  - title: "warfarin.wiki, tutorial Status Level (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_statuslevel
  - title: "warfarin.wiki, tutorial Stagger (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_poise
  - title: "warfarin.wiki, tutorial Finisher (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_execute
  - title: "warfarin.wiki, tutorial Basic Attack: Final Strike (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_heavy_attack
  - title: "warfarin.wiki, tutorial Skill Points (SP) (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_sp
  - title: "warfarin.wiki, tutorial Skill: Battle Skills (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_normal_skill
  - title: "warfarin.wiki, tutorial Skill: Combo Skills (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_combo
  - title: "warfarin.wiki, tutorial Skill: Ultimates (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_ultimite_skill
  - title: "warfarin.wiki, tutorial Team Combat (game data 1.6)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_bat_team
  - title: "warfarin.wiki, operators (element, skill costs and cooldowns in game data 1.6)"
    url: https://warfarin.wiki/en/operators
  - title: "Endfield Talos Wiki, Operator (team size)"
    url: https://endfield.wiki.gg/wiki/Operator
---

Damage in Arknights: Endfield is Physical, Arts or Æther, and Arts damage is Heat, Electric, Cryo or Nature. Arts hits leave Arts Inflictions on an enemy, up to 4 stacks: a second Infliction of the same element sets off an Arts Burst, one of another element sets off an Arts Reaction (Combustion, Electrification, Solidification or Corrosion). Physical Status hits first make an enemy Vulnerable; Lift and Knock Down then add stacks, Crush and Breach spend them. Stagger fills a meter that leaves the enemy Staggered and open to a Finisher. Damage is a product of multipliers: base damage (usually from ATK), critical hits, damage bonuses, the target's DEF and resistances, and the Staggered state. Player tests on the NGA forum in Version 1.0 put the DEF multiplier at 100 / (DEF + 100), 0.5 against the usual base DEF of 100, and a Staggered enemy at ×1.3 damage.

## Damage formula

NGA forum player 666bj measured these formulas in Version 1.0. Ordinary damage, which is every hit except Physical Statuses, Arts Reactions and Arts Bursts, is the product of the following multipliers:

| Multiplier | Value | How several effects combine |
| --- | --- | --- |
| Base damage | DMG multiplier × the stat the effect scales with (usually ATK), plus any flat base-damage increase | |
| Critical | 1 + Critical DMG on a critical hit, otherwise 1; on average 1 + Critical Rate × Critical DMG | |
| DMG bonus | 1 + the sum of all DMG bonuses: damage type, skill type, damage to Staggered enemies and others | Add |
| DMG Reduction | The product of (1 − each reduction) | Multiply |
| Amp | 1 + the sum of Amp effects | Add |
| Weakness | The product of (1 − each Weakness) | Multiply |
| Protect | 1 − the strongest Protect | Only the strongest counts |
| Susceptible | 1 + the sum of Susceptible effects | Add |
| Other damage-taken increases | 1 + the sum of effects that raise damage taken without being called Susceptible, such as the Arts damage increase of Electrification and the Physical damage increase of Breach | Add |
| DEF | 100 / (DEF + 100) when effective DEF is 0 or more; 1 for damage that ignores DEF | |
| Stagger | 1.3 against a Staggered enemy, otherwise 1 | |
| Resistance | 1 − Resistance / 100 + ignored Resistance / 100 | |
| Off-field | 1, or 0 to 0.7 for some strong enemy attacks on operators who are not controlled | |
| Link | Battle skills +30%, +45%, +60% or +75% and ultimates +20%, +30%, +40% or +50% at 1 to 4 Link stacks | Add up, with less effect each |
| Special | Other effects that stand apart from the multipliers above | Multiply |

- ATK = [(operator base ATK + weapon base ATK) × (1 + ATK % bonuses) + flat ATK bonuses] × (1 + attribute bonus). The attribute points give Main Attribute × 0.005 + Secondary Attribute × 0.002 of the attribute bonus, using whole attribute points; some operator talents add more attribute bonus.
- Operators start with 5% Critical Rate and 50% Critical DMG. Enemies have 0% Critical Rate and 50% Critical DMG.
- All Skill DMG covers battle skills, combo skills and ultimates, not basic attacks. Finishers gain from Basic Attack DMG Bonus.
- Enemies have 100 base DEF at every level, so the DEF multiplier of a hit that uses DEF is 0.5 unless an effect changes their DEF. Operators have 0 base DEF; their DEF normally comes from the main stat of gear.
- One point of resistance cuts damage of that type by 1%. The game shows an enemy's resistance as a grade: D for 0, C for 20 to 40, B for 50 and 60. Most enemy resistances are 0 or 20; a few enemies have 30, 35, 40, 50 or 60 in one element, and no enemy resists Æther. Every enemy's values are in [Enemy resistances](/systems/enemies/).
- An operator's Physical Resistance is 100 − 100 / (0.001 × Agility + 1), and Arts Resistance the same with Intellect, using the whole-number part of Agility and Intellect. An operator's resistance multiplier never falls below 0.1.
- Many values in the game are shown rounded down, so a calculation from the shown numbers can be off by a few points.

Physical Statuses, Arts Reactions and Arts Bursts that operators trigger use the multipliers above without Off-field and Link, and two more:

| Multiplier | Value |
| --- | --- |
| Level | Arts Reactions and Arts Bursts: 1 + (level of the triggering operator − 1) / 196, which is 1.454 at level 90. Physical Statuses: 1 + (level − 1) / 392, which is 1.227 at level 90 |
| Arts Intensity | 1 + Arts Intensity / 100 |

| Damage | DMG multiplier (of ATK) |
| --- | --- |
| Combustion, Electrification, Solidification, Corrosion: first hit | 80% × (1 + Status Level) |
| Combustion: each second of damage over time | 12% × (1 + Status Level) |
| Shatter (Physical damage, counted as an Arts Reaction for the Level multiplier) | 120% × (1 + Status Level) |
| Any Arts Burst | 160% |
| Lift, Knock Down | 120%, plus 10 Stagger |
| Breach | 50% × (1 + Status Level) |
| Crush | 150% × (1 + Status Level) |

| Effect at Status Level 1 / 2 / 3 / 4 | Value |
| --- | --- |
| Electrification: enemy takes more Arts damage | +12% / 16% / 20% / 24%, for 12 / 18 / 24 / 30 s |
| Breach: enemy takes more Physical damage | +12% / 16% / 20% / 24%, for 12 / 18 / 24 / 30 s |
| Corrosion: all resistances fall | 3.6 / 4.8 / 6 / 7.2 at once, then 0.84 / 1.12 / 1.4 / 1.68 a second, up to 12 / 16 / 20 / 24; initial duration 15 s; refreshing Corrosion keeps the reduction already reached |
| Combustion | 10 s |
| Solidification | 6 / 7 / 8 / 9 s |

- Arts Intensity also strengthens the extra effects of Breach, Electrification and Corrosion: the effect is multiplied by 1 + 2 × Arts Intensity / (Arts Intensity + 300). An effect that raises such an extra effect to a multiple of its value (for example ×1.33 from a Potential) multiplies the result after that. On Lift and Knock Down each point adds 0.5% Stagger.
- A reaction that a skill applies directly, without consuming Inflictions, deals no first-hit damage by default.

## Damage types and elements

| Damage type | Kind | Operators with this element (game data 1.6) |
| --- | --- | --- |
| Physical | Physical | 9 |
| Heat | Arts | 5 |
| Electric | Arts | 7 |
| Cryo | Arts | 8 |
| Nature | Arts | 5 |
| Æther | Æther | 0 |

Each of the 34 operators in game data 1.6 has Physical or one of the four Arts elements as its element; none has Æther. The operators of each element are listed under Operators by element.

## Arts Inflictions, Arts Bursts and Arts Reactions

| Term | What it is |
| --- | --- |
| Arts Infliction | An Arts mark on an enemy, of one of the four elements. Stacks up to 4 per element. |
| Arts Burst | Adding an Infliction of the same element to an enemy that already carries it: a hit of that element's damage. |
| Arts Reaction | Inflictions of two different elements on one enemy: an Arts debuff that consumes them. The game writes each one as another Infliction plus one element's Infliction, for example Combustion = another Infliction + Heat Infliction. |
| Status Level | The number of Infliction stacks (or Vulnerable stacks) consumed by a reaction or Physical Status, at most 4. A higher level gives a stronger effect. |

| Element | Arts Burst | Arts Reaction (that element plus an Infliction of another) | Reaction effect on an enemy | At 4 stacks on an operator |
| --- | --- | --- | --- | --- |
| Heat | Heat Burst: Heat damage | Combustion | Takes Heat damage over time | Combusted: Heat damage over time that ignores DEF |
| Electric | Electric Burst: Electric damage | Electrification | Takes more Arts damage | Electrified: short stun, and takes more Arts damage for a time |
| Cryo | Cryo Burst: Cryo damage | Solidification | Cannot move; Vulnerable or a Physical Status on it sets off Shatter | Solidified: cannot move for a time |
| Nature | Nature Burst: Nature damage | Corrosion | All resistances fall gradually | Corroded: cannot dash and moves slower for a time |

Enemy skills can stack Inflictions on operators too; the last column is what 4 stacks of one element do to an operator.

## Physical Statuses and Vulnerable

The first Physical Status hit on an enemy does not apply the status: it makes the enemy Vulnerable. Vulnerable stacks up to 4.

| Physical Status | On a Vulnerable enemy |
| --- | --- |
| Lift | Adds 1 Vulnerable stack, deals Physical damage and Stagger |
| Knock Down | Adds 1 Vulnerable stack, deals Physical damage and Stagger (same rule as Lift) |
| Crush | Consumes every Vulnerable stack for heavy Physical damage |
| Breach | Consumes every Vulnerable stack, deals Physical damage, and the enemy takes more Physical damage for a time |
| Shatter | Not a status of its own: Vulnerable or any Physical Status on a Solidified enemy consumes Solidification for heavy Physical damage |

Crush and Breach have a Status Level, as Arts Reactions do: the number of Vulnerable stacks they consume.

## Stagger, Finisher and Final Strike

| Term | What it is |
| --- | --- |
| Stagger | Build-up dealt by most skills and by the controlled operator's Final Strike. A full meter leaves the enemy Staggered. |
| Staggered | For a time the enemy cannot move and takes more damage. An enemy Staggered very quickly gains Stagger more slowly for a while after the first Staggered state ends. |
| Stagger Node | A mark on the meter of some strong enemies. Reaching it interrupts the enemy and makes it stumble. |
| Finisher | The first basic attack on a Staggered enemy: heavy damage and some SP back. |
| Final Strike | The last hit of the basic attack sequence. From the controlled operator it deals Stagger and restores SP. |

## SP, skills and Ultimate Energy

| Skill | Cost | Cooldown | Notes from game data 1.6 |
| --- | --- | --- | --- |
| Basic attack | None | None | Teammates who are not controlled attack on their own |
| Battle skill | SP | None | 100 SP for 33 of 34 operators; 25 SP for [Liino](/operators/liino/) |
| Combo skill | None | Yes | Cast only when the operator's own trigger is met; cooldown 3 s to 40 s at skill level 1 |
| Ultimate | All Ultimate Energy | Short, after the cast | Needs a full gauge: 70 to 300 Ultimate Energy by operator; cooldown 10, 15, 20 or 30 s |

- SP pays for battle skills. It refills over time, and the controlled operator's Final Strike and Finishers restore more.
- Ultimate Energy comes from battle skills (the same amount to every teammate) and combo skills (to the caster only). An operator whose ultimate enhances them gains no Ultimate Energy while the enhancement lasts.
- A team has up to four operators. Battle skills, combo skills and ultimates of every member are cast by hand.

## Buffs, debuffs and other terms

| Term | Effect | Several of the same type |
| --- | --- | --- |
| Amp | The target deals more damage of one element (Physical Amp, Heat Amp, Arts Amp and so on) for a time | Add up |
| Susceptible | The target takes more damage of one element for a time | Add up |
| Protect | The target takes less damage for a time | Only the strongest counts |
| Weakness | The target deals less damage for a time | Add up, but not linearly |
| Shield | Absorbs damage while it lasts; some shields absorb only certain damage types | |
| Slow | Lower movement speed for a time | Only the strongest counts |
| Haste | Higher movement speed for a time | Add up to a speed cap |
| Immobilization | The target cannot act while it lasts | |
| Dispel | Removes certain debuffs from an operator | |
| Link | The team's next battle skill or ultimate deals more damage, battle skills more so; spent on use | Add up, with less effect each |
| SP Return | Part of the SP just spent comes back when a condition is met. It is not SP recovery: it does not trigger effects that react to recovering SP, and spending it gives no Ultimate Energy | |
| Debuff Consumption | A debuff ends early because another effect used it up: Crush consumes Vulnerable, a reaction consumes Inflictions | |
| Absorb | A debuff ends early in a special way; this does not count as consumption | |
| DMG Over Time | Damage dealt over time; it cannot be a critical hit | |
| Fixed DMG | Ignores DEF and resistances and is not changed by any damage increase or reduction | |

States that belong to one operator:

| State | Operator | Effect |
| --- | --- | --- |
| Originium Crystal | [Endministrator](/operators/endministrator/) | Attached to enemies by the combo skill; they cannot move |
| Razor Clawmark | [Rossi](/operators/rossi/) | From the battle skill: Physical damage over time, and the enemy takes more Physical and Heat damage |
| Sign | [Typhoeus](/operators/typhoeus/) | Gained by consuming Nature Infliction or by Nature Bursts; her combo skill turns Signs into Hunting Arrows |
| Hunting Arrow | [Typhoeus](/operators/typhoeus/) | Spent while she hovers for stronger shots that also set off Nature Burst |

## Operators by element

| Element | 6-star | 5-star | 4-star |
| --- | --- | --- | --- |
| Physical | [Endministrator](/operators/endministrator/), [Lifeng](/operators/lifeng/), [Mi Fu](/operators/mi-fu/), [Pogranichnik](/operators/pogranichnik/), [Rossi](/operators/rossi/) | [Chen Qianyu](/operators/chen-qianyu/), [Da Pan](/operators/da-pan/), [Purrchena](/operators/purrchena/) | [Catcher](/operators/catcher/) |
| Heat | [Camille](/operators/camille/), [Ember](/operators/ember/), [Laevatain](/operators/laevatain/) | [Wulfgard](/operators/wulfgard/) | [Akekuri](/operators/akekuri/) |
| Electric | [Argent Flow](/operators/argent-flow/), [Liino](/operators/liino/), [Zhuang Fangyi](/operators/zhuang-fangyi/) | [Arclight](/operators/arclight/), [Avywenna](/operators/avywenna/), [Perlica](/operators/perlica/) | [Antal](/operators/antal/) |
| Cryo | [Last Rite](/operators/last-rite/), [Si](/operators/si/), [Tangtang](/operators/tangtang/), [Yvonne](/operators/yvonne/) | [Alesh](/operators/alesh/), [Snowshine](/operators/snowshine/), [Xaihi](/operators/xaihi/) | [Estella](/operators/estella/) |
| Nature | [Arcane](/operators/arcane/), [Ardelia](/operators/ardelia/), [Gilberta](/operators/gilberta/), [Typhoeus](/operators/typhoeus/) | | [Fluorite](/operators/fluorite/) |

## Names in three scripts

| English | 繁體中文 | 簡體中文 |
| --- | --- | --- |
| Physical DMG | 物理傷害 | 物理伤害 |
| Arts DMG | 法術傷害 | 法术伤害 |
| Æther DMG | 超域傷害 | 超域伤害 |
| Heat | 灼熱 | 灼热 |
| Electric | 電磁 | 电磁 |
| Cryo | 寒冷 | 寒冷 |
| Nature | 自然 | 自然 |
| Arts Infliction | 法術附著 | 法术附着 |
| Arts Burst | 法術爆發 | 法术爆发 |
| Arts Reaction | 法術異常 | 法术异常 |
| Combustion | 燃燒 | 燃烧 |
| Electrification | 導電 | 导电 |
| Solidification | 凍結 | 冻结 |
| Corrosion | 腐蝕 | 腐蚀 |
| Status Level | 異常等級 | 异常等级 |
| Physical Status | 物理異常 | 物理异常 |
| Vulnerable | 破防 | 破防 |
| Lift | 擊飛 | 击飞 |
| Knock Down | 倒地 | 倒地 |
| Crush | 猛擊 | 猛击 |
| Breach | 碎甲 | 碎甲 |
| Shatter | 碎冰 | 碎冰 |
| Stagger | 失衡值 | 失衡值 |
| Stagger Node | 失衡節點 | 失衡节点 |
| Finisher | 處決 | 处决 |
| Final Strike | 重擊 | 重击 |
| Skill Points (SP) | 技力 | 技力 |
| Battle skill | 戰技 | 战技 |
| Combo skill | 連攜技 | 连携技 |
| Ultimate | 終結技 | 终结技 |
| Amp | 增幅 | 增幅 |
| Susceptible | 脆弱 | 脆弱 |
| Protect | 庇護 | 庇护 |
| Weakness | 虛弱 | 虚弱 |
| Shield | 護盾 | 护盾 |
| Slow | 緩速 | 缓速 |
| Haste | 加速 | 加速 |
| Immobilization | 定身 | 定身 |
| Dispel | 淨化 | 净化 |
| Link | 連擊 | 连击 |
| SP Return | 返還技力 | 返还技力 |
| Debuff Consumption | 狀態消耗 | 状态消耗 |
| Absorb | 吸收 | 吸收 |
| DMG Over Time | 持續傷害 | 持续伤害 |
| Fixed DMG | 固定傷害 | 固定伤害 |

Link (連擊) is the team damage buff above, not the combo skill (連攜技).
