from django.urls import path
from user_auth import views

urlpatterns = [
    path('signup', views.SignUpAPIView.as_view()),
    path('token', views.TokenAPIView.as_view()),
    path('revoke_token', views.RevokeTokenAPIView.as_view()),
]
