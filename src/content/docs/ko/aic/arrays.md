---
title: "배열과 금지 구역 재건"
description: "《명일방주: 엔드필드》 무릉의 배열은 적동 조각과 식양에 명·회·형 특성을 부여하며, 금지 구역 재건에 쓰인다."
appliesTo: "《명일방주: 엔드필드》 글로벌 서비스, 1.7 버전. 배열, 제작법, 재건 데이터는 게임 데이터 1.7 기준"
caveat: "배열은 완전히 겹칠 때만 중첩된다. 같은 종류의 배열 두 개를 겹치면 단계가 오르고, 배열 · 명을 배열 · 회에 겹쳐 배열 · 형이 되는 것은 공업 기술 「명회 중첩」을 연구한 뒤뿐이다."
lastVerified: 2026-11-26
effectiveDate: 2026-11-25
aliases:
  - Arrays and Exclusion Zone Rebuilding
  - 陣列與重建禁區
  - 阵列与重建禁区
  - 陣と封鎖区域再建
  - Forge of Luminance
  - Forge of Equilibrium
  - 明晦爐
  - 平衡爐
sources:
  - title: "「뜻밖의 만남, 버섯 동산 대모험」 버전 업데이트 설명"
    url: https://endfield.gryphline.com/en-us/news/0740
  - title: "warfarin.wiki, 게임 내 튜토리얼 「명회로」(게임 데이터 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_ming
  - title: "warfarin.wiki, 게임 내 튜토리얼 「배열 · 회」(게임 데이터 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_hui
  - title: "warfarin.wiki, 게임 내 튜토리얼 「배열 · 형」(게임 데이터 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_1_heng
  - title: "warfarin.wiki, 게임 내 튜토리얼 「분화 명회로」(게임 데이터 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_spwaner_2
  - title: "warfarin.wiki, 게임 내 튜토리얼 「균형로」(게임 데이터 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_magic_balancer_1
  - title: "warfarin.wiki, 게임 내 튜토리얼 「재건 공급 포트」(게임 데이터 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_wonder_supply_port_1
  - title: "warfarin.wiki, 게임 내 튜토리얼 「고효율 휘동 생산 라인」(게임 데이터 1.7)"
    url: https://warfarin.wiki/en/tutorials/wiki_tut_fac_copper_bright_cube
  - title: "배열 표 FactoryFormationTable, FactoryFormationLevelTable, FactoryFormationTransTable(게임 데이터 1.7): 배열 종류, 단계와 부여 확률"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationTransTable.json
  - title: "명회로 표 FactoryFormationStakeTable(게임 데이터 1.7): 기체 식양과 배열 범위"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryFormationStakeTable.json
  - title: "설비 표 FactoryBuildingTable(게임 데이터 1.7): 소비 전력, 포트와 점유 면적"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryBuildingTable.json
  - title: "제작법 표 FactoryMachineCraftTable(게임 데이터 1.7): 균형로와 재건 물자"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FactoryMachineCraftTable.json
  - title: "공업 계획 표 FacSTTNodeTable(게임 데이터 1.7): 배열 관련 기술"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/FacSTTNodeTable.json
  - title: "재건 표 WonderStageTable(게임 데이터 1.7): 단계와 물자"
    url: https://github.com/rmxlinux/EndfieldData/blob/887923b9e56e132f2570a25e8c2cf5e971508736/TableCfg/WonderStageTable.json
---

## 설비

| 설비 | 소비 전력 | 점유 면적 | 역할 |
| --- | --- | --- | --- |
| 명회로 | — | 5 × 5 | 앞쪽에 배열 1개(배열 · 명 또는 배열 · 회)를 생성한다 |
| 분화 명회로 | — | 5 × 5 | 앞쪽과 옆쪽에 배열 2개를 생성한다 |
| 균형로 | 50 | 5 × 5 | 한 재료의 명형과 회형을 합쳐 새로운 재료로 만든다. 컨베이어 벨트 입력 포트 5개와 출력 포트 5개가 있다 |
| 재건 공급 포트 | — | 3 × 3 | 투입된 재건 물자를 북쪽 금지 구역의 재건 창고로 보낸다 |

이 설비들은 모두 무릉에서만 지을 수 있다. 명회로는 전력을 쓰지 않으며, 액체 포트에 기체 식양을 일정한 유속으로 계속 주입하면 활성화된다. 필요한 최저 유속은 고체 · 기체 전환기의 활성화 포트와 같다. 각 배열은 명회로에서 일정 거리 떨어진 곳에 5 × 5 범위를 차지한다.

## 배열

| 배열 | 영어 | 중국어 번체 | 생성 방식 | 적동 조각이 바뀌는 것 | 식양이 바뀌는 것 |
| --- | --- | --- | --- | --- | --- |
| 배열 · 명 | L-Array | 陣列·明 | 명회로 | 명형 적동 | 명형 식양 |
| 배열 · 회 | T-Array | 陣列·晦 | 명회로(회형 확장 연구 후) | 회형 적동 | 회형 식양 |
| 배열 · 형 | E-Array | 陣列·衡 | 완전히 겹친 배열 · 명과 배열 · 회(명회 중첩 연구 후) | 형동 | 형식양 |

