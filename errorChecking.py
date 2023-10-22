def isNumeric(*args) -> bool:
    for arg in args:
        if not arg.isnumeric():
            return False
    return True