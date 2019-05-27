from discord_cli.validation import (validate_string, validate_integer, validate_word)

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
        if not validate_integer(input_string):
            return None
        
        result = int(input_string)

        if self._min is not None:
            if result < self._min:
                return None
            if self._include_min == False and result == self._min:
                return None
        
        if self._max is not None:
            if result > self._max:
                return None
            if self._include_max == False and result == self._max:
                return None
        
        return int(input_string)
    
class Word_Parser(Base_Parser):

    def __init__(self, min_length, max_length, include_min_length, include_max_length):
        super(Word, self).__init__()
        self._min_length = min_length
        self._max_length = max_length
        self._include_min_length = include_min_length
        self._include_max_length = include_max_length
    
    def parse(self, input_string):
        if not validate_word(input_string):
            return None

        if self._min_length is not None:
            if len(input_string) < self._min_length:
                return None
            if self._include_min_length == False and len(input_string) == self._min_length:
                return None
        
        if self._max_length is not None:
            if len(input_string) > self._max_length:
                return None
            if self._include_max_length == False and len(input_string) == self._max_length:
                return None