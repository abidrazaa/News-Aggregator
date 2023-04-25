from django.urls import path
from . import views

urlpatterns = [
    path('list',views.listNews),
    path('get',views.get_news),
    path(' favourite',views.toggle_favorite),
]