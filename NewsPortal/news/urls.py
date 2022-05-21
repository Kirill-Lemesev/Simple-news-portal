from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_index),
    path('news/', views.main_page),
    path('news/<int:post_id>/', views.show_article),
    path('news/create/', views.add_article)
]

