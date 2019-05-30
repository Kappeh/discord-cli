import discord_cli.parsers as parsers
import discord_cli.exceptions as exceptions
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
    
    async def parse(self, input_string):
        result = self._parser.parse(input_string)
        if result is None:
            return exceptions.Invalid_Option_Error()
        return result

class Option_Builder(object):
    
    def __init__(self, command):
        self._command = command
        
        self._options = []
        self._name_table = {}
        self._letter_table = {}
        self._word_table = {}
        self._option_count = 0
    
    def _add_option(self, option):
        if option.name in self._name_table:
            raise ValueError
        if option.letter in self._letter_table:
            raise ValueError
        if option.word in self._word_table:
            raise ValueError

        if option.name in self._command._argument_builder.name_table:
            raise ValueError
        if option.name in self._command._tag_builder.name_table:
            raise ValueError
        if option.letter in self._command._tag_builder.letter_table:
            raise ValueError
        if option.word in self._command._tag_builder.word_table:
            raise ValueError

        self._options.append(option)
        self._name_table[option.name] = option
        self._letter_table[option.letter] = option
        if option.word is not None:
            self._word_table[option.word] = option

        self._option_count += 1
    
    def integer(self, name, description = None, letter = None, word = None, min = None, max = None, include_min = True, include_max = False):
        self._add_option(Option(name, description, letter, word, parsers.Integer_Parser(min, max, include_min, include_max)))
    
    def word(self, name, description = None, letter = None, word = None, min_length = None, max_length = None, include_min_length = True, include_max_length = False):
        self._add_option(Option(name, description, letter, word, parsers.Word_Parser(min_length, max_length, include_min_length, include_max_length)))
    
    @property
    def options(self):
        return self._options
    
    @property
    def name_table(self):
        return self._name_table

    @property
    def letter_table(self):
        return self._letter_table
    
    @property
    def word_table(self):
        return self._word_table

    @property
    def option_count(self):
        return self._option_count