// ##########     GENERAL VARIABLES     ##########
// varaible DIRECTION | status de mouvement d'un object

var DIRECTION = {
    IDLE: 0,
	UP: 1,
	DOWN: 2,
	LEFT: 3,
	RIGHT: 4,
}

var keys = {};
var rounds = [5, 5, 3, 3, 2];
var colors = ['#1abc9c', '#2ecc71', '#3498db', '#8c52ff', '#9b59b6'];

// ##########     BALL     ##########
// l.19 | fonction qui cree un object (balle). | ici "new" n'est pas un operateur absolu, il est remplacable par le mot de son choix.
//		| appel avec par exemple [var balle = Ball.new(incrementedSpeed)] | methode 'new' != operateur 'new'

var Ball = {
    new: function (incrementedSpeed) {
        return {
            width: 18,
            height: 18,
            x: (this.canvas.width / 2) - 9,
            y: (this.canvas.height / 2) - 9,
            moveX: DIRECTION.IDLE,
            moveY: DIRECTION.IDLE,
            speed: incrementedSpeed || 7
        };
    }
};

// ##########     BAR    ########## 
// l.40 | true/false sitation | [consition] ? [action si condition true] : [action si condition false]

var Ai = {
    new: function (side) {
        return {
            username: player,
            width: 18,
            height: 180,
            x: side === 'left' ? 150 : this.canvas.width - 150,
            y: (this.canvas.height / 2) - 35,
            score: 0,
            round_score: 0,
            move: DIRECTION.IDLE,
            speed: 8
        };
    }
};

// ##########     GAME     ##########
// l.58  | 'document' = fichier HTML |
//		 | querySelector = selection de secteur (truc comme ca -> <secteur>) dans le HTML, le secteur peut etre appele par un truc qui le definit (class, ID, etc...)
//		 | getContext = fonction pour canva qui permet d'utiliser des fonctions pour dessiner selon son parametre, ici '2d'.
// l.67  | call() = definit le contexte dans lequel est appele la fonction |
//		 | ici call(this, 'left') creera l'object au 'left' de l'object 'Game', car appele dans la definition de 'Game'.

