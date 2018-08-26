## Requirement
It should provide the following:
* A way to start a new bowling game;
* A way to input the number of pins knocked down by each ball;
* A way to output the current game score (score for each frame and total score).

This API can be used by a bowling house. On the screen the user starts the game, then after each throw the machine, with a sensor, counts how many pins were dropped and calls the API sending this information. In the meantime the screen is constantly (for example: every 2 seconds) asking the API for the current game status and displays it. For scoring rules, please check [this](https://en.wikipedia.org/wiki/Ten-pin_bowling).

## Prerequisites
* Flask
* Flask-RESTful

## Setup
```
pip install -r requirements.txt
```


## Assumptions
* This application supports one game and one player at a time.
* When a new game is started previous game's score will be lost.
* -1 in frame score indicates either rolls not made for this frame or score is not updated yet, it is dependent on future rolls.
* -1 in frame roll indicates either roll not made for this frame or first roll in this frame was knocked with a strike.

## API Endpoints :-
**/start-game**
- description: Starts a new game.
- method: `POST`
- arguments: `None`
- data: `None`
- returns: Success message in JSON format.
- HTTP response: `200 OK`

**/pins-knocked**
- description: Input pins knocked in a roll.
- method: `POST`
- arguments: `None`
- data: Number of pins knocked, e.g. `pins-knocked=5`
- returns: Success message or error message based on pins-knocked in JSON format.
- HTTP response: `200 OK`

**/get-score**
- method: `GET`
- arguments: `None`
- returns: Total score and per frame pins knocked and corresponding score.
- HTTP response: `200 OK`

## Usage
* Application:
```
python app.py
```
* Tests:
```
python -m unittest game_manager_test
```
* Coverage:
    * Run coverage:
    ```
    python -m coverage run game_manager_test.py
    ```
    * Get stats report:
    ```
    python -m coverage report -m
    ```
    * Generate HTML report:
    ```
    python -m coverage html
    ```

## Example
Any rest client like postman or curl can be used. Below are some curl commands used with above application:
* Start new game
  ```
  curl http://127.0.0.1:5000/start-game -X POST
  ```
* Input pins knocked down by ball
  ```
  curl http://127.0.0.1:5000/pins-knocked -d "pins-knocked=10" -X POST
  ```
* Output current game score
  ```
  curl http://127.0.0.1:5000/get-score
  curl http://127.0.0.1:5000
  ```
