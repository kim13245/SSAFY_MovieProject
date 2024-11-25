from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from movies.models import Movie, Genre, Emotion
from movies.serilalizers import MovieListSerializer
import openai

openai.api_key = "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"

emotion_translations = {
    "Depressed": "우울",
    "Excited": "신남",
    "Tired": "피곤",
    "Angry": "분노",
    "Anxious": "불안",
    "Helpless": "무력감",
    "Happy": "행복",
    "Relaxed": "편안"
}

class ChatbotView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        user_input  = request.data.get("message")
        if not user_input:
            return Response({"error": "메세지가 입력되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Step 1: DB의 감정 목록 가져오기
            all_emotions = list(Emotion.objects.values_list('name', flat=True))
            if not all_emotions:
                return Response({"error":"DB에 가용한 감정이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            
            # Step 2: OpenAI에 사용자 입력 및 감정 목록 전달
            emotion_list_str = ", ".join(all_emotions)
            prompt = (
                f"사용자가 느낀 감정은 다음과 같습니다: '{user_input}'."
                f"사용 가능한 감정 목록은 다음과 같습니다: '{emotion_list_str}'."
                f"이 중에서 가장 가까운 감정을 선택하여 감정 이름을 맨 처음에 '{emotion_list_str}'처럼 영어로한 단어로 나타내고," 
                "사용자가 느끼는 감정에 대한 답변은 모두 한국어로 해주세요."
            )

            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 친절한 정신 상담사 입니다. 당신의 임무는 질문자의 감정을 파익하고 해당 감정에 맞는 영화를 추천하는 일입니다. 말 끝에는 이런 멘트를 기본으로 가지고 있습니다 '당신의 감정은 무엇이고 아래와 같은 영화를 추천합니다'"},
                    {"role": "user", "content": prompt}
                ]
            )
            extracted_emotion = openai_response['choices'][0]['message']['content'].strip()

            # 응답 데이터 구성
            response_data = {
                "user_emotion": extracted_emotion,
                "openai_response": f"사용자 입력에서 추출된 감정은 다음과 같습니다. '{extracted_emotion}'.",

            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

