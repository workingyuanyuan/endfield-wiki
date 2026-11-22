---
title: 地区建设
description: 《明日方舟：终末地》的地区建设，包括据点、调度券、仓储节点与跨地区传输。
appliesTo: 《明日方舟：终末地》国际版，1.6 版；教学文字取自游戏数据 1.6
caveat: 跨地区传输依传输起点地区的地区建设等级解锁。库存传输会从起点地区的仓库扣除物品；只有更高等级才解锁的超库存传输不扣除起点的物品。
lastVerified: 2026-11-21
effectiveDate: 2026-10-15
aliases:
  - Regional Development
  - 地區建設
  - 地域建設
  - 지역 건설
sources:
  - title: warfarin.wiki 游戏内教学「跨地区传输」（游戏数据 1.6）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_domain_transport
  - title: warfarin.wiki 游戏内教学「地区建设系统」（游戏数据 1.6）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_domain
  - title: warfarin.wiki 游戏内教学「据点供货」（游戏数据 1.6）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_settlement
  - title: warfarin.wiki 游戏内教学「物资调度」「弹性需求物资」（游戏数据 1.6）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_domain_shop_1
  - title: warfarin.wiki 游戏内教学「仓储节点」「货物装箱」「转交运送委托」（游戏数据 1.6）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_domain_depot_2
  - title: warfarin.wiki 游戏内教学「地区仓库」「扩张管理系统」（游戏数据 1.6）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_map_storage
  - title: Endfield Talos Wiki 的 Regional Development 页
    url: https://endfield.wiki.gg/wiki/Regional_Development
  - title: Endfield Talos Wiki 的 Automated Industry Complex 页
    url: https://endfield.wiki.gg/wiki/Automated_Industry_Complex
  - title: Endfield Talos Wiki 的 Thermal Bank 页
    url: https://endfield.wiki.gg/wiki/Thermal_Bank
  - title: Endfield Talos Wiki 的 Outpost 页
    url: https://endfield.wiki.gg/wiki/Outpost
  - title: Endfield Talos Wiki 的 Stock Redistribution 页
    url: https://endfield.wiki.gg/wiki/Stock_Redistribution
  - title: Endfield Talos Wiki 的 Depot Node 页
    url: https://endfield.wiki.gg/wiki/Depot_Node
  - title: 「新潮起，故渊离」版本更新说明
    url: https://endfield.gryphline.com/en-us/news/8907
  - title: 「春晓时」版本更新说明
    url: https://endfield.gryphline.com/en-us/news/0751
  - title: 「寻遗散记」版本更新说明
    url: https://endfield.gryphline.com/en-us/news/0758
  - title: 「向渊行」版本更新说明
    url: https://endfield.gryphline.com/en-us/news/5200
  - title: 「丹青渡」版本更新说明
    url: https://endfield.gryphline.com/en-us/news/9560
  - title: 「丹青渡」版本开发组通讯
    url: https://endfield.gryphline.com/en-us/news/7014
---

地区建设是四号谷地与武陵各自的发展进度，以地区建设等级衡量。探索地区、向据点供货等方式会获得地区建设值，累积后提升地区建设等级；等级提升会开放跨地区传输等功能、提高矿物产率，并增加可摆放的设备数量。据点以调度券收购集成工业产物；调度券可在物资调度购买货品，也用于升级仓储节点、各类终端与集成核心区域。

## 跨地区传输：在武陵与四号谷地之间运送物品

跨地区传输把物品从一个地区的仓库送到另一个地区的仓库，在协议核心的协议管理处使用。两种模式都依传输起点地区的地区建设等级解锁：

| 模式 | 起点仓库 | 终点仓库 | 解锁 |
| --- | --- | --- | --- |
| 库存传输 | 扣除送出的物品 | 获得等量物品 | 起点地区达到对应建设等级 |
| 超库存传输 | 不扣除物品 | 获得对应物品 | 起点地区达到较高建设等级 |

设定传输后，物品会持续传输，每 1 小时一次。以四号谷地为起点地区时：

| 四号谷地等级 | 跨地区传输 |
| --- | --- |
| 8 | 解锁，传输总值 800 |
| 9 | 900 |
| 10 | 1,000 |
| 11 | 1,200 |
| 12 | 1,500，并解锁超库存传输 |

以武陵电池运转四号谷地的热能池：

