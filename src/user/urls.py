from django.urls import path
from .views import UserDetailView, UserUpdateView, UserLoginView, UserRegistrationView, logout_user

app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('reg/', UserRegistrationView.as_view(), name='reg'),
    path('<slug:slug>/', UserDetailView.as_view(), name='detail'),
    path('edit/<slug:slug>/', UserUpdateView.as_view(), name='edit'),
]
