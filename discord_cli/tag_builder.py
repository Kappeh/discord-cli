import discord_cli.validation as validation

class Tag(object):

    def __init__(self, name, description, letter, word):
        if not validation.validate_word(name):
            raise ValueError
        if description is not None and not validation.validate_string(description):
            raise ValueError

        if letter is None:
            letter = name[0]
        elif not validation.validate_letter(letter):
            raise ValueError
        
        if word is not None and not validation.validate_word(word):
            raise ValueError

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

class Tag_Builder(object):

    def __init__(self, command):
        self._command = command
        
        self._tags = []
        self._tag_count = 0
    
    def tag(self, name, description, letter, word):
        self._tags.append(Tag(name, description, letter, word))
        self._tag_count += 1
    
    @property
    def tags(self):
        return self._tags
    
    @property
    def tag_count(self):
        return self._tag_count