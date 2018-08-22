from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
  def get(self):
    return {'hello': 'world'}

  def put(self, pins_knocked):
    return pins_knocked + '-test'

api.add_resource(HelloWorld,
                 '/',
                 '/get-score',
                 '/pins-knocked/<int:pins_knocked>')

if __name__ == '__main__':
    app.run(debug=True)
