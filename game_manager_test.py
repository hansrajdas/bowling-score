"""Contains unit test cases for game_manager.py."""

import unittest

from game_manager import GameManager
from utils import constants


class GameManagerTest(unittest.TestCase):
    """Unit tests for game manager module."""

    def setUp(self):
        """Initialises all test cases."""
        self.game = GameManager()
        self.game.frame_counter = 0
        self.game.frame_scores = None
        self.game.roll = 0
        self.maxDiff = None

    def test_get_score(self):
        """Verifies, score is fetched in expected format when is ongoing.

        And if game has not started yet, error string should be returned."""

        # Case 1: Game is not started yet, should return error message.
        self.assertEqual(self.game.get_score(),
                         {'message': constants.GAME_NOT_STARTED})

        # Case 2: No pins knocked, should return initial score.
        self.game.start_new_game()
        frame_scores = {
          frame_id: {
            'roll': {
              0: -1,
              1: -1
            },
            'score': -1
          }
          for frame_id in range(constants.TOTAL_FRAMES)
        }
        expected_rsp = {'frame-scores': frame_scores, 'total-score': 0}
        self.assertEqual(self.game.get_score(), expected_rsp)

    def test_pins_knocked_negative(self):
        """Verifies that if pins knocked is invalid, error is returned."""

        # Case 1: Game not started, should return relevant error message.
        self.assertEqual(
          self.game.pins_knocked('5'),
          {'message': constants.PINS_KNOCKED_BEFORE_GAME_STARTED})

        self.game.start_new_game()

        # Case 2: Pins knocked is not number, should return relevant error.
        self.assertEqual(self.game.pins_knocked('a'),
                         {'message': constants.INVALID_PINS_KNOCKED})

        # Case 3: Pins knocked more than 10, should return relevant error.
        self.assertEqual(self.game.pins_knocked('20'),
                         {'message': constants.INVALID_PINS_KNOCKED})

        # Case 4: Sum of pins knocked in first and second roll exceeds 10.
        roll1 = '8'
        roll2 = '5'
        self.assertEqual(self.game.pins_knocked(roll1),
                         {'message': constants.SCORES_UPDATED})

        err_msg = constants.INVALID_SECOND_ROLL.format(first_roll_pins=roll1)
        self.assertEqual(self.game.pins_knocked(roll2), {'message': err_msg})

        # Case 5: Pins knocked received when game has ended, should ask for
        # starting new game.
        self.game.start_new_game()
        for roll in range(2*constants.TOTAL_FRAMES):
            self.assertEqual(self.game.pins_knocked('1'),
                             {'message': constants.SCORES_UPDATED})

        self.assertEqual(self.game.pins_knocked('1'),
                         {'message': constants.GAME_ENDED})

    def test_pins_knocked_all_strikes(self):
        """Verifies perfect 300 case."""

        self.game.start_new_game()
        # Last frame has 3 rolls so +2.
        for roll in range(constants.TOTAL_FRAMES + 2):
            self.assertEqual(self.game.pins_knocked('10'),
                             {'message': constants.SCORES_UPDATED})

        # Verify score after all strikes.
        scores = {}
        for frame in range(constants.TOTAL_FRAMES - 1):
            scores[frame] = {'roll': {0: 10, 1: -1}, 'score': 30}

        # Update score for last frame.
        scores[constants.TOTAL_FRAMES - 1] = {
          'roll': {0: 10, 1: 10, 2: 10},
          'score': 30
        }

        self.assertEqual(self.game.get_score(),
                         {'frame-scores': scores, 'total-score': 300})

    def test_pins_knocked_all_spares(self):
        """Verifies case when all frames knocked with a spare."""

        self.game.start_new_game()
        # Last frame has 3 rolls so +1.
        for roll in range(2*constants.TOTAL_FRAMES + 1):
            self.assertEqual(self.game.pins_knocked('5'),
                             {'message': constants.SCORES_UPDATED})

        # Verify score after all spares.
        scores = {}
        for frame in range(constants.TOTAL_FRAMES - 1):
            scores[frame] = {'roll': {0: 5, 1: 5}, 'score': 15}

        # Update score for last frame.
        scores[constants.TOTAL_FRAMES - 1] = {
          'roll': {0: 5, 1: 5, 2: 5},
          'score': 15
        }

        self.assertEqual(self.game.get_score(),
                         {'frame-scores': scores, 'total-score': 150})

    def test_pins_knocked_normal(self):
        """Verifies case when no frame is knocked with a strike or spare."""

        self.game.start_new_game()
        for roll in range(2*constants.TOTAL_FRAMES):
            self.assertEqual(self.game.pins_knocked('4'),
                             {'message': constants.SCORES_UPDATED})

        scores = {}
        for frame in range(constants.TOTAL_FRAMES):
            scores[frame] = {'roll': {0: 4, 1: 4}, 'score': 8}

        self.assertEqual(self.game.get_score(),
                         {'frame-scores': scores, 'total-score': 80})


if __name__ == '__main__':
    unittest.main()
