import discord_cli.permissions as permissions
import discord_cli.exceptions as exceptions

class Permission_Builder(object):

    """
    The permission builder class represents a set of criteria which
    a user must meet in order to execute and view a command.

    A permission builder can hold multiple permissions. A user need only
    meet one of the permissions to be granted access to a command.

    Note: If you wish for a user to have to meet multiple criteria to
    be granted access to a command, use a
    discord_cli.permissions.And_Permission_Operator instance.
    """

    def __init__(self, command):
        """
        command : discord_cli.command.Command - The command the permission builder belongs to
        """

        self._command = command

        self._permissions = []
        self._permission_count = 0
    
    def permission(self, permission):
        """
        permission : discord_cli.permissions.Base_Permission - The permission to be added to the command

        Raises discord_cli.exceptions.Discord_CLI_Error if input is invalid
        """

        if not isinstance(permission, permissions.Base_Permission):
            raise exceptions.Type_Error('permission must be a permission type')

        self._permissions.append(permission)
        self._permission_count += 1
    
    @property
    def permissions(self):
        """
        Returns : list - The list of permissions
        """

        return self._permissions
    
    @property
    def permission_count(self):
        """
        Returns : int - The amount of permissions in the list
        """

        return self._permission_count
    
    async def evaluate(self, client, message):
        """
        Checks if a user meets the criteria specified by the permissions in the list

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message which envoked the command to be executed

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are invalid
        """

        if self._permission_count == 0:
            return True

        for permission in self._permissions:
            if await permission.evaluate(client, message):
                return True
                
        return False