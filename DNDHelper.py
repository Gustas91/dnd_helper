import random
from abc import ABC, abstractmethod
import os
class CharacterManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.characters = []
        return cls._instance

    def add_character(self, character):
        self.characters.append(character)

    def get_characters(self):
        return self.characters     

    def edit_character(self, index):
        character = self.characters[index]
        while True:
            print("\n1. Edit attributes")
            print("2. Add ability")
            print("3. Remove ability")
            print("4. Add item")
            print("5. Remove item")
            print("6. Export character")
            print("7. Done editing")
            edit_choice = input("Choose an option: ")

            if edit_choice == "1":
                self.edit_attribute(character)
            elif edit_choice == "2":
                ability_name = input("Enter ability name: ")
                description = input("Enter ability description: ")
                character.add_ability(ability_name, description)
            elif edit_choice == "3":
                ability_name = input("Enter ability name to remove: ")
                if ability_name in character.abilities:
                    del character.abilities[ability_name]
                    print(f"{ability_name} has been removed.")
                else:
                    print("Ability not found.")
            elif edit_choice == "4":
                item_name = input("Enter item name: ")
                character.add_item(item_name)
            elif edit_choice == "5":
                item_name = input("Enter item name to remove: ")
                if item_name in character.inventory:
                    character.inventory.remove(item_name)
                    print(f"{item_name} has been removed from inventory.")
                else:
                    print("Item not found in inventory.")
            elif edit_choice == "6":
                self.export_character(character)
            elif edit_choice == "7":
                break
            else:
                print("Invalid option. Please try again.")

    def export_character(self, character):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        print("Exporting to:", current_directory)
        filename = f"{character.attributes['Name']}_character_sheet.txt"
        full_path = os.path.join(current_directory, filename)
        with open(full_path, "w") as file:
            file.write(f"Character Sheet for {character.attributes['Name']}:\n")
            file.write("Attributes:\n")
            for attribute, value in character.attributes.items():
                file.write(f"{attribute}: {value}\n")
            file.write("\nAbilities:\n")
            for ability, description in character.abilities.items():
                file.write(f"{ability}: {description}\n")
            file.write("\nInventory:\n")
            for item in character.inventory:
                file.write(f"{item}\n")
        print(f"Character sheet for {character.attributes['Name']} exported to {filename}.")

    def import_character(self, filename):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_directory, filename)
        try:
            with open(full_path, "r") as file:
             lines = file.readlines()
        except FileNotFoundError:
            print("File not found")
            self.handle_file_not_found()
            return     

        character_type = lines[2].strip().split(": ")[1]
         
        if character_type == "Player":
         character = PlayerCharacter()
        elif character_type == "NPC":
         character = NPCCharacter()
        else:
         raise ValueError("Invalid character type")

        current_section = None
        for line in lines:
            line = line.strip()
            if line == "Attributes:":
                current_section = "Attributes"
            elif line == "Abilities:":
                current_section = "Abilities"
            elif line == "Inventory:":
                current_section = "Inventory"
            elif current_section == "Attributes":
                attribute_data = line.split(": ", 1)
                if len(attribute_data) == 2:
                    attribute, value = attribute_data
                    character.attributes[attribute] = value
            elif current_section == "Abilities":
                ability_data = line.split(": ", 1)
                if len(ability_data) == 2:
                    ability, description = ability_data
                    character.abilities[ability] = description
            elif current_section == "Inventory":
                character.inventory.append(line) 

        self.add_character(character)
        print(f"Character {character.attributes['Name']} imported successfully.")

    def handle_file_not_found(self):
        while True:
          choice = input("Do you want to try importing another file? (yes/no): ")
          if choice.lower() == "yes":
            filename = input("Enter the filename to import: ")
            self.import_character(filename)
            break
          elif choice.lower() == "no":
            return
          else:
            print("Invalid choice. Please enter 'yes' or 'no'.")    

    def edit_attribute(self, character):
        attribute_to_edit = input("Enter the name of the attribute you want to edit: ")
        if attribute_to_edit in character.attributes:
            new_value = input(f"Enter the new value for {attribute_to_edit}: ")
            character.attributes[attribute_to_edit] = new_value
            print(f"{attribute_to_edit} has been updated to {new_value}.")
        else:
            print("Attribute not found.")


class Character(ABC):  
    def __init__(self):
        self.attributes = {
            "Type": None,
            "Name": None,
            "Class": None,
            "Level": None,
            "Background": None,
            "Player name": None,
            "Race": None,
            "Alignment": None,
            "Experience points": None,
            "Strength": None,
            "Dexterity": None,
            "Constitution": None,
            "Intelligence": None,
            "Wisdom": None,
            "Charisma": None,
            "Health": None,
        }
        self.abilities = {}
        self.inventory = []

    @abstractmethod
    def roll_dice(self, sides):
        pass

    @abstractmethod
    def calculate_health(self):
        pass

    def add_ability(self, ability_name, description):
        self.abilities[ability_name] = description

    def add_item(self, item_name):
        self.inventory.append(item_name)

class NPCCharacter(Character):
    def __init__(self):
        super().__init__()
        self.attributes["Type"] = "NPC"

    def roll_dice(self, sides):  
        return random.randint(1, sides)

    def calculate_health(self):  
        self.health = self.roll_dice(10) + 5
        self.attributes["Health"] = self.health

