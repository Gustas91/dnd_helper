# DND Helper

## Introduction
- This is Gustas's coursework project. The goal was to create a project based on a topic that I chose that would meet all the requirements set by the coursework guide, which include: uploading my work to GitHub, implementing the 4 OOP pillars, using at least 2 design patterns, reading and writing from files, testing.
- My chosen topic is "Dungeons and Dragons Helper". This application would need to be a digital sheet creator, capable of creating and editing characters with names, classes and history. It would also need to edit their statistics and add health values, abilities and items to each character.  
- This application is titled "DND Helper". It allows users to easily create, modify, save and import characters with attributes that are commonly used in "Dungeons & Dragons" games.
- To run the program, download the code and run it through cmd by navigating to the folder where the code is located and typing in `python DNDHelper.py` or by using a code editor like Visual Studio Code.
- Upon running the program, a user interface will appear with several options that allow the user to choose what action they want to perform. These actions include:
1. Creating player characters;
2. Creating non player characters;
3. Printing current character names;
4. Printing character attributes;
5. Editing character attributes;
6. Exporting characters to text files;
7. Importing characters from text files;
8. Exiting the program.

To access these actions, the user must simply input a number corresponding to the action they want to do. Afterwards, the menu will write out what the next steps are and what the user needs to input to complete the command.

To import characters, the text file needs to be located in the **SAME** folder as the program. Exported characters are automatically placed into this folder. 

## Body/Analysis

- The program is designed to to manage and maintain multiple DND characters.
- The class `Character(ABC)` provides the framework for character attributes, abilities, items and health calculation. It inherits from the abstract base class `ABC` which allows it to define abstract methods within the class. The abstract base class `Character`
defines abstract methods such as `roll_dice()`, which rolls a die in order to find values for attribute statistics, and `calculate_health()`, which calculates the health points of any character, so that subclasses such as `PlayerCharacter` and `NPCCharacter` implement these methods but define them differently. This is called **Abstraction**, which
is used to hide irrelevant details from the user and show the details that are relevant to the users. Abstraction can also be seen in the class `CharacterSheetUI` as it provides an interface for interacting with characters while hiding the code logic from the user. This abstraction simplifies interactions between the user and the code,
promoting ease of use.

```
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
```

- Abstraction can also be seen in one of the design patterns used in this code, called **Factory method**. This pattern allows a class to create an object, but lets subclasses decide which class or object to create. Objects using this pattern are created without exposing the logic to the user. The factory method `create_character`
 provides a flexible mechanism for creating new characters. New types of characters can be easily added by extending the code without modifying existing code, which makes this design pattern particularly useful in this project, as there could be numerous different character types in a DND game.

```
class CharacterFactory:
    @staticmethod
    def create_character(character_type):
        if character_type == "Player":
            return PlayerCharacter()
        elif character_type == "NPC":
            return NPCCharacter()

class PlayerCharacter(Character):
    def __init__(self):
        super().__init__()
        self.attributes["Type"] = "Player"

class NPCCharacter(Character):
    def __init__(self):
        super().__init__()
        self.attributes["Type"] = "NPC"
```

- The subclasses `PlayerCharacter` and `NPCCharacter` both inherit attributes and methods from the class `Character`, which is a case of **Inheritance**. It allows you to inherit properties from a base class in order to establish relationships between classes. Inheritance provides reusability, as it removes the need to
  write the same code over and over again. In this example, classes `PlayerCharacter` and `NPCCharacter` inherit common attributes and behavior from the `Character` class, such as abilities, inventory management, and abstract methods like `roll_dice()` and `calculate_health()`. This reduces code duplication and promotes maintainability.
  `super()` is used to call methods defined in the parent class `Character` and in this case removes the need to rewrite the `__init__` method for subclasses.

```
  class PlayerCharacter(Character):
    def __init__(self):
        super().__init__()
  
   class NPCCharacter(Character):
    def __init__(self):
        super().__init__()
 ```
- Another OOP pillar called **Polymorphism** can be seen in these 2 subclasses. Polymorphism refers to methods or functions with the same name that can be executed on many objects or classes.
  Despite having a different implementation of calculating health points, the method name is the same. New character types can be easily added by creating subclasses of `Character` and providing implementations for the abstract methods.
  These new subclasses can seamlessly integrate with existing code that operates on `Character` objects. This promotes flexibility and extensibility in the code by allowing for the addition of new subclasses that adhere to the common interface.

```
  class PlayerCharacter(Character):
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
 
  class NPCCharacter(Character):
   def calculate_health(self):  
        self.health = self.roll_dice(10) + 5
        self.attributes["Health"] = self.health
```
- To manage all characters and their attributes, the **Singleton pattern** is used to ensure that only one instance of the class can exist throughout the program's execution. Class `CharacterManager` provides a centralized point for managing character objects across the entire application.
  All interactions with character objects, such as adding, editing, or exporting characters, are handled through the singleton instance, ensuring consistency and preventing potential conflicts that could arise from multiple instances managing characters independently.
  
