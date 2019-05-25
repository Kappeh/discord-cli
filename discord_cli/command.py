from inspect import iscoroutine

from discord_cli.validation import (validate_integer, validate_string, validate_word)
from discord_cli.exceptions import CommandAlreadyExistsException

class Command(object):

    # Should only be called from within the package
    def __init__(self, name, description = None, parent = None, function = None):
        
        if description is not None:
            validate_string(description)

        if function is not None and not iscoroutine(function):
            raise TypeError

        self._name = name
        self._description = description

        self._parent = parent
        self._function = function

        self._sub_commands = {}
        self._sub_command_count = 0
    
    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def sub_commands(self):
        return self._sub_commands
    
    @property
    def sub_command_count(self):
        return self._sub_command_count

    @property
    def function(self):
        return self._function

    def command(self, name, description = None):
        
        #validate_word(name)
        if name in self._sub_commands:
            raise CommandAlreadyExistsException
        
        self._sub_commands[name] = Command(name, description, parent = self)
        self._sub_command_count += 1
        return self._sub_commands[name]

    def tree_string(self, details = False, prefix = '', include_name = True):
        result = ''
        if include_name:
            result += prefix + self._name + '\n'

        # Add details here when implimented

        for i, (command_name, command_obj) in enumerate(self._sub_commands.items()):
            result += '{0}| \n{0}+-+ {1}\n'.format(prefix, command_name)
            new_prefix = prefix + '| ' if i < self._sub_command_count - 1 else prefix + '  '
            result += command_obj.tree_string(details = details, prefix = new_prefix, include_name = False)
        
        return result