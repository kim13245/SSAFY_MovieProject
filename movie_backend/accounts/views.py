from drf_spectacular.utils import extend_schema
# Django REST Framework(DRF)에서 제공하는 클래스 기반 뷰(Class-Based View, CBV)의 기본 클래스
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from movies.serilalizers import MovieListSerializer, ReviewSerializer, ReviewCommentSerializer
from .serializer import UserSerializer
# APIView는 RESTful API의 각 HTTP 메서드(GET, POST, PUT, DELETE, 등)를 처리하기 위한 메서드(get, post, put, delete 등)를 제공
# 기본적으로 APIView는 HTTP 메서드별로 요청을 처리하도록 설계되어 있음

"""
** 클래스 기반 뷰를 선택해야 하는 상황 **
- 프로젝트가 점점 커질 가능성이 있는 경우.
- 공통 동작을 여러 뷰에서 재사용해야 하는 경우.
- 권한 설정, 직렬화기 연동, 스키마 자동화를 적극 활용해야 하는 경우.
- RESTful API의 HTTP 메서드(GET, POST, PUT, DELETE)를 명확히 분리해서 처리해야 하는 경우.
"""
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password  # 비밀번호 해싱
from rest_framework.permissions import IsAuthenticated # 사용자 권한 인증
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from movies.models import Review, ReviewComment

User = get_user_model()

class UserInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

class RegisterView(APIView):

    @extend_schema(
        request=UserInfoSerializer,  # 입력 데이터
        responses=UserInfoSerializer,  # 응답 데이터
        description="This API retrieves or updates example data.",
    )
    def post(self, request):
        username = request.data.get('username')
        nickname = request.data.get('nickname', "크와와와왕")
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not nickname:
            return Response({"error": "아이디 혹은 패스워드 혹은 프로필 이름 입력이 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "이미 사용 중인 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "이미 사용 중인 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(nickname=nickname).exists():
            return Response({"error": "이미 사용 중인 프로필 이름입니다."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            username = username,
            nickname = nickname,
            password = make_password(password),
            email = email,
        )
        return Response(status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        #사용자 인증
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "아이디 혹은 비밀번호가 잘못되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response([{"token": token.key}, {"userId": user.id}, {"userName":username}], status=status.HTTP_200_OK)
        
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "로그아웃 했습니다."}, status=status.HTTP_204_NO_CONTENT)
        except AttributeError:
            return Response({"error": "로그인 중이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

class SignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        
        user = request.user

        try:
            Token.objects.filter(user=user).delete()
            Session.objects.filter(session_data__icontains=user.id).delete()
            user.delete()
            return Response({"message": "회원탈퇴 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"에러: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

 
class ProfileUserView(APIView):

    
    def get(self, request, user_id):
        # user.id, username, email, user_profile, user_intro, kept_movies, following, follower 수
        # 유저가 작성한 리뷰들 id도 모아서 뿌리기
        # 유저의 플레이 리스트 정보도 같이 뿌리기
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, user_id):

        user = User.objects.get(id=user_id)
        if user.id != request.user.id:
            return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
        input_data = request.data

        user.user_profile = input_data.get('user_profile', user.user_profile)
        user.email = input_data.get('email', user.email)
        user.nickname = input_data.get('nickname', user.nickname)
        user.user_intro = input_data.get('user_intro', user.user_intro)
        user.save()

        return Response({'message': '수정 완료'}, status=status.HTTP_200_OK)

class UserFollowView(APIView):
    def post(self, request, user_id):
        target = User.objects.get(pk=user_id)
        if target == request.user:
            return Response({'error': '자기 자신을 팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_following = target.followers.filter(id=request.user.id).exists()

        # 팔로윙 취소
        if is_following:
            target.followers.remove(request.user)
            message = '팔로우를 취소'
        # 팔로우 추가
        else:
            target.followers.add(request.user)
            message = '팔로우!!!!!!!'
        
        return Response({'message': message}, status=status.HTTP_200_OK)

class UserReviewView(APIView):
    def get(self, request, user_id):
        user_reviews = Review.objects.filter(user=user_id)
        serializer = ReviewSerializer(user_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserReviewCommentView(APIView):
    def get(self, request, user_id):
        user_reviews = ReviewComment.objects.filter(user=user_id)
        serializer = ReviewCommentSerializer(user_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserMovieView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        kept_movies = user.kept_movies.all()
        serializers = MovieListSerializer(kept_movies, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

        
    