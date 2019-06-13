from inspect import iscoroutinefunction
import discord_cli.exceptions as exceptions

class Base_Permission(object):

    """
    The base permission class defines which methods a permission class must have.
    A class which derives this class represents a set of criteria a user must meet
    to be granted access to some feature; most likely to execute and/or view a command.
    """

    def __init__(self):
        """
        The base class cannot be instanciated. It serves only functionality for derived classes.
        Raises discord_cli.exceptions.Cannot_Create_Instance_Of_Base_Class_Error if attempted to instanciate.
        """
        
        if self.__class__ == Base_Permission:
            raise exceptions.Cannot_Create_Instance_Of_Base_Class_Error('Cannot create instance of Base_Permission')

    def __and__(self, other):
        """
        Overloads & operator

        self    : discord_cli.permissions.Base_Permission           - The permission on the left of operator
        other   : discord_cli.permissions.Base_Permission           - The permission on the right of operator
        Returns : discord_cli.permissions.And_Permission_Operator   - The resulting permission

        Raises discord_cli.exceptions.Type_Error if other is not an instance of discord_cli.permissions.Base_Permission
        """

        return And_Permission_Operator(self, other)

    def __or__(self, other):
        """
        Overloads | operator.

        self    : discord_cli.permissions.Base_Permission           - The permission on the left of operator
        other   : discord_cli.permissions.Base_Permission           - The permission on the right of operator
        Returns : discord_cli.permissions.Or_Permission_Operator    - The resulting permission

        Raises discord_cli.exceptions.Type_Error if other is not an instance of discord_cli.permissions.Base_Permission
        """

        return Or_Permission_Operator(self, other)

    async def evaluate(client, message):
        """
        Makes this method necessary to overwrite when creating derived class.
        Raises NotImplementedError if called.
        """

        raise NotImplementedError('Cannot run evaluate on base permission class')

class Permission_Operator(Base_Permission):

    """
    The permission operator represents some boolean operation applied to the results of two permissions.
    """

    def __init__(self, perm1, perm2):
        """
        The permission operator cannot be instanciated. It serves only functionality for derived classes.

        perm1   : discord_cli.permissions.Base_Permission   - The permission on the left of the operator
        perm2   : discord_cli.permissions.Base_Permission   - The permission on the right of the operator

        Raises discord_cli.exceptions.Cannot_Create_Instance_Of_Base_Class_Error if attempted to instanciate.
        Raises discord_cli.exceptions.Type_Error if either perm1 or perm2 is not instance of discord_cli.permission.Base_Permission
        """

        if self.__class__ == Permission_Operator:
            raise exceptions.Cannot_Create_Instance_Of_Base_Class_Error('Cannot create instance of Permission_Operator')

        super(Permission_Operator, self).__init__()

        if not isinstance(perm1, Base_Permission):
            raise exceptions.Type_Error('Permission operator perm1 expected Base_Permission instance, {} found'.format(perm1.__class__.__name__))
        if not isinstance(perm2, Base_Permission):
            raise exceptions.Type_Error('Permission operator perm2 expected Base_Permission instance, {} found'.format(perm1.__class__.__name__))

        self._perm1 = perm1
        self._perm2 = perm2

class And_Permission_Operator(Permission_Operator):
    
    def __init__(self, perm1, perm2):
        """
        perm1   : discord_cli.permissions.Base_Permission   - The permission on the left of the operator
        perm2   : discord_cli.permissions.Base_Permission   - The permission on the right of the operator

        Raises discord_cli.exceptions.Type_Error if either perm1 or perm2 is not instance of discord_cli.permission.Base_Permission
        """

        super(And_Permission_Operator, self).__init__(perm1, perm2)

    async def evaluate(self, client, message):
        """
        Checks whether a user in a channel meets the criteria for both permissions

        client  : discord.Client    - The discord bot client
        message : discord.Message   - A message from the user in the channel

        Raises discord_cli.exceptions.Discord_CLI_Error if the inputs are invalid
        """
        
        return await self._perm1.evaluate(client, message) and await self._perm2.evaluate(client, message)

    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        left_str = str(self._perm1)
        right_str = str(self._perm2)
        if isinstance(self._perm1, Permission_Operator):
            left_str = '(' + left_str + ')'
        if isinstance(self._perm2, Permission_Operator):
            right_str = '(' + right_str + ')'
        return left_str + ' and ' + right_str

