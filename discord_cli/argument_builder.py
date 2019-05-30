import discord_cli.parsers as parsers
import discord_cli.exceptions as exceptions
import discord_cli.validation as validation

class Argument(object):

    def __init__(self, name, description, parser):
        if not validation.validate_word(name):
            raise ValueError
        if description is not None and not validation.validate_string(description):
            raise ValueError

        self._name = name
        self._description = description

        self._parser = parser
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    async def parse(self, input_string):
        result = self._parser.parse(input_string)
        if result is None:
            return exceptions.Invalid_Argument_Error()
        return result
    
class Argument_Builder(object):

    def __init__(self, command):
        self._command = command
        self._name_table = {}
        self._arguments = []
        self._argument_count = 0

        self._first_is_text = False
    
    def _add_argument(self, argument):
        if argument.name in self._command._option_builder.name_table:
            raise ValueError
        if argument.name in self._command._tag_builder.name_table:
            raise ValueError

        self._arguments.append(argument)
        self._name_table[argument.name] = argument
        self._argument_count += 1

    def integer(self, name, description = None, min = None, max = None, include_min = None, include_max = None):
        self._add_argument(Argument(name, description, parsers.Integer_Parser(min, max, include_min, include_max)))
    
    def word(self, name, description = None, min_length = None, max_length = None, include_min_length = True, include_max_length = False):
        if self._command.sub_command_count != 0:
            raise exceptions.Ambiguous_Parameter_Error
        if self._argument_count == 0:
            self._first_is_text = True
        self._add_argument(Argument(name, description, parsers.Word_Parser(min_length, max_length, include_min_length, include_max_length)))
    
    @property
    def arguments(self):
        return self._arguments
    
    @property
    def argument_count(self):
        return self._argument_count
    
    @property
    def name_table(self):
        return self._name_table
    
    @property
    def first_is_text(self):
        return self._first_is_text