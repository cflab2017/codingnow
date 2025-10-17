# 점프 런 (Jump Run)

## 게임 설명

"Jump Run"은 파이썬(Python)과 Pygame을 사용하여 만든 2D 러닝 게임입니다. 플레이어 캐릭터는 자동으로 오른쪽으로 달리며, 장애물을 피해야 합니다. 시간이 지날수록 게임 속도가 빨라져 난이도가 증가합니다.

## 게임 규칙

-   **조작:**
    -   `스페이스바`: 점프
    -   `↓ (아래쪽 화살표 키)`: 슬라이드
-   **목표:** 장애물을 피하면서 최대한 오래 살아남으세요.
-   **게임 오버:** 장애물과 충돌하면 게임이 종료됩니다.
-   **점수:** 생존 시간 또는 피한 장애물의 수로 점수가 계산됩니다.

## 아이템

-   **하트:** 획득 시 생명력이 증가합니다.

## 코드 구성

```
.
├── main.py         # 게임의 메인 루프 및 초기 설정
├── assets/         # 게임에 사용되는 이미지 파일
│   ├── bg.png
│   ├── dirt.png
│   ├── drone.png
│   ├── explosion_0.png
│   ├── explosion_1.png
│   ├── explosion_2.png
│   ├── explosion_3.png
│   ├── heart.png
│   ├── lava.png
│   ├── missile.png
│   ├── platform.png
│   ├── player_0.png
│   ├── player_1.png
│   ├── player_2.png
│   ├── player_3.png
│   └── player_lie.png
├── src/            # 게임의 주요 로직 (모듈화)
│   ├── background.py   # 배경 스크롤 처리
│   ├── drone.py        # 드론 장애물 관련 로직
│   ├── explosion.py    # 폭발 애니메이션 효과
│   ├── ground.py       # 지형 관련 로직
│   ├── item.py         # 아이템 관련 로직
│   ├── keyboard.py     # 화면에 표시되는 키보드 UI
│   ├── lava.py         # 용암 장애물 관련 로직
│   ├── map_manager.py  # 맵 생성 및 관리
│   ├── missile.py      # 미사일 장애물 관련 로직
│   └── player.py       # 플레이어 캐릭터 로직
└── readme_kr.md      # 게임 설명 (한글)
└── readme_en.md      # 게임 설명 (영문)
```
