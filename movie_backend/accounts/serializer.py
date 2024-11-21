from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    kept_movies_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'user_profile', 'user_intro', 
                  'followers_count', 'followings_count', 'kept_movies_count')
        read_only_fields = ('id', 'folloers_count', 'followings_count', 'kept_movies_count')

        def get_followers_count(self, obj):
            return obj.followers.count()
        
        def get_followings_count(self, obj):
            return obj.followings.count()
        
        def get_kept_movies_count(self, obj):
            return obj.kept_movies.count()

