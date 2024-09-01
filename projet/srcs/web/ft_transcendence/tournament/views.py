from django.shortcuts   import render
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
def affichage_matchs(request):
    make_matches()
    matchs = []
    for i in Players.matchs:
        matchs.extend(i)
    return render(request, 'Tournoi.html', {'matchs': matchs})

#Setup des joueurs, on les obtiens grâce au beau html Setup_players (svp rendez le plus beau)
def setup_players(request):
    if request.method == 'POST':
        Players.players.clear()

        # Récupérer tous les noms des joueurs envoyés depuis le formulaire
        for key, value in request.POST.items():
            if key.startswith('player'):
                Players.players.append(value)

        return render(request, 'Confirmation_Tournoi.html', {'players': Players.players})

    return render(request, 'Setup_players.html')