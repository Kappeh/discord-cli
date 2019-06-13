import discord_cli.parsers as parsers
import discord_cli.exceptions as exceptions
import discord_cli.validation as validation

class Option(object):

    """
    This class represents a single option for a command.
    An option is an optional parameter for a command.

    Options have a name, an optional description, a datatype,
    a letter and an optional word.

    The letter and word are identifiers used to specify the option
    within the command string.
    """
    
    def __init__(self, name, description, letter, word, parser):
        """
        If letter is None, the first letter of the name
        is used instead.

        name            : str                               - The name of the option
        description     : str | None                        - A description of the option
        letter          : str | None                        - The letter identifier for the option (If None, set to the first letter of the name)
        word            : str | None                        - The word identifier of the option
        parser          : discord_cli.parsers.Base_Parser   - The parser used to parse this option

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

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
        """
        Returns : str - The name of the option
        """
        return self._name
    
    @property
    def description(self):
        """
        Returns : str | None - A description of the option
        """
        return self._description
    
    @property
    def letter(self):
        """
        Returns : str - The letter identifier for the option
        """
        return self._letter
    
    @property
    def word(self):
        """
        Returns : str | None - The word identifier of the option
        """
        return self._word
    
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
        E.g. 'index:integer | -i | --index | The index of the record to display'
        """

        elements = ['{}:{}'.format(self._name, str(self._parser)), '-' + self._letter]
        if self._word is not None:
            elements.append('--' + self._word)
        if self._description is not None:
            elements.append(self._description)
        return ' | '.join(elements)

