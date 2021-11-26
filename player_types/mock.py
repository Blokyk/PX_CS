from random import randint

from player_types.base import Player

class MockPlayer(Player):
    """A player that just tries random spots"""

    def get_next_action(self):
        return (randint(0, 9), randint(0, 9))