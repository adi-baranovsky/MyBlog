from rest_framework import serializers
from .models import Post, Comment, Like, Profile

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        #fields = ['id', 'title', 'author', 'content', 'picture', 'created_date', 'likes']
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        #fields = ['id', 'author', 'content', 'post', 'parent_comment', 'created_on']
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        #fields = ['id', 'user', 'content_type', 'object_id']
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        #fields = ['id', 'user', 'bio', 'avatar']
        fields = '__all__'