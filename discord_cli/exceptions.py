class Command_Already_Exists_Error(Exception): pass
class Ambiguous_Parameter_Error(Exception): pass

class Parsing_Error(object):
    def __init__(self, message):
        self._message = 'Pasring Error: ' + message

    @property
    def message(self):
        return self._message

class Command_Not_Found_Error(Parsing_Error):
    def __init__(self):
        super(Command_Not_Found_Error, self).__init__('Command not found')

class Unexpected_Argument_Error(Parsing_Error):
    def __init__(self):
        super(Unexpected_Argument_Error, self).__init__('Unexpected argument')

class Unexpected_Word_Error(Parsing_Error):
    def __init__(self):
        super(Unexpected_Word_Error, self).__init__('Unexpected word')

class Unexpected_Letter_Error(Parsing_Error):
    def __init__(self):
        super(Unexpected_Letter_Error, self).__init__('Unexpected letter')

class Invalid_Argument_Error(Parsing_Error):
    def __init__(self):
        super(Invalid_Argument_Error, self).__init__('Invalid argument')

class Invalid_Option_Error(Parsing_Error):
    def __init__(self):
        super(Invalid_Option_Error, self).__init__('Invalid option')

class Expected_Arguments_Error(Parsing_Error):
    def __init__(self):
        super(Expected_Arguments_Error, self).__init__('Expected more arguments')

class Command_Not_Executable_Error(Parsing_Error):
    def __init__(self):
        super(Command_Not_Executable_Error, self).__init__('Command not executable')

class Insufficient_Permissions_Error(Parsing_Error):
    def __init__(self):
        super(Insufficient_Permissions_Error, self).__init__('Insufficient permissions')
