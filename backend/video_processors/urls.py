from django.urls import path, include
from rest_framework.routers import DefaultRouter
from video_processors.api.views import VideoViewSet

router = DefaultRouter()
router.register(r'videos', VideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
