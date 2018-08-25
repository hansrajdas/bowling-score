"""Implements and maps each handler to respective class."""

from flask import Flask
from flask import request

from flask_restful import Api
from flask_restful import Resource

from game_manager import GameManager

app = Flask(__name__)
api = Api(app)

gameMgr = GameManager()


class GetScore(Resource):
    def get(self):
        return gameMgr.getScore()


class StartGame(Resource):
    def post(self):
        return gameMgr.startNewGame()


class PinsKnocked(Resource):
    def post(self):
        if request.form.get('pins-knocked', None) is None:
            return {
              'message': 'Invalid request, parameter `pins-knocked` missing.'
            }
        return gameMgr.pinsKnocked(request.form['pins-knocked'])


api.add_resource(StartGame, '/start-game')
api.add_resource(PinsKnocked, '/pins-knocked')
api.add_resource(GetScore, '/', '/get-score')


if __name__ == '__main__':
    app.run(debug=True)
