import React from 'react';

export default function GameOverView({game, highscore, onRestartGame}) {
    let resultText;

    if(game.state === "WON"){
        resultText = "You Won!"
    } else if(game.state === "LOST"){
        resultText = "You Lost!"
    }

    return (
        <div>
            <p>{resultText}</p>
            <p>Score: {game.score}</p>
            <p>High Score: {highscore}</p>
            <button
                type="button"
                onClick={() => onRestartGame()}
            >
                Play Again
            </button>
        </div>
    );
}
