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

    # Should return error message as game is not started yet.
    self.assertEqual(
      self.game.getScore(), {'message': constants.GAME_NOT_STARTED})

    # Starting game and then fetching score.
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

if __name__ == '__main__':
    unittest.main()