class Or_Permission_Operator(Permission_Operator):
    
    def __init__(self, perm1, perm2):
        """
        perm1   : discord_cli.permissions.Base_Permission   - The permission on the left of the operator
        perm2   : discord_cli.permissions.Base_Permission   - The permission on the right of the operator

        Raises discord_cli.exceptions.Type_Error if either perm1 or perm2 is not instance of discord_cli.permission.Base_Permission
        """

        super(Or_Permission_Operator, self).__init__(perm1, perm2)

    async def evaluate(self, client, message):
        """
        Checks whether a user in a channel meets the criteria for either permissions

        client  : discord.Client    - The discord bot client
        message : discord.Message   - A message from the user in the channel

        Raises discord_cli.exceptions.Discord_CLI_Error if the inputs are invalid
        """

        return await self._perm1.evaluate(client, message) or await self._perm2.evaluate(client, message)

    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        left_str = str(self._perm1)
        right_str = str(self._perm2)
        if isinstance(self._perm1, Permission_Operator):
            left_str = '(' + left_str + ')'
        if isinstance(self._perm2, Permission_Operator):
            right_str = '(' + right_str + ')'
        return left_str + ' or ' + right_str

class Permission_Operand(Base_Permission):
    """
    The permission operand represents some single criteria for a user to meet.
    """

    def __init__(self):
        """
        The permission operand cannot be instanciated. It serves only functionality for derived classes.
        Raises discord_cli.exceptions.Cannot_Create_Instance_Of_Base_Class_Error if attempted to instanciate.
        """

        if self.__class__ == Permission_Operand:
            raise exceptions.Cannot_Create_Instance_Of_Base_Class_Error('Cannot create instance of Permission_Operand')
        super(Permission_Operand, self).__init__()

class User_Permission(Permission_Operand):

    def __init__(self, user_id):
        """
        user_id : int - The id of the user that meets this criteria

        Raises discord_cli.exceptions.Discord_CLI_Error if the input is invalid
        """

        super(User_Permission, self).__init__()
        self._user_id = user_id

    async def evaluate(self, client, message):
        """
        Checks if the user that sent the message has the specified user id

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message sent by a user
        Returns : bool              - Whether the user's id matches the specified id
        """

        return message.author.id == self._user_id
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'user:{}'.format(self._user_id)

class Guild_Permission(Permission_Operand):

    def __init__(self, guild_id):
        """
        user_id : int - The id of the user that meets this criteria

        Raises discord_cli.exceptions.Discord_CLI_Error if the input is invalid
        """

        super(Guild_Permission, self).__init__()
        self._guild_id = guild_id

    async def evaluate(self, client, message):
        """
        Checks if the guild the message was sent within matches a specified id

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message sent in a guild
        Returns : bool              - Whether the message was sent in the guild with the specified id
        """

        return message.guild.id == self._guild_id
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'guild:{}'.format(self._guild_id)

class Custom_Permission(Permission_Operand):

    def __init__(self, permission_function):
        """
        permission_function : function - The function which evaluates some criteria
        
        The function must be a corroutine function
        The function must accept, and only accept, the parameters:
            client  : discord.Client    - The discord bot client
            message : discord.Message   - The message the command was invoked by
        The function must return:
            bool                        - Whether the criteria is met

        Raises discord_cli.exceptions.Discord_CLI_Error if input is invalid
        """
        
        super(Custom_Permission, self).__init__()
        if not iscoroutinefunction(permission_function):
            raise exceptions.Not_Async_Function_Error('Custom permission function must be an async function')
        self._permission_function = permission_function

    async def evaluate(self, client, message):
        """
        Checks if the criteria is met

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the criteria is met

        Raises Exception if input is invalid
        """

        return await self._permission_function(client, message)

    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'custom'

class Discord_Permission(Permission_Operand):

    """
    The discord permission class represents a discord permission user must have in a channel.
    """

    def __init__(self):
        """
        The discord permission class cannot be instanciated. It serves only functionality for derived classes.
        Raises discord_cli.exceptions.Cannot_Create_Instance_Of_Base_Class_Error if attempted to instanciate.
        """

        if self.__class__ == Discord_Permission:
            raise exceptions.Cannot_Create_Instance_Of_Base_Class_Error('Cannot create instance of Discord_Permission')
        super(Discord_Permission, self).__init__()

