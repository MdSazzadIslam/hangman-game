import hangman


class GameManager:
    def __init__(self):
        self.games = {}
        self.next_game_id = 1

    def create_game(self):
        game = hangman.create_hangman_game()
        game_id = self.next_game_id
        self.games[game_id] = game
        self.next_game_id += 1

        return game_id, game

    def get_game(self, game_id):
        return self.games.get(game_id, None)

    def guess(self, game_id, letter):
        game = self.get_game(game_id)
        if not game:
            return "Game not found!"

        guess_result = game.guess(letter)
        if guess_result == hangman.GuessResult.CORRECT:
            if game.state == hangman.GameState.WON:
                return "You won!"
            else:
                return "Correct guess!"
        elif guess_result == hangman.GuessResult.INCORRECT:
            if game.state == hangman.GameState.LOST:
                return f"You lost! The word was: {game.word}"
            else:
                return "Incorrect guess!"
        elif guess_result == hangman.GuessResult.FAIL_INVALID_INPUT:
            return "Invalid guess input!"
        elif guess_result == hangman.GuessResult.FAIL_ALREADY_GAME_OVER:
            return "Game is already over!"
        elif guess_result == hangman.GuessResult.FAIL_ALREADY_GUESSED:
            return "Letter already guessed!"

        return "Unknown error occurred!"

    def reset_game(self, game_id):
        game = self.get_game(game_id)
        if game:
            game.reset_game()
            return game
        return None
