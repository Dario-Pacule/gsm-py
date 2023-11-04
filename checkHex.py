def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
