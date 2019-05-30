import discord_cli.validation as validation
import discord_cli.exceptions as exceptions

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

        validation.validate_integer(input_string)
        result = int(input_string)
        validation.validate_bounds(result, self._min, self._max, self._include_min, self._include_max)
        return result
    
class Word_Parser(Base_Parser):

    def __init__(self, min_length, max_length, include_min_length, include_max_length):
        super(Word_Parser, self).__init__()
        self._min_length = min_length
        self._max_length = max_length
        self._include_min_length = include_min_length
        self._include_max_length = include_max_length
    
    async def parse(self, input_string):
        validation.validate_word(input_string)
        try:
            validation.validate_bounds(len(input_string), self._min_length, self._max_length, self._include_min_length, self._include_max_length)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('length {}'.format(str(e)))
        return input_string