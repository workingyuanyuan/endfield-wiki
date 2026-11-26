---
title: 阵列与重建禁区
description: 《明日方舟：终末地》武陵的阵列为赤铜块与息壤赋予明、晦或衡的特性，供重建禁区使用。
appliesTo: 《明日方舟：终末地》国际版，1.7 版；阵列、配方与重建资料取自游戏数据 1.7
caveat: 阵列只有完全重叠才会叠加：两个同种阵列提升等阶，阵列·明与阵列·晦要在研究工业技术「明晦相叠」后才能叠加成阵列·衡。
lastVerified: 2026-11-26
effectiveDate: 2026-11-25
aliases:
  - Arrays and Exclusion Zone Rebuilding
  - 陣列與重建禁區
  - 陣と封鎖区域再建
  - 배열과 금지 구역 재건
  - Forge of Luminance
  - Forge of Equilibrium
  - 明晦爐
  - 平衡爐
sources:
  - title: 「穿越甚大蘑境与你相逢」版本更新说明
    url: https://endfield.gryphline.com/en-us/news/0740
  - title: warfarin.wiki 游戏内教学「明晦炉」（游戏数据 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_ming
  - title: warfarin.wiki 游戏内教学「阵列·晦」（游戏数据 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_hui
  - title: warfarin.wiki 游戏内教学「阵列·衡」（游戏数据 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_heng
  - title: warfarin.wiki 游戏内教学「分影明晦炉」（游戏数据 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_2
  - title: warfarin.wiki 游戏内教学「平衡炉」（游戏数据 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_balancer_1
  - title: warfarin.wiki 游戏内教学「重建供应端口」（游戏数据 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_wonder_supply_port_1
  - title: warfarin.wiki 游戏内教学「高效辉铜产线」（游戏数据 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_copper_bright_cube
  - title: "阵列表 FactoryFormationTable、FactoryFormationLevelTable、FactoryFormationTransTable（游戏数据 1.7）：阵列种类、等阶与赋予概率"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationTransTable.json
  - title: "明晦炉表 FactoryFormationStakeTable（游戏数据 1.7）：息壤气与阵列范围"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationStakeTable.json
  - title: "设备表 FactoryBuildingTable（游戏数据 1.7）：耗电、接口与占地"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryBuildingTable.json
  - title: "配方表 FactoryMachineCraftTable（游戏数据 1.7）：平衡炉与重建物资"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryMachineCraftTable.json
  - title: "工业计划表 FacSTTNodeTable（游戏数据 1.7）：阵列相关技术"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FacSTTNodeTable.json
  - title: "重建表 WonderStageTable（游戏数据 1.7）：阶段与物资"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/WonderStageTable.json
---

## 设备

| 设备 | 耗电 | 占地 | 用途 |
| --- | --- | --- | --- |
| 明晦炉 | — | 5 × 5 | 在前方生成 1 个阵列（明或晦） |
| 分影明晦炉 | — | 5 × 5 | 在前方与侧方各生成 1 个阵列，共 2 个 |
| 平衡炉 | 50 | 5 × 5 | 把同一材料的明、晦两种形态合成新材料；5 个传送带输入口、5 个输出口 |
| 重建供应端口 | — | 3 × 3 | 把输入的重建物资送往北部禁区的重建仓库 |

四种设备都只能在武陵建造。明晦炉不耗电：向它的管道接口持续通入息壤气即可启用，所需的最低流速与固气转化机启动口相同。每个阵列的范围为 5 × 5，位在距明晦炉固定距离处。

## 阵列

| 阵列 | 英文 | 产生方式 | 赤铜块转为 | 息壤转为 |
| --- | --- | --- | --- | --- |
| 阵列·明 | L-Array | 明晦炉 | 明状赤铜 | 明状息壤 |
| 阵列·晦 | T-Array | 明晦炉，研究「晦型扩展」后 | 晦状赤铜 | 晦状息壤 |
| 阵列·衡 | E-Array | 阵列·明与阵列·晦完全叠加，研究「明晦相叠」后 | 衡铜 | 衡息壤 |

阵列作用于传送带运过其范围的赤铜块与息壤，每隔一段时间为它们赋予阵列的特性，每次赋予以阵列等阶的概率成功。

