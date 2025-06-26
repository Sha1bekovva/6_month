from django.urls import path
from .views import RegisterView, ConfirmUserView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/', ConfirmUserView.as_view(), name='user-confirm'),
    path('login/', LoginView.as_view(), name='login'),
]
