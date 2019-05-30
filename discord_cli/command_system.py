from discord_cli.command import Command
import discord_cli.exceptions as exceptions

class Command_System(object):
    
    def __init__(self, name = 'Command System', description = None):
        self._root = Command(name, description)
    
    def command(self, name, description = None, function = None):
        return self._root.command(name, description, function)
    
    @property
    def commands(self):
        return self._root.sub_commands
    
    @property
    def command_count(self):
        return self._root._sub_command_count
    
    def tree_string(self, details = False):
        return self._root.tree_string(details = details)

    async def _split_command_string(self, command_string):
        # Splitting all elements
        sub_elements = command_string.split('\\ ')
        elements = [x.split() for x in sub_elements]

        # Joining elements with escaped space
        for i in range(len(elements) - 1):
            if len(elements[i + 1]) == 0:
                continue
            first_from_next = elements[i + 1].pop(0)

            if len(elements[i]) == 0:
                elements[i].append(first_from_next)
            else:
                elements[i][-1] += ' ' + first_from_next

        # Combining into one list
        result = []
        for i in elements:
            for e in i:
                result.append(e)
            
        return result

    async def execute(self, client, message, command_string, *argv, **kwargs):
        command_elements = await self._split_command_string(command_string)
        cmd, params = await self._root.get_command(*command_elements)
        if cmd is self._root:
            return exceptions.Command_Not_Found_Error()
        return await cmd.execute(client, message, params, *argv, **kwargs)