배열은 컨베이어 벨트가 그 범위를 지나며 운반하는 적동 조각과 식양에 작용한다. 일정 시간마다 배열의 특성을 부여하며, 부여는 매번 배열 단계에 따른 확률로 성공한다.

## 단계와 부여 확률

| 배열 | 1단계 | 2단계 | 3단계 | 4단계 |
| --- | --- | --- | --- | --- |
| 배열 · 명 | 20% | 40% | 60% | 100% |
| 배열 · 회 | 20% | 40% | 60% | 100% |
| 배열 · 형 | 40% | 80% | — | — |

같은 종류의 배열이 완전히 겹치면 중첩되어 단계가 오르며, 최대 4단계까지 오른다. 배열 · 명끼리 완전히 겹치면 2단계 배열 · 명이 된다. 일부만 겹친 배열은 중첩되지 않는다. 분화 명회로의 배열은 다른 분화 명회로의 배열과 둘 다 중첩되며, 두 배열의 단계가 동시에 오른다.

## 균형로 제작법

| 재료 | 생산품 | 시간 |
| --- | --- | --- |
| 명형 식양 ×5, 회형 식양 ×5 | 중식양 ×2 | 10초 |
| 명형 적동 ×10, 회형 적동 ×10 | 혁동 조각 ×5 | 10초 |
| 형식양 ×10, 형동 ×10 | 휘동 ×5 | 10초 |

## 재건 물자

| 물자 | 설비 | 재료 | 생산품 | 시간 |
| --- | --- | --- | --- | --- |
| 명형 적동 부품 | 부품 가공기 | 명형 적동 ×1 | 명형 적동 부품 ×1 | 2초 |
| 회형 적동 부품 | 부품 가공기 | 회형 적동 ×1 | 회형 적동 부품 ×1 | 2초 |
| 휘동 부품 | 부품 가공기 | 휘동 ×1 | 휘동 부품 ×1 | 2초 |
| 적동 명양 부품 | 포장기 | 명형 적동 부품 ×10, 명형 식양 ×5 | 적동 명양 부품 ×5 | 10초 |
| 적동 중장갑 부품 | 포장기 | 회형 적동 부품 ×15, 중식양 ×2 | 적동 중장갑 부품 ×5 | 10초 |
| 휘동 에너지 블록 | 포장기 | 휘동 부품 ×5, 고밀도 오리지늄 가루 ×5 | 휘동 에너지 블록 ×5 | 10초 |

휘동은 기체로도 만들 수 있다. 기체 반응로가 기체 형동 ×1과 기체 형식양 ×1을 맑은 기체 휘동 ×2로 바꾸고, 고체 · 기체 전환기가 맑은 기체 휘동 ×2를 휘동 ×2로 바꾼다. 기체 형동과 기체 형식양은 고체 · 기체 전환기에서 형동과 형식양으로 만든다.

## 금지 구역 재건

| 단계 | 투입하는 물자 |
| --- | --- |
| 1, 남쪽 건설 | 적동 명양 부품 |
| 2, 북쪽 건설 | 적동 명양 부품, 적동 중장갑 부품 |
| 3, 배열 점화 | 적동 명양 부품, 적동 중장갑 부품, 휘동 에너지 블록 |
| 4, 지속 유지 | 적동 명양 부품, 적동 중장갑 부품, 휘동 에너지 블록 |

이 모드는 서브 임무 「고향 재건(2)」로 해금된다. 1단계와 2단계에서 북쪽 금지 구역의 남쪽, 이어서 북쪽에 천사장 배열을 세우고, 3단계에서 두 곳을 점화하며, 마지막인 4단계에서 이를 유지한다. 물자는 재건 공급 포트를 거쳐 재건 창고에 도착하며, 재건 창고는 물자를 종류마다 최대 8,000개까지 보관한다. 재건은 무릉의 지역 건설을 진행시킨다([지역 건설](/ko/aic/regional-development/) 참조).

## 통합 공업 기술

| 기술 | 선행 기술 | 공업 계획 | 해금 대상 | 진행 후 연구할 수 있는 임무 |
| --- | --- | --- | --- | --- |
| 명회로 점화 | — | 무릉 공업 I | 명회로, 배열 · 명 | — |
| 재건 공급 | 명회로 점화 | 무릉 공업 I | 재건 공급 포트 | 고향 재건(2) |
| 회형 확장 | 재건 공급 | 무릉 공업 II | 배열 · 회 | 고향 재건(2) |
| 명회 균형 | 회형 확장 | 무릉 공업 II | 균형로 | 고향 재건(2) |
| 명회 중첩 | 명회 균형 | 무릉 공업 III | 배열 · 형 | 고향 재건(3) |
| 명회 분화 | 명회 중첩 | 무릉 공업 III | 분화 명회로 | 고향 재건(3) |

설비를 해금하는 기술을 연구하면 그 설비도 2개 얻는다.
