from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('bonds/', views.BondsView.as_view(), name='create_bond'),
]