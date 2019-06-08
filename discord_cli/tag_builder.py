import discord_cli.validation as validation
import discord_cli.exceptions as exceptions

class Tag(object):

    def __init__(self, name, description, letter, word):
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
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def letter(self):
        return self._letter

    @property
    def word(self):
        return self._word
    
    def __str__(self):
        elements = [self._name, '-' + self._letter]
        if self._word is not None:
            elements.append('--' + self._word)
        if self._description is not None:
            elements.append(self._description)
        return ' | '.join(elements)

class Tag_Builder(object):

    def __init__(self, command):
        self._command = command
        
        self._tags = []
        self._name_table = {}
        self._letter_table = {}
        self._word_table = {}
        self._tag_count = 0
    
    def tag(self, name, description, letter, word):
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
        return self._tags
    
    @property
    def name_table(self):
        return self._name_table

    @property
    def letter_table(self):
        return self._letter_table
    
    @property
    def word_table(self):
        return self._word_table

    @property
    def tag_count(self):
        return self._tag_count