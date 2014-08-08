# command prompt processing
import cmd
import sys
import pickle

import dialogue_engine
import inventory_engine


class engine_context:
    'Enumerated list of imput contexts'

    Default, DialogueChoice, InventoryManagement = range(3)


class testEngine(cmd.Cmd):
    intro = 'Welcome to the test. Type help or ? to list commands.\n'
    prompt = 'Enter a command -> '
    doc_header = 'GAME: Main Menu'
    current_scene = dialogue_engine.Scene()
    current_inventory = inventory_engine.inventory()
    current_context = 0

    def do_quit(self, arg):
        'Quit the game: QUIT'
        print('Exiting the game')
        return True

    def do_save(self, arg):
        'Saves progress: SAVE'
        try:
            with open('scene_' + arg + '.pickle', 'wb') as f:
                pickle.dump(self.current_scene, f)
            print('Test saved to slot ' + arg + '.')
        except IOError:
            print('Unable to save your test.')
        except:
            print(sys.exc_info()[0])

    def do_load(self, arg):
        'Loads the test from a save file: LOAD'
        try:
            with open('scene_' + arg + '.pickle', 'rb') as f:
                self.current_scene = pickle.load(f)
            print('Test loaded.')
        except IOError:
            print("Can't find that file.")
        except:
            print(sys.exc_info()[0])

    def do_play(self, arg):
        'Plays a specific scene: PLAY'
        try:
            self.current_scene.load_scene('scene_' + arg + '.xml')
            output, output_type = self.current_scene.play_scene()
            self.render_action(output, output_type)
        except IOError:
            print("Can't find that scene.")
        except:
            print(sys.exc_info()[0])

    def do_goto(self, arg):
        'Moves to a specific action in a loaded scene: GOTO'
        pass

    def render_action(self, output, output_type):
        if output_type == dialogue_engine.ActionType.Line:
            print(output)
            self.current_context = engine_context.Default
            self.prompt = 'Enter a command -> '
        elif output_type == dialogue_engine.ActionType.Choice:
            print(output)
            self.current_context = engine_context.DialogueChoice
            self.prompt = 'Choose -> '
        else:
            print('FIN\n')

    def move_next(self):
        'Moves to the next element of the scene.'
        output, output_type = self.current_scene.move_next()
        self.render_action(output, output_type)

    def do_inventory(self, arg):
        "Displays the contents of the main character's inventory: INVENTORY"
        print('Inventory List:\n')

        if len(self.current_inventory.keys()) == 0:
            print('No items.\n')
        else:
            for i in self.current_inventory.keys():
                print(self.current_inventory[i].name + ' - ' + self.current_inventory[i].description + ' x' + str(
                    self.current_inventory[i].quantity) + '\n')

        print('Total weight:' + str(self.current_inventory.get_total_weight()))
        self.current_context = engine_context.InventoryManagement
        self.prompt = 'Inventory -> '

    def make_choice(self, line):
        'Chooses between two or more actions'
        choice = line.split()
        output, output_type = self.current_scene.make_choice(choice[0])
        self.render_action(output, output_type)

    def inventory_commands(self, line):
        'Handles inventory managment commands'
        inventory_command_list = line.split()

        if inventory_command_list[0].lower() == 'drop':
            print('item dropped')
        elif inventory_command_list[0].lower() == 'exit':
            self.current_context == engine_context.Default
            self.prompt = 'Enter a command -> '
        else:
            self.current_context == engine_context.Default
            self.prompt = 'Enter a command -> '

    def default(self, line):
        if self.current_context == engine_context.Default:
            self.move_next()
        elif self.current_context == engine_context.DialogueChoice:
            self.make_choice(line)
        elif self.current_context == engine_context.InventoryManagement:
            self.inventory_commands(line)
        else:
            print('"' + line + '" is not a valid command. Type help or ? to list commands.\n')

    def precmd(self, line):
        line = line.lower()
        return line

    def emptyline(self):
        if self.current_context == engine_context.Default:
            self.move_next()
        elif self.current_context == engine_context.InventoryManagement:
            self.inventory_commands('exit')
        else:
            print('Type help or ? to list commands.\n')


if __name__ == '__main__':
    testEngine().cmdloop()
