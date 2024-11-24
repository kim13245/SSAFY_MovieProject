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
from rest_framework.permissions import IsAuthenticated, AllowAny # 사용자 권한 인증
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from movies.models import Review, ReviewComment, Movie

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample

User = get_user_model()

# 스펙타큘러 docs 유저 예시를 위한 클래스

class UserInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

# 회원가입
class RegisterView(APIView):

    @extend_schema(
        summary="회원가입",
        description=(
            "새로운 사용자를 등록 "
            "사용자 이름, 닉네임, 비밀번호, 이메일이 필요 "
            "중복된 사용자 이름, 이메일, 닉네임은 허용되지 않음"
        ),
        request=UserInfoSerializer,  # 입력 데이터
        responses={
            201: OpenApiResponse(description="회원가입 성공"),
            400: OpenApiResponse(description="요청 데이터 오류 또는 중복된 정보"),
        },
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

# 로그인
class LoginView(APIView):

    @extend_schema(
        summary="로그인",
        description="사용자 이름과 비밀번호를 통해 로그인. 성공 시 인증 토큰을 반환",
        request=UserInfoSerializer,  # 입력 데이터
        responses={
            200: OpenApiResponse(
                description="로그인 성공",
                examples={
                    "token": "abc123...",
                    "userId": 1,
                    "userName": "example_user",
                },
            ),
            401: OpenApiResponse(description="아이디 또는 비밀번호가 잘못되었습니다."),
        },
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        #사용자 인증
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "아이디 혹은 비밀번호가 잘못되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response([{"token": token.key}, {"userId": user.id}, {"userName":username}], status=status.HTTP_200_OK)
        
# 로그아웃
class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="로그아웃",
        description="현재 로그인된 사용자의 인증 토큰을 삭제",
        responses={
            204: OpenApiResponse(description="로그아웃 성공"),
            400: OpenApiResponse(description="로그인 상태가 아닙니다."),
        },
    )
    def delete(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "로그아웃 했습니다."}, status=status.HTTP_204_NO_CONTENT)
        except AttributeError:
            return Response({"error": "로그인 중이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

# 회원탈퇴
class SignoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="회원탈퇴",
        description="현재 로그인된 사용자의 계정을 삭제",
        responses={
            204: OpenApiResponse(description="회원탈퇴 성공"),
            400: OpenApiResponse(description="회원탈퇴 중 오류 발생"),
        },
    )
    def delete(self, request):
        
        user = request.user

        try:
            Token.objects.filter(user=user).delete()
            Session.objects.filter(session_data__icontains=user.id).delete()
            user.delete()
            return Response({"message": "회원탈퇴 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"에러: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

# 내 프로필
class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="내 프로필 조회",
        description="로그인한 사용자의 프로필 정보를 반환",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="인증 실패"),
        },
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="내 프로필 수정",
        description="로그인한 사용자가 자신의 프로필 정보를 수정",
        request=UserSerializer,
        responses={
            200: OpenApiResponse(description="프로필 수정 완료"),
            400: OpenApiResponse(description="잘못된 요청"),
            401: OpenApiResponse(description="인증 실패"),
        },
    )
    def put(self, request):
        user = request.user
        input_data = request.data

        user.user_profile = input_data.get('user_profile', user.user_profile)
        user.email = input_data.get('email', user.email)
        user.nickname = input_data.get('nickname', user.nickname)
        user.user_intro = input_data.get('user_intro', user.user_intro)
        user.save()

        return Response({'message': '프로필 수정 완료'}, status=status.HTTP_200_OK)

