from rest_framework import serializers
from .models import Post, Comment, Like, Profile, User
from django.contrib.contenttypes.models import ContentType

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'




from rest_framework import serializers
from .models import Comment

from rest_framework import serializers
from .models import Comment
from django.contrib.auth.models import User

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_username', 'author_avatar', 'post', 'created_date']
        read_only_fields = ['author_username', 'author_avatar']

    def get_author_username(self, obj):
        return obj.author.username

    def get_author_avatar(self, obj):
        profile = getattr(obj.author, 'profile', None)
        return profile.get_avatar() if profile else None

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)





class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type', 'object_id']
    
    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user  # Assign the user from the request
        else:
            raise serializers.ValidationError("User must be authenticated.")
        
        # Ensure that content_type is properly assigned
        content_type = validated_data.get('content_type')
        if not content_type:
            # Check if it's a Post or Comment and set the content_type accordingly
            if validated_data.get('object_id'):
                obj = Post.objects.filter(id=validated_data['object_id']).first() or Comment.objects.filter(id=validated_data['object_id']).first()
                if isinstance(obj, Post):
                    validated_data['content_type'] = ContentType.objects.get_for_model(Post)
                elif isinstance(obj, Comment):
                    validated_data['content_type'] = ContentType.objects.get_for_model(Comment)
        
        return super().create(validated_data)




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
