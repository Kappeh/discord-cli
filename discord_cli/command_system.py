from discord_cli.command import Command
import discord_cli.exceptions as exceptions

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
        
        # Splitting all elements
        sub_elements = command_string.split('\\ ')
        elements = [x.split() for x in sub_elements]

        # Joining elements with escaped space
        for i in range(len(elements) - 1):
            if len(elements[i]) == 0:
                continue
            if len(elements[i + 1]) == 0:
                elements[i + 1].append(elements[i].pop(-1))
            else:
                elements[i + 1][0] = elements[i].pop(-1) + ' ' + elements[i + 1][0]

        # Combining into one list
        result = []
        for list_of_element in elements:
            for element in list_of_element:
                result.append(element)
            
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

        command_elements = await self._split_command_string(command_string)
        cmd_params = await self._root.get_command(client, message, *command_elements)
        cmd, params = cmd_params
        if cmd is self._root:
            raise exceptions.Command_Not_Found_Error('Command not found')
        return await cmd.execute(client, message, params, *argv, **kwargs)

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