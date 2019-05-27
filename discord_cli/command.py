from inspect import iscoroutine

import discord_cli.validation as validation
from discord_cli.exceptions import CommandAlreadyExistsException

from discord_cli.argument_builder import Argument_Builder
from discord_cli.option_builder import Option_Builder

class Command(object):

    # Should only be called from within the package
    def __init__(self, name, description = None, parent = None, function = None):
        
        # TODO: Move validation to command system class when implimented
        if description is not None and not validation.validate_string(description):
            raise Exception

        if function is not None and not iscoroutine(function):
            raise Exception

        self._name = name
        self._description = description

        self._parent = parent
        self._function = function

        self._argument_builder = Argument_Builder(self)
        self._option_builder = Option_Builder(self)

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

    # Adding parameters and permissions ======================================================
    
    @property
    def argument(self):
        return self._argument_builder

    @property
    def option(self):
        return self._option_builder
    
    # ---------- TODO ----------
    # def tag(self, name, description , letter = None, word = None):
    #     self._tag_builder.tag(name, description, letter, word)
    #
    # def permission(self, permission):
    #     self._permission_builder.permission(permission)
    # --------------------------

    # ========================================================================================

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