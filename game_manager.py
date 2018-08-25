"""Contains class and all methods required to manager bowling score."""

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
    self.frameScores = {
      frameId: {
        'roll': {
          0: -1,
          1: -1
        },
        'score': -1
      }
      for frameId in range(constants.TOTAL_FRAMES)
    }
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
    """Checks if given frame counter was strike or not.

    Args:
      frameCounter: Frame counter, 0 to 9.

    Returns: True or False.
    """
    return self.frameScores[frameCounter]['roll'][0] == constants.MAX_PINS

  def _isSpare(self, frameCounter):
    """Checks if given frame counter was spare or not.

    Args:
      frameCounter: Frame counter, 0 to 9.

    Returns: True or False.
    """
    roll = self.frameScores[frameCounter]['roll']
    return roll[0] + roll[1] == constants.MAX_PINS

  def validPinsKnocked(self, pinsKnocked):
    """Validates if pins knocked received is correct or not.

    This also validates based to rolls, this is first, second or
    third(in case of last frame) roll.

    Args:
      pinsKnocked: Number of pins knocked.

    Returns: True, if pinks knocked is valid else False with error message.
    """
    if not pinsKnocked.isdigit():
      return False, constants.INVALID_PINS_KNOCKED

    pins = int(pinsKnocked)
    if pins < 0 or pins > constants.MAX_PINS:
      return False, constants.INVALID_PINS_KNOCKED

    frameTries = self.frameScores[self.frameCounter]['roll']
    if self.frameCounter == constants.TOTAL_FRAMES - 1:
      if not self._isStrike(self.frameCounter) and (
          self.roll == 1 and frameTries[0] + pins > constants.MAX_PINS):
        return False, constants.INVALID_SECOND_ROLL.format(
            firstRollPins=frameTries[0])
      else:
        return True, ''

    if self.roll and frameTries[0] + pins > constants.MAX_PINS:
      return False, constants.INVALID_SECOND_ROLL.format(
          firstRollPins=frameTries[0])

    return True, ''

  def updateScore(self, currentFrame, roll):
    """Updates score for current frame.

    Also updates score for previous frames if pending for this roll.

    Args:
      currentFrame: Current frame, frame for which roll is made.
      roll: Roll count, 0 or 1. Can be 2 also but only when currentFrame is 9.
    """

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
        previousData['score'] = constants.MAX_PINS + bonus1
      else:
        # If previous was an strike hit, it might be possible that previous to
        # previous was also strike and score not set.
        if currentFrame > 1:
          data = self.frameScores[currentFrame - 2]
          if data['score'] == -1:
            data['score'] = 20 + bonus1  # Double strike case.

        # Update previous frame's score.
        if roll:
          previousData['score'] = constants.MAX_PINS + bonus1 + bonus2

    # If its last frame and all roles are made, we just have to add pins knocked
    # in all (3 for strike and spare and 2 for normal) rolls made.
    if currentFrame == constants.TOTAL_FRAMES - 1 and (not self.roll):
      frameData['score'] = sum(frameData['roll'][r] for r in frameData['roll'])

  def updatePinsAndScore(self, pinsKnocked):
    """Updates pins knocked and score for a frame.

    Also tracks next roll will be in same frame or next frame (in case there is
    strike in this frame).

    Args:
      pinsKnocked: Number of pins knocked.
    """
    currentFrame = self.frameCounter
    roll = self.roll
    self.frameScores[self.frameCounter]['roll'][self.roll] = pinsKnocked

    if self.frameCounter == constants.TOTAL_FRAMES - 1:
      # If strike or spare in last frame, there would be 3 rolls.
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
    """Updates score when a new pin is knocked.

    Args:
      pinsKnocked: Number of pins knocked in a particular roll.

    Returns: Dictionary with success string or required error string in case of
      some error.
    """
    if self.frameScores is None:
      return {'message': constants.PINS_KNOCKED_BEFORE_GAME_STARTED}

    if self.frameCounter == constants.TOTAL_FRAMES:
      return {'message': constants.GAME_ENDED}

    status, errorMsg = self.validPinsKnocked(pinsKnocked)
    if not status:
      return {'message': errorMsg}

    self.updatePinsAndScore(int(pinsKnocked))
    return {'message': constants.SCORES_UPDATED}
