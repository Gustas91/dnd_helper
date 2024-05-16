import unittest
from unittest.mock import patch
import os
from DNDHelper import CharacterManager, PlayerCharacter, NPCCharacter

class TestCharacterManager(unittest.TestCase):
    def setUp(self):
        self.manager = CharacterManager()

    @classmethod
    def tearDownClass(cls):
        for file_name in os.listdir('.'):
            if file_name.endswith('_character_sheet.txt'):
                os.remove(file_name)    

    def test_add_character(self):
        character = PlayerCharacter()
        self.manager.add_character(character)
        self.assertIn(character, self.manager.get_characters())

    def test_add_and_export_character(self):
        self.manager.add_character(NPCCharacter())
        character = self.manager.get_characters()[0]
        self.manager.export_character(character)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        exported_file_name = f"{character.attributes['Name']}_character_sheet.txt"
        exported_file_path = os.path.join(current_directory, exported_file_name)
        self.assertTrue(os.path.exists(exported_file_path))

    def test_import_character(self):
        filename = "None_character_sheet.txt" 
        self.manager.import_character(filename)
        self.assertEqual(len(self.manager.get_characters()), 3)
        imported_character = self.manager.get_characters()[0]
        self.assertIsInstance(imported_character, NPCCharacter)        

if __name__ == '__main__':
    unittest.main()
