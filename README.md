![header](https://capsule-render.vercel.app/api?type=waving&height=300&color=gradient&text=MoodFlix&fontColor=61FBFF&descAlign=96&descAlignY=91)

# SSAFY 관통 프로젝트

### 목차

1. 프로젝트 소개
2. 기술 스택
3. 주요 기능
4. 설치 및 실행 방법


## 1. 프로젝트 소개
- 영화는 단순한 시청각 콘텐츠가 아닌 사람의 감정과 교감하는 특별한 매개체, 종합예술
- 사용자의 현재 감정에 따라 영화로부터 느낄 수 있는 감정이 다를 수 있음

### 특징
- 감정과 영화 장르의 매칭
    - 예시로, "행복한" 감정은 '코미디', '가족', '음악' 장르의 영화가 포함될 수 있음
- 사용자 경험 강화
    - 감정을 입력하면 AI가 분석해서 적합한 영화를 추천함

### 페르소나: 김하나 (Hana Kim)
#### 기본 정보
- 이름: 김하나
- 나이: 27세
- 직업: 마케팅 회사 대리
- 거주지: 서울시 마포구
- 가족 상태: 1인 가구
- 취미: 영화 감상, 카페 탐방, SNS 활동
- 배경과 성격
- 배경: <br>
김하나는 바쁜 업무와 촉박한 마감일로 인해 스트레스를 자주 받는다. 평소 영화를 보는 것이 스트레스 해소와 힐링의 중요한 수단이다. 하지만 어떤 영화를 선택해야 할지 고민하는 시간이 많아 종종 선택 장애를 겪는다.

- 성격: <br>
감성적이고 직관적인 성격으로, 영화나 콘텐츠를 통해 감정을 느끼는 것을 중요하게 여긴다. 영화 리뷰나 추천 알고리즘보다는 현재의 기분에 맞는 영화를 선택하고 싶어 한다.

- 목표 <br>
기분에 맞는 영화를 빠르고 정확하게 추천받고 싶다.
스트레스를 풀거나 에너지를 충전할 수 있는 감정 기반의 영화 리스트를 확인하고 싶다.
다른 사용자들과 영화에 대해 소통하며 공감대를 형성하고 싶다.
- 문제점 <br>
기존 영화 추천 서비스는 장르나 평점 중심이라 현재 감정에 맞는 영화를 찾기 어렵다.
선택할 영화가 너무 많아 시간을 낭비하거나, 선택 후 만족하지 못하는 경우가 많다.
추천받은 영화가 자신의 현재 기분과 맞지 않아 몰입하기 힘들 때가 있다.

#### MoodFlix와의 연결

- 기대하는 경험:

    - 기분을 "행복", "우울", "신나는", "잔잔한" 등으로 입력했을 때, 감정에 딱 맞는 영화를 추천받고 싶다.

    - 추천받은 영화의 줄거리와 리뷰를 확인해 선택의 확신을 얻고 싶다.

    - 댓글 기능을 활용해 비슷한 감정을 느낀 사용자들과 영화에 대해 소통하고 공감하고 싶다.

##### 주요 사용 시나리오:

- 금요일 저녁, 퇴근 후 스트레스를 풀고 싶어 "짜릿한 기분"을 선택 → 액션, 어드벤처, SF 장르의 추천 리스트 확인.
- 비 오는 날, 창밖을 보며 차분한 감정을 느낄 때 "잔잔한 기분"을 선택 → 감성 드라마와 음악 영화 추천.
- 영화 감상 후 프로필 페이지에서 자신이 남긴 댓글과 좋아요 기록을 확인.

### 기술 활용
- AI 감정 분석: <br>
    - "짜증난 하루였어"와 같은 입력을 통해 OpenAI가 김하나의 감정을 분석, 해당 감정에 맞는 영화 리스트를 추천.

- 맞춤형 추천 알고리즘: <br>
    - 김하나가 자주 선택하는 감정 패턴을 분석하여 개인화된 영화 추천.

- 키워드
    - 감정적, 감성적, 직관적, 몰입, 개인화된 추천

##2. 기술 스택
#### Backend
- Django :
    - DRF (Django Rest Framework)를 사용한 API 설계
    - CBV (Class-Based View)를 활용한 구조화된 코드
    - DRF 문서화를 통해 API 명세 제공
    - sqlite3(DB)
#### Frontend
- Vues.js :
    - Pinia를 사용한 상태 관리
    - Axios를 통한 백엔드 API 호출
    - JQuery 및 Slick을 활용한 UI 효과
#### 사용된 API
- TMDB API: 영화 데이터 (세부 정보, 장르, 평점 등) 제공
- OpenAI API: 사용자의 입력 감정을 기반으로 영화 추천
## 3. 주요 기능
1. 영화 메인 페이지
    ![로그인페이지](/uploads/34a220a3a8a14f8b1d3f4e3fa4c5c760/로그인페이지.png)
    ![메인페이지](/uploads/d7baba8224adca6a8679859045fa7796/메인페이지.png)
    - 개봉 예정작과 최신 리뷰를 한눈에 볼 수 있습니다.

2. 감정 추천 페이지
    ![감정추천-1](/uploads/f3f5d65e0d0e72dee55ecda721eeff59/감정추천-1.png)
    ![감정추천-2](/uploads/349b3e20554c767beb6269707b47c6d5/감정추천-2.png)
    - 감정별로 분류된 영화 목록을 제공합니다.
    - 예: "행복한 감정" → 코미디, 가족, 음악 장르의 영화.

3. 영화 세부 정보 페이지
    ![검색페이지](/uploads/5d57d896c12b85f7cae50fb152ebf266/검색페이지.png)
    ![상세페이지-1](/uploads/8618fcee1f263cdb8c5bfb77e0156495/상세페이지-1.png)
    ![상세페이지-2](/uploads/d7092490c27a1754b37867e40ff6aeef/상세페이지-2.png)
    - 영화의 세부 정보를 확인할 수 있습니다.
        - TMDB API로부터 가져온 정보 (제목, 줄거리, 배우 등)
        - 사용자 댓글 기능 (좋아요 포함)
        - 사용자 프로필 페이지

4. 사용자 개인화 기능 제공:
    ![프로필_페이지](/uploads/614451d6fc7f5afd2969bc2c2238b949/프로필_페이지.png)
    - 팔로워 및 팔로잉 관리
    - 찜한 영화, 작성한 리뷰, 댓글 기록 확인
    - 감정을 바탕으로 하는 영화 추천 페이지

5. 감정 분석 기능 제공
    ![감정분석-1](/uploads/983895ba9f8fba151b811006a734d1da/감정분석-1.png)
    ![감정분석-2](/uploads/fcb80d6abb12a8667cf6bc7373a9fbe2/감정분석-2.png)
    - 사용자가 감정을 입력하면 OpenAI를 통해 해당 감정을 분석하여 적합한 영화를 추천.

## 4. 설치 및 실행 방법
### 필수 요건
- Python 3.9 이상
- Node.js 16.x 이상
- npm 6.x 이상
### 설치 과정
1. 백엔드(Django) 설정
```bash

# 저장소 클론
git clone https://github.com/username/project-name.git
cd project-name/backend

# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  
# Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python manage.py runserver
```
2. 프론트엔드(Vue.js) 설정

```bash
코드 복사
cd ../frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run serve

```
3. 브라우저에서 http://localhost:8000 (백엔드) 및 http://localhost:5173 (프론트엔드)로 접속.
