from django.urls import path
from . import views

app_name = "study"

urlpatterns = [
    path('create', views.create_study_view, name="create"),
]