from django.db import models
from user_manage.models import CustomUser

class PongResult(models.Model):
	player1 = models.CharField(max_length=255, default="", null=True)
	player2 = models.CharField(max_length=255, 	default="", null=True)
	players = models.ManyToManyField(CustomUser, related_name='pong_results')
	player1_score = models.IntegerField(null=True)
	player2_score = models.IntegerField(null=True)
	winner = models.ForeignKey(CustomUser, related_name='won_games', on_delete=models.SET_NULL, null=True, blank=True)
	loser = models.ForeignKey(CustomUser, related_name='lost_games', on_delete=models.SET_NULL, null=True, blank=True)
	tournament = models.ForeignKey('tournament.Tournament', related_name='matches', on_delete=models.CASCADE, null=True)
	round_number = models.IntegerField(default=1)
	date_played = models.DateTimeField(null=True)

	def __str__(self):
		p1 = self.player1 or "Guest"
		p2 = self.player2 or "Guest"
		w  = self.winner.username if self.winner else "Guest"
		return f"{p1} vs {p2} - Winner: {w}"