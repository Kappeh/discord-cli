import discord_cli.validation as validation
import discord_cli.exceptions as exceptions

from datetime import datetime

class Base_Parser(object):
    
    """
    Base parser outlines the methods that have to be implimented in all other parsers.
    Each parser represents a datatype that is acceptable to use within the command line.
    Each parser takes a string input, validates it and parses it into the correct datatype.

    The base parser cannot be instanciated on it's own. It is an abstract class and parse
    if a pure virtual function.
    """

    def __init__(self):
        if self.__class__ == Base_Parser:
            raise exceptions.Cannot_Create_Instance_Of_Base_Class_Error('Cannot create instance of Base_Parser')
    
    async def parse(self, input_string):
        raise NotImplementedError

class Integer_Parser(Base_Parser):

    def __init__(self, min, max, include_min, include_max):
        """
        min         : int | None    - The lower bound of valid input
        max         : int | None    - The upper bound of valid input
        include_min : bool          - Whether to include the minumum as valid
        include_max : bool          - Whether to inlucde the maximum as valid

        raises discord_cli.exceptions.Discord_CLI_Error is inputs are not valid
        """

        super(Integer_Parser, self).__init__()

        if min is not None:
            try:
                validation.validate_integer(min)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('min {}'.format(str(e)))
            self._min = int(min)
        else:
            self._min = None
        
        if max is not None:
            try:
                validation.validate_integer(max)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('max {}'.format(str(e)))
            self._max = int(max)
        else:
            self._max = None

        if self._min is not None and self._max is not None and self._min > self._max:
            raise exceptions.Value_Error('min cannot be greater than max')

        if not isinstance(include_min, bool):
            raise exceptions.Type_Error('include_min expected bool instance, {} found'.format(include_min.__class__.__name__))
        if not isinstance(include_max, bool):
            raise exceptions.Type_Error('include_max expected bool instance, {} found'.format(include_max.__class__.__name__))

        self._include_min = include_min
        self._include_max = include_max
    
    async def parse(self, input_string):
        """
        Converts the input string into an integer

        input_string    : str   - The string to be converted to an integer
        Returns         : int   - The resulting parsed integer

        Raises discord_cli.exceptions.Discord_CLI_Error is input is invalid
        """

        await validation.async_validate_integer(input_string)
        result = int(input_string)
        await validation.async_validate_bounds(result, self._min, self._max, self._include_min, self._include_max)
        return result
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'integer'
    
class Word_Parser(Base_Parser):

    def __init__(self, min_length, max_length, include_min_length, include_max_length):
        """
        min_length          : int | None    - The lower bound of valid input length
        max_length          : int | None    - The upper bound of valid input length
        include_min_length  : bool          - Whether to include the minumum length as valid
        include_max_length  : bool          - Whether to inlucde the maximum length as valid

        raises discord_cli.exceptions.Discord_CLI_Error is inputs are not valid
        """

        super(Word_Parser, self).__init__()

        if min_length is not None:
            try:
                validation.validate_integer(min_length)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('min_length {}'.format(str(e)))
            self._min_length = int(min_length)
        else:
            self._min_length = None
        
        if max_length is not None:
            try:
                validation.validate_integer(max_length)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('max_length {}'.format(str(e)))
            self._max_length = int(max_length)
        else:
            self._max_length = None

        if self._min_length is not None and self._max_length is not None and self._min_length > self._max_length:
            raise exceptions.Value_Error('min_length cannot be greater than max_length')

        if not isinstance(include_min_length, bool):
            raise exceptions.Type_Error('include_min_length expected bool instance, {} found'.format(include_min_length.__class__.__name__))
        if not isinstance(include_max_length, bool):
            raise exceptions.Type_Error('include_max_length expected bool instance, {} found'.format(include_max_length.__class__.__name__))

        self._include_min_length = include_min_length
        self._include_max_length = include_max_length
    
    async def parse(self, input_string):
        """
        Converts the input string into an word

        input_string    : str   - The string to be converted to an word
        Returns         : str   - The resulting parsed word

        Raises discord_cli.exceptions.Discord_CLI_Error is input is invalid
        """

        await validation.async_validate_word(input_string)
        try:
            await validation.async_validate_bounds(len(input_string), self._min_length, self._max_length, self._include_min_length, self._include_max_length)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('length {}'.format(str(e)))
        return input_string
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'word'

