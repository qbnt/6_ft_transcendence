from django.shortcuts   import render, redirect
from django.http        import HttpResponse
from .models	        import *

#Création des matchs, Algo utilisé: Round-Robin (aucune idée, il a juste un nom stylé)
def make_matches():
    n = len(Players.players)
    if (n % 2 != 0):
        Players.players.append(None) #Dans le cas ou il y a un nombre impair de joueurs
    
    for round in range(n - 1):
        round_matches = []
        for i in range(n // 2):
            one = Players.players[i]
            two = Players.players[n - 1 - i]
            if one is not None and two is not None:
                round_matches.append((one, two))
        Players.matchs.append(round_matches)
        Players.players.insert(1, Players.players.pop())
            
#Début du tournoi
def Tournoi(request):
    make_matches()
    return render(request, 'Tournoi.html')

#Setup des joueurs, on les obtiens grâce au beau html Setup_players (svp rendez le plus beau)
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