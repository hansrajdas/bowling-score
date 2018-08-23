import collections

from utils import constants
from utils import singleton

@singleton.singleton
class GameManager(object):
  """Manages score of bowling game."""

  def __init__(self):
    self.frameScores = None  # Hold pins knocked and score scored in each frame.
    self.frameCounter = 0  # Would be 0 to 9.

  def startNewGame(self):
    """Starts a new game."""
    self.frameScores = collections.OrderedDict([
        (frameId, {'tries': {0: 0, 1: 0}, 'score': 0})
        for frameId in range(10)
    ])
    return {'message': 'New game started successfully.'}

  def getScore(self):
    if self.frameScores is None:
      return {'message': 'Please start game before fetching score.'}

    totalScore = sum(self.frameScores[frame]['score']
                     for frame in self.frameScores)
    return {'frame-scores': self.frameScores, 'total-score': totalScore}

  def pinsKnocked(self, pinsKnocked):
    """Updates score when a new pin is knocked."""
    self.frameScores[constants.TOTAL_FRAMES - 1]['tries'][2] = pinsKnocked
    if self.frameScores is None:
      return {'message': 'Please start game before this operation.'}
    else:
      return {'message': 'Scores updated for this move.'}
