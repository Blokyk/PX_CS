from typing_utils import GameBoard, Position

def get_position_of_piece(piece: str, board: GameBoard) -> Position:
    for line_number in range(len(board)):
        for col_number, p in enumerate(board[line_number]):
            if p == piece:
                return Position(line_number, col_number)

    return Position(-1, -1)
