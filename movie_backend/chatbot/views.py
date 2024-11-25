from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from movies.models import Movie, Genre, Emotion
from movies.serilalizers import MovieListSerializer
import openai
from openai import OpenAI

client = OpenAI(api_key="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")


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
                f"사용자가 느낀 감정은 다음과 같습니다: '{user_input}'.\n"
                f"사용 가능한 감정 목록은 다음과 같습니다: '{emotion_list_str}'.\n"
                f"응답 형식:\n"
                f"1. 첫 줄에는 감정 목록 중에서 가장 적절한 감정을 영어로 한 단어만 작성\n"
                f"2. 둘째 줄부터는 공감과 영화 추천을 포함한 답변을 한국어로 작성"
            )

            openai_response = client.chat.completions.create(
                model="gpt-4",  # 모델명 수정
                messages=[
                    {"role": "system", "content": "당신의 임무는 질문자의 감정을 파악하고 해당 감정에 맞는 영화를 추천하는 일입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # 응답을 줄바꿈을 기준으로 분리
            full_response = openai_response.choices[0].message.content.strip()
            response_parts = full_response.split('\n', 1)
            
            # 첫 줄은 감정, 나머지는 설명
            emotion = response_parts[0].strip()
            explanation = response_parts[1].strip() if len(response_parts) > 1 else ""

            # 응답 데이터 구성
            response_data = {
                "user_emotion": emotion,
                "openai_response": explanation
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
