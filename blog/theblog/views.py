# Create your views here.
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Profile
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, ProfileSerializer
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
# views.py
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login


from django.contrib.auth.hashers import make_password

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists."}, status=400)

        user = User.objects.create(username=username, email=email, password=make_password(password))
        
        Profile.objects.create(user=user)
        login(request, user)  # התחברות אוטומטית
        
        return JsonResponse({
            "message": "User registered successfully!",
            "profile_url": f"/profile/?user={username}"
        }, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_profile(request):
    username = request.GET.get('user')

    try:
        user = User.objects.get(username=username)
        
        profile = Profile.objects.get(user=user)
        return JsonResponse({
            "username": user.username,
            "bio": profile.bio,
            "profile_image": profile.avatar_url if profile.avatar_url else request.build_absolute_uri(profile.avatar.url)
        })
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post', None)
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.none()

    @swagger_auto_schema(
        operation_description="Get comments for a specific post by ID",
        manual_parameters=[openapi.Parameter('post', openapi.IN_QUERY, description="ID of the post", type=openapi.TYPE_INTEGER)]
    )
    @action(detail=False, methods=['get'], url_path='comments-by-post')
    def comments_by_post(self, request):
        post_id = request.query_params.get('post', None)
        if post_id:
            # מציאת התגובות שקשורות לפוסט
            comments = Comment.objects.filter(post_id=post_id)
            serializer = self.get_serializer(comments, many=True)
            return Response(serializer.data)
        return Response({"detail": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)



class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer

    def get_queryset(self):
        object_id = self.request.query_params.get('object_id', None)
        content_type = self.request.query_params.get('content_type', None)
        if object_id and content_type:
            return Like.objects.filter(object_id=object_id, content_type=content_type)
        return Like.objects.none()
    
    @swagger_auto_schema(
        operation_description="Get likes for a specific post by ID",
        manual_parameters=[openapi.Parameter('post', openapi.IN_QUERY, description="ID of the post", type=openapi.TYPE_INTEGER)]
    )
    @action(detail=False, methods=['get'], url_path='likes-by-post')
    def likes_by_post(self, request):
        post_id = request.query_params.get('post', None)
        if post_id:
            # מציאת הלייקים שקשורים לפוסט
            likes = Like.objects.filter(object_id=post_id, content_type=ContentType.objects.get_for_model(Post))
            serializer = self.get_serializer(likes, many=True)
            return Response(serializer.data)
        return Response({"detail": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)



class PostPagination(PageNumberPagination):
    page_size = 2  # 2 posts per page


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    queryset = Post.objects.all()  # Default queryset

    def get_serializer_context(self):
        return {'request': self.request}

    @swagger_auto_schema(
        manual_parameters=[ 
            openapi.Parameter('user', openapi.IN_QUERY, description="Username of the author", type=openapi.TYPE_STRING)
        ]
    )
    @action(detail=False, methods=['get'], url_path='posts-by-user')
    def posts_by_user(self, request):
        user = request.query_params.get('user', None)
        if user:
            try:
                user_instance = User.objects.get(username=user)
                posts = Post.objects.filter(author=user_instance)
                serializer = self.get_serializer(posts, many=True)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "User parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        if user:
            return Profile.objects.filter(user__username=user)  # Filter by username
        return super().get_queryset()

    @swagger_auto_schema(
        operation_description="Get Profile for a specific username",
        manual_parameters=[openapi.Parameter('user', openapi.IN_QUERY, description="Username of the user", type=openapi.TYPE_STRING)]
    )
    @action(detail=False, methods=['get'], url_path='profile-by-username')
    def profile_by_username(self, request):
        user = request.query_params.get('user', None)
        if user:
            profile = Profile.objects.filter(user__username=user).first()  # Get single profile if exists
            if profile:
                serializer = self.get_serializer(profile)
                return Response(serializer.data)
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Username parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
