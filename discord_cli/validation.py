import re
import discord_cli.exceptions as exceptions

def validate_string(string):
    if not isinstance(string, str):
        raise exceptions.Type_Error('expected str instance, {} found'.format(string.__class__.__name__))
    if len(string) == 0:
        raise exceptions.Value_Error('must not have 0 length')

def validate_command_name(string):
    validate_string(string)
    if re.match('.*[^a-zA-Z_].*', string):
        raise exceptions.Value_Error('must only contain letters and underscores')

def validate_word(string):
    validate_string(string)
    if re.match('.*[^a-zA-Z].*', string):
        raise exceptions.Value_Error('must only contain letters')

def validate_integer(string):
    validate_string(string)
    if re.match('.*[^0-9].*', string):
        raise exceptions.Value_Error('must only contain digits')

def validate_letter(string):
    validate_word(string)
    if len(string) > 1:
        raise exceptions.Value_Error('must have length 1')

def validate_bounds(value, min, max, include_min, inlucde_max):
    if min is not None:
        if include_min == False and result <= min:
            raise exceptions.Value_Error('must be greater than {}'.format(min))
        if result < min:
            raise exceptions.Value_Error('cannot be less than {}'.format(min))
    
    if max is not None:
        if include_max == False and result >= max:
            raise exceptions.Value_Error('must be less than {}'.format(min))
        if result > max:
            raise exceptions.Value_Error('cannot be greater than {}'.format(max))