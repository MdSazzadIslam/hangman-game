/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from "react";

function Word({ revealedWord }) {
  const wordWithSpaces = revealedWord.split("").join(" ");
  return <p>{wordWithSpaces}</p>;
}

function GuessDisplay({ game, guessResult }) {
  return (
    <div>
      <p>Guesses Remaining: {game.numFailedGuessesRemaining}</p>
      <p>{guessResult.error ? guessResult.error : ""}</p>
    </div>
  );
}

function GuessInput({ onLetterUpdated, onGuess }) {
  const [letter, setLetter] = useState("");

  useEffect(() => {
    if (typeof onLetterUpdated === "function") {
      onLetterUpdated();
    }
  }, [letter]);

  function submitGuess() {
    setLetter("");
    if (typeof onGuess === "function") {
      onGuess(letter);
      console.log(letter);
    }
  }

  function onKeyPress(ev) {
    if (ev.key === "Enter") {
      submitGuess();
    }
  }

  return (
    <div>
      <input
        type="text"
        value={letter}
        autoFocus
        onChange={(e) => setLetter(e.target.value)}
        onKeyPress={(e) => onKeyPress(e)}
      />
      <button type="button" onClick={() => submitGuess()}>
        Guess
      </button>
    </div>
  );
}

export default function GameView({
  game,
  guessResult,
  onLetterUpdated,
  onGuess,
}) {
  return (
    <div>
      <Word revealedWord={game.revealedWord} />
      <GuessDisplay game={game} guessResult={guessResult} />
      <GuessInput onLetterUpdated={onLetterUpdated} onGuess={onGuess} />
    </div>
  );
}
