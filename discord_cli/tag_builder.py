import discord_cli.validation as validation
import discord_cli.exceptions as exceptions

class Tag(object):

    """
    The tag class represents a single tag that is a component of a command
    """

    def __init__(self, name, description, letter, word):
        """
        name        : str           - The name of the tag
        description : str | None    - A description of the tag
        letter      : str | None    - The letter identifier of the tag (If None, the first letter of name is used)
        word        : str | None    - The word identifier of the tag

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        try:
            validation.validate_word(name)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Tag name {}, \'{}\' given'.format(str(e), name))
        
        try:
            if description is not None:
                validation.validate_string(description)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Tag description {}, \'{}\' given'.format(str(e), description))

        if letter is None:
            letter = name[0]
        
        try:
            validation.validate_letter(letter)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Tag letter {}, \'{}\' given'.format(str(e), letter))

        try:
            if word is not None:
                validation.validate_word(word)
        except exceptions.Discord_CLI_Error as e:
            raise type(e)('Tag word {}, \'{}\' given'.format(str(e), word))

        self._name = name
        self._description = description
        self._letter = letter
        self._word = word
    
    @property
    def name(self):
        """
        Returns : str - The name of the tag
        """

        return self._name
    
    @property
    def description(self):
        """
        Returns : str | None - A description of the tag
        """

        return self._description
    
    @property
    def letter(self):
        """
        Returns : str - The letter identifier for the tag
        """

        return self._letter

    @property
    def word(self):
        """
        Returns : str | None - The word identifier for the tag
        """

        return self._word
    
    def __str__(self):
        """
        Returns : str - A string representation of the tag
        
        E.g. 'embed | -e | --embed | displays response in an embed'
        """

        elements = [self._name, '-' + self._letter]
        if self._word is not None:
            elements.append('--' + self._word)
        if self._description is not None:
            elements.append(self._description)
        return ' | '.join(elements)

class Tag_Builder(object):

    """
    The tag builder serves as a list of tags which belong to a command.
    """

    def __init__(self, command):
        """
        command : discord_cli.command.Command - The command the tags belong to
        """

        self._command = command
        
        self._tags = []
        self._name_table = {}
        self._letter_table = {}
        self._word_table = {}
        self._tag_count = 0
    
    def tag(self, name, description, letter, word):
        """
        Adds a tag to the list of tags

        name        : str           - The name of the tag
        description : str | None    - A description of the tag
        letter      : str | None    - The letter identifier of the tag (If None, the first letter of name is used)
        word        : str | None    - The word identifier of the tag

        Raises discord_cli.exceptions.Discord_CLI_Error if inputs are not valid
        """

        new_tag = Tag(name, description, letter, word)

        if new_tag.name in self._name_table:
            raise exceptions.Name_Already_In_Use_Error('Name \'{}\' is in use by another tag'.format(name))
        if new_tag.letter in self._letter_table:
            raise exceptions.Letter_Already_In_Use_Error('Letter \'-{}\' is in use by another tag'.format(letter))
        if new_tag.word is not None and new_tag.word in self._word_table:
            raise exceptions.Word_Already_In_Use_Error('Word \'--{}\' already in use by another tag'.format(word))

        if new_tag.name in self._command._argument_builder.name_table:
            raise exceptions.Name_Already_In_Use_Error('Name \'{}\' is in use by an argument'.format(name))
        if new_tag.name in self._command._option_builder.name_table:
            raise exceptions.Name_Already_In_Use_Error('Name \'{}\' is in use by an option'.format(name))
        if new_tag.letter in self._command._option_builder.letter_table:
            raise exceptions.Letter_Already_In_Use_Error('Letter \'-{}\' is in use by an option'.format(letter))
        if new_tag.word in self._command._option_builder.word_table:
            raise exceptions.Word_Already_In_Use_Error('Word \'--{}\' already in use by an option'.format(word))

        self._tags.append(new_tag)
        self._name_table[new_tag.name] = new_tag
        self._letter_table[new_tag.letter] = new_tag
        if new_tag.word is not None:
            self._word_table[new_tag.word] = new_tag
        self._tag_count += 1
    
    @property
    def tags(self):
        """
        Returns : list - The list of tags
        """

        return self._tags
    
    @property
    def name_table(self):
        """
        Returns : dict - A dictionary which associates each name with the tag that has that name
        """

        return self._name_table

    @property
    def letter_table(self):
        """
        Returns : dict - A dictionary which associates each letter identifier with the tag that has that letter identifier
        """

        return self._letter_table
    
    @property
    def word_table(self):
        """
        Returns : dict - A dictionary which associates each word identifier with the tag that has that word identifier
        """

        return self._word_table

    @property
    def tag_count(self):
        """
        Returns : int - The amount of tags in the list
        """

        return self._tag_count