from enum import Enum

def get_size(ship: str) -> int:
        return {
            ' ': 0,
            'T': 2,
            'S': 3,
            'R': 3,
            'C': 4,
            'P': 5
        }[ship]
