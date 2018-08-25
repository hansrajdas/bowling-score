## Requirement
* Bowling score calculator

## Prerequisites
* pip install -i requirements.txt

## Run
* Application: python app.py
* Tests: python -m unittest game_manager_test
* Coverage: python -m coverage report -m

## API Endpoints
* Start a new game
* Input pins knocked
* Get score

## Example
* Start new game: curl http://127.0.0.1:5000/start-game -X POST
* Input pins knocked down by ball: curl http://127.0.0.1:5000/pins-knocked -d "pins-knocked=10" -X POST
* Output current game score: curl http://127.0.0.1:5000/get-score or curl http://127.0.0.1:5000
