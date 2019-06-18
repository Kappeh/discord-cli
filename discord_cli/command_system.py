import discord

from discord_cli.command import Command
import discord_cli.exceptions as exceptions
from inspect import iscoroutinefunction

class Command_System(object):

    """
    The command system is a class which is used to generate and execute a set of commands
    """
    
    def __init__(self, name = 'Command_System', description = None):
        """
        name            : str           - The name of the command system
        description     : str | None    - A description of the command system

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        self._root = Command(name, description)
        self._execution_error_callback = default_execution_error_callback
    
    def set_execution_error_callback(self, callback):
        """
        Sets which function is to be called when there is an error when parsing a command

        callback : function - The function to be called upon error

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        if not iscoroutinefunction(callback):
            raise exceptions.Not_Async_Function_Error('Callback must be a couroutine function')
        self._execution_error_callback = callback

    def command(self, name, description = None, function = None):
        """
        Adds a command to the root of the command system

        name            : str               - The name of the command
        description     : str | None        - A description of the command
        function        : function | None   - The function which is associated with this command

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        return self._root.command(name, description, function)
    
    @property
    def commands(self):
        """
        Returns : list - A list of all of the commands at the root of the command system
        """

        return self._root.sub_commands
    
    @property
    def command_count(self):
        """
        Returns : int - The amound of commands at the root of the command system
        """

        return self._root._sub_command_count
    
    def tree_string(self, details = False):
        """
        Gets a string which shows the names of the commands in the whole command
        system along with the connections between commands and sub-commands

        If details is True, the arguments, options, tags and permissions for
        each command will also be displayed

        details : bool  - Whether to include details about each command
        Returns : str   - A string which represents the command tree
        """

        return self._root.tree_string(details = details)

    async def _split_command_string(self, command_string):
        """
        Splits a command string into a list which contains individual
        command identifiers and parameters

        command_string  : str   - The command string to be split
        Returns         : list  - A list containing the individual command identifiers and parameters
        """

        result = []
        char_ptr = -1

        current_string = ''

        within_quotes = False
        
        escape_next_char = False
        escape_char = False

        while True:
            char_ptr += 1
            if char_ptr == len(command_string):
                if current_string != '':
                    result.append(current_string)
                break

            escape_char = escape_next_char
            escape_next_char = False

            char = command_string[char_ptr]

            if char == ' ' and within_quotes == False and escape_char == False:
                if current_string == '':
                    continue    
                result.append(current_string)
                current_string = ''
                continue
            
            if char == '\\' and escape_char == False:
                escape_next_char = True
                continue

            if char == '"' and escape_char == False:
                if within_quotes == False and current_string != '':
                    raise exceptions.Value_Error('A quote used to start escaping text must follow a space')
                if within_quotes == True and char_ptr + 1 < len(command_string) and command_string[char_ptr + 1] != ' ':
                    raise exceptions.Value_Error('A quote used to end escaping text must be followed by a space')
                within_quotes = not within_quotes
                continue
            
            current_string += char

        return result

    async def execute(self, client, message, command_string, *argv, **kwargs):
        """
        Executes a command string for a user as client in a channel depending on the properties of message

        client          : discord.Client    - The discord bot client executing the command
        message         : discord.Message   - The message from the user containing the command being executed
        command_string  : str               - The command string to be parsed and executed
        argv                                - Arguments to be passed onto the command executable
        kwargs                              - Keyword arguments to be passed onto the command's function
        Returns         : object            - The return value of the command's function

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        try:
            command_elements = await self._split_command_string(command_string)
            cmd_params = await self._root.get_command(client, message, *command_elements)
            cmd, params = cmd_params
            if cmd is self._root:
                raise exceptions.Command_Not_Found_Error('Command not found')
            return await cmd.execute(client, message, params, *argv, **kwargs)
        except exceptions.Discord_CLI_Error as e:
            return await self._execution_error_callback(e)

    async def usage_message(self, client, message, command_string):
        """
        Gets the usage / help message for a command. The client and message are
        passed in to hide commands from users with insufficient permissions

        client          : discord.Client    - The discord bot client executing the command
        message         : discord.Message   - The message from the user containing the command being executed
        command_string  : str               - The command string which represents the command
        Returns         : str               - The usage message for the command

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        command_elements = await self._split_command_string(command_string)
        cmd_params = await self._root.get_command(client, message, *command_elements)
        cmd, params = cmd_params
        if cmd is self._root:
            raise exceptions.Command_Not_Found_Error('Command not found')
        return await cmd.usage_message(client, message)

async def default_execution_error_callback(exception):
    """
    Returns a red discord embed with the error message in it
    """

    return discord.Embed(title = 'Error parsing command', description = ':x:' + str(exception), color = 0xf04747)