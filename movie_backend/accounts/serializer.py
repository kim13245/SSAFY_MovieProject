from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Review, ReviewComment, Community, Comment
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    kept_movies_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    review_comment_count = serializers.SerializerMethodField()
    community_count = serializers.SerializerMethodField()
    community_comment_count = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = (
            'id', 'username', 'nickname', 'email', 'user_profile', 'user_intro',
            'followers_count', 'followings_count', 'kept_movies_count',
            'review_count', 'review_comment_count', 'community_count', 'community_comment_count'
        )

        read_only_fields = (
            'id', 'followers_count', 'followings_count', 
            'kept_movies_count', 'review_count', 'review_comment_count', 
            'community_count', 'community_comment_count'
        )

    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_followings_count(self, obj):
        return obj.followings.count()
    
    def get_kept_movies_count(self, obj):
        return obj.kept_movies.count()
    
    def get_review_count(self, obj):
        return Review.objects.filter(user=obj).count()

    def get_review_comment_count(self, obj):
        return ReviewComment.objects.filter(user=obj).count()

    def get_community_count(self, obj):
        return Community.objects.filter(user=obj).count()

    def get_community_comment_count(self, obj):
        return Comment.objects.filter(user=obj).count()
