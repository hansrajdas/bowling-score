from flask import Flask, request
from flask import request

from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
api = Api(app)

class GetScore(Resource):
  def get(self):
    return {1: 'x'}

class StartGame(Resource):
  def post(self):
    return "New game started..."

class PinsKnocked(Resource):
  def post(self):
    return "Score updated..."

api.add_resource(StartGame, '/start-game')
api.add_resource(PinsKnocked, '/pins-knocked')
api.add_resource(GetScore, '/', '/get-score')

if __name__ == '__main__':
    app.run(debug=True)
