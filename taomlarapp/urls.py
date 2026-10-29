
from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.home, name="home"),
    path("retsept/<slug:slug>/", views.recipe_detail, name="detail"),
]

