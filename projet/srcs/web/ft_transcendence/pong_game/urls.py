from django.urls import path
from . import views

app_name='pong'

urlpatterns = [
    path('', views.pong_view, name='pong'),
	path('pong_game/save_result/', views.save_pong_result, name='save_pong_result'),
]