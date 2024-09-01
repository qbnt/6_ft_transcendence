from django.urls import path
from . import views

app_name = "tournament"

urlpatterns = [
    path('affichage_matchs', views.affichage_matchs, name='affichage_matchs'),
	path('setup_players', views.setup_players, name="setup_players"),
]