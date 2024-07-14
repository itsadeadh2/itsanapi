from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api import views

router = DefaultRouter()
router.register(r"projects", views.ProjectViewSet, basename="project")
router.register(r"scores", views.ScoreViewSet, basename="score")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/csrf/", views.CustomLoginView.as_view(), name="login-csrf"),
    path("login/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("contacts/", views.CreateContactRequestView.as_view(), name="contact"),
    path("health/", views.health_check, name="health"),
    path("hangman/", views.HangmanListView.as_view(), name="hangman-list"),
    path(
        "hangman/<int:pk>/guess/",
        views.HangmanGuessView.as_view(),
        name="hangman-guess",
    ),
    path("hangman/<int:pk>/", views.HangmanDetailView.as_view(), name="hangman-detail"),
]
