from django.db							import models
from user_manage.models					import CustomUser

# Create your models here.
class	Players(CustomUser):
	
	nb_players = 0
	players = []
	matchs = []

	def __init__(self, nb_players, players):
		self.nb_players = nb_players
		self.players = players
