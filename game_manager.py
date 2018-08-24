import collections

from utils import constants
from utils import singleton

@singleton.singleton
class GameManager(object):
  """Manages score of bowling game."""

  def __init__(self):
    self.frameScores = None  # Hold pins knocked and score scored in each frame.
    self.frameCounter = 0  # Would be 0 to 9.
    self.roll = 0  # 0 or 1

  def startNewGame(self):
    """Starts a new game."""
    self.frameCounter = 0
    self.roll = 0
    self.frameScores = collections.OrderedDict([
        (frameId, {'tries': {0: -1, 1: -1}, 'score': 0})
        for frameId in range(10)
    ])
    return {'message': 'New game started successfully.'}

  def getScore(self):
    if self.frameScores is None:
      return {'message': 'Please start game before fetching score.'}

    totalScore = sum(self.frameScores[frame]['score']
                     for frame in self.frameScores)
    return {'frame-scores': self.frameScores, 'total-score': totalScore}

  def _isStrike(self):
    return self.frameScores[self.frameCounter]['tries'][0] == constants.MAX_PINS

  def _isSpare(self):
    tries = self.frameScores[self.frameCounter]['tries']
    return tries[0] + tries[1] == constants.MAX_PINS

  def _validPinsKnocked(self, pinsKnocked):
    if not pinsKnocked.isdigit():
      return False, 'Pins knocked should be a number.'

    pins = int(pinsKnocked)
    if pins < 0 or pins > 10:
      return False, 'Pins knocked should be positive number, less than 10.'

    frameTries = self.frameScores[self.frameCounter]['tries']
    if self.frameCounter == constants.TOTAL_FRAMES - 1:
      if not self._isStrike() and (
          self.roll == 1 and frameTries[0] + pins > constants.MAX_PINS):
        return False, constants.INVALID_SECOND_ROLL.format(
            firstRollPins=frameTries[0])
      else:
        return True, ''

    if self.roll == 1 and frameTries[0] + pins > constants.MAX_PINS:
      return False, constants.INVALID_SECOND_ROLL.format(
          firstRollPins=frameTries[0])

    return True, ''

  def _updateScore(self, pinsKnocked):
    self.frameScores[self.frameCounter]['tries'][self.roll] = pinsKnocked

    # If strike or spare in last frame.
    if self.frameCounter == constants.TOTAL_FRAMES - 1:
      print 'here, frame ctr is 9 and roll', self.roll
      if (not self.roll) or (
          self.roll < 2 and (self._isStrike() or self._isSpare())):
        self.roll += 1
      else:
        self.frameCounter += 1
    elif not self._isStrike():
      self.roll += 1
    else:
      self.roll = 0
      self.frameCounter += 1

  def pinsKnocked(self, pinsKnocked):
    """Updates score when a new pin is knocked."""
    if self.frameScores is None:
      return {'message': 'Please start game before this operation.'}

    if self.frameCounter == constants.TOTAL_FRAMES:
      return {
          'message': ('All rolls done for this game, please check score and '
                      'start a new game.')
        }

    status, errorMsg = self._validPinsKnocked(pinsKnocked)
    if not status:
      return {'message': errorMsg}

    self._updateScore(int(pinsKnocked))
    return {'message': 'Scores updated for this move.'}
