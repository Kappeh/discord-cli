from inspect import iscoroutinefunction

import discord_cli.exceptions as exceptions
import discord_cli.validation as validation

from discord_cli.argument_builder import Argument_Builder
from discord_cli.option_builder import Option_Builder
from discord_cli.tag_builder import Tag_Builder
from discord_cli.permission_builder import Permission_Builder

class Command(object):

    # Should only be called from within the package
    def __init__(self, name, description = None, parent = None, command_string = None, function = None):
        
        # TODO: Move validation to command system class when implimented
        if description is not None and not validation.validate_string(description):
            raise Exception

        if function is not None and not iscoroutinefunction(function):
            raise Exception

        self._name = name
        self._description = description

        self._parent = parent
        self._function = function

        self._command_string = command_string

        self._argument_builder = Argument_Builder(self)
        self._option_builder = Option_Builder(self)
        self._tag_builder = Tag_Builder(self)
        self._permission_builder = Permission_Builder(self)

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
    
    def tag(self, name, description = None, letter = None, word = None):
        self._tag_builder.tag(name, description, letter, word)
    
    def permission(self, permission):
        self._permission_builder.permission(permission)

    # ========================================================================================

    async def get_command(self, client, message, *argv):
        if len(argv) == 0:
            return self, []
        if argv[0] in self._sub_commands:
            sub_command = self._sub_commands[argv[0]]
            if not await sub_command._permission_builder.evaluate(client, message):
                return exceptions.Insufficient_Permissions_Error()
            return await sub_command.get_command(client, message, *argv[1:])
        return self, argv

    async def _parse_params(self, params):
        args = {}
        opts = {}
        tags = {}

        for arg in self._argument_builder.arguments:
            args[arg.name] = None
        for opt in self._option_builder.options:
            opts[opt.name] = None
        for tag in self._tag_builder.tags:
            tags[tag.name] = False

        # Parsing params
        param_ptr = 0
        argument_ptr = 0

        while param_ptr < len(params):
            param = params[param_ptr]
            option = None
            tag = None

            if param.startswith('--'):
                word = param[2:]
                if word in self._option_builder.word_table:
                    option = self._option_builder.word_table[word]
                elif word in self._tag_builder.word_table:
                    tag = self._tag_builder.word_table[word]
                else:
                    return exceptions.Unexpected_Word_Error()
            elif param.startswith('-'):
                letter = param[1:]
                if letter in self._option_builder.letter_table:
                    option = self._option_builder.letter_table[letter]
                elif letter in self._tag_builder.letter_table:
                    tag = self._tag_builder.letter_table[letter]
                else:
                    return exceptions.Unexpected_Letter_Error()

            if option is not None:
                param_ptr += 1
                if param_ptr >= len(params):
                    return exceptions.Invalid_Option_Error()
                parsed_param = await option.parse(params[param_ptr])
                if isinstance(parsed_param, exceptions.Parsing_Error):
                    return parsed_param
                opts[option.name] = parsed_param
            elif tag is not None:
                tags[tag.name] = True
            else:
                if argument_ptr >= self._argument_builder.argument_count:
                    return exceptions.Unexpected_Argument_Error()
                argument = self._argument_builder.arguments[argument_ptr]
                parsed_param = await argument.parse(param)
                if isinstance(parsed_param, exceptions.Parsing_Error):
                    return parsed_param
                args[argument.name] = parsed_param

                argument_ptr += 1

            param_ptr += 1
        
        if argument_ptr < self._argument_builder.argument_count:
            return exceptions.Expected_Arguments_Error()
        
        return {**args, **opts, **tags}

    async def execute(self, client, message, params, *argv, **kwargs):
        params = await self._parse_params(params)
        if isinstance(params, exceptions.Parsing_Error):
            return params
        if not callable(self._function):
            return exceptions.Command_Not_Executable_Error()
        return await self._function(client, message, params, *argv, **kwargs)
        

    def command(self, name, description = None, function = None):
        
        #validate_word(name)
        if name in self._sub_commands:
            raise exceptions.CommandAlreadyExistsException
        
        command_string = None
        if self._command_string is None:
            command_string = name
        else:
            command_string = self._command_string + ' ' + name

        self._sub_commands[name] = Command(name, description, command_string = command_string, parent = self, function = function)
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
    
    async def usage_message(self, client, message, command_string):
        lines = []
        
        params = []
        if self._argument_builder.argument_count != 0:
            params.append(' '.join(['<{}>'.format(x.name) for x in self._argument_builder.arguments]))
        if self._option_builder.option_count != 0:
            params.append('[OPTIONS]')
        if self._tag_builder.tag_count != 0:
            params.append('[TAGS]')
        params = ' '.join(params)

        lines.append('Usage: ' + self._command_string + ' ' +params)
        if self._description is not None:
            lines.append(self._description)
        
        if self._argument_builder.argument_count != 0:
            lines.append('Arguments:')
            for arg in self._argument_builder.arguments:
                tmp = [arg.name]
                if arg.description is not None:
                    tmp.append(arg.description)
                lines.append('  ' + ' | '.join(tmp))
        
        if self._option_builder.option_count != 0:
            lines.append('Options:')
            for opt in self._option_builder.options:
                tmp = [opt.name, '-' + opt.letter]
                if opt.word is not None:
                    tmp.append('--' + opt.word)
                if opt.description is not None:
                    tmp.append(opt.description)
                lines.append('  ' + ' | '.join(tmp))
        
        if self._tag_builder.tag_count != 0:
            lines.append('Tags:')
            for tag in self._tag_builder.tags:
                tmp = [tag.name, '-' + tag.letter]
                if tag.word is not None:
                    tmp.append('--' + tag.word)
                if tag.description is not None:
                    tag.append(tag.description)
                lines.append('  ' + ' | '.join(tmp))
        
        if self._sub_command_count != 0:
            first = True
            for _, sub_command in self._sub_commands.items():
                if await sub_command._permission_builder.evaluate(client, message):
                    if first:
                        lines.append('Subcommands:')
                        first = False
                    lines.append('  {}'.format(sub_command.name))        
        
        return '\n'.join(lines)