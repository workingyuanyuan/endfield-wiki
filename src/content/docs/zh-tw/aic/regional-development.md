---
title: 地區建設
description: "《明日方舟：終末地》的地區建設是各地區的等級，升級會開放跨地區傳輸並增加可放置的設施。"
appliesTo: 《明日方舟：終末地》國際版，1.7 版；教學文字取自遊戲資料 1.7
caveat: 跨地區傳輸依傳輸起點地區的地區建設等級解鎖。庫存傳輸會從起點地區的倉庫扣除物品；只有更高等級才解鎖的超庫存傳輸不扣除起點的物品。
lastVerified: 2026-11-26
effectiveDate: 2026-11-25
aliases:
  - Regional Development
  - 地区建设
  - 地域建設
  - 지역 건설
sources:
  - title: warfarin.wiki 遊戲內教學「跨地區傳輸」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_domain_transport
  - title: warfarin.wiki 遊戲內教學「地區建設系統」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_domain
  - title: warfarin.wiki 遊戲內教學「據點供貨」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_settlement
  - title: warfarin.wiki 遊戲內教學「物資調度」「彈性需求物資」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_domain_shop_1
  - title: warfarin.wiki 遊戲內教學「倉儲節點」「貨物裝箱」「轉交運送委託」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_sys_domain_depot_2
  - title: warfarin.wiki 遊戲內教學「地區倉庫」「擴張管理系統」（遊戲資料 1.7）
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_map_storage
  - title: Endfield Talos Wiki 的 Regional Development 頁
    url: https://endfield.wiki.gg/wiki/Regional_Development
  - title: Endfield Talos Wiki 的 Automated Industry Complex 頁
    url: https://endfield.wiki.gg/wiki/Automated_Industry_Complex
  - title: Endfield Talos Wiki 的 Thermal Bank 頁
    url: https://endfield.wiki.gg/wiki/Thermal_Bank
  - title: Endfield Talos Wiki 的 Outpost 頁
    url: https://endfield.wiki.gg/wiki/Outpost
  - title: Endfield Talos Wiki 的 Stock Redistribution 頁
    url: https://endfield.wiki.gg/wiki/Stock_Redistribution
  - title: Endfield Talos Wiki 的 Depot Node 頁
    url: https://endfield.wiki.gg/wiki/Depot_Node
  - title: 「新潮起，故淵離」版本更新說明
    url: https://endfield.gryphline.com/en-us/news/8907
  - title: 「春曉時」版本更新說明
    url: https://endfield.gryphline.com/en-us/news/0751
  - title: 「尋遺散記」版本更新說明
    url: https://endfield.gryphline.com/en-us/news/0758
  - title: 「向淵行」版本更新說明
    url: https://endfield.gryphline.com/en-us/news/5200
  - title: 「丹青渡」版本更新說明
    url: https://endfield.gryphline.com/en-us/news/9560
  - title: 「丹青渡」版本開發組通訊
    url: https://endfield.gryphline.com/en-us/news/7014
  - title: 「穿越甚大蘑境與你相逢」版本更新說明
    url: https://endfield.gryphline.com/en-us/news/0740
---

## 地區建設等級

地區建設是四號谷地與武陵各自的發展進度，以地區建設等級衡量。探索地區、向據點供貨等方式會獲得地區建設值，累積後提升地區建設等級；等級提升會開放跨地區傳輸等功能、提高礦物產率，並增加可擺放的設備數量。據點以調度券收購集成工業產物；調度券可在物資調度購買貨品，也用於升級倉儲節點、各類終端與集成核心區域。

## 跨地區傳輸：在武陵與四號谷地之間運送物品

跨地區傳輸把物品從一個地區的倉庫送到另一個地區的倉庫，在協議核心的協議管理處使用。兩種模式都依傳輸起點地區的地區建設等級解鎖：

| 模式 | 起點倉庫 | 終點倉庫 | 解鎖 |
| --- | --- | --- | --- |
| 庫存傳輸 | 扣除送出的物品 | 獲得等量物品 | 起點地區達到對應建設等級 |
| 超庫存傳輸 | 不扣除物品 | 獲得對應物品 | 起點地區達到較高建設等級 |

設定傳輸後，物品會持續傳輸，每 1 小時一次。以四號谷地為起點地區時：

| 四號谷地等級 | 跨地區傳輸 |
| --- | --- |
| 8 | 解鎖，傳輸總值 800 |
| 9 | 900 |
| 10 | 1,000 |
| 11 | 1,200 |
| 12 | 1,500，並解鎖超庫存傳輸 |

以武陵電池運轉四號谷地的熱能池：