class PlayerCharacter(Character):
    def __init__(self):
        super().__init__()
        self.attributes["Type"] = "Player"

    def roll_dice(self, sides):  
        return random.randint(1, sides)

    def calculate_health(self):  
        char_class = self.attributes["Class"]
        if char_class in ["Wizard", "Sorcerer"]:
            self.health = self.roll_dice(6) + 6
        elif char_class in ["Artificer", "Bard", "Cleric", "Druid", "Monk", "Rogue", "Warlock"]:
            self.health = self.roll_dice(8) + 8
        elif char_class in ["Fighter", "Paladin", "Ranger"]:
            self.health = self.roll_dice(10) + 10
        elif char_class == "Barbarian":
            self.health = self.roll_dice(12) + 12 
        else:
            self.health = self.roll_dice(20) + 8
        self.attributes["Health"] = self.health

class CharacterFactory:
    @staticmethod
    def create_character(character_type):
        print(f"Creating character of type: {character_type}")
        if character_type == "Player":
            return PlayerCharacter()
        elif character_type == "NPC":
            return NPCCharacter()

class CharacterSheetUI:
    def __init__(self):
        self.character_manager = CharacterManager()
        self.character_factory = CharacterFactory()

    def run(self):
        while True:
            print("\n1. Add a player character")
            print("2. Add an NPC")
            print("3. Print character names")
            print("4. Print character attributes")
            print("5. Edit character")
            print("6. Export character")
            print("7. Import character")
            print("8. Exit")
            choice = input("Choose an option: ")
            if choice == "1":
                self.add_player_character()
            elif choice == "2":
                self.add_npc()
            elif choice == "3":
                self.print_character_names()
            elif choice == "4":
                self.print_character_attributes()
            elif choice == "5":
                self.edit_character()
            elif choice == "6":
                self.export_character()
            elif choice == "7":
                self.import_character()
            elif choice == "8":
                break
            else:
                print("Invalid option. Please try again.")

    def add_player_character(self):
        self.add_character("Player")

    def add_npc(self):
        self.add_character("NPC")

    def add_attribute(self, character, attribute_name):
        if attribute_name in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
            new_value = character.roll_dice(20)
            print(f"{attribute_name} rolled a {new_value}!")
        else:
            new_value = input(f"Write {attribute_name}: ")
        character.attributes[attribute_name] = new_value   

    def calculate_health(self, character):
        if character.attributes["Type"] == "Player":
            player_character = PlayerCharacter()
            player_character.attributes = character.attributes
            player_character.calculate_health()
            character.attributes["Health"] = player_character.attributes["Health"]
        else:
            npc_character = NPCCharacter()
            npc_character.attributes = character.attributes
            npc_character.calculate_health()
            character.attributes["Health"] = npc_character.attributes["Health"]

    def add_character(self, character_type):
     character = self.character_factory.create_character(character_type)
     for attribute in character.attributes.keys():
        if attribute not in ["Health", "Type"]:
            self.add_attribute(character, attribute)
        elif attribute == "Health":
            self.calculate_health(character)
     while True:
        ability_choice = input("Do you want to add abilities for this character? (yes/no): ")
        if ability_choice.lower() == "yes":
            ability_name = input("Enter ability name: ")
            description = input("Enter ability description: ")
            character.add_ability(ability_name, description)
        elif ability_choice.lower() == "no":
            break
     while True:
        item_choice = input("Do you want to add items to this character's inventory? (yes/no): ")
        if item_choice.lower() == "yes":
            item_name = input("Enter item name: ")
            character.add_item(item_name)
        elif item_choice.lower() == "no":
            break
     self.character_manager.add_character(character)
 
    def print_character_names(self):
     characters = self.character_manager.get_characters()
     print("Player Characters:")
     for index, character in enumerate(characters):
        if character.attributes["Type"] == "Player":
            print(f"{index + 1}. {character.attributes['Name']}")
     print("\nNPCs:")
     for index, character in enumerate(characters):
        if character.attributes["Type"] == "NPC":
            print(f"{index + 1}. {character.attributes['Name']}")

    def print_character_attributes(self):
        characters = self.character_manager.get_characters()
        index = int(input("Enter the index of the character: ")) - 1
        if 0 <= index < len(characters):
            character = characters[index]
            print(f"\nAttributes for {character.attributes['Name']}:")
            for attribute, value in character.attributes.items():
                print(f"{attribute}: {value}")
            print("\nAbilities:")
            for ability, description in character.abilities.items():
                print(f"{ability}: {description}")
            print("\nInventory:")
            for item in character.inventory:
                print(item)
        else:
            print("Invalid index.")

    def edit_character(self):
        characters = self.character_manager.get_characters()
        index = int(input("Enter the index of the character to edit: ")) - 1
        if 0 <= index < len(characters):
            self.character_manager.edit_character(index)
        else:
            print("Invalid index.")

    def export_character(self):
        characters = self.character_manager.get_characters()
        index = int(input("Enter the index of the character to export: ")) - 1
        if 0 <= index < len(characters):
            self.character_manager.export_character(characters[index])
        else:
            print("Invalid index.")

    def import_character(self):
        filename = input("Enter the filename to import: ")
        self.character_manager.import_character(filename)


def main():
    try:
        ui = CharacterSheetUI()
        ui.run()
    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
 main()
