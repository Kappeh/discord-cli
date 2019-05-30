class Base_Permission(object):
    def __init__(self):
        pass
    async def evaluate(client, message):
        raise NotImplementedError

class Permission_Operator(Base_Permission):
    def __init__(self, perm1, perm2):
        super(Permission_Operator, self).__init__()
        self._perm1 = perm1
        self._perm2 = perm2
    
class And_Permission_Operator(Permission_Operator):
    def __init__(self, perm1, perm2):
        super(And_Permission_Operator, self).__init__(perm1, perm2)
    async def evaluate(self, client, message):
        return await self._perm1.evaluate(client, message) and await self._perm2.evaluate(client, message)

class Or_Permission_Operator(Permission_Operator):
    def __init__(self, perm1, perm2):
        super(Or_Permission_Operator, self).__init__(perm1, perm2)
    async def evaluate(self, client, message):
        return await self._perm1.evaluate(client, message) or await self._perm2.evaluate(client, message)

class Permission_Operand(Base_Permission):
    def __init__(self):
        super(Permission_Operand, self).__init__()
    def __and__(self, other):
        return And_Permission_Operator(self, other)
    def __or__(self, other):
        return Or_Permission_Operator(self, other)

class User_Permission(Permission_Operand):
    def __init__(self, user_id):
        super(User_Permission, self).__init__()
        self._user_id = user_id
    async def evaluate(self, client, message):
        return message.author.id == self._user_id

class Guild_Permission(Permission_Operand):
    def __init__(self, guild_id):
        super(Guild_Permission, self).__init__()
        self._guild_id = guild_id
    async def evaluate(self, client, message):
        return message.guild.id == self._guild_id