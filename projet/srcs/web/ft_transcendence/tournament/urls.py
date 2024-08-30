from django.urls import path
from . import views

app_name = "tournament"

urlpatterns = [
    path('tournament/Tournoi', views.Tournoi, name='tournoi'),
	path('tournament/setup_players', views.setup_players, name="setup_players"),
]