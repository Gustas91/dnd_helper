import unittest
from unittest.mock import patch
from DNDHelper import CharacterManager, PlayerCharacter, NPCCharacter

class TestCharacterManager(unittest.TestCase):
    def setUp(self):
        self.manager = CharacterManager()

    def test_add_character(self):
        character = PlayerCharacter()
        self.manager.add_character(character)
        self.assertIn(character, self.manager.get_characters())

if __name__ == '__main__':
    unittest.main()
