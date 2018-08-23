import collections

class GameManager(object):
  """Manages score of bowling game."""

  frameScores = None  # Hold pins knocked and score scored in each frame.
  frameCounter = 0  # Would be 0 to 9.

  @classmethod
  def startNewGame(self):
    """Starts a new game."""
    GameManager.frameScores = collections.OrderedDict([
        (frameId, {'first-try': 0, 'second-try': 0, 'score': 0})
        for frameId in range(10)
    ])
    return {'message': 'Game started successfully.'}

  @classmethod
  def getScore(self):
    totalScore = sum(GameManager.frameScores[frame]['score']
                     for frame in GameManager.frameScores)
    return {'frame-scores': GameManager.frameScores, 'total-score': totalScore}

  @classmethod
  def pinsKnocked(self):
    """Updates score when a new pin is knocked."""
    if GameManager.frameScores is None:
      return {'message': 'Please start game before this operation.'}
    else:
      return {'message': 'Scores updated for this move.'}
    # GameManager.frameScores[0]['first-try'] = 10
