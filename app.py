from flask import Flask
from flask import request

from flask_restful import Api
from flask_restful import Resource

from game_manager import GameManager

app = Flask(__name__)
api = Api(app)

class GetScore(Resource):
  def get(self):
    return GameManager.getScore()

class StartGame(Resource):
  def post(self):
    return GameManager.startNewGame()

class PinsKnocked(Resource):
  def post(self):
    return GameManager.pinsKnocked()

api.add_resource(StartGame, '/start-game')
api.add_resource(PinsKnocked, '/pins-knocked')
api.add_resource(GetScore, '/', '/get-score')

if __name__ == '__main__':
  app.run(debug=True)
