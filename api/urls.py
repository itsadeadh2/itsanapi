from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'contacts', views.ContactRequestViewSet, basename='contact')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'games', views.GameViewSet, basename='game')
router.register(r'hangman', views.HangmanViewSet, basename='play')
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'scores', views.ScoreViewSet, basename='score')

urlpatterns = [
    path('', include(router.urls)),
]
