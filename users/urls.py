from django.urls import path
from .views import RegisterView, ConfirmUserView, authorization_api_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/', ConfirmUserView.as_view(), name='user-confirm'),
    path('login/', authorization_api_view, name='login'),
]