## 等阶与赋予概率

| 阵列 | 1 阶 | 2 阶 | 3 阶 | 4 阶 |
| --- | --- | --- | --- | --- |
| 阵列·明 | 20% | 40% | 60% | 100% |
| 阵列·晦 | 20% | 40% | 60% | 100% |
| 阵列·衡 | 40% | 80% | — | — |

同种阵列完全重叠时会叠加并提升等阶，最高 4 阶：两个阵列·明完全重叠即为 2 阶阵列·明。只有部分重叠的阵列不会叠加。分影明晦炉的两个阵列可与另一台分影明晦炉的两个阵列叠加，两个阵列同时升一阶。

## 平衡炉配方

| 原料 | 产物 | 时间 |
| --- | --- | --- |
| 明状息壤 ×5、晦状息壤 ×5 | 重息壤 ×2 | 10 秒 |
| 明状赤铜 ×10、晦状赤铜 ×10 | 赫铜块 ×5 | 10 秒 |
| 衡息壤 ×10、衡铜 ×10 | 辉铜 ×5 | 10 秒 |

## 重建物资

| 物资 | 设备 | 原料 | 产物 | 时间 |
| --- | --- | --- | --- | --- |
| 明状赤铜零件 | 配件机 | 明状赤铜 ×1 | 明状赤铜零件 ×1 | 2 秒 |
| 晦状赤铜零件 | 配件机 | 晦状赤铜 ×1 | 晦状赤铜零件 ×1 | 2 秒 |
| 辉铜零件 | 配件机 | 辉铜 ×1 | 辉铜零件 ×1 | 2 秒 |
| 铜封明壤元件 | 封装机 | 明状赤铜零件 ×10、明状息壤 ×5 | 铜封明壤元件 ×5 | 10 秒 |
| 铜封重装组件 | 封装机 | 晦状赤铜零件 ×15、重息壤 ×2 | 铜封重装组件 ×5 | 10 秒 |
| 辉铜能量块 | 封装机 | 辉铜零件 ×5、致密源石粉末 ×5 | 辉铜能量块 ×5 | 10 秒 |

辉铜也能由气体生产：气体反应炉把气态衡铜 ×1 与气态衡息壤 ×1 转为清型辉铜气 ×2，固气转化机再把清型辉铜气 ×2 转为辉铜 ×2。气态衡铜与气态衡息壤由固气转化机从衡铜与衡息壤制成。

## 重建禁区

| 阶段 | 投入的物资 |
| --- | --- |
| 1，南部建设 | 铜封明壤元件 |
| 2，北部建设 | 铜封明壤元件、铜封重装组件 |
| 3，阵列点火 | 铜封明壤元件、铜封重装组件、辉铜能量块 |
| 4，持续维护 | 铜封明壤元件、铜封重装组件、辉铜能量块 |

完成支线任务「重建家园·其二」后解锁这个玩法。第 1、2 阶段先后在北部禁区的南侧与北侧建设天师桩阵列，第 3 阶段为两处阵列点火，第 4 阶段是最后一个阶段，持续维护阵列。物资经重建供应端口送进重建仓库，每种最多存放 8,000 个。重建会提升武陵的地区发展度（见[地区建设](/zh-cn/aic/regional-development/)）。

## 工业技术

| 技术 | 前置技术 | 工业计划 | 解锁 | 推进以下任务后可研究 |
| --- | --- | --- | --- | --- |
| 明炉燃火 | — | 武陵工业一期 | 明晦炉、阵列·明 | — |
| 重建供应 | 明炉燃火 | 武陵工业一期 | 重建供应端口 | 重建家园·其二 |
| 晦型扩展 | 重建供应 | 武陵工业二期 | 阵列·晦 | 重建家园·其二 |
| 清浊平衡 | 晦型扩展 | 武陵工业二期 | 平衡炉 | 重建家园·其二 |
| 明晦相叠 | 清浊平衡 | 武陵工业三期 | 阵列·衡 | 重建家园·其三 |
| 明晦分影 | 明晦相叠 | 武陵工业三期 | 分影明晦炉 | 重建家园·其三 |

研究解锁设备的技术时，另外获得两台该设备。
