class CharacterManager:
    def __init__(self):
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)

    def list_characters(self):
        for character in self.characters:
            print(character)

    def find_character(self, first_name):
        for character in self.characters:
            if character.first_name == first_name:
                return character
        return None

    def remove_character(self, first_name):
        character = self.find_character(first_name)
        if character:
            self.characters.remove(character)
            return True
        return False