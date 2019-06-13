import discord_cli.parsers as parsers
import discord_cli.exceptions as exceptions
import discord_cli.validation as validation

class Argument(object):

    """
    This class represents a single argument for a command.
    An argument is a required parameter for a command.

    Arguments have a name, an optional description and a datatype.
    The datatype is determined by the parser which it is given.
    """

    def __init__(self, name, description, parser):
        """
        name        : str                               - The name of the argument
        description : str | None                        - A description of the argument
        parser      : discord_cli.parsers.Base_Parser   - The parser used to parse this argument

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        try:
            validation.validate_word(name)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Argument name {}'.format(str(e)))

        try:
            if description is not None:
                validation.validate_string(description)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Argument description {}'.format(str(e)))

        self._name = name
        self._description = description

        self._parser = parser
    
    @property
    def name(self):
        """
        Returns : str - The name of the argument
        """

        return self._name
    
    @property
    def description(self):
        """
        Returns : str | None - A description of the argument
        """
        
        return self._description
    
    async def parse(self, input_string):
        """
        Parses an input string into the datatype specified by the parser

        input_string    : str       - The string that represents the input for this argument
        Returns         : object    - The parsed version of input_string

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        return await self._parser.parse(input_string)
    
    def __str__(self):
        """
        Returns : str - A string representation of the argument
        E.g. 'index:integer | The index of the record to display'
        """

        elements = ['{}:{}'.format(self._name, str(self._parser))]
        if self._description is not None:
            elements.append(self._description)
        return ' | '.join(elements)
    
