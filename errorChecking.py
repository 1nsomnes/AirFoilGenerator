def isNumeric(*args) -> bool:
    for arg in args:
        try:
            float(arg)
        except ValueError:
            return False
    return True