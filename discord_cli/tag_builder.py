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
        self._name_table = {}
        self._letter_table = {}
        self._word_table = {}
        self._tag_count = 0
    
    def tag(self, name, description, letter, word):
        new_tag = Tag(name, description, letter, word)

        if new_tag.name in self._name_table:
            raise ValueError
        if new_tag.letter in self._letter_table:
            raise ValueError
        if new_tag.word in self._word_table:
            raise ValueError

        if new_tag.name in self._command._argument_builder.name_table:
            raise ValueError
        if new_tag.name in self._command._option_builder.name_table:
            raise ValueError
        if new_tag.letter in self._command._option_builder.letter_table:
            raise ValueError
        if new_tag.word in self._command._option_builder.word_table:
            raise ValueError

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