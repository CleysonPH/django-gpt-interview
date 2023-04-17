from django.urls import path

from job import views

app_name = "job"
urlpatterns = [
    path("", views.list, name="list"),
    path("<int:pk>/", views.details, name="details"),
]
