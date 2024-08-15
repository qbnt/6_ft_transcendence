from django.db import models
from user_manage.models import CustomUser

class PongResult(models.Model):
	player1 = models.ForeignKey(CustomUser, related_name='player1_games', on_delete=models.SET_NULL, null=True, blank=True)
	player2 = models.ForeignKey(CustomUser, related_name='player2_games', on_delete=models.SET_NULL, null=True, blank=True)
	player1_score = models.IntegerField()
	player2_score = models.IntegerField()
	winner = models.ForeignKey(CustomUser, related_name='won_games', on_delete=models.SET_NULL, null=True, blank=True)
	loser = models.ForeignKey(CustomUser, related_name='lost_games', on_delete=models.SET_NULL, null=True, blank=True)
	date_played = models.DateTimeField(auto_now_add=True)

	def __str__(self):
        return f"{self.player1.username} vs {self.player2.username} - Winner: {self.winner.username}"