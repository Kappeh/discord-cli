import discord_cli.permissions as permissions
import discord_cli.exceptions as exceptions

class Permission_Builder(object):

    def __init__(self, command):
        self._command = command

        self._permissions = []
        self._permission_count = 0
    
    def permission(self, permission):
        if not isinstance(permission, permissions.Base_Permission):
            raise exceptions.Type_Error('permission must be a permission type')

        self._permissions.append(permission)
        self._permission_count += 1
    
    @property
    def permissions(self):
        return self._permissions
    
    @property
    def permission_count(self):
        return self._permission_count
    
    async def evaluate(self, client, message):
        if self._permission_count == 0:
            return True

        for permission in self._permissions:
            if await permission.evaluate(client, message):
                return True
                
        return False