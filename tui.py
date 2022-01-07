
from typing import AnyStr, List
from typing_utils import T, GameBoard, Position

import move_utils
from board_utils import get_position_of_piece

def __get_separator_for_str(text: str) -> str:
    return '  ' + '—'*len(text)

def print_game_board(board: GameBoard) -> None:

    for (number, line) in enumerate(board):
        line_str = format_line(line)
        print(__get_separator_for_str(line_str))
        print(str(number + 1) + ' ' + line_str)

    print(__get_separator_for_str(format_line(board[0])))

def format_line(board_line: List[str]) -> str:
    output = ''

    output += '| '

    output += ' | '.join(board_line)

    output += ' |'

    return output

def input_position(player_suffix: str, board: GameBoard, round: int) -> Position:
    piece = input("Enter the piece you want to move :\n\t")

    def ask_new_pos() -> Position:
        pos_arr = input("Enter the new position :\n\t").split(' ')
        return Position(int(pos_arr[0]), int(pos_arr[1]))

    while not is_move_valid(piece + player_suffix, get_position_of_piece(piece + player_suffix, board), new_pos := ask_new_pos(), round):
        continue

    return new_pos

def is_move_valid(piece: str, old_pos: Position, new_pos: Position, round: int) -> bool:
    if new_pos == old_pos:
        return False

    if new_pos.line < 0 or new_pos.column < 0:
        return False

    if old_pos.line < 0 or old_pos.column < 0:
        return False


    if 'RO' in piece or 'RE' in piece: # pesky exceptions >:(
        piece_type = piece
    else:
        piece_type = piece[0]

    if 'P' in piece: # peskier exception >>>>:(
        color = piece[-1]
        return move_utils.is_pawn_move_valid(old_pos, new_pos, color, round == 1)

    return {
        'RO': move_utils.is_king_move_valid,
        'RE': move_utils.is_queen_move_valid,
        'T':  move_utils.is_tower_move_valid,
        'F':  move_utils.is_bishop_move_valid,
        'C':  move_utils.is_knight_move_valid,
        # no need for pawns, we already took care of that
    }[piece_type](old_pos, new_pos)