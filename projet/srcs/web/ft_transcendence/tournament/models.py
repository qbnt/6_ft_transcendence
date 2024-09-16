from django.db			import models
from user_manage.models	import CustomUser
from pong_game.models	import PongResult
import random

class Tournament(models.Model):
	players = models.ManyToManyField(CustomUser, related_name='tournaments')
	current_round = models.IntegerField(default=1)
	winner = models.ForeignKey(CustomUser, related_name='won_tournaments', on_delete=models.CASCADE, null=True)

	def get_next_match(self):
		return self.matches.filter(winner__isnull=True, round_number=self.current_round).first()

	def advance_round(self):
		players = [match.winner for match in self.matches.filter(round_number=self.current_round)]
		self.current_round += 1
		if len(players) == 1:
			self.winner = players[0]
		self.save()

		random.shuffle(players)
		while len(players) > 1:
			player1 = players.pop()
			player2 = players.pop()

			PongResult.objects.create(
				player1=player1,
				player2=player2,
				tournament=self,
				round_number=self.current_round
			)


	def __str__(self):
		return f"Tournoi.{self.id}"
