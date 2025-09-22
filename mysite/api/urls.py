from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r"registration", views.UserRegistrationViewSet, basename="registration",)
router.register(r"login", views.LoginViewSet, basename="login",)
router.register(r"token_auth", views.TokenAuthenticateViewSet, basename="token_auth",)
router.register(r"logout", views.LogoutViewSet, basename="logout",)
router.register(r"profile", views.ProfileViewSet, basename="profile",)
router.register(r"questions", views.QuestionsViewSet, basename="questions",)

urlpatterns = [
    path("", include(router.urls)),
]