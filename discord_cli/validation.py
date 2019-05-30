import re

def validate_string(string):
    if not isinstance(string, str):
        return False
    if len(string) == 0:
        return False
    return True

def validate_command_name(string):
    if not validate_string(string):
        return False
    if re.match('.*[^a-zA-Z_].*'):
        return False
    return True

def validate_word(string):
    if not validate_string(string):
        return False
    if re.match('.*[^a-zA-Z].*', string):
        return False
    return True

def validate_integer(string):
    if not validate_string(string):
        return False
    if re.match('.*[^0-9].*', string):
        return False
    return True

def validate_letter(string):
    if not validate_word(string):
        return False
    if len(string) > 1:
        return False
    return True

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