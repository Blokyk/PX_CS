if __name__ != '__main__':
    raise ImportError("main.py should never be imported !")

from typing import List
from board_utils import print_board, print_side_by_side_boards
from game_board import GameBoard

from ships import ShipPart, get_size
from utils import format_error, format_pos_and_angle, letter_to_idx
from main_utils import *

boards = [init_board(10, 10), init_board(10, 10)]

for board in boards:
   for part in map(lambda l: ShipPart(l), ['P', 'C', 'R', 'S', 'T']):
       print("Where do you want to put your" + str(part) + "(" + str(get_size(part)) + " spaces) ?")

       pos = enter_position(board)
       ori = enter_orientation()

       while not board.can_insert_ship_at(part, ori, pos[0], pos[1]):
           print("You can't put a ship there !", end='')

           if (board[pos[0]][pos[1]] != ' '):
               print("There's already a" + str(board[pos[0]][pos[1]]) + "!", end='')

           print()

           pos = enter_position(board)
           ori = enter_orientation()

       board.insert_ship_at(part, ori, pos[0], pos[1])
       print_board(board)
       #print("Successfully inserted" + str(part) + "@ " + format_pos_and_angle(pos[0], pos[1], ori))

# boards[0].insert_boat_at(ShipPart('C'), 'H', 6 - 1, 6 - 1)
# boards[0].insert_boat_at(ShipPart('C'), 'V', 5 - 1, 1 - 1)

# boards[1].insert_boat_at(ShipPart('P'), 'V', 2 - 1, 3 - 1)

print_side_by_side_boards(boards)