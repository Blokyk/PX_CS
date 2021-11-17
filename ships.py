from enum import Enum

class ShipPart():
    value: str
    touched: bool

    def __init__(self, val: str) -> None:
        self.touched = False
        self.value = val

    def __str__(self) -> str:
        if self.touched:
            return '~' + self.value + '~'
        else:
            return ' ' + self.value + ' '

    def __repr__(self) -> str:
        return self.__str__()


def get_size(ship: ShipPart) -> int:
        return {
            ' ': 0,
            'T': 2,
            'S': 3,
            'R': 3,
            'C': 4,
            'P': 5
        }[ship.value]
