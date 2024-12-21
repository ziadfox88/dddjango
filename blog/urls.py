from django.urls import path,include
from . import views



urlpatterns = [
    path('', views.post_list , name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail , name='post_detail'),
]
