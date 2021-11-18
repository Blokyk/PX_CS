from typing import List, Optional

def letter_to_idx(letter: str) -> int:
    return ord(letter.upper()) - 0x41

def idx_to_letter(idx: int) -> str:
    assert(0 <= idx <= 9)
    return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J'][idx]