# 다른 유저 프로필
class UserProfileView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary="다른 유저 프로필 조회",
        description="특정 유저의 프로필 정보를 조회",
        parameters=[
            OpenApiParameter("user_id", int, description="조회할 유저의 ID"),
        ],
        responses={
            200: UserSerializer,
            404: OpenApiResponse(description="유저를 찾을 수 없습니다."),
        },
    )
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 유저 팔로우 기능
class UserFollowView(APIView):
    
    @extend_schema(
        summary="사용자 팔로우/언팔로우",
        description=(
            "특정 사용자를 팔로우하거나 언팔로우 "
            "자기 자신을 팔로우할 수 없음"
        ),
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=int,
                description="팔로우 또는 언팔로우할 사용자의 ID",
                required=True,
            )
        ],
        responses={
            200: OpenApiResponse(description="팔로우 상태 변경 성공"),
            400: OpenApiResponse(description="잘못된 요청"),
        },
    )
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

# 유저가 쓴 리뷰 목록 들고오기
class UserReviewView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary="사용자가 작성한 리뷰 조회",
        description="특정 사용자가 작성한 모든 리뷰를 조회",
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=int,
                description="리뷰를 조회할 사용자의 ID",
                required=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer(many=True),
                description="사용자가 작성한 리뷰 목록",
            ),
            404: OpenApiResponse(description="사용자를 찾을 수 없습니다."),
        },
    )
    def get(self, request, user_id):
        user_reviews = Review.objects.filter(user=user_id)
        serializer = ReviewSerializer(user_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 유저가 쓴 리뷰 댓글 목록 들고오기
class UserReviewCommentView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary="사용자가 작성한 리뷰 댓글 조회",
        description="특정 사용자가 작성한 모든 리뷰 댓글을 조회",
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=int,
                description="리뷰 댓글을 조회할 사용자의 ID",
                required=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=ReviewCommentSerializer(many=True),
                description="사용자가 작성한 리뷰 댓글 목록",
            ),
            404: OpenApiResponse(description="사용자를 찾을 수 없습니다."),
        },
    )
    def get(self, request, user_id):
        user_reviews = ReviewComment.objects.filter(user=user_id)
        serializer = ReviewCommentSerializer(user_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 유저가 찜한 영화 목록 들고오기
class UserMovieView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary="찜한 영화 목록 조회",
        description="특정 사용자가 찜한 영화의 목록을 반환(각 영화에 대한 사용자의 리뷰 평점(user_rating)도 포함)",
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=int,
                description="찜한 영화를 조회할 사용자의 ID",
                required=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=MovieListSerializer(many=True),
                examples=[
                    OpenApiExample(
                        name="찜한 영화 목록 예제",
                        value=[
                            {"id": 101, "title": "Movie 1", "poster_path": "/path1.jpg", "user_rating": 4.5},
                            {"id": 102, "title": "Movie 2", "poster_path": "/path2.jpg", "user_rating": None},
                        ],
                    )
                ],
            )
        },
    )
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        kept_movies = user.kept_movies.all()
        
        movie_data = []
        for movie in kept_movies:
            user_review = movie.review_set.filter(user=user).first()
            movie_data.append({
                'id': movie.id,
                'title': movie.title,
                'poster_path': movie.poster_path,
                'user_rating': user_review.rating if user_review else None
            })
        return Response(movie_data, status=status.HTTP_200_OK)

# 영화 찜하기
class UserKeepMovieView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="영화 찜하기/찜 취소",
        description="특정 영화를 현재 로그인된 사용자의 찜 목록에 추가하거나 제거",
        parameters=[
            OpenApiParameter(
                name="movie_id",
                type=int,
                description="찜하거나 찜 취소할 영화의 ID",
                required=True,
            )
        ],
        responses={
            200: OpenApiResponse(description="찜 상태 변경 성공"),
        },
    )
    def post(self, request, movie_id):
        user = request.user
        movie = get_object_or_404(Movie, id=movie_id)

        # 찜 여부 확인
        if user.kept_movies.filter(id=movie.id).exists():
            user.kept_movies.remove(movie)  # 찜 취소
            message = "찜이 취소되었습니다."
        else:
            user.kept_movies.add(movie)  # 찜 추가
            message = "영화를 찜 목록에 추가했습니다."

        return Response({"message": message}, status=status.HTTP_200_OK)