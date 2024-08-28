from django.shortcuts   import render, redirect
from django.http        import HttpResponse
from .models	        import *

def make_matches():
    n = len(Players.players)
    for i in range(n):
        for j in range(i + 1, n):
            Players.matchs.append((Players.players[i], Players.players[j]))

def start(request):
    make_matches()
    return HttpResponse("Hello, this is some view!")

def setup_players(request):
    if request.method == 'POST':
        # Clear the existing player list to avoid duplicates on subsequent POSTs
        Players.players.clear()

        # Récupérer tous les noms des joueurs envoyés depuis le formulaire
        for key, value in request.POST.items():
            if key.startswith('player'):
                Players.players.append(value)

        return render(request, 'Confirmation_Tournoi.html', {'players': Players.players})

    # Redirect to the URL pattern name for the setup players page
    return render(request, 'Setup_players.html')