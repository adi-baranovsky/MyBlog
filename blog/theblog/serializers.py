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
    profile_image = serializers.SerializerMethodField()  # Add a custom field for the profile image
    username = serializers.CharField(source='user.username')  # Include the username from the related User model

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'profile_image']  # Include username in the fields

    def get_profile_image(self, obj):
        # Return avatar_url if it exists, otherwise return the avatar file URL
        if obj.avatar_url:
            return obj.avatar_url
        elif obj.avatar:
            return obj.avatar.url
        return None