class Create_Instant_Invite(Discord_Permission):

    def __init__(self):
        super(Create_Instant_Invite, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to create instant invites

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can create instant invites
        """

        return message.author.permissions_in(message.channel).create_instant_invite
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'create_instant_invite'

class Kick_Members(Discord_Permission):

    def __init__(self):
        super(Kick_Members, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to kick members

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can kick members
        """

        return message.author.permissions_in(message.channel).kick_members
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'kick_members'

class Ban_Members(Discord_Permission):

    def __init__(self):
        super(Ban_Members, self).__init__()

    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to ban members

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can ban members
        """

        return message.author.permissions_in(message.channel).ban_members
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'ban_members'

class Administrator(Discord_Permission):

    def __init__(self):
        super(Administrator, self).__init__()

    async def evaluate(self, client, message):
        """
        Checks if a user is an administrator

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - whether the user is an administrator
        """

        return message.author.permissions_in(message.channel).administrator
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'administrator'

class Manage_Channels(Discord_Permission):

    def __init__(self):
        super(Manage_Channels, self).__init__()

    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to manage channel

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can manage channel
        """

        return message.author.permissions_in(message.channel).manage_channels
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'manage_channels'

class Manage_Guild(Discord_Permission):

    def __init__(self):
        super(Manage_Guild, self).__init__()

    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to manage the guild

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can manage the guild
        """

        return message.author.permissions_in(message.channel).manage_guild
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'manage_guild'

class Add_Reactions(Discord_Permission):

    def __init__(self):
        super(Add_Reactions, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to add reactions

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can add reactions
        """

        return message.author.permissions_in(message.channel).add_reactions
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'add_reactions'

class View_Audit_Log(Discord_Permission):

    def __init__(self):
        super(View_Audit_Log, self).__init__()

    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to view the audit logs

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can view the audit logs
        """
        
        return message.author.permissions_in(message.channel).view_audit_log

    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'view_audit_log'

class Read_Messages(Discord_Permission):

    def __init__(self):
        super(Read_Messages, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to read messages

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can read messages
        """
        
        return message.author.permissions_in(message.channel).read_messages
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'read_messages'

class Send_Messages(Discord_Permission):

    def __init__(self):
        super(Send_Messages, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to send messages

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can send messages
        """

        return message.author.permissions_in(message.channel).send_messages
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'send_messages'

class Send_TTS_Messages(Discord_Permission):

    def __init__(self):
        super(Send_TTS_Messages, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to send tts messages

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can send tts messages
        """

        return message.author.permissions_in(message.channel).send_tts_messages
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'send_tts_messages'

class Manage_Messages(Discord_Permission):

    def __init__(self):
        super(Manage_Messages, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to manage messages

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can manage messages
        """

        return message.author.permissions_in(message.channel).manage_messages
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'manage_messages'

class Embed_Links(Discord_Permission):

    def __init__(self):
        super(Embed_Links, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to embed links

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can embed links
        """

        return message.author.permissions_in(message.channel).embed_links
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'embed_links'

class Attach_Files(Discord_Permission):

    def __init__(self):
        super(Attach_Files, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to attach files

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can attach files
        """

        return message.author.permissions_in(message.channel).attach_files
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'attach_files'

class Read_Message_History(Discord_Permission):

    def __init__(self):
        super(Read_Message_History, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to read message history

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can read message history
        """

        return message.author.permissions_in(message.channel).read_message_history
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'read_message_history'

class Mention_Everyone(Discord_Permission):

    def __init__(self):
        super(Mention_Everyone, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to mention everyone

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can mention everyone
        """

        return message.author.permissions_in(message.channel).mention_everyone
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'mention_everyone'

class External_Emojis(Discord_Permission):

    def __init__(self):
        super(External_Emojis, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to use external emojis

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can use external emojis
        """

        return message.author.permissions_in(message.channel).external_emojis
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'external_emojis'

class Change_Nickname(Discord_Permission):

    def __init__(self):
        super(Change_Nickname, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to change their nickname

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can change their nickname
        """

        return message.author.permissions_in(message.channel).change_nickname
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'change_nickname'

class Manage_Nicknames(Discord_Permission):

    def __init__(self):
        super(Manage_Nicknames, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to manage nickanems

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can manage nickanems
        """

        return message.author.permissions_in(message.channel).manage_nicknames
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'manage_nicknames'

class Manage_Roles(Discord_Permission):

    def __init__(self):
        super(Manage_Roles, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to manage_roles

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can manage_roles
        """

        return message.author.permissions_in(message.channel).manage_roles
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'manage_roles'

class Manage_Webhooks(Discord_Permission):

    def __init__(self):
        super(Manage_Webhooks, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to manage webhooks

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can manage webhooks
        """

        return message.author.permissions_in(message.channel).manage_webhooks
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'manage_webhooks'

class Manage_Emojis(Discord_Permission):

    def __init__(self):
        super(Manage_Emojis, self).__init__()
    
    async def evaluate(self, client, message):
        """
        Checks if a user has the ability to manage emojis

        client  : discord.Client    - The discord bot client
        message : discord.Message   - The message that envoked the command
        Returns : bool              - Whether the user can manage emojis
        """

        return message.author.permissions_in(message.channel).manage_emojis
    
    def __str__(self):
        """
        Returns : str - A string which represents the criteria to be met
        """

        return 'manage_emojis'