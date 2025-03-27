
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from theblog.views import PostViewSet, CommentViewSet, LikeViewSet, ProfileViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Blog API",
      default_version='v1',
      description="API for Blog App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@blogapi.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')  # הגדרת basename
router.register(r'comments', CommentViewSet, basename='comment')  # הגדרת basename
router.register(r'likes', LikeViewSet, basename='like')  # הגדרת basename
router.register(r'profiles', ProfileViewSet, basename='profile')  # הגדרת basename

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]