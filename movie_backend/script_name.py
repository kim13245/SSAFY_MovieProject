import os
import django
from django.core.management import call_command

# Django 설정 파일 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_manage.settings')

# Django 초기화
django.setup()

# dumpdata 실행
with open('movie_data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'movies', indent=4, stdout=f)