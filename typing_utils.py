from typing import List, Tuple, TypeVar


T = TypeVar('T')
GameBoard = List[List[str]]


class Position():
    def __init__(self, line: int, column: int) -> None:
        super().__init__()
        self.line = line
        self.column = column