var Game = {
    initialize: function () {
        this.canvas = document.querySelector('canvas');
        this.context = this.canvas.getContext('2d');
 
        this.canvas.width = 1400;
        this.canvas.height = 1000;
 
        this.canvas.style.width = (this.canvas.width / 2) + 'px';
        this.canvas.style.height = (this.canvas.height / 2) + 'px';
 
        this.player1 = Ai.new.call(this, 'left');
        this.player2 = Ai.new.call(this, 'right');
        this.ball = Ball.new.call(this);
 
        this.running = this.over = false;
        this.turn = this.player2;
        this.timer = this.round = 0;
        this.color = '#8c52ff';
 
        Pong.menu();
        Pong.listen();
    },

// l.91  | fillRect(pox x, pos y, largeur, hauteur) | probablement utilisable grace au context '2d'
// l.100 | fillText(text, x, y)
// l.105 | setTimeout(fonction, delai) | execute la fonction au bout du delai.
// l.106 | assign(lieu de copie des proprietes de la source, la source)
//		 | ici '{}' signifie qu'on ne veut retenir les propriete d'aucune cible, en gros on copie la source dans un lieu vide 

	endGameMenu: function (text) { 
        Pong.context.font = '45px Gentium Plus';
        Pong.context.fillStyle = this.color;
 
        Pong.context.fillRect(
            Pong.canvas.width / 2 - 350,
            Pong.canvas.height / 2 - 48,
            700,
            100
        );
 
        Pong.context.fillStyle = '#ffffff';
 
        Pong.context.fillText(text,
            Pong.canvas.width / 2,
            Pong.canvas.height / 2 + 15
        );

		setTimeout(function () {
            Pong = Object.assign({}, Game);
            Pong.initialize();
        }, 3000);
    },

// l.117/126 | fillStyle s'applique pour les elements suivants jusqu'a ce qu'un autre appel de fillStyle soit fait (ou fin du scope ?)

    menu: function () {
        Pong.draw();
 
        this.context.font = '50px Gentium Plus';
        this.context.fillStyle = this.color;
 
        this.context.fillRect(
            this.canvas.width / 2 - 350,
            this.canvas.height / 2 - 48,
            700,
            100
        );
 
        this.context.fillStyle = '#ffffff';
 
        this.context.fillText('Press any key to begin',
            this.canvas.width / 2,
            this.canvas.height / 2 + 15
        );
    },

// !!!   | en canva HTML l'axe des y augmente vers le bas !!
// l.154 | Math.random(); genere un float entre 0 et 1 si pas d'argument | si Math.random() * [valeur max], entre 0 et [valeur max]
//       | Math.round(); arrodit l'argument a l'entier le plus proche
//       | Avec un tableau devant comme ici le resultat de 'Math.random()' determinera l'index de la valeur choisie
//       | Math.floor(); arrondit a l'entier inferieur

    update: function () {
        if (!this.over) {
            if (this.ball.x <= 0) Pong._resetTurn.call(this, this.player2, this.player1);
            if (this.ball.x >= this.canvas.width - this.ball.width) Pong._resetTurn.call(this, this.player1, this.player2);
            if (this.ball.y <= 0) this.ball.moveY = DIRECTION.DOWN;
            if (this.ball.y >= this.canvas.height - this.ball.height) this.ball.moveY = DIRECTION.UP;
 
            if (this.player1.move === DIRECTION.UP) this.player1.y -= this.player1.speed;
            else if (this.player1.move === DIRECTION.DOWN) this.player1.y += this.player1.speed;

            if (this.player2.move === DIRECTION.UP) this.player2.y -= this.player2.speed;
            else if (this.player2.move === DIRECTION.DOWN) this.player2.y += this.player2.speed;
 
            if (Pong._turnDelayIsOver.call(this) && this.turn) {
                this.ball.moveX = this.turn === this.player1 ? DIRECTION.LEFT : DIRECTION.RIGHT;
                this.ball.moveY = [DIRECTION.UP, DIRECTION.DOWN][Math.round(Math.random())];
                this.ball.y = Math.floor(Math.random() * this.canvas.height - 200) + 200;
                this.turn = null;
            }
 
            if (this.player1.y <= 0) this.player1.y = 0;
            else if (this.player1.y >= (this.canvas.height - this.player1.height)) this.player1.y = (this.canvas.height - this.player1.height);

            if (this.player2.y <= 0) this.player2.y = 0;
            else if (this.player2.y >= (this.canvas.height - this.player2.height)) this.player2.y = (this.canvas.height - this.player2.height);
 
            if (this.ball.moveY === DIRECTION.UP) this.ball.y -= (this.ball.speed / 1.5);
            else if (this.ball.moveY === DIRECTION.DOWN) this.ball.y += (this.ball.speed / 1.5);
            if (this.ball.moveX === DIRECTION.LEFT) this.ball.x -= this.ball.speed;
            else if (this.ball.moveX === DIRECTION.RIGHT) this.ball.x += this.ball.speed;
           
            if (this.ball.x - this.ball.width <= this.player1.x && this.ball.x >= this.player1.x - this.player1.width) {
                if (this.ball.y <= this.player1.y + this.player1.height && this.ball.y + this.ball.height >= this.player1.y) {
                    this.ball.x = (this.player1.x + this.ball.width);
                    this.ball.moveX = DIRECTION.RIGHT;
                    this.ball.speed += 0.1;
                }
            }
            
            if (this.ball.x - this.ball.width <= this.player2.x && this.ball.x >= this.player2.x - this.player2.width) {
                if (this.ball.y <= this.player2.y + this.player2.height && this.ball.y + this.ball.height >= this.player2.y) {
                    this.ball.x = (this.player2.x - this.ball.width);
                    this.ball.moveX = DIRECTION.LEFT;
                    this.ball.speed += 0.1;
                }
            }
        }
        
        if (this.player1.score === rounds[this.round]) {
            if (!rounds[this.round + 1] || this.player1.round_score + 1 === 3) {
                this.over = true;
                this.player1.round_score += 1;
                setTimeout(function () { Pong.endGameMenu('Player 1 Wins!'); }, 1000);
            } else {
                this.color = this._generateRoundColor();
                this.player1.score = this.player2.score = 0;
                this.player1.round_score += 1;
                this.player1.speed = this.player2.speed += 0.5;
                this.ball.speed = 7;
                this.round += 1;
                
            }
        }
        else if (this.player2.score === rounds[this.round]) {
            if (!rounds[this.round + 1] || this.player2.round_score + 1 === 3) {
                this.player2.round_score += 1;
                this.over = true;
                setTimeout(function () { Pong.endGameMenu('Player 2 Wins!'); }, 1000);
            } else {
                this.color = this._generateRoundColor();
                this.player1.score = this.player2.score = 0;
                this.player2.round_score += 1;
                this.player1.speed = this.player2.speed += 0.5;
                this.ball.speed = 7;
                this.round += 1;
                
            }
        }
    },

// l.223 | clearRect(pos x, pos y, largeur, hauteur) efface dans la zone du rectangle donnee
// l.264 | beginPath(); indique que le trace a suivre ne prends pas en compte les parametres precedents
//       | setLineDash([longueur segment de ligne, longueur espaces]); trace une ligne segmentee
//       | moveTo(pos x, pos y); positionne le debut du trace
//       | lineTo(pos x, pos y); positionne la fin du trace
//       | stroke(); finalise les parametres du trace

    draw: function () {
        this.context.clearRect(
            0,
            0,
            this.canvas.width,
            this.canvas.height
        );
 
        this.context.fillStyle = this.color;
 
        this.context.fillRect(
            0,
            0,
            this.canvas.width,
            this.canvas.height
        );
 
        this.context.fillStyle = '#ffffff';
 
        this.context.fillRect(
            this.player1.x,
            this.player1.y,
            this.player1.width,
            this.player1.height
        );
 
        this.context.fillRect(
            this.player2.x,
            this.player2.y,
            this.player2.width,
            this.player2.height 
        );
 
        if (Pong._turnDelayIsOver.call(this)) {
            this.context.fillRect(
                this.ball.x,
                this.ball.y,
                this.ball.width,
                this.ball.height
            );
        }
 
        this.context.beginPath();
        this.context.setLineDash([7, 15]);
        this.context.moveTo((this.canvas.width / 2), this.canvas.height - 70);
        this.context.lineTo((this.canvas.width / 2), 140);
        this.context.lineWidth = 10;
        this.context.strokeStyle = '#ffffff';
        this.context.stroke();
 
        this.context.font = '100px Gentium Plus';
        this.context.textAlign = 'center';
 
        this.context.fillText(
            this.player1.score.toString(),
            (this.canvas.width / 2) - 300,
            200
        );
 
        this.context.fillText(
            this.player2.score.toString(),
            (this.canvas.width / 2) + 300,
            200
        );
 
        this.context.font = '30px Gentium Plus';
 
        this.context.fillText(
            'Round ' + (Pong.round + 1),
            (this.canvas.width / 2),
            35
        );
 
        this.context.font = '40px Gentium Plus';
 
        this.context.fillText(
            rounds[Pong.round] ? rounds[Pong.round] : rounds[Pong.round - 1],
            (this.canvas.width / 2),
            80
        );

        this.context.fillText(
            (`${this.player1.round_score} - ${this.player2.round_score}`),
            (this.canvas.width / 2),
            120
        );
    },

// l.310 | requestAnimationFrame(fonction); fonction native du navigateur qui appelle la fonction en parametre avant le rafraichissement de l'ecran

    loop: function () {
        Pong.update();
        Pong.draw();

        if (!Pong.over) requestAnimationFrame(Pong.loop);
    },

//  l.316 | addEventListener(event, fonction); ajoute un ecouteur d'event qui lance la fonction en parametre si l'event en parametre a lieu

    listen: function () {
        document.addEventListener('keydown', function (key) {
            keys[key.keyCode] = true;

            if (Pong.running === false) {
                Pong.running = true;
                window.requestAnimationFrame(Pong.loop);
            }
 
            updatePlayerMovement();
        });
 
        document.addEventListener('keyup', function (key) {
            keys[key.keyCode] = false 
            updatePlayerMovement();
        });
        
        function updatePlayerMovement() {
            if (keys[38]) Pong.player2.move = DIRECTION.UP;
            else if (keys[40]) Pong.player2.move = DIRECTION.DOWN;
            else Pong.player2.move = DIRECTION.IDLE;

            if (keys[87]) Pong.player1.move = DIRECTION.UP;
            else if (keys[83]) Pong.player1.move = DIRECTION.DOWN;
            else Pong.player1.move = DIRECTION.IDLE;
        }
    },

    _resetTurn: function(victor, loser) {
        this.ball = Ball.new.call(this, this.ball.speed);
        this.turn = loser;
        this.timer = (new Date()).getTime();
        
        victor.score++;
    },
    
    // l.345 | [new Date()).getTime()] = timestamp Unix = nb ms ecoulees depuis 01/01/1970
    
    _turnDelayIsOver: function() {
        return ((new Date()).getTime() - this.timer >= 1000);
    },

    _generateRoundColor: function () {
        var newColor = colors[Math.floor(Math.random() * colors.length)];
        if (newColor === this.color) return Pong._generateRoundColor();
        return newColor;
    }
};

var Pong = Object.assign({}, Game);
Pong.initialize();

function sendPongResult(player1Id, player2Id, player1Score, player2Score) {
    const data = new URLSearchParams();
    data.append('player1_username', player1Id);
    data.append('player2_id', player2Id);
    data.append('player1_score', player1Score);
    data.append('player2_score', player2Score);

    fetch('/save_result/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// ##########     AI JS     ##########


/*         // Handle ai (AI) UP and DOWN movement
         if (this.ai.y > this.ball.y - (this.ai.height / 2)) {
             if (this.ball.moveX === DIRECTION.RIGHT) this.ai.y -= this.ai.speed / 1.5;
             else this.ai.y -= this.ai.speed / 4;
         }
         if (this.ai.y < this.ball.y - (this.ai.height / 2)) {
             if (this.ball.moveX === DIRECTION.RIGHT) this.ai.y += this.ai.speed / 1.5;
             else this.ai.y += this.ai.speed / 4;
         }

         // Handle ai (AI) wall collision
         if (this.ai.y >= this.canvas.height - this.ai.height) this.ai.y = this.canvas.height - this.ai.height;
         else if (this.ai.y <= 0) this.ai.y = 0; */