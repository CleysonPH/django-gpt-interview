from django.urls import path

from interview import views

app_name = "interview"
urlpatterns = [
    path("<uuid:uuid>/", view=views.details, name="details"),
    path("create/<int:job_pk>/", view=views.create, name="create"),
    path(
        "<uuid:chat_uuid>/create-message/",
        view=views.create_message,
        name="create_message",
    ),
]
