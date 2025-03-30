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

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username:
            try:
                user_instance = User.objects.get(username=username)
                return Profile.objects.filter(user=user_instance)
            except User.DoesNotExist:
                raise NotFound(detail="User not found")
        return Profile.objects.all()  # all profiles



"""
#swagger
@swagger_auto_schema(operation_description="search for specific user")
@action(detail=False, methods=['get'], url_path='user-posts')
def user_posts(self, request):
    user = request.query_params.get('user', None)
    if user:
        posts = Post.objects.filter(author__username=user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    return Response({"detail": "User Not Found"}, status=400)
"""