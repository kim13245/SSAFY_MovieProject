![header](https://capsule-render.vercel.app/api?type=waving&height=300&color=gradient&text=MOODFLEX&fontColor=61FBFF&descAlign=96&descAlignY=91)

# SSAFY 관통 프로젝트

---

### 목차

1. 프로젝트 소개
2. 기술 스택
3. 주요 기능
4. 설치 및 실행 방법
5. ERD & UserFlow
6. 프로젝트 후기

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

## 2. 기술 스택

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
   https://private-user-images.githubusercontent.com/61528451/399174498-2623585c-9488-4b6d-872d-51a77e9db614.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzU0OTA3MjcsIm5iZiI6MTczNTQ5MDQyNywicGF0aCI6Ii82MTUyODQ1MS8zOTkxNzQ0OTgtMjYyMzU4NWMtOTQ4OC00YjZkLTg3MmQtNTFhNzdlOWRiNjE0LmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjI5VDE2NDAyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWE2YThkMzgwZTBiYzA3NGE4YmVmYWUyOTcyOGZmMjJhNDc2N2QzZDljY2ViZGEzYTE1MzhkYmFjNjgyMzVkNDUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.lzWuYPFH8iLaV2N9-Aqyao7ztG0Z8tVuJjbE6RhW_XI
   https://private-user-images.githubusercontent.com/61528451/399174562-46c73606-8bf3-472c-b16e-2d1e608d1179.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzU0OTA3MjcsIm5iZiI6MTczNTQ5MDQyNywicGF0aCI6Ii82MTUyODQ1MS8zOTkxNzQ1NjItNDZjNzM2MDYtOGJmMy00NzJjLWIxNmUtMmQxZTYwOGQxMTc5LmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjI5VDE2NDAyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTYzNzY3Zjk3MzBlMmU3ZWI5YWQ1MGRlNTE0NzI0NjRkZGM3N2IyZDQ0YmM0Nzk5OGQ3ZGJlYzNkMTRiYTdiMGYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.7vQSVniRa-20YoapH40DRsJPuxN1LJBKpoW6XVhe1h8

   - 개봉 예정작과 최신 리뷰를 한눈에 볼 수 있습니다.

3. 감정 추천 페이지
   https://private-user-images.githubusercontent.com/61528451/399174612-34811567-12b3-446a-811a-02d537e4b453.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzU0OTA3MjcsIm5iZiI6MTczNTQ5MDQyNywicGF0aCI6Ii82MTUyODQ1MS8zOTkxNzQ2MTItMzQ4MTE1NjctMTJiMy00NDZhLTgxMWEtMDJkNTM3ZTRiNDUzLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjI5VDE2NDAyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTkwZDYwYWNkN2QxMTI0NjVmMzBlZThjNDc1ODRhMDU1MThjOTQzM2FmYjBjNzM0NGJiOTg2OWViZDM1N2U5NDYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.gYWjuFIR9bHgsnXaEZJsx-wK6WQiKuYMtpkFh9J1jC4

   - 감정별로 분류된 영화 목록을 제공합니다.
   - 예: "행복한 감정" → 코미디, 가족, 음악 장르의 영화.

4. 영화 세부 정보 페이지
   https://private-user-images.githubusercontent.com/61528451/399174655-e8c48be5-0fe8-4541-bb28-9af86a0583f1.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzU0OTA3MjcsIm5iZiI6MTczNTQ5MDQyNywicGF0aCI6Ii82MTUyODQ1MS8zOTkxNzQ2NTUtZThjNDhiZTUtMGZlOC00NTQxLWJiMjgtOWFmODZhMDU4M2YxLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjI5VDE2NDAyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWM0NjRhOGRlZTgwNGI5ZWQwNTgzZTgxZjg5MjFkNmUzZGQwODhhZmM3NTYwOTZlNjdlOWI2YTRkOTZlN2M5MmQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.YW2ou21VmoG7Zfl3qNk3dOx-Yc3DaaE-xRrrCDh-Cew

   - 영화의 세부 정보를 확인할 수 있습니다.
     - TMDB API로부터 가져온 정보 (제목, 줄거리, 배우 등)
     - 사용자 댓글 기능 (좋아요 포함)
     - 사용자 프로필 페이지

5. 사용자 개인화 기능 제공:
   https://private-user-images.githubusercontent.com/61528451/399174717-6e2f1012-ffea-444f-bb35-b54c1b909d10.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzU0OTA3MjcsIm5iZiI6MTczNTQ5MDQyNywicGF0aCI6Ii82MTUyODQ1MS8zOTkxNzQ3MTctNmUyZjEwMTItZmZlYS00NDRmLWJiMzUtYjU0YzFiOTA5ZDEwLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjI5VDE2NDAyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTc2MjU3NDg1NTZiMzEyMDQ4NDY3YTFmNzkyZGYxMjc4NmNmNGVlZGUzNjZjMTZkMWRiZjdiMTFmM2E1ZjY1YjgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.5UMHGSPyqWmCMLLQF7aRtrpmicnff45rMq_cCLONPEo

   - 팔로워 및 팔로잉 관리
   - 찜한 영화, 작성한 리뷰, 댓글 기록 확인
   - 감정을 바탕으로 하는 영화 추천 페이지

6. 감정 분석 기능 제공
   [![감정분석-1](/uploads/983895ba9f8fba151b811006a734d1da/감정분석-1.png)](https://private-user-images.githubusercontent.com/61528451/399174766-673d4c28-1c7f-40ea-bb33-3a9f0eee073c.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzU0OTA3MjcsIm5iZiI6MTczNTQ5MDQyNywicGF0aCI6Ii82MTUyODQ1MS8zOTkxNzQ3NjYtNjczZDRjMjgtMWM3Zi00MGVhLWJiMzMtM2E5ZjBlZWUwNzNjLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjI5VDE2NDAyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTAxYTcyMmU4MjIwYzQxNzU1MzMyYzQ2MWMyZTAyMjljNWU1NTZjNGQyYjY5MWZlYzk5NjMxMGE0ZjY2MzczZmYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.M47Mxk10ukhVW-j_UOr7WUWWXSk9ikTJ7n3e-075S0Y)
   [![감정분석-2](/uploads/fcb80d6abb12a8667cf6bc7373a9fbe2/감정분석-2.png)](https://private-user-images.githubusercontent.com/61528451/399174768-729dad5a-1fc7-4d82-90fa-ad8e027a0c88.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzU0OTA3MjcsIm5iZiI6MTczNTQ5MDQyNywicGF0aCI6Ii82MTUyODQ1MS8zOTkxNzQ3NjgtNzI5ZGFkNWEtMWZjNy00ZDgyLTkwZmEtYWQ4ZTAyN2EwYzg4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjI5VDE2NDAyN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTdkNWJmNjZiNjYwZTUyMWZiOGUwODE2YmRlNmVhOTgxMzYyM2FlZGMwOWU2YjM2NzcyYTY0NGYxMGFiM2YzNDEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.nBJ8Xe9Yk_JzgbXDNyv-MCdlP6ZForo1rzUP--CR4Cs)
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

# DB 세팅
python manage.py dumpdata movies --indent 4 > movies_data.json
python manage.py migrate

# 서버 실행
`python manage.py runserver`
```

2. 프론트엔드(Vue.js) 설정

```bash
코드 복사
`cd ../frontend`

# 의존성 설치
npm install

# 개발 서버 실행
npm run serve

```

## 5. ERD & UserFlow

### ERD

![ERD](/uploads/92d6638832a02f00293758e73200d9fd/ERD.png)

### UserFlow

![UserFlow](/uploads/d9118d9d2d765f15d0630536875ab244/UserFlow.png)

## 6. 프로젝트 후기

### 우준규

- 첫 개발 프로젝트를 통해 다양한 경험과 소중한 성장의 기회를 얻었습니다.
  Vue.js를 활용하면서 프론트엔드 개발의 전반적인 과정을 깊이 있게 이해할 수 있었습니다. 컴포넌트 구조를 학습하고, 받은 데이터를 효과적으로 활용하는 방법을 익혔습니다. 특히 동적인 데이터 바인딩과 상태 관리의 중요성을 실제 프로젝트를 통해 체감할 수 있었죠.
  개발 과정에서 가장 값진 경험은 문제 해결 능력을 키운 것입니다. 오류가 발생했을 때 원인을 찾아 디버깅하는 과정은 쉽지 않았지만, 점차 체계적으로 접근하는 방법을 배웠습니다. 오류 메시지를 분석하고, 코드의 로직을 꼼꼼히 검토하며 문제를 해결해 나가는 과정은 개발자로서 성장하는 중요한 밑거름이 되었습니다.
  이번 프로젝트를 발판 삼아 앞으로 더 다양하고 복잡한 프로젝트에 도전하고 싶습니다. 기술적 역량을 지속적으로 확장하고, 새로운 프레임워크와 기술을 탐구하며 실무 중심의 경험을 쌓아가고 싶습니다. 첫 프로젝트는 시작일 뿐, 앞으로의 개발 여정이 더욱 기대됩니다.

### 김세현

- 사실상 제대로된 팀원과의 협업은 처음이라 많이 방황했던 것 같습니다.
- 백엔드 파트에서 고려해야할 부분이 너무 많았습니다.
  - 모델 설계에서 관계 설정(외래키, ManyToMany)에 많은 애를 먹었던 것 같습니다.
  - CORS 에러가 자주 나 설정에 많은 애를 먹었습니다.
  - 사용자 토큰을 어떻게 처리해야 하는지에 대해 많은 애를 먹었습니다. permission_classes 설정이 문제였습니다.
  - 가장 어려웠던 부분이 위의 사용자 인증 부분이었던 것 같습니다. 이 문제로 며칠을 앓았습니다.
  - 모델의 쿼리 작성(objects.filter 등)부분에서 많은 방법을 배웠습니다. 추후 복습이 필요할 것 같습니다.
  - 위 과정을 진행하면서 Django가 얼마나 강력한 기능들을 제공하는지 체험했습니다. 하지만 강력한 기능과 반대로 커스터마이징하기 매우 힘든 것 같습니다.
- Git 사용에서 많은 애를 먹었습니다.
  - git merge를 많이 경험할 수 있었습니다.
  - git push를 하기 전에 반드시 pull을 받아서 최신 상태인지 체크해야 한다는 사실을 배웠습니다.
  - git pull 하기 전에 자신의 작업내용을 commit해서 보존해놓아야 날라가지 않는다는 사실을 배웠습니다.
  - git merge conflict를 어떻게 해야 하는지에 대해 배웠습니다.
- 프로젝트를 경험하면서 팀원과의 소통이 얼마나 중요한지 다시 한번 체감할 수 있었습니다.
  - 명세서 작성이 소통에 얼마나 도움이 되는지 체감할 수 있었던 것 같습니다.
