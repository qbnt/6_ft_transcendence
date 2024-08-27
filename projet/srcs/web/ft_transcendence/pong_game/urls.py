from django.urls import path
from . import views

urlpatterns = [
    path('', views.pong_view, name='pong'),
	path('static/pong_game/start_game/', views.start_game, name='start_game'),
]