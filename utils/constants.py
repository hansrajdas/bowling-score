"""Contains constants and success/error strings."""

TOTAL_FRAMES = 10
MAX_PINS = 10

SCORES_UPDATED = 'Scores updated for this move.'

# Error messages
GAME_NOT_STARTED = 'Please start game before fetching score.'

PINS_KNOCKED_BEFORE_GAME_STARTED = 'Please start game before this operation.'

INVALID_PINS_KNOCKED = 'Pins knocked should be positive number, less than 10.'

INVALID_SECOND_ROLL = ('Sum of pins knocked in first roll and second roll '
                       'cannot be more than 10, {first_roll_pins} pins were '
                       'knocked in first roll.')
GAME_ENDED = ('Game is over, all rolls done for this game. Please check score '
              'and start a new game.')
