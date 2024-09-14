from django.shortcuts 				import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib					import messages
from .models 						import Tournament
from pong_game.models 				import PongResult
from user_manage.models				import CustomUser
from django.http 					import JsonResponse
import random

@login_required
def setup_players(request):
	if request.method == 'POST':
		tournament = Tournament.objects.create()

		player_ids = []
		for key, value in request.POST.items():
			if key.startswith('player'):
				player_ids.append(value)

		if not player_ids:
			messages.error(request, "Aucun joueur n'a été sélectionné.")
			return redirect('tournament:setup_players')

		for player in player_ids:
			try:
				user = CustomUser.objects.get(username=player)
			except CustomUser.DoesNotExist:
				messages.error(request, f"{player} n'est pas un compte existant sur le site.")
				return redirect('tournament:setup_players')
			tournament.players.add(user)

		players_list = list(tournament.players.all())
		random.shuffle(players_list)

		while len(players_list) > 1:
			player1 = players_list.pop()
			player2 = players_list.pop()

			match = PongResult.objects.create(
				player1=player1,
				player2=player2,
				tournament=tournament,
				round_number=1
			)

		return redirect('tournament:tournament_detail', tournament_id=tournament.id)

	return render(request, 'tournoi/Setup_players.html')

@login_required
def tournament_detail(request, tournament_id):
	tournament = Tournament.objects.get(id=tournament_id)

	matches_exist = tournament.matches.filter(winner__isnull=True, round_number=tournament.current_round).exists()
	matches = tournament.matches.filter(winner__isnull=True, round_number=tournament.current_round)
	matches_end = tournament.matches.filter(winner__isnull=False)
	winner = tournament.winner

	context = {
		'tournament': tournament,
		'matches_exist': matches_exist,
		'matches': matches,
		'matches_end': matches_end,
		'winner': winner,
	}

	return render(request, 'tournoi/Tournoi_Matches.html', context)


@login_required
def t_pong(request, pong_id):
	match = get_object_or_404(PongResult, id=pong_id)
	context = {
		'player1': match.player1,
		'player2': match.player2,
		'pong_id': match.id
	}
	return render(request, 'tournoi/pong_tournoi.html', context)

@login_required
def save_pong_result(request):
	if request.method == 'POST':
		player1_username = request.POST.get('player1_username')
		player2_username = request.POST.get('player2_username')
		player1_score = int(request.POST.get('player1_score'))
		player2_score = int(request.POST.get('player2_score'))

		user1 = CustomUser.objects.filter(username=player1_username).first()
		user2 = CustomUser.objects.filter(username=player2_username).first()

		if player1_score > player2_score:
			winner, loser = user1, user2
		else:
			winner, loser = user2, user1

		pong_id = request.POST.get('pong_id')
		match = PongResult.objects.get(id=pong_id)

		match.player1_score = player1_score
		match.player2_score = player2_score
		match.winner = winner
		match.loser = loser
		if user1:
			match.players.add(user1)
		if user2:
			match.players.add(user2)
		match.save()

		tournament = match.tournament

		if not tournament.matches.filter(winner__isnull=True, round_number=tournament.current_round).exists():
			tournament.advance_round()

		return JsonResponse({'status': 'success', 'tournament_id': tournament.id})

	return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
