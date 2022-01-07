from typing_utils import GameBoard, Position


def is_king_move_valid(old_pos: Position, new_pos: Position) -> bool:
    return abs(old_pos.line - new_pos.line) <= 1 and abs(old_pos.column - new_pos.column) <= 1

def is_queen_move_valid(old_pos: Position, new_pos: Position) -> bool:
    return is_tower_move_valid(old_pos, new_pos) or is_bishop_move_valid(old_pos, new_pos)

def is_tower_move_valid(old_pos: Position, new_pos: Position) -> bool:
    return old_pos.line == new_pos.line or old_pos.column == new_pos.column

def is_bishop_move_valid(old_pos: Position, new_pos: Position) -> bool:
    return abs(old_pos.line/(old_pos.column+1)) == abs(new_pos.line/(new_pos.column+1))

def is_knight_move_valid(old_pos: Position, new_pos: Position) -> bool:
    return (abs(old_pos.line - new_pos.line), abs(old_pos.column - new_pos.column)) in [ (2, 1), (1, 2) ]

def is_pawn_move_valid(old_pos: Position, new_pos: Position, color: str, is_first_round: bool = False) -> bool:
    if old_pos.column != new_pos.column:
        return False

    line_offset = old_pos.line - new_pos.line

    if is_first_round:
        line_offset /= 2

    if color == 'B':
        return 0 <= line_offset <= 1
    else:
        return 1 >= line_offset >= 0
