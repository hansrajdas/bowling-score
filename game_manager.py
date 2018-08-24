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

  def _isStrike(self, frameCounter):
    return self.frameScores[frameCounter]['tries'][0] == constants.MAX_PINS

  def _isSpare(self, frameCounter):
    tries = self.frameScores[frameCounter]['tries']
    return tries[0] + tries[1] == constants.MAX_PINS

  def _validPinsKnocked(self, pinsKnocked):
    if not pinsKnocked.isdigit():
      return False, 'Pins knocked should be a number.'

    pins = int(pinsKnocked)
    if pins < 0 or pins > 10:
      return False, 'Pins knocked should be positive number, less than 10.'

    frameTries = self.frameScores[self.frameCounter]['tries']
    if self.frameCounter == constants.TOTAL_FRAMES - 1:
      if not self._isStrike(self.frameCounter) and (
          self.roll == 1 and frameTries[0] + pins > constants.MAX_PINS):
        return False, constants.INVALID_SECOND_ROLL.format(
            firstRollPins=frameTries[0])
      else:
        return True, ''

    if self.roll == 1 and frameTries[0] + pins > constants.MAX_PINS:
      return False, constants.INVALID_SECOND_ROLL.format(
          firstRollPins=frameTries[0])

    return True, ''

  def _updateBonusScore(self, currentFrame):
    """Updates bonus score for last to last frame.

    Like bonus for frame-0 will be added to score once frame-2 has completed
    because there may be cases where multiple strikes can be made in sequence so
    next to next pins knocked will be required to calculate current bonus."""

    if currentFrame < 2:
      return None

    previousFrameId = currentFrame - 2
    if not (self._isStrike(previousFrameId) or self._isSpare(previousFrameId)):
      return None

    bonus1 = self.frameScores[previousFrameId + 1]['tries'][0]
    bonus2 = 0
    if self._isStrike(previousFrameId):
      bonus2 = self.frameScores[previousFrameId + 1]['tries'][1]
      if self._isStrike(previousFrameId + 1):
        bonus2 = self.frameScores[previousFrameId + 2]['tries'][0]
    self.frameScores[previousFrameId]['score'] += bonus1 + bonus2

    # If reached at last frame, update bonus score for second last also.
    if currentFrame == constants.TOTAL_FRAMES - 1:
      bonus1 = 0
      bonus2 = 0
      if self._isStrike(currentFrame - 1):
        bonus1 = self.frameScores[currentFrame]['tries'][0]
        bonus2 = self.frameScores[currentFrame]['tries'][1]
      elif self._isSpare(previousFrameId):
        bonus1 = self.frameScores[currentFrame]['tries'][0]
      self.frameScores[currentFrame - 1]['score'] += bonus1 + bonus2

  def _updateScore(self, pinsKnocked):
    currentFrame = self.frameCounter
    self.frameScores[self.frameCounter]['tries'][self.roll] = pinsKnocked
    self.frameScores[self.frameCounter]['score'] += pinsKnocked

    # If strike or spare in last frame.
    if self.frameCounter == constants.TOTAL_FRAMES - 1:
      if not self.roll or (self.roll < 2 and (
          self._isStrike(self.frameCounter) or
          self._isSpare(self.frameCounter))):
        self.roll += 1
      else:
        self.frameCounter += 1
    elif not (self.roll or self._isStrike(self.frameCounter)):
      self.roll += 1
    else:
      self.roll = 0
      self.frameCounter += 1

    # Updating bonus scores for previous strike and spare frames if frame has
    # changed after this role.
    if currentFrame != self.frameCounter:
      self._updateBonusScore(currentFrame)

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
