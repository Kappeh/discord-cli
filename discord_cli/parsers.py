import discord_cli.validation as validation
import discord_cli.exceptions as exceptions

from datetime import datetime

class Base_Parser(object):
    
    def __init__(self):
        pass
    
    async def parse(self, input_string):
        raise NotImplementedError

class Integer_Parser(Base_Parser):
    
    def __init__(self, min, max, include_min, include_max):
        super(Integer_Parser, self).__init__()
        self._min = min
        self._max = max
        self._include_min = include_min
        self._include_max = include_max
    
    async def parse(self, input_string):

        await validation.async_validate_integer(input_string)
        result = int(input_string)
        await validation.async_validate_bounds(result, self._min, self._max, self._include_min, self._include_max)
        return result
    
class Word_Parser(Base_Parser):

    def __init__(self, min_length, max_length, include_min_length, include_max_length):
        super(Word_Parser, self).__init__()
        self._min_length = min_length
        self._max_length = max_length
        self._include_min_length = include_min_length
        self._include_max_length = include_max_length
    
    async def parse(self, input_string):
        await validation.async_validate_word(input_string)
        try:
            await validation.async_validate_bounds(len(input_string), self._min_length, self._max_length, self._include_min_length, self._include_max_length)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('length {}'.format(str(e)))
        return input_string

# Float
class Float_Parser(Base_Parser):

    def __init__(self, min, max, include_min, include_max):
        super(Float_Parser, self).__init__()
        self._min = min
        self._max = max
        self._include_min = include_min
        self._include_max = include_max
    
    async def parse(self, input_string):
        await validation.async_validate_float(input_string)
        result = float(input_string)
        await validation.async_validate_bounds(result, self._min, self._max, self._include_min, self._include_max)
        return result

# String
class String_Parser(Base_Parser):

    def __init__(self, min_length, max_length, include_min_length, include_max_length):
        super(String_Parser, self).__init__()
        self._min_length = min_length
        self._max_length = max_length
        self._include_min_length = include_min_length
        self._include_max_length = include_max_length
    
    async def parse(self, input_string):
        await validation.async_validate_string(input_string)
        try:
            await validation.async_validate_bounds(len(input_string), self._min_length, self._max_length, self._include_min_length, self._include_max_length)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('length {}'.format(str(e)))
        return input_string

# User Mention
# Without nickname      <@95584437231689728>
# With nickname         <@!95584437231689728>
class User_Mention_Parser(Base_Parser):

    def __init__(self):
        super(User_Mention_Parser, self).__init__()
    
    async def parse(self, input_string):
        await validation.async_validate_user_mention(input_string)
        for c in '<@!>':
            input_string = input_string.replace(c, '')
        return int(input_string)

# Channel Mention
# <#291649024409468928>

class Channel_Mention_Parser(Base_Parser):

    def __init__(self):
        super(Channel_Mention_Parser, self).__init__()
    
    async def parse(self, input_string):
        await validation.async_validate_channel_mention(input_string)
        for c in '<#>':
            input_string = input_string.replace(c, '')
        return int(input_string)

# Role Mention
# <@&357235474869387276>
class Role_Mention_Parser(Base_Parser):

    def __init__(self):
        super(Role_Mention_Parser, self).__init__()
    
    async def parse(self, input_string):
        await validation.async_validate_role_mention(input_string)
        for c in '<@&>':
            input_string = input_string.replace(c, '')
        return int(input_string)

# Date
# In the format %d/%m/%Y for now, may become customizable in future
class Date_Parser(Base_Parser):
    
    def __init__(self, min, max, include_min, include_max):
        super(Date_Parser, self).__init__()
        self._min = min
        self._max = max
        self._include_min = include_min
        self._include_max = include_max
    
    async def parse(self, input_string):
        await validation.async_validate_date(input_string)
        result = datetime.strptime(input_string, '%d/%m/%Y')
        await validation.async_validate_bounds(result, self._min, self._max, self._include_min, self._include_max)
        return result

# Time
# In the format %H:%M:%S for now, may become customizable in future
class Time_Parser(Base_Parser):

    def __init__(self, min, max, include_min, include_max):
        super(Time_Parser, self).__init__()
        self._min = min
        self._max = max
        self._include_min = include_min
        self._include_max = include_max
    
    async def parse(self, input_string):
        await validation.async_validate_time(input_string)
        result = datetime.strptime(input_string, '%H:%M:%S')
        await validation.async_validate_bounds(result, self._min, self._max, self._include_min, self._include_max)
        return result

# Enum
class Enum_Parser(Base_Parser):

    def __init__(self, values):
        super(Enum_Parser, self).__init__()
        if not isinstance(values, list):
            raise exceptions.Type_Error('Enum values expected list instance, {} found'.format(values.__class__.__name__))
        if len(values) == 0:
            raise exceptions.Value_Error('Enum values must not have length 0')
        try:
            for string in values:
                validation.validate_word(string)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Enum values elements ' + str(e))
        self._values = values
    
    async def parse(self, input_string):
        await validation.async_validate_string(input_string)
        if input_string not in self._values:
            raise exceptions.Value_Error('must be element in {}'.format(str(self._values)))
        return input_string