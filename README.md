
***
### 2016003681 오현주
***

# **TETRIS**

## 실행방법
'clond or download'로 파일 저장

`python tetris.py`을 입력하여 실행

## 조작법
- ← : 왼쪽 이동
- → : 오른쪽 이동
- ↑ : 오른쪽으로 회전
- ↓ : 한칸씩 내려감
- 스페이스바 : 바닥으로 내리기
- P 키 : 게임 정지
- Z 키 : 다음 블록으로 바꾸기
- R 키 : 메인 메뉴로 돌아가기

## 특성
- ### 메인 메뉴 >
   게임시작, 음소거 기능, 최고점수 알려주기, 조작법 설명, 게임 종료
![](https://github.com/hjoo5/2017OSD_GAME/blob/master/Picture/startscreen.PNG)
- ### 게임 안에서 >
   게임점수, 게임 최고점수, 게임 레벨, 다음 블록으로 바꾸기, 메인메뉴로 돌아가기
![](https://github.com/hjoo5/2017OSD_GAME/blob/master/Picture/gamescreen.PNG)
- ### 게임 정지 화면 >
![](https://github.com/hjoo5/2017OSD_GAME/blob/master/Picture/pause.PNG)
- ### 게임오버 화면 >
![](https://github.com/hjoo5/2017OSD_GAME/blob/master/Picture/gameover.PNG)
- ### 음악 > 음소거 가능
![](https://github.com/hjoo5/2017OSD_GAME/blob/master/Picture/mute.PNG)
- ### 최고 점수 >
![](https://github.com/hjoo5/2017OSD_GAME/blob/master/Picture/highscore.PNG)
   점수설정은 한줄을 지우면 1점이 올라가는 것이다.

   10점이 올라갈때 마다 레벨이 1씩 증가한다. 레벨이 증가하면 블록이 내려오는 속도가 빨라진다.
- ### 조작법 설명 >
![](https://github.com/hjoo5/2017OSD_GAME/blob/master/Picture/instruction.PNG)


자세한 설명은 WIKI


## 부족한 부분 / 추가하고 싶은 것
- 메뉴를 선택하고 메인메뉴로 넘어갈 때, 화면에 이전 메뉴 화면이 남아있다.
- 메뉴를 번호로만 선택할 수 있다. 방향키로 이동하여 선택하는 방법을 추가하고 싶다.
- 블록을 이동할 때, 블록 한줄이 삭제될 때 등의 이벤트가 발생할때 효과음을 추가하고 싶다.
- 게임이벤트> 게임 도중에 5초안에 한줄을 없애지못하면 게임이 종료되는 이벤트를 추가하고 싶다.
- 폭탄이 블록 대신 떨어지면서 폭탄을 이동시키다 바닥에 놓으면 주위 블록이 사라지도록 하고 싶다.