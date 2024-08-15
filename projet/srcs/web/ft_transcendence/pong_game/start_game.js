document.getElementById('startGameForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const player1Username = document.getElementById('player1Username').value;
    const player2Username = document.getElementById('player2Username').value;

    fetch('/start_game/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            player1_username: player1Username,
            player2_username: player2Username
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Masquer le formulaire et afficher le jeu
            document.getElementById('login-container').style.display = 'none';
            document.getElementById('game-container').style.display = 'block';
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});