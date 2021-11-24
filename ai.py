from typing import List, Tuple

def gen_pattern_for(size: int) -> List[Tuple[int, int]]:
    output = []

    mod_counter = 0

    for line in range(10):
        for col in range(10):
            if col % size == mod_counter:
                output.append((line, col))

        mod_counter += 1
        mod_counter %= size

    # for line in range(10):
    #     for offset in range(line % size, 10):
    #         if (line + offset - 1 > 10):
    #             break
    #         if ((offset-1) % size == 0):
    #             output.append((line, line + offset - 1))
    return output

min_quadrants: List[List[Tuple[int, int]]] = [gen_pattern_for(i) for i in [2, 4]]