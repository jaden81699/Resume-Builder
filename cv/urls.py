from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from cv import views

router = SimpleRouter()

router.register("", views.ResumeViewset, basename="resume")

urlpatterns = [
    # path("download/<int:pk>/", views.ResumePDFView.as_view()),
    # path("display/<int:pk>", views.DisplayResumeView, name="display-resume")
    path("test", views.TestView, name="test"),
    path("display-casual", views.TestDisplayCasual, name="display-casual"),
    path("display-professional", views.TestDisplayProfessional, name="display-professional"),

] + router.urls
