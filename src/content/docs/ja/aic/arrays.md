---
title: "陣と封鎖区域再建"
description: "『アークナイツ：エンドフィールド』武陵の陣は赤銅塊と息壌に明・晦・衡の特性を与え、封鎖区域再建に使われる。"
appliesTo: "『アークナイツ：エンドフィールド』グローバル版、バージョン1.7。陣、レシピ、再建のデータはゲームデータ 1.7 による"
caveat: "陣は完全に重ねたときだけ重なり合う。同じ種類の陣を2つ重ねるとレベルが上がり、明の陣を晦の陣に重ねて衡の陣になるのは、工業技術「晦明の重なり」を研究した後だけである。"
lastVerified: 2026-11-26
effectiveDate: 2026-11-25
aliases:
  - Arrays and Exclusion Zone Rebuilding
  - 陣列與重建禁區
  - 阵列与重建禁区
  - 배열과 금지 구역 재건
  - Forge of Luminance
  - Forge of Equilibrium
  - 明晦爐
  - 平衡爐
sources:
  - title: "「キノコ菌グ！？君との大冒険！」 バージョンアップデートについて"
    url: https://endfield.gryphline.com/en-us/news/0740
  - title: "warfarin.wiki、ゲーム内チュートリアル「晦明炉」（ゲームデータ 1.7）"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_ming
  - title: "warfarin.wiki、ゲーム内チュートリアル「晦の陣」（ゲームデータ 1.7）"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_hui
  - title: "warfarin.wiki、ゲーム内チュートリアル「衡の陣」（ゲームデータ 1.7）"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_heng
  - title: "warfarin.wiki、ゲーム内チュートリアル「双影晦明炉」（ゲームデータ 1.7）"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_2
  - title: "warfarin.wiki、ゲーム内チュートリアル「均衡炉」（ゲームデータ 1.7）"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_balancer_1
  - title: "warfarin.wiki、ゲーム内チュートリアル「再建用供給口」（ゲームデータ 1.7）"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_wonder_supply_port_1
  - title: "warfarin.wiki、ゲーム内チュートリアル「効率化輝銅生産ライン」（ゲームデータ 1.7）"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_copper_bright_cube
  - title: "陣表 FactoryFormationTable、FactoryFormationLevelTable、FactoryFormationTransTable（ゲームデータ 1.7）：陣の種類、レベル、付与確率"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationTransTable.json
  - title: "晦明炉表 FactoryFormationStakeTable（ゲームデータ 1.7）：息壌ガスと陣の範囲"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationStakeTable.json
  - title: "設備表 FactoryBuildingTable（ゲームデータ 1.7）：消費電力、接続口、占有面積"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryBuildingTable.json
  - title: "レシピ表 FactoryMachineCraftTable（ゲームデータ 1.7）：均衡炉と再建物資"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryMachineCraftTable.json
  - title: "工業計画表 FacSTTNodeTable（ゲームデータ 1.7）：陣関連の技術"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FacSTTNodeTable.json
  - title: "再建表 WonderStageTable（ゲームデータ 1.7）：段階と物資"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/WonderStageTable.json
---

## 設備

| 設備 | 消費電力 | 占有面積 | 役割 |
| --- | --- | --- | --- |
| 晦明炉 | — | 5 × 5 | 前方に陣を1つ（明の陣または晦の陣）生成する |
| 双影晦明炉 | — | 5 × 5 | 前方と横側に陣を2つ生成する |
| 均衡炉 | 50 | 5 × 5 | ある素材の明の形態と晦の形態を組み合わせて新しい素材にする。ベルトの搬入口5つと搬出口5つを持つ |
| 再建用供給口 | — | 3 × 3 | 受け取った再建物資を北部封鎖区域の再建倉庫へ送る |

これらの設備はすべて武陵でしか建てられない。晦明炉は電力を使わず、液体ポートに息壌ガスを一定の流量で送り続けると起動する。必要な最低流量はガス固体転換機の起動接続口と同じである。各陣は晦明炉から一定距離の位置に5 × 5の範囲を持つ。

## 陣

| 陣 | 英語 | 繁体字中国語 | 生成元 | 赤銅塊が変わるもの | 息壌が変わるもの |
| --- | --- | --- | --- | --- | --- |
| 明の陣 | L-Array | 陣列·明 | 晦明炉 | 赤銅・明 | 息壌・明 |
| 晦の陣 | T-Array | 陣列·晦 | 晦明炉（拡張・晦の研究後） | 赤銅・晦 | 息壌・晦 |
| 衡の陣 | E-Array | 陣列·衡 | 完全に重ねた明の陣と晦の陣（晦明の重なりの研究後） | 衡銅 | 衡息壌 |

