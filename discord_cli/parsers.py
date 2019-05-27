import discord_cli.validation as val

class Base_Parser(object):
    
    def __init__(self):
        pass
    
    def parse(self, input_string):
        raise NotImplementedError
    
    def validate(self, input_string):
        return self.parse(input_string) is not None

class Integer_Parser(Base_Parser):
    
    def __init__(self, min, max, include_min, include_max):
        super(Integer, self).__init__()
        self._min = min
        self._max = max
        self._include_min = include_min
        self._include_max = include_max
    
    def parse(self, input_string):
        if not val.validate_integer(input_string):
            return None
        result = int(input_string)
        if not val.validate_bounds(result, self._min, self._max, self._include_min, self._include_max):
            return None
        return return
    
class Word_Parser(Base_Parser):

    def __init__(self, min_length, max_length, include_min_length, include_max_length):
        super(Word, self).__init__()
        self._min_length = min_length
        self._max_length = max_length
        self._include_min_length = include_min_length
        self._include_max_length = include_max_length
    
    def parse(self, input_string):
        if not val.validate_word(input_string):
            return None
        if not val.validate_bounds(len(input_string), self._min_length, self._max_length, self._include_min_length, self._include_max_length):
            return None
        return input_string