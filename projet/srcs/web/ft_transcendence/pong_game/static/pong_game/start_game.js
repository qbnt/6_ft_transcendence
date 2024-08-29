document.getElementById('startGameForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const player1Username = document.getElementById('player1Username').value;
    const player2Username = document.getElementById('player2Username').value;

    if (player2Username.trim() === '') {
        fetch('pong_game/start_game_ai/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                player1_username: player1Username
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById('login-container').style.display = 'none';
                document.getElementById('game-container').style.display = 'block';

                startAiPongGame();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    } else {
        fetch('pong_game/start_game/', {
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
                document.getElementById('login-container').style.display = 'none';
                document.getElementById('game-container').style.display = 'block';

                startPongGame();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }
});

