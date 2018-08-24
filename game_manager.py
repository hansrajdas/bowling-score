import collections

from utils import constants
from utils import singleton

@singleton.singleton
class GameManager(object):
  """Manages score of bowling game."""

  def __init__(self):
    """Initialises object."""
    self.frameScores = None  # Hold pins knocked and score scored in each frame.
    self.frameCounter = 0  # Would be 0 to 9.
    self.roll = 0  # 0 or 1

  def startNewGame(self):
    """Initialises all object variables to starts a new game.

    Returns: Dictionary with success message string.
    """
    self.frameCounter = 0
    self.roll = 0
    self.frameScores = collections.OrderedDict([
        (frameId, {'roll': {0: -1, 1: -1}, 'score': -1})
        for frameId in range(constants.TOTAL_FRAMES)
    ])
    return {'message': 'New game started successfully.'}

  def getScore(self):
    """Returns total score and per frame score if game is ongoing.

    Returns: Dictionary with error message if game is not started otherwise
      total and per frame score.
    """
    if self.frameScores is None:
      return {'message': constants.GAME_NOT_STARTED}

    totalScore = sum(self.frameScores[frame]['score']
                     for frame in self.frameScores
                     if self.frameScores[frame]['score'] != -1)

    return {'frame-scores': self.frameScores, 'total-score': totalScore}

  def _isStrike(self, frameCounter):
    return self.frameScores[frameCounter]['roll'][0] == constants.MAX_PINS

  def _isSpare(self, frameCounter):
    roll = self.frameScores[frameCounter]['roll']
    return roll[0] + roll[1] == constants.MAX_PINS

  def validPinsKnocked(self, pinsKnocked):
    if not pinsKnocked.isdigit():
      return False, 'Pins knocked should be a number.'

    pins = int(pinsKnocked)
    if pins < 0 or pins > 10:
      return False, 'Pins knocked should be positive number, less than 10.'

    frameTries = self.frameScores[self.frameCounter]['roll']
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

  def updateScore(self, currentFrame, roll):
    """...."""

    frameData = self.frameScores[currentFrame]

    # Update score for current frame if both rolls are done its not a spare.
    isStrike = self._isStrike(currentFrame)
    isSpare = self._isSpare(currentFrame)
    if roll and not (isSpare or isStrike):
      frameData['score'] = frameData['roll'][0] + frameData['roll'][1]

    # If this is the first frame, no need to check for previous frames.
    if currentFrame < 1:
      return None

    # If previous frame scores are not updated as they were strike or spare,
    # then update those using pins knocked in current frame rolls.
    previousData = self.frameScores[currentFrame - 1]
    if previousData['score'] == -1:
      bonus1 = frameData['roll'][0]
      bonus2 = frameData['roll'][1]
      if self._isSpare(currentFrame - 1):
        previousData['score'] = 10 + bonus1
      else:
        # If previous was an strike hit, it might be possible that previous to
        # previous was also strike and score not set.
        if currentFrame > 1:
          data = self.frameScores[currentFrame - 2]
          if data['score'] == -1:
            data['score'] = 10 + 10 + bonus1

        # Update previous frame's score.
        if roll:
          previousData['score'] = 10 + bonus1 + bonus2

    # If its last frame and all roles are made, we just have to add pins knocked
    # in all (3 for strike and spare and 2 for normal) rolls made.
    if currentFrame == constants.TOTAL_FRAMES - 1 and (not self.roll):
      frameData['score'] = sum(frameData['roll'][r] for r in frameData['roll'])

  def updatePinsAndScore(self, pinsKnocked):
    currentFrame = self.frameCounter
    roll = self.roll
    self.frameScores[self.frameCounter]['roll'][self.roll] = pinsKnocked

    # If strike or spare in last frame.
    if self.frameCounter == constants.TOTAL_FRAMES - 1:
      if not self.roll or (self.roll < 2 and (
          self._isStrike(self.frameCounter) or
          self._isSpare(self.frameCounter))):
        self.roll += 1
      else:
        self.roll = 0
        self.frameCounter += 1
    elif not (self.roll or self._isStrike(self.frameCounter)):
      self.roll += 1
    else:
      self.roll = 0
      self.frameCounter += 1

    self.updateScore(currentFrame, roll)

  def pinsKnocked(self, pinsKnocked):
    """Updates score when a new pin is knocked."""
    if self.frameScores is None:
      return {'message': 'Please start game before this operation.'}

    if self.frameCounter == constants.TOTAL_FRAMES:
      return {
          'message': ('All rolls done for this game, please check score and '
                      'start a new game.')
        }

    status, errorMsg = self.validPinsKnocked(pinsKnocked)
    if not status:
      return {'message': errorMsg}

    self.updatePinsAndScore(int(pinsKnocked))
    return {'message': 'Scores updated for this move.'}
