# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CreateLecturerView,
    CreateStudentView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-lecturer/', CreateLecturerView.as_view(), name='create_lecturer'),
    path('create-student/', CreateStudentView.as_view(), name='create_student'),
]