# Float
class Float_Parser(Base_Parser):

    def __init__(self, min, max, include_min, include_max):
        """
        min         : int | None    - The lower bound of valid input
        max         : int | None    - The upper bound of valid input
        include_min : bool          - Whether to include the minumum as valid
        include_max : bool          - Whether to inlucde the maximum as valid

        raises discord_cli.exceptions.Discord_CLI_Error is inputs are not valid
        """

        super(Float_Parser, self).__init__()
        
        if min is not None:
            try:
                validation.validate_integer(min)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('min {}'.format(str(e)))
            self._min = int(min)
        else:
            self._min = None
        
        if max is not None:
            try:
                validation.validate_integer(max)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('max {}'.format(str(e)))
            self._max = int(max)
        else:
            self._max = None

        if self._min is not None and self._max is not None and self._min > self._max:
            raise exceptions.Value_Error('min cannot be greater than max')

        if not isinstance(include_min, bool):
            raise exceptions.Type_Error('include_min expected bool instance, {} found'.format(include_min.__class__.__name__))
        if not isinstance(include_max, bool):
            raise exceptions.Type_Error('include_max expected bool instance, {} found'.format(include_max.__class__.__name__))

        self._include_min = include_min
        self._include_max = include_max
    
    async def parse(self, input_string):
        """
        Converts the input string into an float

        input_string    : str   - The string to be converted to an float
        Returns         : float - The resulting parsed float

        Raises discord_cli.exceptions.Discord_CLI_Error is input is invalid
        """

        await validation.async_validate_float(input_string)
        result = float(input_string)
        await validation.async_validate_bounds(result, self._min, self._max, self._include_min, self._include_max)
        return result
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'float'

# String
class String_Parser(Base_Parser):

    def __init__(self, min_length, max_length, include_min_length, include_max_length):
        """
        min_length          : int | None    - The lower bound of valid input length
        max_length          : int | None    - The upper bound of valid input length
        include_min_length  : bool          - Whether to include the minumum length as valid
        include_max_length  : bool          - Whether to inlucde the maximum length as valid

        raises discord_cli.exceptions.Discord_CLI_Error is inputs are not valid
        """

        super(String_Parser, self).__init__()
        
        if min_length is not None:
            try:
                validation.validate_integer(min_length)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('min_length {}'.format(str(e)))
            self._min_length = int(min_length)
        else:
            self._min_length = None
        
        if max_length is not None:
            try:
                validation.validate_integer(max_length)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('max_length {}'.format(str(e)))
            self._max_length = int(max_length)
        else:
            self._max_length = None

        if self._min_length is not None and self._max_length is not None and self._min_length > self._max_length:
            raise exceptions.Value_Error('min_length cannot be greater than max_length')

        if not isinstance(include_min_length, bool):
            raise exceptions.Type_Error('include_min_length expected bool instance, {} found'.format(include_min_length.__class__.__name__))
        if not isinstance(include_max_length, bool):
            raise exceptions.Type_Error('include_max_length expected bool instance, {} found'.format(include_max_length.__class__.__name__))

        self._include_min_length = include_min_length
        self._include_max_length = include_max_length
    
    async def parse(self, input_string):
        """
        Converts the input string into an string

        input_string    : str   - The string to be converted to an string
        Returns         : str   - The resulting string

        Raises discord_cli.exceptions.Discord_CLI_Error is input is invalid
        """

        await validation.async_validate_string(input_string)
        try:
            await validation.async_validate_bounds(len(input_string), self._min_length, self._max_length, self._include_min_length, self._include_max_length)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('length {}'.format(str(e)))
        return input_string
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'string'

# User Mention
# Without nickname      <@95584437231689728>
# With nickname         <@!95584437231689728>
class User_Mention_Parser(Base_Parser):

    def __init__(self):
        super(User_Mention_Parser, self).__init__()
    
    async def parse(self, input_string):
        """
        Converts a user mention string into a user id

        input_string    : str   - The string to be converted into a user id
        Returns         : int   - The user id

        Raises discord_cli.exceptions.Discord_CLI_Error is input is invalid
        """

        await validation.async_validate_user_mention(input_string)
        for c in '<@!>':
            input_string = input_string.replace(c, '')
        return int(input_string)
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'user_mention'

# Channel Mention
# <#291649024409468928>

class Channel_Mention_Parser(Base_Parser):

    def __init__(self):
        super(Channel_Mention_Parser, self).__init__()
    
    async def parse(self, input_string):
        """
        Converts a channel mention string into a channel id

        input_string    : str   - The string to be converted into a channel id
        Returns         : int   - The channel id

        Raises discord_cli.exceptions.Discord_CLI_Error is input is invalid
        """

        await validation.async_validate_channel_mention(input_string)
        for c in '<#>':
            input_string = input_string.replace(c, '')
        return int(input_string)
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'channel_mention'

# Role Mention
# <@&357235474869387276>
class Role_Mention_Parser(Base_Parser):

    def __init__(self):
        super(Role_Mention_Parser, self).__init__()
    
    async def parse(self, input_string):
        """
        Converts a role mention string into a role id

        input_string    : str   - The string to be converted into a role id
        Returns         : int   - The role id

        Raises discord_cli.exceptions.Discord_CLI_Error is input is invalid
        """

        await validation.async_validate_role_mention(input_string)
        for c in '<@&>':
            input_string = input_string.replace(c, '')
        return int(input_string)
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'role_mention'

