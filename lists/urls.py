from lists import views
from django.urls import path

urlpatterns = [
    path('new', views.new_list, name='new_list'),
    path('<str:list_id>/', views.view_list, name='view_list'),
    path('<str:list_id>/add_item', views.add_item, name='add_item'),
]

