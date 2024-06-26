from server import app
import json
import sys
import hangman
import pytest

# Monkey patch the create game function so we can have a deterministic word to test with. This should
# probably read the words from some config and not rely on hardcoded vars but this is simpler.
original_hangman_create = hangman.create_hangman_game


def create_game_with_override_words(words=None, guess_limit=5):
    return original_hangman_create(words=["abac"], guess_limit=5)


hangman.create_hangman_game = create_game_with_override_words


def parse_response(response):
    return json.loads(response.get_data().decode(sys.getdefaultencoding()))


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def game(client):
    return parse_response(client.post("/api/hangman"))


@pytest.fixture()
def game_get_resource(client, game):
    game_id = game["gameId"]
    return parse_response(client.get(f"/api/hangman/{game_id}"))


def test_create_game(game):
    response = game

    assert "gameId" in response
    assert response["state"] == "IN_PROGESS"
    assert response["revealedWord"] == "____"
    assert response["numFailedGuessesRemaining"] == 5
    assert response["score"] == 5 * 10


def test_get_game(game_get_resource):
    response = game_get_resource

    assert "gameId" in response
    assert response["state"] == "IN_PROGESS"
    assert response["revealedWord"] == "____"
    assert response["numFailedGuessesRemaining"] == 5
    assert response["score"] == 5 * 10


def test_guess(client, game):
    game_id = game["gameId"]
    initial_revealed_word = game["revealedWord"]

    # Make a correct guess (assuming the word is "abac")
    guess_data = {"letter": "a"}
    response = client.post(f"/api/hangman/{game_id}/guess", json=guess_data)
    assert response.status_code == 200

    response_data = parse_response(response)
    assert "message" in response_data
    assert response_data["message"] == "Correct guess!"

    # Get updated game state after guess
    updated_game = parse_response(client.get(f"/api/hangman/{game_id}"))
    assert updated_game["revealedWord"] != initial_revealed_word

    # Make an incorrect guess
    guess_data = {"letter": "z"}
    response = client.post(f"/api/hangman/{game_id}/guess", json=guess_data)
    assert response.status_code == 200

    response_data = parse_response(response)
    assert "message" in response_data
    assert response_data["message"] == "Incorrect guess!"

    # Get updated game state after incorrect guess
    updated_game = parse_response(client.get(f"/api/hangman/{game_id}"))
    assert updated_game["numFailedGuessesRemaining"] < 5

    # Make repeated guess which should fail
    guess_data = {"letter": "a"}
    response = client.post(f"/api/hangman/{game_id}/guess", json=guess_data)
    assert response.status_code == 400

    response_data = parse_response(response)
    assert "error" in response_data
    assert "already guessed" in response_data["error"].lower()


def test_reset(client, game):
    game_id = game["gameId"]

    # Make some guesses to change game state
    guess_data = {"letter": "a"}
    client.post(f"/api/hangman/{game_id}/guess", json=guess_data)
    guess_data = {"letter": "z"}
    client.post(f"/api/hangman/{game_id}/guess", json=guess_data)

    # Reset the game
    response = client.post(f"/api/hangman/{game_id}/reset")
    assert response.status_code == 200

    response_data = parse_response(response)
    assert "gameId" in response_data
    assert response_data["gameId"] == game_id
    assert response_data["state"] == "IN_PROGRESS"
    assert response_data["revealedWord"] == "____"
    assert response_data["numFailedGuessesRemaining"] == 5
    assert response_data["score"] == 5 * 10
