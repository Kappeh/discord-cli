from inspect import iscoroutinefunction

import discord_cli.exceptions as exceptions
import discord_cli.validation as validation

from discord_cli.argument_builder import Argument_Builder
from discord_cli.option_builder import Option_Builder
from discord_cli.tag_builder import Tag_Builder
from discord_cli.permission_builder import Permission_Builder

class Command(object):

    """
    A command object represents a single command. Commands can be executable. If they are,
    they contain an function and can contain arguments, options and tags.

    All commands can contain: permissions which restrict who can see and execute the command and
    a description which explains what the command / command tree is used for.

    All commands can also contain sub commands. For example, `git add` is a sub command of `git`.
    """

    # Should only be called from within the package
    def __init__(self, name, description = None, parent = None, command_string = None, function = None):
        """
        name            : str                                   - The name of the command
        description     : str | None                            - A description for the command
        parent          : discord_cli.command.Command | None    - The parent command of the command
        command_string  : str | None                            - The full command identifier including ancestor commands' names
        function        : function | None                       - The executable function associated with this command

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        try:
            validation.validate_command_name(name)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Command name {}'.format(str(e)))

        try:
            if description is not None:
                validation.validate_string(description)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Command description {}'.format(str(e)))

        if function is not None and not iscoroutinefunction(function):
            raise exceptions.Not_Async_Function_Error('Command function must be an async function')

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
        """
        Returns : discord_cli.command.Command - The parent command of this command
        """

        return self._parent

    @property
    def name(self):
        """
        Returns : str - The name of this command
        """

        return self._name
    
    @property
    def description(self):
        """
        Returns : str - A description for this command
        """

        return self._description
    
    @property
    def command_string(self):
        """
        Returns : str - The full command identifier including ancestor commands' names
        """
        
        return self._command_string

    @property
    def sub_commands(self):
        """
        Returns : list - A list containing all of the sub commands of this command
        """

        return self._sub_commands
    
    @property
    def sub_command_count(self):
        """
        Returns : int - The amount of sub commands that belong to this command
        """

        return self._sub_command_count

    @property
    def function(self):
        """
        Returns : function - The executable function associated with this command
        """

        return self._function
    
    @property
    def argument(self):
        """
        Returns : discord_cli.argument_builder.Argument_Builder - The argument builder for this command
        """

        return self._argument_builder

    @property
    def option(self):
        """
        Returns : discord_cli.option_builder.Option_Builder - The option builder for this command
        """

        return self._option_builder
    
    def tag(self, name, description = None, letter = None, word = None):
        """
        Adds a tag to the command

        name            : str           - The name of the tag
        description     : str | None    - A description of the tags purpose
        letter          : str | None    - The letter identifier for the tag (If None, set to the first letter of the name)
        word            : str | None    - The word identifier for the tag

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._tag_builder.tag(name, description, letter, word)
    
    def permission(self, permission):
        """
        Adds a permission to the command

        permission : discord_cli.permissions.Base_Permission - The permisison to be added to the command

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid     
        """

        self._permission_builder.permission(permission)

    async def get_command(self, client, message, *argv):
        """
        Gets a command specified by identifiers in argv and returns the elements in argv which are parameters

        client  : discord.Client                    - The discord bot client
        message : discord.Message                   - A message from a user in a channel to specify permissions
        argv                                        - The elements of the command string
        Returns : discord_cli.command.Command, list - The command, the remaining elements

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid or user does not have sufficient permissions for command
        """

        if len(argv) == 0:
            return self, []
        if argv[0] in self._sub_commands:
            sub_command = self._sub_commands[argv[0]]
            if not await sub_command._permission_builder.evaluate(client, message):
                raise exceptions.Insufficient_Permissions_Error('Insufficient permissions')
            return await sub_command.get_command(client, message, *argv[1:])
        return self, argv

    async def _parse_params(self, params):
        """
        Takes the parameters inputted as strings and parses them into the correct types and
        assigns them to the correct argument, option and tag identifiers

        params : list - A list of strings which represent the inputted parameters

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

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
            tag_list = []

            if param.startswith('--'):
                word = param[2:]
                if word in self._option_builder.word_table:
                    option = self._option_builder.word_table[word]
                elif word in self._tag_builder.word_table:
                    tag_list = [self._tag_builder.word_table[word]]
                else:
                    raise exceptions.Unexpected_Word_Error('\'{}\' has no option or tag associated with --{}'.format(self._command_string, word))
            elif param.startswith('-'):
                letters = param[1:]
                if letters in self._option_builder.letter_table:
                    option = self._option_builder.letter_table[letters]
                else:
                    for letter in letters:
                        if letter in self._tag_builder.letter_table:
                            tag_list.append(self._tag_builder.letter_table[letter])
                        else:
                            raise exceptions.Unexpected_Letter_Error('\'{}\' has no option or tag associated with -{}'.format(self._command_string, letter))

            if option is not None:
                param_ptr += 1
                if param_ptr >= len(params):
                    raise exceptions.Invalid_Option_Error('Option \'{}\' requires a value'.format(option.name))
                parsed_param = None

                try:
                    parsed_param = await option.parse(params[param_ptr])
                except exceptions.Discord_CLI_Error as e:
                    raise type(e)('{} {}'.format(option.name, str(e)))

                if isinstance(parsed_param, exceptions.Discord_CLI_Error):
                    return parsed_param
                opts[option.name] = parsed_param
            elif len(tag_list) != 0:
                for tag in tag_list:
                    tags[tag.name] = True
            else:
                if argument_ptr >= self._argument_builder.argument_count:
                    raise exceptions.Unexpected_Argument_Error('\'{}\' only expected {} arguments'.format(self._command_string, self._argument_builder.argument_count))
                argument = self._argument_builder.arguments[argument_ptr]
                parsed_param = None

                try:
                    parsed_param = await argument.parse(param)
                except exceptions.Discord_CLI_Error as e:
                    raise type(e)('{} {}'.format(argument.name, str(e)))

                if isinstance(parsed_param, exceptions.Discord_CLI_Error):
                    return parsed_param
                args[argument.name] = parsed_param

                argument_ptr += 1

            param_ptr += 1
        
        if argument_ptr < self._argument_builder.argument_count:
            raise exceptions.Expected_Arguments_Error('\'{}\' expected {} arguments, got {}'.format(self._command_string, self._argument_builder.argument_count, argument_ptr))
        
        return {**args, **opts, **tags}

    async def execute(self, client, message, params, *argv, **kwargs):
        """
        Executes this command's function

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message which contained the command string
        params  : list              - A list of strings containing the parameter input strings
        argv                        - The arguments to be passed to the command function
        kwargs                      - The keyword arguments to be passed to the command function
        Returns : object            - The returned value from the command's function

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        if not callable(self._function):
            raise exceptions.Command_Not_Executable_Error('No function is associated with \'{}\''.format(self._command_string))
        params = await self._parse_params(params)
        return await self._function(client, message, params, *argv, **kwargs)

    def command(self, name, description = None, function = None):
        """
        Adds a sub command to this command

        name        : str                           - The name of the sub command
        description : str | None                    - A description for the sub command
        function    : function | None               - The sub command's function
        Returns     : discord_cli.command.Command   - The new sub command

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """
        
        if self._argument_builder._first_is_text:
            raise exceptions.Ambiguous_Parameter_Error('Cannot add sub commands to \'{}\' as it\'s first argument can contain text'.format(self._command_string))
        
        validation.validate_command_name(name)
        if name in self._sub_commands:
            raise exceptions.Command_Already_Exists_Error('\'{}\' already exists'.format(self._command_string + ' ' + name))
        command_string = name if self._command_string is None else self._command_string + ' ' + name

        self._sub_commands[name] = Command(name, description, command_string = command_string, parent = self, function = function)
        self._sub_command_count += 1
        return self._sub_commands[name]

    def tree_string(self, details = False, prefix = '', include_name = True):
        """
        Gets a string representing the command tree with this command as the root node

        details         : bool  - Whether to show arguments, options, tags and permissions for commands
        prefix          : str   - A string to add to the beginning of each line
        include_name    : bool  - Whether to include the root node command name at the top of the tree
        Returns         : str   - A string representing the command tree
        """

        result = ''
        if include_name:
            result += prefix + '+ ' + self._name + '\n'
        
        command_prefix = prefix + '| ' if self._sub_command_count != 0 else prefix + '  '
        
        if details:
            if self._argument_builder.argument_count != 0:
                result += command_prefix + 'Arguments:\n'
                for arg in self._argument_builder.arguments:
                    result += command_prefix + '  ' + str(arg) + '\n'
            
            if self._option_builder.option_count != 0:
                result += command_prefix + 'Options:\n'
                for opt in self._option_builder.options:
                    result += command_prefix + '  ' + str(opt) + '\n'
            
            if self._tag_builder.tag_count != 0:
                result += command_prefix + 'Tags:\n'
                for tag in self._tag_builder.tags:
                    result += command_prefix + '  ' + str(tag) + '\n'
            
            if self._permission_builder.permission_count != 0:
                result += command_prefix + 'Pemrissions:\n'
                for perm in self._permission_builder.permissions:
                    result += command_prefix + '  ' + str(perm) + '\n'

        for i, (command_name, command_obj) in enumerate(self._sub_commands.items()):
            result += '{0}| \n{0}+-+ {1}\n'.format(prefix, command_name)
            new_prefix = prefix + '| ' if i < self._sub_command_count - 1 else prefix + '  '
            result += command_obj.tree_string(details = details, prefix = new_prefix, include_name = False)
        
        return result
    
    async def usage_message(self, client, message):
        """
        Gets a string which represents a usage message for this command

        client  : discord.Client    - The discord bot client 
        message : discord.Message   - A message from a user in a channel to specify permissions 
        Returns : str               - The usage message string
        """

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
                    tags.append(tag.description)
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