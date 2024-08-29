from django.urls import path
from . import views

urlpatterns = [
    path('', views.pong_view, name='pong'),
	path('pong_game/start_game/', views.start_game, name='start_game'),
	path('pong_game/start_game_ai/', views.start_game_ai, name='start_game_ai'),
	path('pong_game/save_result/', views.save_pong_result, name='save_pong_result'),
]