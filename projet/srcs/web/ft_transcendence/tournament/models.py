from django.db			import models
from user_manage.models	import CustomUser

class Tournament(models.Model):
	players = models.ManyToManyField(CustomUser, related_name='tournaments_palyers')
	matches = models.ManyToManyField('pong_game.PongResult', related_name='tournaments_games')

	def get_next_match(self):
		"""
		Retourne le prochain match à jouer.
		"""
		return self.matches.filter(winner__isnull=True).first()

	def __str__(self):
		return f"Tournoi.{self.id}"
