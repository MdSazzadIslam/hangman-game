from flask import Blueprint, request, jsonify
import hangman
from gamemanager import GameManager


api = Blueprint("api", __name__)

# This is fine for single process server but if running in multiple processes the game management will have to be
# stored in some other shared memory
game_manager = GameManager()


# Allow the web-app to access these endpoints. This shouldn't be used in prod unless we wanna allow access to the api
# from other domains other than our own
@api.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


def jsonifyGame(game_id, game):
    to_enum_string = {
        hangman.GameState.IN_PROGRESS: "IN_PROGESS",
        hangman.GameState.WON: "WON",
        hangman.GameState.LOST: "LOST",
    }

    return jsonify(
        {
            "gameId": game_id,
            "state": to_enum_string[game.state],
            "revealedWord": game.revealed_word,
            "numFailedGuessesRemaining": game.num_failed_guesses_remaining,
            "score": hangman.HangmanGameScorer.score(game),
        }
    )


@api.route("/api/hangman", methods=["POST"])
def post_hangman():
    game_id, game = game_manager.create_game()
    return jsonifyGame(game_id, game), 200


@api.route("/api/hangman/<int:game_id>", methods=["GET"])
def get_hangman(game_id):
    game = game_manager.get_game(game_id)

    if game is None:
        return jsonify({"error": "Game not found"}), 404

    return jsonifyGame(game_id, game), 200


# todo: add a way to make a guess
@api.route("/api/hangman/<int:game_id>/guess", methods=["POST"])
def post_guess(game_id):
    # Retrieve JSON data from the request body
    data = request.get_json()

    # Check if data is present and if "letter" field exists
    if not data or "letter" not in data:
        return jsonify({"error": "Letter not provided in request body."}), 400

    # Extract and normalize the guessed letter
    letter = data.get("letter", "").strip().lower()

    # Validate the guessed letter format
    if not letter.isalpha() or len(letter) != 1:
        return jsonify(
            {"error": "Invalid guess. Please provide a single alphabetical letter."}
        ), 400

    # Call GameManager's guess method to process the guess for the given game_id
    result_message = game_manager.guess(game_id, letter)

    # Return a JSON response with the result message and status code
    return jsonify({"message": result_message}), 200


# todo: add a way to reset the game


@api.route("/api/hangman/<int:game_id>/reset", methods=["POST"])
def post_reset(game_id):
    # Call GameManager's reset_game method to reset the game with the given game_id
    game = game_manager.reset_game(game_id)

    # Check if game is found or not
    if game is None:
        # Return a JSON response with error message and status code 404 if game is not found
        return jsonify({"error": "Game not found"}), 404

    # Return a JSON response with the updated game state and status code 200
    return jsonifyGame(game_id, game), 200
