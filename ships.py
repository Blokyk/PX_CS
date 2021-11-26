ship_types = ['P', 'C', 'R', 'S', 'T']

def get_size(ship_type: str) -> int:
    """Returns the number of spots taken by a boat of type `ship_type`
    """
    return {
        ' ': 0,
        'T': 2,
        'S': 3,
        'R': 3,
        'C': 4,
        'P': 5
    }[ship_type]
