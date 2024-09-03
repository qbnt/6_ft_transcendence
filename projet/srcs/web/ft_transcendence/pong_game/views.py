from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from pong_game.models import PongResult
from user_manage.models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

def pong_view(request):
    return render(request, 'pong_game/pong.html')

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

        pong_result = PongResult.objects.create(
            player1=user1.username if user1 else None,
            player2=user2.username if user2 else None,
            player1_score=player1_score,
            player2_score=player2_score,
            winner=winner,
            loser=loser,
            date_played=datetime.now()
        )

        if user1:
            pong_result.players.add(user1)
        if user2:
            pong_result.players.add(user2)

        return JsonResponse({'status': 'success', 'message': 'Result saved successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

# `def check_usernames(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         player1_username = data.get('player1_username')
#         player2_username = data.get('player2_username')

#         user1_exists = CustomUser.objects.filter(username=player1_username).exists()
#         user2_exists = CustomUser.objects.filter(username=player2_username).exists()

#         if not user1_exists:
#             return JsonResponse({'status': 'error', 'message': 'Player 1 username does not exist.'}, status=400)

#         if player2_username and not user2_exists:
#             return JsonResponse({'status': 'error', 'message': 'Player 2 username does not exist.'}, status=400)

#         return JsonResponse({'status': 'success'})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)`