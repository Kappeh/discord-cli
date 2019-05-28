import discord_cli.parsers as parsers
import discord_cli.validation as validation

class Option(object):
    
    def __init__(self, name, description, letter, word, parser):
        if not validation.validate_word(name):
            raise ValueError
        if description is not None and not validation.validate_string(description):
            raise ValueError

        if letter is None:
            letter = name[0]
        elif not validation.validate_letter(letter):
            raise ValueError

        if word is not None and not validation.validate_word(word):
            raise ValueError

        self._name = name
        self._description = description
        self._letter = letter
        self._word = word

        self._parser = parser
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def letter(self):
        return self._letter
    
    @property
    def word(self):
        return self._word
    
    def parse(self, input_string):
        return self._parser.parse(input_string)

class Option_Builder(object):
    
    def __init__(self, command):
        self._command = command
        
        self._options = []
        self._option_count = 0
    
    def _add_option(self, option):
        self._options.append(option)
        self._option_count += 1
    
    def integer(self, name, description = None, letter = None, word = None, min = None, max = None, include_min = True, include_max = False):
        self._add_option(Option(name, description, letter, word, parsers.Integer_Parser(min, max, include_min, include_max)))
    
    def word(self, name, description = None, letter = None, word = None, min_length = None, max_length = None, include_min_length = True, include_max_length = False):
        self._add_option(Option(name, description, letter, word, parsers.Word_Parser(min_length, max_length, include_min_length, include_max_length)))
    
    @property
    def options(self):
        return self._options
    
    @property
    def option_count(self):
        return self._option_count