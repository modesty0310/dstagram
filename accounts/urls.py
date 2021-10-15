from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

app_name = 'accounts'

# LoginView, LogoutView를 바로 template로 전달
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
]