class Option_Builder(object):
    
    """
    An option builder is used to create and store an array of options
    that belong to a command.

    This class is referenced by the discord_cli.command.Command class
    after construction for parsing command strings ready to be executed.
    """

    def __init__(self, command):
        """
        command : discord_cli.command.Command - The command the option builder belongs to
        """

        self._command = command
        
        self._options = []
        self._name_table = {}
        self._letter_table = {}
        self._word_table = {}
        self._option_count = 0
    
    def _add_option(self, option):
        """
        Adds an option into the array of options

        option : discord_cli.option_builder.Option - The option to be added
        """

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
        """
        Adds an integer option into the array of options

        name        : str           - The name of the integer option
        description : str | None    - A description of the integer option
        letter      : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word        : str | None    - The word identifier of the option
        min         : int | None    - The lower bound of valid input
        max         : int | None    - The upper bound of valid input
        include_min : bool          - Whether to include the minimum value as valid
        include_max : bool          - Whether to include the maximum value as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_option(Option(name, description, letter, word, parsers.Integer_Parser(min, max, include_min, include_max)))
    
    def word(self, name, description = None, letter = None, word = None, min_length = None, max_length = None, include_min_length = True, include_max_length = False):
        """
        Adds a word option into the array of options

        name                : str           - The name of the word option
        description         : str | None    - A description of the word option
        letter              : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word                : str | None    - The word identifier of the option
        min_length          : int | None    - The lower bound of valid input length
        max_length          : int | None    - The upper bound of valid input length
        include_min_length  : bool          - Whether to inlucde the minimum length as valid
        include_max_length  : bool          - Whether to include the maximum length as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """


        self._add_option(Option(name, description, letter, word, parsers.Word_Parser(min_length, max_length, include_min_length, include_max_length)))
    
    def float(self, name, description = None, letter = None, word = None, min = None, max = None, include_min = True, include_max = False):
        """
        Adds an float option into the array of options

        name        : str           - The name of the float option
        description : str | None    - A description of the float option
        letter      : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word        : str | None    - The word identifier of the option
        min         : int | None    - The lower bound of valid input
        max         : int | None    - The upper bound of valid input
        include_min : bool          - Whether to include the minimum value as valid
        include_max : bool          - Whether to include the maximum value as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_option(Option(name, description, letter, word, parsers.Float_Parser(min, max, include_min, include_max)))

    def string(self, name, description = None, letter = None, word = None, min_length = None, max_length = None, include_min_length = True, include_max_length = False):
        """
        Adds a string option into the array of options

        name                : str           - The name of the string option
        description         : str | None    - A description of the string option
        letter              : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word                : str | None    - The word identifier of the option
        min_length          : int | None    - The lower bound of valid input length
        max_length          : int | None    - The upper bound of valid input length
        include_min_length  : bool          - Whether to inlucde the minimum length as valid
        include_max_length  : bool          - Whether to include the maximum length as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_option(Option(name, description, letter, word, parsers.String_Parser(min_length, max_length, include_min_length, include_max_length)))

    def user_mention(self, name, description = None, letter = None, word = None):
        """
        Adds a user mention option into the array of options

        name        : str           - The name of the user mention option
        description : str | None    - A description of the user mention option
        letter      : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word        : str | None    - The word identifier for the option

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """
        self._add_option(Option(name, description, letter, word, parsers.User_Mention_Parser()))

    def channel_mention(self, name, description = None, letter = None, word = None):
        """
        Adds a channel mention option into the array of options

        name        : str           - The name of the channel mention option
        description : str | None    - A description of the channel mention option
        letter      : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word        : str | None    - The word identifier for the option

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_option(Option(name, description, letter, word, parsers.Channel_Mention_Parser()))

    def role_mention(self, name, description = None, letter = None, word = None):
        """
        Adds a role mention option into the array of options

        name        : str           - The name of the role mention option
        description : str | None    - A description of the role mention option
        letter      : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word        : str | None    - The word identifier for the option

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_option(Option(name, description, letter, word, parsers.Role_Mention_Parser()))
    
    def date(self, name, description = None, letter = None, word = None, min = None, max = None, include_min = True, include_max = False):
        """
        Adds an date option into the array of options

        name        : str           - The name of the date option
        description : str | None    - A description of the date option
        letter      : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word        : str | None    - The word identifier of the option
        min         : str | None    - The lower bound of valid input in form '%d/%m/%Y'
        max         : str | None    - The upper bound of valid input in form '%d/%m/%Y'
        include_min : bool          - Whether to include the minimum value as valid
        include_max : bool          - Whether to include the maximum value as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_option(Option(name, description, letter, word, parsers.Date_Parser(min, max, include_min, include_max)))
    
    def time(self, name, description = None, letter = None, word = None, min = None, max = None, include_min = True, include_max = False):
        """
        Adds an time option into the array of options

        name        : str           - The name of the time option
        description : str | None    - A description of the time option
        letter      : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word        : str | None    - The word identifier of the option
        min         : str | None    - The lower bound of valid input in form '%H:%M:%S'
        max         : str | None    - The upper bound of valid input in form '%H:%M:%S'
        include_min : bool          - Whether to include the minimum value as valid
        include_max : bool          - Whether to include the maximum value as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_option(Option(name, description, letter, word, parsers.Time_Parser(min, max, include_min, include_max)))

    def enum(self, name, values, description = None, letter = None, word = None):
        """
        Adds an enum option into the array of options

        name            : str           - The name of the enum option
        values          : list          - A list of valid strings
        description     : str | None    - A description of the enum option
        letter          : str | None    - The letter identifier for the option (If None, set to the first letter of the name) 
        word            : str | None    - The word identifier of the option

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._add_option(Option(name, description, letter, word, parsers.Enum_Parser(values)))

    @property
    def options(self):
        """
        Returns : list - A list of the options
        """
        
        return self._options
    
    @property
    def name_table(self):
        """
        Returns : dict - A table which associates each name to an option with that name
        """
        
        return self._name_table

    @property
    def letter_table(self):
        """
        Returns : dict - A table which associates each letter identifier to an option with that letter identifier
        """

        return self._letter_table
    
    @property
    def word_table(self):
        """
        Returns : dict - A table which associates each word identifier to an option with that word identifier
        """

        return self._word_table

    @property
    def option_count(self):
        """
        Returns : int - The amound of options in the array
        """

        return self._option_count