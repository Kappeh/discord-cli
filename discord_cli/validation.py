import re
import discord_cli.exceptions as exceptions

def validate_string(string):
    """
    Checks if the input is a string of non-zero length

    string  : str   - The string to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if string is not of the correct format
    """

    if not isinstance(string, str):
        raise exceptions.Type_Error('expected str instance, {} found'.format(string.__class__.__name__))
    if len(string) == 0:
        raise exceptions.Value_Error('must not have 0 length')

def validate_command_name(string):
    """
    Checks if the input is a string of non-zero length that contains only letters and underscores

    string  : str   - The string to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if string is not of the correct format
    """

    validate_string(string)
    if re.match('.*[^a-zA-Z_].*', string):
        raise exceptions.Value_Error('must only contain letters and underscores')

def validate_word(string):
    """
    Checks if the input is a string of non-zero length that contains only letters

    string  : str   - The string to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if string is not of the correct format
    """

    validate_string(string)
    if re.match('.*[^a-zA-Z].*', string):
        raise exceptions.Value_Error('must represent a word')

def validate_float(obj):
    """
    Checks if the input can be converted to a float

    obj : object    - The object to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if object cannot be converted to a float
    """

    try:
        float(obj)
    except ValueError:
        raise exceptions.Value_Error('must represent a float')

def validate_integer(obj):
    """
    Checks if the input can be converted to a integer

    string  : object    - The object to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if object cannot be converted to a integer
    """
    
    try:
        int(obj)
    except ValueError:
        raise exceptions.Value_Error('must represent an integer')

def validate_letter(string):
    """
    Checks if the input is a string of length 1 that contains only letters

    string  : str   - The string to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if string is not of the correct format
    """

    validate_word(string)
    if len(string) != 1:
        raise exceptions.Value_Error('must have length 1')

def validate_bounds(value, min, max, include_min, include_max):
    """
    Checks if a value lies within an interval defined by a min and a max

    min         : object    - The lower bound of the interval (if None, assumed to be negative infinity)
    max         : object    - The upper bound of the interval (if None, assumed to be positive infinity)
    include_min : object    - Whether the lower bound is not a strict inequality
    include_max : object    - Whether the upper bound is not a strict inequality

    Raises discord_cli.exceptions.Discord_CLI_Error if the value lies outside the interval
    """

    if min is not None:
        if include_min == False and value <= min:
            raise exceptions.Value_Error('must be greater than {}'.format(min))
        if value < min:
            raise exceptions.Value_Error('cannot be less than {}'.format(min))
    
    if max is not None:
        if include_max == False and value >= max:
            raise exceptions.Value_Error('must be less than {}'.format(max))
        if value > max:
            raise exceptions.Value_Error('cannot be greater than {}'.format(max))

def validate_user_mention(string):
    """
    Checks if the input is a string that represents a discord user mention

    string  : str   - The string to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if string is not of the correct format
    """

    validate_string(string)
    if not re.match('<@!?\d+>', string):
        raise exceptions.Value_Error('must represent a user mention')

def validate_channel_mention(string):
    """
    Checks if the input is a string that represents a discord channel mention

    string  : str   - The string to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if string is not of the correct format
    """

    validate_string(string)
    if not re.match('<#\d+>', string):
        raise exceptions.Value_Error('must represent a channel mention')

def validate_role_mention(string):
    """
    Checks if the input is a string that represents a discord role mention

    string  : str   - The string to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if string is not of the correct format
    """
    
    validate_string(string)
    if not re.match('<@&\d+>', string):
        raise exceptions.Value_Error('must represent a role mention')

def validate_date(string):
    """
    Checks if the input is a string that represents a date in the form '%d/%m/%Y'

    string  : str   - The string to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if string is not of the correct format
    """

    validate_string(string)
    if not re.match('\d\d/\d\d/\d\d', string):
        raise exceptions.Value_Error('must represent a date')

def validate_time(string):
    """
    Checks if the input is a string that represents a time in the form '%H:%M:%S'

    string  : str   - The string to be checked

    Raises discord_cli.exceptions.Discord_CLI_Error if string is not of the correct format
    """

    validate_string(string)
    if not re.match('\d\d:\d\d:\d\d', string):
        raise exceptions.Value_Error('must represent a time')

"""
Async counterparts =============================================================================================

All of the methods below do exactly the same thing as their sync equivilent except are defined as corroutines
so that they can be called during the command execution process without having to start a new thread.
"""

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
        raise exceptions.Value_Error('must represent a word')

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
        raise exceptions.Value_Error('must represent an integer')

async def async_validate_letter(string):
    await async_validate_word(string)
    if len(string) > 1:
        raise exceptions.Value_Error('must have length 1')

async def async_validate_bounds(value, min, max, include_min, include_max):
    if min is not None:
        if include_min == False and value <= min:
            raise exceptions.Value_Error('must be greater than {}'.format(min))
        if value < min:
            raise exceptions.Value_Error('cannot be less than {}'.format(min))
    
    if max is not None:
        if include_max == False and value >= max:
            raise exceptions.Value_Error('must be less than {}'.format(max))
        if value > max:
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