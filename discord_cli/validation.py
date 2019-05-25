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