class Argument_Builder(object):

    """
    An argument builder is used to create and store an
    ordered array of arguments that belong to a command.

    This class is referenced by the discord_cli.command.Command class
    after construction for parsing command strings ready to be executed.
    """

    def __init__(self, command):
        """
        command : discord_cli.command.Command - The command the argument builder belongs to
        """

        self._command = command
        self._name_table = {}
        self._arguments = []
        self._argument_count = 0

        self._first_is_text = False
    
    def _add_argument(self, argument):
        """
        Adds an argument into the array of arguments

        argument : discord_cli.argument_builder.Argument - The argument to be added
        """

        if argument.name in self._command._option_builder.name_table:
            raise exceptions.Name_Already_In_Use_Error('Name \'{}\' is in use by an option'.format(name))
        if argument.name in self._command._tag_builder.name_table:
            raise exceptions.Name_Already_In_Use_Error('Name \'{}\' is in use by a tag'.format(name))

        self._arguments.append(argument)
        self._name_table[argument.name] = argument
        self._argument_count += 1

    def integer(self, name, description = None, min = None, max = None, include_min = True, include_max = False):
        """
        Adds an integer argument into the array of arguments

        name            : str           - The name of the integer argument
        description     : str | None    - A description of the integer argument
        min             : int | None    - The lower bound of valid input
        max             : int | None    - The upper bound of valid input
        include_min     : bool          - Whether to include the minimum value as valid
        include_max     : bool          - Whether to include the maximum value as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_argument(Argument(name, description, parsers.Integer_Parser(min, max, include_min, include_max)))
    
    def word(self, name, description = None, min_length = None, max_length = None, include_min_length = True, include_max_length = False):
        """
        Adds a word argument into the array of arguments

        name                    : str           - The name of the word argument
        description             : str | None    - A desscription of the word argument
        min_length              : int | None    - The lower bound of valid length
        max_length              : int | None    - The upper bound of valid length
        include_min_length      : bool          - Whether to include the minimum length as valid
        include_max_length      : bool          - Whether to include the maximum length as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """
        
        if self._command.sub_command_count != 0:
            raise exceptions.Ambiguous_Parameter_Error('Cannot add word argument to {} as it has sub commands'.format(self._command.command_string))
        if self._argument_count == 0:
            self._first_is_text = True
        self._add_argument(Argument(name, description, parsers.Word_Parser(min_length, max_length, include_min_length, include_max_length)))
    
    def float(self, name, description = None, min = None, max = None, include_min = True, include_max = False):
        """
        Adds a float argument into the array of arguments

        name            : str           - The name of the float argument
        description     : str | None    - A description of the float argument
        min             : int | None    - The lower bound of valid input
        max             : int | None    - The upper bound of valid input
        include_min     : bool          - Whether to include the minimum value as valid
        include_max     : bool          - Whether to include the maximum value as valid        

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_argument(Argument(name, description, parsers.Float_Parser(min, max, include_min, include_max)))

    def string(self, name, description = None, min_length = None, max_length = None, include_min_length = True, include_max_length = False):
        """
        Adds a string argument into the array of arguments

        name                    : str           - The name of the string argument
        description             : str | None    - A desscription of the string argument
        min_length              : int | None    - The lower bound of valid length
        max_length              : int | None    - The upper bound of valid length
        include_min_length      : bool          - Whether to include the minimum length as valid
        include_max_length      : bool          - Whether to include the maximum length as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        if self._command.sub_command_count != 0:
            raise exceptions.Ambiguous_Parameter_Error('Cannot add string argument to {} as it has sub commands'.format(self._command.command_string))
        if self._argument_count == 0:
            self._first_is_text = True
        self._add_argument(Argument(name, description, parsers.String_Parser(min_length, max_length, include_min_length, include_max_length)))

    def user_mention(self, name, description = None):
        """
        Adds a user mention argument into the array of arguments

        name        : str           - The name of the argument
        description : str | None    - A description of the string argument

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """
        self._add_argument(Argument(name, description, parsers.User_Mention_Parser()))

    def channel_mention(self, name, description = None):
        """
        Adds a channel mention argument into the array of arguments

        name        : str           - The name of the argument
        description : str | None    - A description of the string argument

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_argument(Argument(name, description, parsers.Channel_Mention_Parser()))

    def role_mention(self, name, description = None):
        """
        Adds a role mention argument into the array of arguments

        name        : str           - The name of the argument
        description : str | None    - A description of the string argument

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_argument(Argument(name, description, parsers.Role_Mention_Parser()))
    
    def date(self, name, description = None, min = None, max = None, include_min = True, include_max = False):
        """
        Adds a date argument into the array of arguments

        name            : str           - The name of the date argument
        description     : str | None    - A description of the date argument
        min             : str | None    - The lower bound of valid inputs in form '%d/%m/%Y'
        max             : str | None    - The upper bound of valid inputs in form '%d/%m/%Y'
        include_min     : bool          - Whether to include the minimum as valid
        include_max     : bool          - Whether to include the maximum as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_argument(Argument(name, description, parsers.Date_Parser(min, max, include_min, include_max)))
    
    def time(self, name, description = None, min = None, max = None, include_min = True, include_max = False):
        """
        Adds a time argument into the array of arguments

        name            : str           - The name of the time argument
        description     : str | None    - A description of the time argument
        min             : str | None    - The lower bound of valid inputs in form '%H:%M:%S'
        max             : str | None    - The upper bound of valid inputs in form '%H:%M:%S'
        include_min     : bool          - Whether to include the minimum as valid
        include_max     : bool          - Whether to include the maximum as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_argument(Argument(name, description, parsers.Time_Parser(min, max, include_min, include_max)))

    def enum(self, name, values, description = None):
        """
        Adds an enum argument into the array of arguments

        name            : str           - The name of the enum argument
        values          : list          - A list of valid strings
        description     : str | None    - A description of the enum argument

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        if self._command.sub_command_count != 0:
            raise exceptions.Ambiguous_Parameter_Error('Cannot add enum argument to {} as it has sub commands'.format(self._command.command_string))
        if self._argument_count == 0:
            self._first_is_text = True
        self._add_argument(Argument(name, description, parsers.Enum_Parser(values)))

    @property
    def arguments(self):
        """
        Returns : list - The array of arguments
        """
        
        return self._arguments
    
    @property
    def argument_count(self):
        """
        Returns : int - The amount of arguments in the array
        """

        return self._argument_count
    
    @property
    def name_table(self):
        """
        Returns : dict - A table which associates each name to an argument with that name
        """

        return self._name_table
    
    @property
    def first_is_text(self):
        """
        Returns : bool - Whether the first argument can be confused with a sub command
        """

        return self._first_is_text