陣は、ベルトコンベアがその範囲を通って運ぶ赤銅塊と息壌に作用する。一定時間ごとに陣の特性を付与し、付与はそれぞれ陣のレベルに応じた確率で成功する。

## レベルと付与確率

| 陣 | Lv.1 | Lv.2 | Lv.3 | Lv.4 |
| --- | --- | --- | --- | --- |
| 明の陣 | 20% | 40% | 60% | 100% |
| 晦の陣 | 20% | 40% | 60% | 100% |
| 衡の陣 | 40% | 80% | — | — |

同じ種類の陣が完全に重なると重なり合い、レベルが上がる（最大Lv.4）。明の陣同士を完全に重ねると明の陣Lv.2になる。一部だけ重なった陣は重なり合わない。双影晦明炉の陣は、別の双影晦明炉の陣と両方とも重なり合い、どちらも同時にレベルが上がる。

## 均衡炉のレシピ

| 原料 | 製品 | 時間 |
| --- | --- | --- |
| 息壌・明 ×5、息壌・晦 ×5 | 重息壌 ×2 | 10秒 |
| 赤銅・明 ×10、赤銅・晦 ×10 | 緋銅塊 ×5 | 10秒 |
| 衡息壌 ×10、衡銅 ×10 | 輝銅 ×5 | 10秒 |

## 再建物資

| 物資 | 設備 | 原料 | 製品 | 時間 |
| --- | --- | --- | --- | --- |
| 赤銅部品・明 | 組立機 | 赤銅・明 ×1 | 赤銅部品・明 ×1 | 2秒 |
| 赤銅部品・晦 | 組立機 | 赤銅・晦 ×1 | 赤銅部品・晦 ×1 | 2秒 |
| 輝銅部品 | 組立機 | 輝銅 ×1 | 輝銅部品 ×1 | 2秒 |
| 銅封明壌部品 | 包装機 | 赤銅部品・明 ×10、息壌・明 ×5 | 銅封明壌部品 ×5 | 10秒 |
| 銅封重モジュール | 包装機 | 赤銅部品・晦 ×15、重息壌 ×2 | 銅封重モジュール ×5 | 10秒 |
| 輝銅エネルギーブロック | 包装機 | 輝銅部品 ×5、高密度源石粉末 ×5 | 輝銅エネルギーブロック ×5 | 10秒 |

輝銅はガスからも作れる。ガス反応装置が衡銅ガス ×1と衡息壌ガス ×1を輝銅ガス・清 ×2に変え、ガス固体転換機が輝銅ガス・清 ×2を輝銅 ×2に変える。衡銅ガスと衡息壌ガスは、ガス固体転換機で衡銅と衡息壌から作る。

## 封鎖区域再建

| 段階 | 納める物資 |
| --- | --- |
| 1、南部建設 | 銅封明壌部品 |
| 2、北部建設 | 銅封明壌部品、銅封重モジュール |
| 3、陣の点火 | 銅封明壌部品、銅封重モジュール、輝銅エネルギーブロック |
| 4、長期運営 | 銅封明壌部品、銅封重モジュール、輝銅エネルギーブロック |

このモードはサブ任務「故郷の再建・その二」で解放される。段階1と段階2で北部封鎖区域の南部、次いで北部に天師杭陣を建て、段階3で両方を点火し、最後の段階4でそれらを維持する。物資は再建用供給口を通って再建倉庫に届き、再建倉庫は物資を種類ごとに最大8,000個まで保管する。再建は武陵の地域建設を進める（[地域建設](/ja/aic/regional-development/)を参照）。

## 集成工業の技術

| 技術 | 前提技術 | 工業計画 | 解放するもの | 進めると研究できる任務 |
| --- | --- | --- | --- | --- |
| 明炉の火 | — | 武陵工業Ⅰ | 晦明炉、明の陣 | — |
| 再建供給 | 明炉の火 | 武陵工業Ⅰ | 再建用供給口 | 故郷の再建・その二 |
| 拡張・晦 | 再建供給 | 武陵工業Ⅱ | 晦の陣 | 故郷の再建・その二 |
| 清濁の均衡 | 拡張・晦 | 武陵工業Ⅱ | 均衡炉 | 故郷の再建・その二 |
| 晦明の重なり | 清濁の均衡 | 武陵工業Ⅲ | 衡の陣 | 故郷の再建・その三 |
| 晦明双影 | 晦明の重なり | 武陵工業Ⅲ | 双影晦明炉 | 故郷の再建・その三 |

設備を解放する技術を研究すると、その設備も2台手に入る。
