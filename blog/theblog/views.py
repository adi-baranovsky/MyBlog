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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

import logging
from django.contrib.auth.hashers import make_password

from rest_framework.exceptions import PermissionDenied
logger = logging.getLogger(__name__)


from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer

from dj_rest_auth.views import UserDetailsView
from rest_framework.response import Response


class CustomUserDetailsView(UserDetailsView):
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({"id": user.id, "username": user.username, "email": user.email})


from django.http import JsonResponse

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found")

        serializer.save(post=post, author=self.request.user)




from rest_framework.authtoken.models import Token

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

        # Set the backend and login
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        # Generate a token for the new user
        token, created = Token.objects.get_or_create(user=user)

        return JsonResponse({
            "message": "User registered successfully!",
            "token": token.key,
            "profile_url": f"/profile/?user={username}"
        }, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)




@api_view(['GET'])
def get_profile(request):
    username = request.GET.get('user')
    logger.info(f"Fetching profile for user: {username}")  # Log the username

    try:
        profile = Profile.objects.get(user__username=username)
        logger.info(f"Profile found for user: {username}")  # Log success
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        logger.error(f"Profile not found for user: {username}")  # Log error
        return Response({"error": "Profile not found."}, status=404)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.none()

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found")

        serializer.save(post=post)

    @swagger_auto_schema(
        operation_description="Get comments for a specific post by ID",
        manual_parameters=[ 
            openapi.Parameter('post', openapi.IN_QUERY, description="ID of the post", type=openapi.TYPE_INTEGER)
        ]
    )
    @action(detail=False, methods=['get'], url_path='comments-by-post')
    def comments_by_post(self, request):
        post_id = request.query_params.get('post')
        if post_id:
            comments = Comment.objects.filter(post_id=post_id)
            serializer = self.get_serializer(comments, many=True)
            return Response(serializer.data)
        return Response({"detail": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        object_id = self.request.query_params.get('object_id', None)
        content_type = self.request.query_params.get('content_type', None)
        user = self.request.user if self.request.user.is_authenticated else None

        if object_id and content_type and user:
            return Like.objects.filter(object_id=object_id, content_type=content_type, user=user)

        return Like.objects.none()


    def create(self, request, *args, **kwargs):
        post_id = request.data.get("object_id")
        content_type_id = request.data.get("content_type")
        
        # Ensure user is authenticated
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the like already exists
        existing_like = Like.objects.filter(object_id=post_id, user=user, content_type=content_type_id).first()

        if existing_like:
            # If it exists, we should delete it (unlike)
            existing_like.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_204_NO_CONTENT)
        else:
            # If it does not exist, we should create the like
            validated_data = {
                "object_id": post_id,
                "content_type": content_type_id,
                "user": user.pk  # Pass user primary key here
            }
            
            serializer = self.get_serializer(data=validated_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check_liked(self, request):
        post_id = request.query_params.get("object_id")
        content_type_id = request.query_params.get("content_type")

        if not post_id or not content_type_id:
            return Response({"detail": "Post ID and content type are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user already liked the post
        liked = Like.objects.filter(object_id=post_id, user=user, content_type=content_type_id).exists()
        
        return Response({"liked": liked}, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'])
    def liked_by(self, request):
        post_id = request.query_params.get("object_id")
        content_type_id = request.query_params.get("content_type")

        if not post_id or not content_type_id:
            return Response({"detail": "Post ID and content type are required."}, status=400)

        likes = Like.objects.filter(object_id=post_id, content_type=content_type_id)
        usernames = [like.user.username for like in likes]

        return Response({"usernames": usernames})





class PostPagination(PageNumberPagination):
    page_size = 2  # 2 posts per page


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    queryset = Post.objects.order_by('-id')  # Default queryset

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
