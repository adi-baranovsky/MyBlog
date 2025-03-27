# Create your views here.
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Profile
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, ProfileSerializer
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post', None)
        if post_id:
            try:
                return Comment.objects.filter(post_id=post_id)
            except Comment.DoesNotExist:
                #raise NotFound(detail="No comments found for this post")
                return Comment.objects.none()
        #return NotFound(detail="No object")
        return Comment.objects.none()


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer

    def get_queryset(self):
        object_id = self.request.query_params.get('object_id', None)
        content_type = self.request.query_params.get('content_type', None)
        if object_id and content_type:
            try:
                return Like.objects.filter(object_id=object_id, content_type=content_type)
            except Like.DoesNotExist:
                return Like.objects.none()
                #raise NotFound(detail="No likes found for this object")
        
        #return NotFound(detail="No object")


# pagination for posts
class PostPagination(PageNumberPagination):
    page_size = 2  # 2 posts per page

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer  # serializers to JSON
    pagination_class = PostPagination  # שימוש ב-pagination מותאם אישית

    def get_queryset(self):
        user = self.request.query_params.get('user', None)  # Look by parameter "user" in URL
        if user:
            try:
                user_instance = User.objects.get(username=user)
                return Post.objects.filter(author=user_instance)
            except User.DoesNotExist:
                return Post.objects.none()  # If not found, return none
        return Post.objects.all()  # if username isn't given, return all



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