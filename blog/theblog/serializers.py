from rest_framework import serializers
from .models import Post, Comment, Like, Profile

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    pic_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_pic_url(self, obj):
        if obj.pic:
            return self.context['request'].build_absolute_uri(obj.pic.url)
        return None


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)  # Show username instead of ID

    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    #user = serializers.CharField(source='user.username', read_only=True)  # Show username instead of ID

    class Meta:
        model = Profile
        fields = '__all__'
