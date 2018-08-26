"""Contains class and all methods required to manager bowling score."""

from utils import constants
from utils import singleton


@singleton.singleton
class GameManager(object):
    """Manages score of bowling game."""
    def __init__(self):
        """Initialises object."""
        self.frame_scores = None  # Holds per frame pins knocked and score.
        self.frame_counter = 0  # Would be 0 to 9.
        self.roll = 0  # 0 or 1, 2 in case last frame is kncoked with strike.

    def start_new_game(self):
        """Initialises all object variables to starts a new game.

        Returns: Dictionary with success message string.
        """
        self.frame_counter = 0
        self.roll = 0
        self.frame_scores = {
          frame_id: {
            'roll': {
              0: -1,
              1: -1
            },
            'score': -1
          }
          for frame_id in range(constants.TOTAL_FRAMES)
        }
        return {'message': 'New game started successfully.'}

    def get_score(self):
        """Returns total score and per frame score if game is ongoing.

        Returns: Dictionary with error message if game is not started otherwise
          total and per frame score.
        """
        if self.frame_scores is None:
            return {'message': constants.GAME_NOT_STARTED}

        total_score = sum(self.frame_scores[frame]['score']
                          for frame in self.frame_scores
                          if self.frame_scores[frame]['score'] != -1)

        return {'frame-scores': self.frame_scores, 'total-score': total_score}

    def _is_strike(self, frame_counter):
        """Checks if given frame counter was strike or not.

        Args:
          frame_counter: Frame counter, 0 to 9.

        Returns: True or False.
        """
        return self.frame_scores[
          frame_counter]['roll'][0] == constants.MAX_PINS

    def _is_spare(self, frame_counter):
        """Checks if given frame counter was spare or not.

        Args:
          frame_counter: Frame counter, 0 to 9.

        Returns: True or False.
        """
        roll = self.frame_scores[frame_counter]['roll']
        return roll[0] + roll[1] == constants.MAX_PINS

    def _valid_pins_knocked(self, pins_knocked):
        """Validates if pins knocked received is correct or not.

        This also validates based to rolls, this is first, second or
        third(in case of last frame) roll.

        Args:
          pins_knocked: Number of pins knocked.

        Returns: True, if pinks knocked is valid else False with error message.
        """
        if not pins_knocked.isdigit():
            return False, constants.INVALID_PINS_KNOCKED

        pins = int(pins_knocked)
        if pins < 0 or pins > constants.MAX_PINS:
            return False, constants.INVALID_PINS_KNOCKED

        frame_tries = self.frame_scores[self.frame_counter]['roll']
        if self.frame_counter == constants.TOTAL_FRAMES - 1:
            if not self._is_strike(self.frame_counter) and (
               self.roll == 1 and frame_tries[0] + pins > constants.MAX_PINS):
                return False, constants.INVALID_SECOND_ROLL.format(
                  first_roll_pins=frame_tries[0])
            else:
                return True, ''

        if self.roll and (frame_tries[0] + pins) > constants.MAX_PINS:
            return False, constants.INVALID_SECOND_ROLL.format(
              first_roll_pins=frame_tries[0])

        return True, ''

    def _update_score(self, current_frame, roll):
        """Updates score for current frame.

        Also updates score for previous frames if pending for this roll.

        Args:
          current_frame: Current frame, frame for which roll is made.
          roll: Roll count, 0 or 1. Can be 2 also but only when current_frame
            is 9.
        """
        frame_data = self.frame_scores[current_frame]

        # Update score for current frame if both rolls are done and its not a
        # spare.
        is_strike = self._is_strike(current_frame)
        is_spare = self._is_spare(current_frame)
        if roll and not (is_spare or is_strike):
            frame_data['score'] = frame_data['roll'][0] + frame_data['roll'][1]

        # If this is the first frame, no need to check for previous frames.
        if current_frame < 1:
            return None

        # If previous frame scores are not updated as they were strike or
        # spare, then update those using pins knocked in current frame rolls.
        previous_data = self.frame_scores[current_frame - 1]
        if previous_data['score'] == -1:
            bonus_1 = frame_data['roll'][0]
            bonus_2 = frame_data['roll'][1]
            if self._is_spare(current_frame - 1):
                previous_data['score'] = constants.MAX_PINS + bonus_1
            else:
                # If previous was an strike hit, it might be possible that
                # previous to previous was also strike and score not set.
                if current_frame > 1:
                    data = self.frame_scores[current_frame - 2]
                    if data['score'] == -1:
                        data['score'] = 20 + bonus_1  # Double strike case.

                # Update previous frame's score.
                if roll:
                    previous_data['score'] = (constants.MAX_PINS + bonus_1 +
                                              bonus_2)

        # If its last frame and all roles are made, we just have to add
        # pins knocked in all (3 for strike and spare and 2 for normal)
        # rolls made.
        if current_frame == constants.TOTAL_FRAMES - 1 and (roll == 2):
            frame_data['score'] = sum(
              frame_data['roll'][r] for r in frame_data['roll'])

    def _update_pins_and_score(self, pins_knocked):
        """Updates pins knocked and score for a frame.

        Also tracks next roll will be in same frame or next frame (in case
        there is strike in this frame).

        Args:
          pins_knocked: Number of pins knocked.
        """
        current_frame = self.frame_counter
        roll = self.roll
        self.frame_scores[self.frame_counter]['roll'][self.roll] = pins_knocked

        if self.frame_counter == constants.TOTAL_FRAMES - 1:
            # If strike or spare in last frame, there would be 3 rolls.
            if not self.roll or (self.roll < 2 and (
               self._is_strike(self.frame_counter) or
               self._is_spare(self.frame_counter))):
                self.roll += 1
            else:
                self.roll = 0
                self.frame_counter += 1
        elif not (self.roll or self._is_strike(self.frame_counter)):
            self.roll += 1
        else:
            self.roll = 0
            self.frame_counter += 1

        self._update_score(current_frame, roll)

    def pins_knocked(self, pins_knocked):
        """Updates score when a new pin is knocked.

        Args:
          pins_knocked: Number of pins knocked in a particular roll.

        Returns: Dictionary with success string or required error string in
          case of some error.
        """
        if self.frame_scores is None:
            return {'message': constants.PINS_KNOCKED_BEFORE_GAME_STARTED}

        if self.frame_counter == constants.TOTAL_FRAMES:
            return {'message': constants.GAME_ENDED}

        status, error_msg = self._valid_pins_knocked(pins_knocked)
        if not status:
            return {'message': error_msg}

        self._update_pins_and_score(int(pins_knocked))
        return {'message': constants.SCORES_UPDATED}
