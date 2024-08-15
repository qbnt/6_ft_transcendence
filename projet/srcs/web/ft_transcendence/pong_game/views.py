from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from pong_game.models import PongResult
from user_manage.models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import json

def pong_view(request):
    return render(request, 'pong_game/pong.html')

def save_pong_result(request):
    if request.method == 'POST':
        player1_username = request.POST.get('player1_username')
        player2_username = request.POST.get('player2_username')
        player1_score = int(request.POST.get('player1_score'))
        player2_score = int(request.POST.get('player2_score'))

        try:
            player1 = CustomUser.objects.get(username=player1_username)
            player2 = CustomUser.objects.get(username=player2_username)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'One or both users not found'}, status=404)
    
        if player1_score > player2_score:
            winner = player1
            loszer = player2
        else:
            winner = player2
            loser = player1

        PongResult.objects.create(
            player1=player1,
            player2=player2,
            player1_score=player1_score,
            player2_score=player2_score,
            winner=winner,
            loser=loser
        )

        return JsonResponse({'status': 'success', 'message': 'Result saved successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt    
def start_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            player1_username = data.get('player1_username')
            player2_username = data.get('player2_username')

            if not player1_username or not player2_username:
                return JsonResponse({'status': 'error', 'message': 'Both usernames are required.'}, status=400)

            # try:
            #     player1 = CustomUser.objects.get(username=player1_username)
            #     player2 = CustomUser.objects.get(username=player2_username)
            # except CustomUser.DoesNotExist:
            #     return JsonResponse({'status': 'error', 'message': 'One or both usernames are invalid.'}, status=400)

            # # Authentifier les utilisateurs (facultatif, si tu as besoin de validation supplémentaire)
            # player1 = authenticate(username=player1_username)
            # player2 = authenticate(username=player2_username)

            # if not player1 or not player2:
            #     return JsonResponse({'status': 'error', 'message': 'Authentication failed.'}, status=400)

            # # Logique pour démarrer le jeu ici (peut-être créer un enregistrement de jeu, etc.)

            return JsonResponse({'status': 'success', 'message': 'Game started successfully.'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
