from django.urls import path

from study.views import (
	create_study_view,
	detail_study_view,
	edit_study_view,
)

app_name = 'study'

urlpatterns = [
    path('create/', create_study_view, name="create"),
    path('<slug>/', detail_study_view, name="detail"),
    path('<slug>/edit/', edit_study_view, name="edit"),
 ]

