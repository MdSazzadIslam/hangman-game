// Just hardcoding this here until we need to actually deploy this somewhere
const API_HOST = "http://localhost:5000";

async function createGame() {
  const url = `${API_HOST}/api/hangman`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  const json = await response.json();
  return json;
}

async function getGame(gameId) {
  const url = `${API_HOST}/api/hangman/${gameId}`;
  const response = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  const json = await response.json();
  return json;
}

async function makeGuess(gameId, letter) {
  const url = `${API_HOST}/api/hangman/${gameId}/guess`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ letter: letter }),
  });
  const json = await response.json();
  return json;
}

const gameExports = {
  createGame,
  getGame,
  makeGuess,
};

export default gameExports;