- 跨地区传输送来的物品进入四号谷地的仓库。协议核心或次级核心的取货口，或仓库取货口，可把仓库中选定的物品送上传送带，运往热能池。
- 低容量与中容武陵电池都是热能池的燃料，电力分别为 1600 与 3200，每个燃烧 40 秒：一座热能池每小时用掉 90 个电池。
- 两种武陵电池都在封装机制造：配方见[集成工业电力](/zh-cn/aic/power/)。

## 据点与调度券

| 项目 | 规则 |
| --- | --- |
| 据点的作用 | 与据点建立联系后开启据点供货：据点会随时间累积调度券，交易据点需要的货物即可获得 |
| 上限 | 调度券累积到上限后停止，要交易后才继续累积；据点的调度券用完时，要等它再累积才能交易 |
| 据点发展值 | 交易会获得据点发展值；足够后提升据点发展阶段，据点需要的货物更多、更好，报酬也更高 |
| 次级核心 | 每个据点都从部署一座次级核心开始 |
| 指派干员 | 可指派一名干员到据点；干员的阵营、爱好与专长符合据点需求时，据点效率提升 |
| 区域防卫 | 在预警终端进行；每完成一级，调度券的累积速度提升 |

谷地调度券在四号谷地的物资调度处使用，武陵调度券在武陵物资调度使用。地区调度券也可在集成管家处升级集成核心区域，让区域面积扩大。

武陵有三个据点：天王坪援助点（1.1 版与 1.3 版提升等级上限）、心脏修缮站（1.2 版新增）与盈天台建设站（1.4 版新增，位于武陵 - 应龙关）。四号谷地也有三个据点。

据点收购的电池：

| 电池 | 价格 | 收购的据点 |
| --- | --- | --- |
| 低容谷地电池 | 30 谷地调度券 | 四号谷地 3 个中的 1 个 |
| 中容谷地电池 | 30 谷地调度券 | 四号谷地 3 个中的 3 个 |
| 高容谷地电池 | 70 谷地调度券 | 四号谷地 3 个中的 3 个 |
| 低容武陵电池 | 25 武陵调度券 | 武陵 3 个中的 2 个 |
| 中容武陵电池 | 54 武陵调度券 | 武陵 3 个中的 3 个 |

## 物资调度与弹性需求物资

- 物资调度可用调度券以较多的折扣购买商品。将其他物资调度员纳入系统或升级现有的物资调度员，可解锁更多商品。
- 商品有库存上限，部分每周更新；终端以调度券升级。
- 弹性需求物资的价格每天波动：低价买入、高价卖出。好友飞船上的价格与当地不同，可前往好友的飞船出售。地区的第一个物资调度终端升到 2 级时开放弹性需求物资。

## 仓储节点与装箱运送

- 解锁与升级仓储节点可提高地区仓库的库存上限。四号谷地有三个仓储节点，武陵有两个；武陵的第二个节点位于武陵 - 试验园区，于 1.2 版新增。
- 装箱运送：在仓储节点把货物装箱，从取货点运至送货点，以赚取调度券。货物应完好送达，滑索架可让运送更快、更安全。每日接取的委托有上限。升级仓储节点可解锁更多可运输的货物类型与更大的包裹。
- 已接取的运送委托可在任务系统中转交给其他玩家。其他玩家完成后，双方都获得等额的尾款。

对于未能按时完成的转交委托，两个来源说法不一。游戏内教学写明，双方仍可获得一半的调度券尾款。1.6 版开发组通讯则写明，自 1.6 版起，转交后超过一定时间没有被接取的委托，会由其他协助者接手并完成。

## 地区建设等级

| 项目 | 规则 |
| --- | --- |
| 如何提升 | 地区建设值，来自探索、向据点供货、在新矿点摆放矿机、升级据点、资源回收站、物资调度终端、仓储节点与环境监测终端，以及完成任务 |
| 提升什么 | 开放新功能、提高矿物产率、增加可摆放的设备：各区域的协议容量、滑索摆放上限、战斗设施上限与矿物纯度 |
| 例子 | 武陵城的协议容量为 200，3 级时 250，5 级时 300，7 级时 350，为上限 |
| 等级上限 | 四号谷地最高 12 级。1.1 至 1.6 版每一版都提升了武陵的上限 |
| 事务总览 | 自 1.3 版起，地区建设界面的事务总览会显示物资调度、仓储节点的信息与地图位置 |

协议容量本身的说明见[生产与物流](/zh-cn/aic/production/)。
