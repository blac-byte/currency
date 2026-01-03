from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("convert_API/", views.convert_API, name="convert_API"),
]
