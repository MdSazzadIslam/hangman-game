# Hangman

A simple hangman server and frontend using Python with Flask on the backend, and
Javascript with React on the frontend.

It's split into two projects:

- [hangman-server](hangman-server)
- [hangman-web-app](hangman-web-app)

## Getting started

Get the server up and running

```
cd hangman-server
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

Get the web-app running

```
cd hangman-web-app
npm install
npm run start
```

Play some hangman!

```
http://localhost:3000
```