from django.urls import path
from . import views

app_name = "tournament"

urlpatterns = [
	path('setup_players/', views.setup_players, name="setup_players"),
	path('t/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
	path('p/<int:pong_id>/', views.t_pong, name='t_pong'),
	path('save_pong_result/', views.save_pong_result, name='save_pong_result'),
]