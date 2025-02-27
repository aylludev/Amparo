
from django.urls import path
from accounts.views.login.views import *

urlpatterns = [
    #path('register/', register_view, name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
