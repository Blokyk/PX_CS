from typing import List, Optional, Tuple

def letter_to_idx(letter: str) -> int:
    """Convert a (case-insensitive) letter into an index based on its ascii position, with A => 0, B => 1, ...
    """
    return ord(letter.upper()) - 0x41

def idx_to_letter(idx: int) -> str:
    """Convert a column index into its letter/human-readable form, with 0 => A, 1 => B, ...
    """
    return chr(idx + 0x41)

def format_pos_and_angle(line: int, col: int, angle: str):
    return angle + '(' + str(line + 1) + ', ' + idx_to_letter(col) + ')'

def format_hit(hit: Tuple[int, int]):
    return '(' + str(hit[0] + 1) + ', ' + idx_to_letter(hit[1]) + ')'

def format_error(text: str) -> str:
    """Adds ANSI sequence for red color to the text
    """
    return '\033[31;1;4m' + text + '\033[0m'

def debug(text):
    if False: return print(text)
    else: return None