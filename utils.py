from typing import List, Optional

def letter_to_idx(letter: str) -> int:
    return ord(letter.upper()) - 0x41