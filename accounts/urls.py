# accounts/urls.py
from django.urls import path

from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('view_all/', AllUserView.as_view(), name='view_all'),
]
