import re

def validate_string(string):
    if not isinstance(string, str):
        raise TypeError
    if len(string) == 0:
        raise ValueError

def validate_word(string):
    validate_string(string)
    if re.match('.*[^a-zA-Z].*', string):
        raise ValueError

def validate_integer(string):
    validate_string(string)
    if re.match('.*[^0-9].*', string):
        raise ValueError

def validate_bounds(value, min, max, include_min, inlucde_max):
    if min is not None:
        if result < min:
            return False
        if include_min == False and result == min:
            return False
    
    if max is not None:
        if result > max:
            return False
        if include_max == False and result == max:
            return False
    
    return True