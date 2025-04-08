from rest_framework import serializers
from .models import Post, Comment, Like, Profile

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'




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
