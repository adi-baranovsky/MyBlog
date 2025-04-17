
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from theblog.views import PostViewSet, CommentViewSet, LikeViewSet, ProfileViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from theblog.views import register_view, get_profile, CommentCreateView, CustomUserDetailsView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from dj_rest_auth.views import UserDetailsView


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
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')  
router.register(r'likes', LikeViewSet, basename='like')  
router.register(r'profiles', ProfileViewSet, basename='profile')  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  
    path('api/', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/register/', register_view, name='register'),
    path('api/profile/', get_profile, name='get_profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('api/auth/', include('dj_rest_auth.urls')),  # This handles /user/
    path('api/auth/user/', CustomUserDetailsView.as_view(), name='user-details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
