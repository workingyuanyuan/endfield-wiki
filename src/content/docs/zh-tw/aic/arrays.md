---
title: 陣列與重建禁區
description: 《明日方舟：終末地》武陵的陣列為赤銅塊與息壤賦予明、晦或衡的特性，供重建禁區使用。
appliesTo: 《明日方舟：終末地》國際版，1.7 版；陣列、配方與重建資料取自遊戲資料 1.7
caveat: 陣列只有完全重疊才會疊加：兩個同種陣列提升等階，陣列·明與陣列·晦要在研究工業技術「明晦相疊」後才能疊加成陣列·衡。
lastVerified: 2026-11-26
effectiveDate: 2026-11-25
aliases:
  - Arrays and Exclusion Zone Rebuilding
  - 阵列与重建禁区
  - 陣と封鎖区域再建
  - 배열과 금지 구역 재건
  - Forge of Luminance
  - Forge of Equilibrium
  - 明晦爐
  - 平衡爐
sources:
  - title: 「穿越甚大蘑境與你相逢」版本更新說明
    url: https://endfield.gryphline.com/en-us/news/0740
  - title: warfarin.wiki 遊戲內教學「明晦爐」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_ming
  - title: warfarin.wiki 遊戲內教學「陣列·晦」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_hui
  - title: warfarin.wiki 遊戲內教學「陣列·衡」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_heng
  - title: warfarin.wiki 遊戲內教學「分影明晦爐」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_2
  - title: warfarin.wiki 遊戲內教學「平衡爐」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_balancer_1
  - title: warfarin.wiki 遊戲內教學「重建供應接口」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_wonder_supply_port_1
  - title: warfarin.wiki 遊戲內教學「高效輝銅產線」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_copper_bright_cube
  - title: "陣列表 FactoryFormationTable、FactoryFormationLevelTable、FactoryFormationTransTable（遊戲資料 1.7）：陣列種類、等階與賦予機率"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationTransTable.json
  - title: "明晦爐表 FactoryFormationStakeTable（遊戲資料 1.7）：息壤氣與陣列範圍"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationStakeTable.json
  - title: "設備表 FactoryBuildingTable（遊戲資料 1.7）：耗電、接口與占地"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryBuildingTable.json
  - title: "配方表 FactoryMachineCraftTable（遊戲資料 1.7）：平衡爐與重建物資"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryMachineCraftTable.json
  - title: "工業計劃表 FacSTTNodeTable（遊戲資料 1.7）：陣列相關技術"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FacSTTNodeTable.json
  - title: "重建表 WonderStageTable（遊戲資料 1.7）：階段與物資"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/WonderStageTable.json
---

## 設備

| 設備 | 耗電 | 占地 | 用途 |
| --- | --- | --- | --- |
| 明晦爐 | — | 5 × 5 | 在前方生成 1 個陣列（明或晦） |
| 分影明晦爐 | — | 5 × 5 | 在前方與側方各生成 1 個陣列，共 2 個 |
| 平衡爐 | 50 | 5 × 5 | 把同一材料的明、晦兩種形態合成新材料；5 個傳送帶輸入口、5 個輸出口 |
| 重建供應接口 | — | 3 × 3 | 把輸入的重建物資送往北部禁區的重建倉庫 |

四種設備都只能在武陵建造。明晦爐不耗電：向它的管道接口持續通入息壤氣即可啟用，所需的最低流速與固氣轉化機啟動口相同。每個陣列的範圍為 5 × 5，位在距明晦爐固定距離處。

## 陣列

| 陣列 | 英文 | 產生方式 | 赤銅塊轉為 | 息壤轉為 |
| --- | --- | --- | --- | --- |
| 陣列·明 | L-Array | 明晦爐 | 明狀赤銅 | 明狀息壤 |
| 陣列·晦 | T-Array | 明晦爐，研究「晦型擴展」後 | 晦狀赤銅 | 晦狀息壤 |
| 陣列·衡 | E-Array | 陣列·明與陣列·晦完全疊加，研究「明晦相疊」後 | 衡銅 | 衡息壤 |

陣列作用於傳送帶運過其範圍的赤銅塊與息壤，每隔一段時間為它們賦予陣列的特性，每次賦予以陣列等階的機率成功。

