"""Contains unit test cases for game_manager.py."""

import unittest

from game_manager import GameManager
from utils import constants


class GameManagerTest(unittest.TestCase):
  """Unit tests for game manager module."""

  def setUp(self):
    self.game = GameManager()
    self.game.frameCounter = 0
    self.game.frameScores = None
    self.game.roll = 0
    self.maxDiff = None

  def testGetScore(self):
    """Verifies that score is fetched in expected format when is ongoing."""

    # Case 1: Game is not started yet, should return error message.
    self.assertEqual(
      self.game.getScore(), {'message': constants.GAME_NOT_STARTED})

    # Case 2: No pins knocked, should return initial score.
    self.game.startNewGame()
    frameScores = {
      frameId: {
        'roll': {
          0: -1,
          1: -1
        },
        'score': -1
      }
      for frameId in range(constants.TOTAL_FRAMES)
    }
    expectedRsp = {'frame-scores': frameScores, 'total-score': 0}
    self.assertEqual(self.game.getScore(), expectedRsp)

  def testPinsKnockedNegative(self):
    """Verifies that if pins knocked is invalid, error message is returned."""

    # Case 1: Game not started, should return relevant error message.
    self.assertEqual(self.game.pinsKnocked('5'),
                     {'message': constants.PINS_KNOCKED_BEFORE_GAME_STARTED})

    self.game.startNewGame()

    # Case 2: Pins knocked is not number, should return relevant error.
    self.assertEqual(
      self.game.pinsKnocked('a'), {'message': constants.INVALID_PINS_KNOCKED})

    # Case 3: Pins knocked more than 10, should return relevant error.
    self.assertEqual(
      self.game.pinsKnocked('20'), {'message': constants.INVALID_PINS_KNOCKED})

    # Case 4: Sum of pins knocked in first and second roll exceeds 10.
    roll1 = '8'
    roll2 = '5'
    self.assertEqual(
      self.game.pinsKnocked(roll1), {'message': constants.SCORES_UPDATED})

    self.assertEqual(
      self.game.pinsKnocked(roll2), {
        'message': constants.INVALID_SECOND_ROLL.format(firstRollPins=roll1)
      })

    # Case 5: Pins knocked received when game has ended, should ask for
    # starting new game.
    self.game.startNewGame()
    for roll in range(2*constants.TOTAL_FRAMES):
      self.assertEqual(
        self.game.pinsKnocked('1'), {'message': constants.SCORES_UPDATED})

    self.assertEqual(
      self.game.pinsKnocked('1'), {'message': constants.GAME_ENDED})

  def testPinsKnockedAllStrikes(self):
    """Verifies perfect 300 case."""

    self.game.startNewGame()
    for roll in range(constants.TOTAL_FRAMES + 2):  # Last frame has 3 rolls
      self.assertEqual(
        self.game.pinsKnocked('10'), {'message': constants.SCORES_UPDATED})

    # Verify score after all strikes.
    scores = {}
    for frame in range(constants.TOTAL_FRAMES - 1):
      scores[frame] = {'roll': {0: 10, 1: -1}, 'score': 30}

    # Update score for last frame.
    scores[constants.TOTAL_FRAMES - 1] = {
      'roll': {0: 10, 1: 10, 2: 10},
      'score': 30
    }

    self.assertEqual(self.game.getScore(),
                     {'frame-scores': scores, 'total-score': 300})

  def testPinsKnockedAllSpares(self):
    """Verifies case when all frames knocked with a spare."""

    self.game.startNewGame()
    for roll in range(2*constants.TOTAL_FRAMES + 1):  # Last frame has 3 rolls
      self.assertEqual(
        self.game.pinsKnocked('5'), {'message': constants.SCORES_UPDATED})

    # Verify score after all spares.
    scores = {}
    for frame in range(constants.TOTAL_FRAMES - 1):
      scores[frame] = {'roll': {0: 5, 1: 5}, 'score': 15}

    # Update score for last frame.
    scores[constants.TOTAL_FRAMES - 1] = {
      'roll': {0: 5, 1: 5, 2: 5},
      'score': 15
    }

    self.assertEqual(self.game.getScore(),
                     {'frame-scores': scores, 'total-score': 150})

  def testPinsKnockedNormal(self):
    """Verifies case when no frame is knocked with a strike or spare."""

    self.game.startNewGame()
    for roll in range(2*constants.TOTAL_FRAMES):
      self.assertEqual(
        self.game.pinsKnocked('4'), {'message': constants.SCORES_UPDATED})

    scores = {}
    for frame in range(constants.TOTAL_FRAMES):
      scores[frame] = {'roll': {0: 4, 1: 4}, 'score': 8}

    self.assertEqual(self.game.getScore(),
                     {'frame-scores': scores, 'total-score': 80})


if __name__ == '__main__':
    unittest.main()
