// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GameScores{
	
	// Structure pour stocker les informations de score
	struct Score {
		uint256	score;
		uint256	time;
	}

	// Mapping pour stocker les scores des joueurs
	mapping(address => Score) private scores;

	// Event pour signaler un nouveau score
	event NewScore(address indexed player, uint256 score);

	// Fonction pour soumettre un score
	function submitScore(uint256 _score) public{
		// Enregistre le score avec le temps actuel
		scores[msg.sender] = Score({
			score: _score,
			time: block.timestamp
		});

		// Transmition du nouveau score
		emit NewScore(msg.sender, _score);
	}

	// Fonction poyur récuperer le score d'un joueur 
	function getScore(address _player) public view returns (uint256, uint256){
		Score memory playerscore = scores[_player];
		return (playerscore.score, playerscore.time);
	}
}