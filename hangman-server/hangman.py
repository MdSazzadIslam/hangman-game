import random
from enum import Enum


class GameState(Enum):
    IN_PROGRESS = 0
    WON = 1
    LOST = 2


class GuessResult(Enum):
    CORRECT = 0
    INCORRECT = 1

    FAIL_INVALID_INPUT = 2
    FAIL_ALREADY_GAME_OVER = 3
    FAIL_ALREADY_GUESSED = 4


class HangmanGame:
    def __init__(self, word, failed_guesses_limit):
        if failed_guesses_limit <= 0:
            raise ValueError("failed_guesses_limit must be over 0")

        if len(word) <= 0:
            raise ValueError("word must have at least 1 letter")

        self.word = word

        self.state = GameState.IN_PROGRESS
        self.guesses = []
        self.failed_guess_limit = failed_guesses_limit
        self.num_failed_guesses_remaining = failed_guesses_limit
        self.revealed_word = "".join(["_" for i in range(len(word))])
        self.num_revealed_letters = 0

    def guess(self, input_letter):
        if not input_letter.isalpha() or len(input_letter) != 1:
            return GuessResult.FAIL_INVALID_INPUT

        if self.state != GameState.IN_PROGRESS:
            return GuessResult.FAIL_ALREADY_GAME_OVER

        if input_letter in self.guesses:
            return GuessResult.FAIL_ALREADY_GUESSED

        self.guesses.append(input_letter)

        if input_letter in self.word:
            new_revealed_word = ""
            for char in self.word:
                if char in self.guesses:
                    new_revealed_word += char
                else:
                    new_revealed_word += "_"

            if new_revealed_word == self.word:
                self.state = GameState.WON
            else:
                self.revealed_word = new_revealed_word
                self.num_revealed_letters = sum(
                    1 for char in new_revealed_word if char.isalpha()
                )

            return (
                GuessResult.CORRECT
                if self.state == GameState.WON
                else GuessResult.CORRECT
            )
        else:
            self.num_failed_guesses_remaining -= 1
            if self.num_failed_guesses_remaining <= 0:
                self.state = GameState.LOST
            return GuessResult.INCORRECT

    def reset_game(self):
        self.word = create_hangman_game().word
        self.state = GameState.IN_PROGRESS
        self.guesses = []
        self.num_failed_guesses_remaining = self.failed_guess_limit
        self.revealed_word = "".join(["_" for _ in range(len(self.word))])
        self.num_revealed_letters = 0


class HangmanGameScorer:
    POINTS_PER_LETTER = 20
    POINTS_PER_REMAINING_GUESS = 10

    @classmethod
    def score(cls, game):
        points = game.num_revealed_letters * HangmanGameScorer.POINTS_PER_LETTER
        points += (
            game.num_failed_guesses_remaining
            * HangmanGameScorer.POINTS_PER_REMAINING_GUESS
        )
        return points


def create_hangman_game(words=None, guess_limit=5):
    if words is None:
        words = ["3d", "marvin", "protolabs", "print", "filament", "order", "layer"]

    if len(words) <= 0:
        raise ValueError("words must have at least 1 word")

    if guess_limit <= 0:
        raise ValueError("guess_limit must be greater than 0")

    rand_word = words[random.randint(0, len(words) - 1)]
    return HangmanGame(rand_word, guess_limit)
