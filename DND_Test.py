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
        self.manager.export_character(self.manager.get_characters()[0])
        exported_file_name = "None_character_sheet.txt"
        self.assertTrue(os.path.exists(exported_file_name))

    def test_import_character(self):
        filename = "None_character_sheet.txt" 
        self.manager.import_character(filename)
        self.assertEqual(len(self.manager.get_characters()), 3)
        imported_character = self.manager.get_characters()[0]
        self.assertIsInstance(imported_character, NPCCharacter)        

if __name__ == '__main__':
    unittest.main()
