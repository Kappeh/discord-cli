import discord_cli.parsers as parsers
import discord_cli.exceptions as exceptions
import discord_cli.validation as validation

class Option(object):
    
    def __init__(self, name, description, letter, word, parser):
        
        try:
            validation.validate_word(name)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Option name {}'.format(str(e)))
        
        try:
            if description is not None:
                validation.validate_string(description)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Option description {}'.format(str(e)))

        if letter is None:
            letter = name[0]
        
        try:
            validation.validate_letter(letter)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Option letter {}'.format(str(e)))

        try:
            if word is not None:
                validation.validate_word(word)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Option word {}'.format(str(e)))

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
        return await self._parser.parse(input_string)

    def __str__(self):
        elements = ['{}:{}'.format(self._name, str(self._parser)), '-' + self._letter]
        if self._word is not None:
            elements.append('--' + self._word)
        if self._description is not None:
            elements.append(self._description)
        return ' | '.join(elements)

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
            raise exceptions.Name_Already_In_Use_Error('Name \'{}\' is in use by another option'.format(name))
        if option.letter in self._letter_table:
            raise exceptions.Letter_Already_In_Use_Error('Letter \'-{}\' is in use by another option'.format(letter))
        if option.word is not None and option.word in self._word_table:
            raise exceptions.Word_Already_In_Use_Error('Word \'--{}\' already in use by another option'.format(word))

        if option.name in self._command._argument_builder.name_table:
            raise exceptions.Name_Already_In_Use_Error('Name \'{}\' is in use by an argument'.format(name))
        if option.name in self._command._tag_builder.name_table:
            raise exceptions.Name_Already_In_Use_Error('Name \'{}\' is in use by a tag'.format(name))
        if option.letter in self._command._tag_builder.letter_table:
            raise exceptions.Letter_Already_In_Use_Error('Letter \'-{}\' is in use by a tag'.format(letter))
        if option.word in self._command._tag_builder.word_table:
            raise exceptions.Word_Already_In_Use_Error('Word \'--{}\' already in use by a tag'.format(word))

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
    
    def float(self, name, description = None, letter = None, word = None, min = None, max = None, include_min = True, include_max = False):
        self._add_option(Option(name, description, letter, word, parsers.Float_Parser(min, max, include_min, include_max)))

    def string(self, name, description = None, letter = None, word = None, min_length = None, max_length = None, include_min_length = True, include_max_length = False):
        self._add_option(Option(name, description, letter, word, parsers.String_Parser(min_length, max_length, include_min_length, include_max_length)))

    def user_mention(self, name, description = None, letter = None, word = None):
        self._add_option(Option(name, description, letter, word, parsers.User_Mention_Parser()))

    def channel_mention(self, name, description = None, letter = None, word = None):
        self._add_option(Option(name, description, letter, word, parsers.Channel_Mention_Parser()))

    def role_mention(self, name, description = None, letter = None, word = None):
        self._add_option(Option(name, description, letter, word, parsers.Role_Mention_Parser()))
    
    def date(self, name, description = None, letter = None, word = None, min = None, max = None, include_min = True, include_max = False):
        self._add_option(Option(name, description, letter, word, parsers.Date_Parser(min, max, include_min, include_max)))
    
    def time(self, name, description = None, letter = None, word = None, min = None, max = None, include_min = True, include_max = False):
        self._add_option(Option(name, description, letter, word, parsers.Time_Parser(min, max, include_min, include_max)))

    def enum(self, name, values, description = None, letter = None, word = None):
        self._add_option(Option(name, description, letter, word, parsers.Enum_Parser(values)))

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