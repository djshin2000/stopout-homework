from django.urls import path
from webtoon import views

urlpatterns = [
    path('', views.webtoon_list, name='webtoon-list'),
    path('<int:pk>/', views.webtoon_detail, name='webtoon-detail'),
]
