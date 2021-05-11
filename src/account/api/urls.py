from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('register', views.registration_view, name="register"),
    path('overview', views.overview_view, name="overview"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
]