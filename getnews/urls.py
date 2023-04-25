from django.urls import path
from . import views

urlpatterns = [
    path('list',views.listNews),
    path('store',views.storeDataInDB),
    path('get',views.collectNews),
    path('favourite',views.toggle_favorite),
]