def remove_leading_zeros(val: str):
    return val.lstrip("0")


def parse_unicode_characters(val: str):
    if isinstance(val, str):
        return val.encode().decode()
    return val
