from django.db import models
from user_manage.models import CustomUser

class PongResult(models.Model):
	player1 = models.CharField(max_length=255, default="")
	player2 = models.CharField(max_length=255, 	default="")
	player1_score = models.IntegerField()
	player2_score = models.IntegerField()
	winner = models.ForeignKey(CustomUser, related_name='won_games', on_delete=models.SET_NULL, null=True, blank=True)	
	loser = models.ForeignKey(CustomUser, related_name='lost_games', on_delete=models.SET_NULL, null=True, blank=True)
	date_played = models.DateTimeField()

	def __str__(self):
		return f"{self.player1} vs {self.player2} - Winner: {self.winner}"