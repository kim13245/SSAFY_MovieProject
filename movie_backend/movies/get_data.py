import requests

API_KEY = 'cd8bc71b153e2ca169a6dca709dbb877'
BASE_URL = 'https://api.themoviedb.org/3'
# YOUTUBE_API_KEY='AIzaSyDFUp9bwjMwxDIneBmCbY7z4cFrKIflrOI'
# YOUTUBE_API_KEY='AIzaSyDKuuARGfk3wwiOEJ3CwGL8heye64UpPz4'
YOUTUBE_API_KEY='AIzaSyANvthbCIvkd64ZPzRJZl4rRDlAgSWRFxM'
def get_genres():
    # 영화 장르 목록 가져오기
    url = f"{BASE_URL}/genre/movie/list"
    params = {
        'api_key': API_KEY,
        'language': 'ko-KR',
    }
    response = requests.get(url, params=params)
    # HTTP 요청이 실패했을 때 예외를 발생시키는 코드
    response.raise_for_status()
    # dictionary의 get. 두번째 인자로 genres라는 키 값을 가져오는데 실패하면 [] 반환
    return response.json().get('genres', [])

def get_movies_by_genre(genre_id, page=1):
    # 해당 장르에 속한 영화 목록 가져오기
    url = f"{BASE_URL}/discover/movie"
    params = {
        'api_key': API_KEY,
        'language': 'ko-KR',
        'with_genres': genre_id,
        'page': page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('results', [])

def get_movie_details(movie_id):
    # 선택한 하나의 영화 상세 정보 가져오기
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'language': 'ko-KR',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_cast_crew(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}/credits'
    params = {
        'api_key': API_KEY,
        'language': 'ko-KR',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_person_details(person_id):
    # 선택한 인물의 상세 정보 가져오기
    url = f"{BASE_URL}/person/{person_id}"
    params = {
        'api_key': API_KEY,
        'language': 'ko-KR',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def serch_movie(title):
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': title,
        'language': 'ko-KR',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_movie_trailer(title):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': "snippet",
        'q': f'{title} 공식 트레일러',
        'type': "video",
        'key': YOUTUBE_API_KEY,
        'maxResults': 1,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if 'items' in data and data['items']:
        item = data['items'][0]['id']['videoId']

        return {
            'videoId': item,
        }   

    return ''