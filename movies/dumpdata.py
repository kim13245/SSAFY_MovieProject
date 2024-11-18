from django.core.management import call_command

# 파일에 UTF-8로 쓰기
with open('movies_data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'movies', indent=4, stdout=f)
