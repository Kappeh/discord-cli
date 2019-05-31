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
        raise exceptions.Value_Error('must represent an integer')

def validate_float(string):
    validate_string(string)
    try:
        float(string)
    except ValueError:
        raise exceptions.Value_Error('must represent a float')

def validate_integer(string):
    validate_string(string)
    try:
        int(string)
    except ValueError:
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

def validate_user_mention(string):
    validate_string(string)
    if not re.match('<@!?\d+>', string):
        raise exceptions.Value_Error('must represent a user mention')

def validate_channel_mention(string):
    validate_string(string)
    if not re.match('<#\d+>', string):
        raise exceptions.Value_Error('must represent a channel mention')

def validate_role_mention(string):
    validate_string(string)
    if not re.match('<@&\d+>', string):
        raise exceptions.Value_Error('must represent a role mention')

def validate_date(string):
    validate_string(string)
    if not re.match('\d\d/\d\d/\d\d', string):
        raise exceptions.Value_Error('must represent a date')

def validate_time(string):
    validate_string(string)
    if not re.match('\d\d:\d\d:\d\d', string):
        raise exceptions.Value_Error('must represent a time')

def validate_date_time(string):
    validate_string(string)
    if not re.match('\d\d:\d\d:\d\d-\d\d/\d\d/\d\d\d\d', string):
        raise exceptions.Value_Error('must represent a datetime')

# Async counterparts

async def async_validate_string(string):
    if not isinstance(string, str):
        raise exceptions.Type_Error('expected str instance, {} found'.format(string.__class__.__name__))
    if len(string) == 0:
        raise exceptions.Value_Error('must not have 0 length')

async def async_validate_command_name(string):
    await async_validate_string(string)
    if re.match('.*[^a-zA-Z_].*', string):
        raise exceptions.Value_Error('must only contain letters and underscores')

async def async_validate_word(string):
    await async_validate_string(string)
    if re.match('.*[^a-zA-Z].*', string):
        raise exceptions.Value_Error('must represent an integer')

async def async_validate_float(string):
    await async_validate_string(string)
    try:
        float(string)
    except ValueError:
        raise exceptions.Value_Error('must represent a float')

async def async_validate_integer(string):
    await async_validate_string(string)
    try:
        int(string)
    except ValueError:
        raise exceptions.Value_Error('must only contain digits')

async def async_validate_letter(string):
    await async_validate_word(string)
    if len(string) > 1:
        raise exceptions.Value_Error('must have length 1')

async def async_validate_bounds(value, min, max, include_min, inlucde_max):
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

async def async_validate_user_mention(string):
    await async_validate_string(string)
    if not re.match('<@!?\d+>', string):
        raise exceptions.Value_Error('must represent a user mention')

async def async_validate_channel_mention(string):
    await async_validate_string(string)
    if not re.match('<#\d+>', string):
        raise exceptions.Value_Error('must represent a channel mention')

async def async_validate_role_mention(string):
    await async_validate_string(string)
    if not re.match('<@&\d+>', string):
        raise exceptions.Value_Error('must represent a role mention')

async def async_validate_date(string):
    await async_validate_string(string)
    if not re.match('\d\d/\d\d/\d\d', string):
        raise exceptions.Value_Error('must represent a date')

async def async_validate_time(string):
    await async_validate_string(string)
    if not re.match('\d\d:\d\d:\d\d', string):
        raise exceptions.Value_Error('must represent a time')

async def async_validate_date_time(string):
    await async_validate_string(string)
    if not re.match('\d\d:\d\d:\d\d-\d\d/\d\d/\d\d\d\d', string):
        raise exceptions.Value_Error('must represent a datetime')