```
  class CharacterManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.characters = []
        return cls._instance
```
- In this class there are multiple methods that do operations with the attribute `characters`, such as `add_character` and `get_characters`. This is an example of **Encapsulation**, which refers to the concept of bundling data and methods that operate on that data within a single unit, such as a class. However, encapsulation
  is not limited to this class, in fact, every class is an example of encapsulation in this code as they all encapsulate a set of attributes and methods related to a specific type of object. For example, the `Character` class encapsulates attributes such as attributes, abilities, and inventory and methods to work with these
  attributes like `add_ability` and `add_item`. Encapsulation in this instance hides the internal representation of a character's attributes, abilities, and inventory from outside of the class and users interact with character objects in a controlled manner without needing to access or manipulate the internal attributes directly.
  This helps prevent accidental modification of internal data.
  
```
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
```
- Class `CharacterManager` is responsible for **editing**, **exporting** and **importing** character text files. To edit character objects, it uses an interface that asks the user to write a number corresponding to the action they want to take. When editing attributes the program asks the user to input the name of the attribute in order to assign
  a new value to the chosen attribute.
  It is capable of editing every attribute, adding and removing abilities, items as well as exporting them for ease of use after editing. If the user wants to change abilities, the code can add them by using `add_ability` from the `Character` class and also remove them by using `del character.abilities[ability_name]`.
  The same code is used for items, except that the removal for items uses `remove` instead of `del` because it is a list and not a dictionary where the abilities are stored.

```
  class CharacterManager:
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

  def edit_attribute(self, character):
        attribute_to_edit = input("Enter the name of the attribute you want to edit: ")
        if attribute_to_edit in character.attributes:
            new_value = input(f"Enter the new value for {attribute_to_edit}: ")
            character.attributes[attribute_to_edit] = new_value
            print(f"{attribute_to_edit} has been updated to {new_value}.")
        else:
            print("Attribute not found.")
```
- To **export** characters, the code first retrieves the current directory where the python program is located using `os.path.dirname(os.path.abspath(__file__))`. This ensures that the exported file is located in the same folder as the program. `os.path.join()` is used to link the directory path with the filename, ensuring that filename is correctly
  appended to the directory path. Then it opens the file for writing using `open(full_path, "w")` and afterwards writes the chosen character's attributes, abilities and items in a structured manner.

```
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
```
- To **import** characters, the code first constructs the full path of the file to be imported. The code then opens the file with `open(full_path_ "r")`. The third line of the file is expected to contain the type of the character, either `Player` or `NPC`. This line is stripped of whitespace, split at `:` and the character type is extracted
  using `character_type = lines[2].strip().split(": ")[1]`. The imported files are iterated over and the data is added to the character object appropriately. The `current_section` tracks whether the method is adding attributes, abilities or items and depending on the section, the data is added differently. Once all the data has been
  gathered, the character object is added to the game.

```
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
```
- To make it easier to test different functionalities and to make the code more user friendly, a user interface was implemented in the class `CharacterSheetUI`. Once it starts, the `run()` method creates an interface where the user can choose various options that include adding, editing, exporting and importing characters.

```
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
```  
  
- When adding characters it uses methods `add_player_character()` and `add_npc()`, which refer to the main method of adding characters named `add_character`. This method utilizes the `CharacterFactory` to create the objects. During creation the program automatically rolls a 20 sided die for numerical attributes and asks for the user's input to add
  other attributes such as name, class, etc.
  It also provides the logic for calculating health differently depending on whether the character is a `Player` or an `NPC`.

```
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
```
- The print methods allow the interface to print out the names of all player characters and npc's and their attributes by selecting their index. It uses the method `get_characters()` from the class `CharacterManager`, which is an example of encapsulation.

```
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
```
- As for editing characters, the method `edit_character()` allows the user to edit characters based on their index.

```      
def edit_character(self):
        characters = self.character_manager.get_characters()
        index = int(input("Enter the index of the character to edit: ")) - 1
        if 0 <= index < len(characters):
            self.character_manager.edit_character(index)
        else:
            print("Invalid index.")
```
- Finally, the export and import methods `export_character()` and `import_character()` use methods that were programmed in the class `CharacterManager`.
  
```
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
```
- **DND_Test.py** is the code responsible for testing, specifically **unit testing**. Unit tests are segments of code written to test other pieces of code. With unittest framework, we can create test cases, fixtures, and suites to verify if our code behaves as expected.
  The class `TestCharacterManager` is responsible for testing whether or not characters are added, exported and imported correctly. The method `TearDownClass` deletes the exported test sheet, so that it does not clutter the folder with unnecessary files.
  `test_add_character` adds a player character and checks whether the `get_characters()` method gets the character's information. The import and export test methods function similarly, by creating mock characters and exporting as well as importing them.

```
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
```

 ## Results

- Overall, I believe that the objectives of the coursework were met: 4 OOP pillars were used and explained, the core functionality of the Dungeons and Dragons Helper was implemented successfully, 2 design patterns were used, importing and exporting files as well as
  testing these methods was programmed in.
- The program correctly creates DND characters with different attributes and statistics, edits these attributes and adds additional abilities or items to each character.
- The biggest challenge was having to learn Python independently and making sure that as the code progressed in development nothing started to break, because the scope of the project and it's capabilities kept increasing.

## Conclusion

- After completing this coursework I have gained important Python knowledge and I am more comfortable working independently with code.
- Implementing the 4 pillars of OOP taught me how to code efficiently and cleanly, while the design patterns challenged me to improve my code further.
- In the future it would be possible to add more character types to this program, maybe Boss characters or Creature characters with their specific attributes, health calculations or perhaps different sided dies to roll for these other characters. 
