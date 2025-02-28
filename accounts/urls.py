from django.urls import path
from accounts.views.login.views import LogoutView, LoginFormView
from accounts.views.user.views import UserCreateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
