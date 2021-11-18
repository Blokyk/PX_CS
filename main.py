from typing import List
from board_utils import print_board, print_side_by_side_boards
from game_board import GameBoard

from ships import ShipPart, get_size
from utils import format_error, format_pos_and_angle, letter_to_idx

boards: List[GameBoard] = [GameBoard(), GameBoard()]

def init_board(column: int, rows: int) -> GameBoard:
    board = GameBoard()

    for line in range(column):
        board.append([]) # create empty line
        for _ in range(rows):
            board[line].append(ShipPart(' ')) # fill line with empty spaces

    return board

if __name__ != '__main__':
    raise ImportError("main.py should never be imported !")

boards[0] = init_board(10, 10)
boards[1] = init_board(10, 10)

def enter_position() -> List[int]:
    def decode(pos: str) -> List[int]:
        return [int(pos.split(' ')[0]) - 1, letter_to_idx(pos.split(' ')[1].upper())]

    output = input("Position (1-10, A-J) : [line] [column]\n\t")

    pos = decode(output)

    while not (len(output.split()) == 2 and boards[0].is_on_board(pos[0], pos[1])):
        print(format_error('Invalid position'))
        output = input("Position (1-10, A-J) : [line] [column]\n\t")
        pos = decode(output)

    return decode(output)

def enter_orientation() -> str:
    output = ''

    def is_valid_position_str(orientation: str):
        return orientation in ['H', 'V']

    while not is_valid_position_str(output := input("Orientation : H or V\n\t").upper()):
        print(format_error('Invalid orientation'))

    return output

for board in boards:
   for l in ['P', 'C', 'R', 'S', 'T']:
       part = ShipPart(l)
       print("Where do you want to put your" + str(part) + "(" + str(get_size(part)) + " spaces) ?")
       pos = enter_position()
       ori = enter_orientation()
       while not board.can_insert_ship_at(part, ori, pos[0], pos[1]):
           print("You can't put a ship there !", end='')
           if (board[pos[0]][pos[1]] != ' '):
               print("There's already a" + str(board[pos[0]][pos[1]]) + "!", end='')
           print()
           pos = enter_position()
           ori = enter_orientation()
       board.insert_ship_at(part, ori, pos[0], pos[1])
       print_board(board)
       #print("Successfully inserted" + str(part) + "@ " + format_pos_and_angle(pos[0], pos[1], ori))

# boards[0].insert_boat_at(ShipPart('C'), 'H', 6 - 1, 6 - 1)
# boards[0].insert_boat_at(ShipPart('C'), 'V', 5 - 1, 1 - 1)

# boards[1].insert_boat_at(ShipPart('P'), 'V', 2 - 1, 3 - 1)

print_side_by_side_boards(boards)