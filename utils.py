from typing import List, Optional

def letter_to_idx(letter: str) -> int:
    """Convert a (case-insensitive) letter into an index based on its ascii position, with A => 0, B => 1"""
    return ord(letter.upper()) - 0x41

def idx_to_letter(idx: int) -> str:
    """Convert a column index into its letter/human-readable form"""
    assert(0 <= idx <= 9)
    return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'][idx]

def format_pos_and_angle(line: int, col: int, angle: str):
    return angle + '(' + str(line + 1) + ', ' + idx_to_letter(col) + ')'

def format_error(text: str) -> str:
    return '\033[31;1;4m' + text + '\033[0m'

def debug(text):
    if False: return print(text)
    else: return None