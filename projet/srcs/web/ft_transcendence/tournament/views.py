from django.shortcuts   import render, redirect
from django.http        import HttpResponse
from .models	        import *

def start(request):
    return HttpResponse("Hello, this is some view!")

def setup_players(request):
    if request.method == 'POST':
        # Récupérer tous les noms des joueurs envoyés depuis le formulaire
        for key, value in request.POST.items():
            if key.startswith('player'):
                Players.players.append(value)

        return render(request, 'Confirmation_Tournoi.html', {'players': Players.players})

    return redirect('/')