# Date
# In the format %d/%m/%Y for now, may become customizable in future
class Date_Parser(Base_Parser):
    
    def __init__(self, min, max, include_min, include_max):
        """
        min         : str | None    - The lower bound of valid input in the form '%d/%m/%Y'
        max         : str | None    - The upper bound of valid input in the form '%d/%m/%Y'
        include_min : bool          - Whether to include the minimum as valid
        include_max : bool          - Whether to include the maximum as valid

        raises discord_cli.exceptions.Discord_CLI_Error if inputs are invalid
        """

        super(Date_Parser, self).__init__()
        
        if min is not None:
            try:
                validation.validate_date(min)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('min {}'.format(str(e)))
            self._min = datetime.strptime(min, '%d/%m/%Y')
        else:
            self._min = None
        
        if max is not None:
            try:
                validation.validate_date(max)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('max {}'.format(str(e)))
            self._max = datetime.strptime(max, '%d/%m/%Y')
        else:
            self._max = None

        if self._min is not None and self._max is not None and self._min > self._max:
            raise exceptions.Value_Error('min cannot be greater than max')

        if not isinstance(include_min, bool):
            raise exceptions.Type_Error('include_min expected bool instance, {} found'.format(include_min.__class__.__name__))
        if not isinstance(include_max, bool):
            raise exceptions.Type_Error('include_max expected bool instance, {} found'.format(include_max.__class__.__name__))

        self._include_min = include_min
        self._include_max = include_max
    
    async def parse(self, input_string):
        """
        Converts the input string into datetime.datetime instance

        input_string    : str               - The string to be converted to a datetime instance in the form '%d/%m/%Y'
        Returns         : datetime.datetime - A datetime object which the input string represents

        Raises discord_cli.exceptions.Discord_CLI_Error if input is invalid
        """

        await validation.async_validate_date(input_string)
        result = datetime.strptime(input_string, '%d/%m/%Y')
        await validation.async_validate_bounds(result, self._min, self._max, self._include_min, self._include_max)
        return result
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'date'

# Time
# In the format %H:%M:%S for now, may become customizable in future
class Time_Parser(Base_Parser):

    def __init__(self, min, max, include_min, include_max):
        """
        min         : str | None    - The lower bound of valid input in the form '%H:%M:%S'
        max         : str | None    - The upper bound of valid input in the form '%H:%M:%S'
        include_min : bool          - Whether to include the minimum as valid
        include_max : bool          - Whether to include the maximum as valid

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are invalid
        """

        super(Time_Parser, self).__init__()
        
        if min is not None:
            try:
                validation.validate_time(min)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('min {}'.format(str(e)))
            self._min = datetime.strptime(min, '%H:%M:%S')
        else:
            self._min = None
        
        if max is not None:
            try:
                validation.validate_time(max)
            except exceptions.Discord_CLI_Error as e:
                raise type(e)('max {}'.format(str(e)))
            self._max = datetime.strptime(max, '%H:%M:%S')
        else:
            self._max = None

        if self._min is not None and self._max is not None and self._min > self._max:
            raise exceptions.Value_Error('min cannot be greater than max')

        if not isinstance(include_min, bool):
            raise exceptions.Type_Error('include_min expected bool instance, {} found'.format(include_min.__class__.__name__))
        if not isinstance(include_max, bool):
            raise exceptions.Type_Error('include_max expected bool instance, {} found'.format(include_max.__class__.__name__))

        self._include_min = include_min
        self._include_max = include_max
    
    async def parse(self, input_string):
        """
        Converts the input string into a datetime.datetime instance

        input_string    : str               - A string that represents a time in the form '%H:%M:%S'
        Returns         : datetime.datetime - A dateimte instance that is represented by the input string

        Raises discord_cli.exceptions.Discord_CLI_Error if input is invalid
        """

        await validation.async_validate_time(input_string)
        result = datetime.strptime(input_string, '%H:%M:%S')
        await validation.async_validate_bounds(result, self._min, self._max, self._include_min, self._include_max)
        return result
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'time'

# Enum
class Enum_Parser(Base_Parser):

    def __init__(self, values):
        """
        values : list - A list of strings which are to be used as the identifiers for the enums

        Raises discord_cli.exceptions.Discord_CLI_Error if input is invalid
        """
        
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
        """
        Converts an input string into an enum

        input_string    : str   - The enum to be checked and parsed
        Returns         : str   - The enum

        Raises discord_cli.exceptions.Discord_CLI_Error if input is invalid
        """

        await validation.async_validate_string(input_string)
        if input_string not in self._values:
            raise exceptions.Value_Error('must be element in {}'.format(str(self._values)))
        return input_string
    
    def __str__(self):
        """
        Returns : str - The datatype of the parser
        """

        return 'enum'