- 跨地區傳輸送來的物品進入四號谷地的倉庫。協議核心或次級核心的取貨口，或倉庫取貨口，可把倉庫中選定的物品送上傳送帶，運往熱能池。
- 低容量、中容量與高容量武陵電池都是熱能池的燃料，電力分別為 1600、3200 與 6400，每個燃燒 40 秒：一座熱能池每小時用掉 90 個電池。
- 三種武陵電池都在封裝機製造（配方見[集成工業電力](/zh-tw/aic/power/)）。

## 據點與調度券

| 項目 | 規則 |
| --- | --- |
| 據點的作用 | 與據點建立聯繫後開啟據點供貨：據點會隨時間累積調度券，交易據點需要的貨物即可獲得 |
| 上限 | 調度券累積到上限後停止，要交易後才繼續累積；據點的調度券用完時，要等它再累積才能交易 |
| 據點發展值 | 交易會獲得據點發展值；足夠後提升據點發展階段，據點需要的貨物更多、更好，報酬也更高 |
| 次級核心 | 每個據點都從部署一座次級核心開始 |
| 指派幹員 | 可指派一名幹員到據點；幹員的陣營、愛好與專長符合據點需求時，據點效率提升 |
| 區域防衛 | 在預警終端進行；每完成一級，調度券的累積速度提升 |

谷地調度券在四號谷地的物資調度處使用，武陵調度券在武陵物資調度使用。地區調度券也可在集成管家處升級集成核心區域，讓區域面積擴大。

武陵有三個據點：天王坪援助點（1.1 版與 1.3 版提升等級上限）、心臟修繕站（1.2 版新增）與盈天台建設站（1.4 版新增，位於武陵 - 應龍關）。四號谷地也有三個據點。

據點收購的電池：

| 電池 | 價格 | 收購的據點 |
| --- | --- | --- |
| 低容量谷地電池 | 30 谷地調度券 | 四號谷地 3 個中的 1 個 |
| 中容量谷地電池 | 30 谷地調度券 | 四號谷地 3 個中的 3 個 |
| 高容量谷地電池 | 70 谷地調度券 | 四號谷地 3 個中的 3 個 |
| 低容量武陵電池 | 25 武陵調度券 | 武陵 3 個中的 2 個 |
| 中容量武陵電池 | 54 武陵調度券 | 武陵 3 個中的 3 個 |

## 物資調度與彈性需求物資

- 物資調度可用調度券以較多的折扣購買商品。將其他物資調度員納入系統或升級現有的物資調度員，可解鎖更多商品。
- 商品有庫存上限，部分每週更新；終端以調度券升級。
- 彈性需求物資的價格每天波動：低價買入、高價賣出。好友飛船上的價格與當地不同，可前往好友的飛船出售。地區的第一個物資調度終端升到 2 級時開放彈性需求物資。

## 倉儲節點與裝箱運送

- 解鎖與升級倉儲節點可提高地區倉庫的庫存上限。四號谷地有三個倉儲節點，武陵有兩個；武陵的第二個節點位於武陵 - 實驗園區，於 1.2 版新增。
- 裝箱運送：在倉儲節點把貨物裝箱，從取貨點運至送貨點，以賺取調度券。貨物應完好送達，滑索架可讓運送更快、更安全。每日接取的委託有上限。升級倉儲節點可解鎖更多可運輸的貨物類型與更大的包裹。
- 已接取的運送委託可在任務系統中轉交給其他玩家。其他玩家完成後，雙方都獲得等額的尾款。

對於未能按時完成的轉交委託，兩個來源說法不一。遊戲內教學寫明，雙方仍可獲得一半的調度券尾款。1.6 版開發組通訊則寫明，自 1.6 版起，轉交後超過一定時間沒有被接取的委託，會由其他協助者接手並完成。

## 地區建設等級

| 項目 | 規則 |
| --- | --- |
| 如何提升 | 地區建設值，來自探索、向據點供貨、在新礦點擺放礦機、升級據點、資源回收站、物資調度終端、倉儲節點與環境監測終端，以及完成任務 |
| 提升什麼 | 開放新功能、提高礦物產率、增加可擺放的設備：各區域的協議容量、滑索擺放上限、戰鬥設施上限與礦物純度 |
| 例子 | 武陵城的協議容量為 200，3 級時 250，5 級時 300，7 級時 350，為上限 |
| 等級上限 | 四號谷地最高 12 級。1.1 至 1.7 版每一版都提升了武陵的上限 |
| 事務總覽 | 自 1.3 版起，地區建設介面的事務總覽會顯示物資調度、倉儲節點的資訊與地圖位置 |


