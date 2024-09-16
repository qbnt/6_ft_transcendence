document.getElementById('startGameForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const player2Username = document.getElementById('player2Username').value;

    document.getElementById('login-container').style.display = 'none';
    document.getElementById('game-container').style.display = 'block';

    if (player2Username.trim() === '') {
        startAiPongGame();
    } else {
        startPongGame();
    }
});

