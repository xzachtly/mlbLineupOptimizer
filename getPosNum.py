# Assigns numerical values to position abbreviations
def getPosNum(name):
    return {
        'SP': 0,
        'RP': 0,
        'P': 0,
        'SP, RP': 0,
        'C': 1,
        'C/OF': 1,
        '1B': 2,
        '1B/OF': 2,
        '1B/3B': 2,
        '1B/C': 2,
        '1B/2B': 2,
        '2B': 3,
        '2B/3B': 3,
        '2B/SS': 3,
        '2B/OF': 3,
        '2B/C': 3,
        '3B': 4,
        '3B/SS': 4,
        '3B/OF': 4,
        '3B/C': 4,
        'SS': 5,
        'OF': 6,
        'OF/SS': 6
    }[name]