## 等階與賦予機率

| 陣列 | 1 階 | 2 階 | 3 階 | 4 階 |
| --- | --- | --- | --- | --- |
| 陣列·明 | 20% | 40% | 60% | 100% |
| 陣列·晦 | 20% | 40% | 60% | 100% |
| 陣列·衡 | 40% | 80% | — | — |

同種陣列完全重疊時會疊加並提升等階，最高 4 階：兩個陣列·明完全重疊即為 2 階陣列·明。只有部分重疊的陣列不會疊加。分影明晦爐的兩個陣列可與另一台分影明晦爐的兩個陣列疊加，兩個陣列同時升一階。

## 平衡爐配方

| 原料 | 產物 | 時間 |
| --- | --- | --- |
| 明狀息壤 ×5、晦狀息壤 ×5 | 重息壤 ×2 | 10 秒 |
| 明狀赤銅 ×10、晦狀赤銅 ×10 | 赫銅塊 ×5 | 10 秒 |
| 衡息壤 ×10、衡銅 ×10 | 輝銅 ×5 | 10 秒 |

## 重建物資

| 物資 | 設備 | 原料 | 產物 | 時間 |
| --- | --- | --- | --- | --- |
| 明狀赤銅零件 | 配件機 | 明狀赤銅 ×1 | 明狀赤銅零件 ×1 | 2 秒 |
| 晦狀赤銅零件 | 配件機 | 晦狀赤銅 ×1 | 晦狀赤銅零件 ×1 | 2 秒 |
| 輝銅零件 | 配件機 | 輝銅 ×1 | 輝銅零件 ×1 | 2 秒 |
| 銅封明壤元件 | 封裝機 | 明狀赤銅零件 ×10、明狀息壤 ×5 | 銅封明壤元件 ×5 | 10 秒 |
| 銅封重裝組件 | 封裝機 | 晦狀赤銅零件 ×15、重息壤 ×2 | 銅封重裝組件 ×5 | 10 秒 |
| 輝銅能量塊 | 封裝機 | 輝銅零件 ×5、緻密源石粉末 ×5 | 輝銅能量塊 ×5 | 10 秒 |

輝銅也能由氣體生產：氣體反應爐把氣態衡銅 ×1 與氣態衡息壤 ×1 轉為清型輝銅氣 ×2，固氣轉化機再把清型輝銅氣 ×2 轉為輝銅 ×2。氣態衡銅與氣態衡息壤由固氣轉化機從衡銅與衡息壤製成。

## 重建禁區

| 階段 | 投入的物資 |
| --- | --- |
| 1，南部建設 | 銅封明壤元件 |
| 2，北部建設 | 銅封明壤元件、銅封重裝組件 |
| 3，陣列點火 | 銅封明壤元件、銅封重裝組件、輝銅能量塊 |
| 4，持續維護 | 銅封明壤元件、銅封重裝組件、輝銅能量塊 |

完成支線任務「重建家園·其二」後解鎖這個玩法。第 1、2 階段先後在北部禁區的南側與北側建設天師樁陣列，第 3 階段為兩處陣列點火，第 4 階段是最後一個階段，持續維護陣列。物資經重建供應接口送進重建倉庫，每種最多存放 8,000 個。重建會提升武陵的地區發展度（見[地區建設](/zh-tw/aic/regional-development/)）。

## 工業技術

| 技術 | 前置技術 | 工業計劃 | 解鎖 | 推進以下任務後可研究 |
| --- | --- | --- | --- | --- |
| 明爐燃火 | — | 武陵工業一期 | 明晦爐、陣列·明 | — |
| 重建供應 | 明爐燃火 | 武陵工業一期 | 重建供應接口 | 重建家園·其二 |
| 晦型擴展 | 重建供應 | 武陵工業二期 | 陣列·晦 | 重建家園·其二 |
| 清濁平衡 | 晦型擴展 | 武陵工業二期 | 平衡爐 | 重建家園·其二 |
| 明晦相疊 | 清濁平衡 | 武陵工業三期 | 陣列·衡 | 重建家園·其三 |
| 明晦分影 | 明晦相疊 | 武陵工業三期 | 分影明晦爐 | 重建家園·其三 |

研究解鎖設備的技術時，另外獲得兩台該設備。
