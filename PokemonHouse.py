import cmd  # for user input/testing
import numpy as np  # generate random number from 0-4
import sys  # to stop the program when you win


class ParseConfig:
    room_num = {}  # format will be: {#number : Room Name}
    default_room_description = {}  # format will be: {Room Name: Room Description}
    doors = {}  # format will be: {starting_room : [[direction, end_room, door status], [direction, end_room, door status]]}
    items = {}  # format will be: {item name : [room location, type of item, optional command]} 'MOVE']}
    item_description = {}  # format will be: {item name : item description}
    start_room = 0
    # door_exits
    with open("C:\\Users\\User\\PokemonHouse\\house_description.txt") as file:  # read in house_description file
        for line in file:  # iterate over each line
            if not line.startswith('#') and not line.startswith('\n'):  # exclude parsing of # or new lines
                temp = line[5:]  # all categories (rooms, doors, item) begin their information after the 5th element

                # to make inner dict of room name:room description
                if line.startswith('room'):
                    default_room_description[temp.partition(':')[0]] = temp.partition(':')[2].strip()

                # parse doors
                elif line.startswith('door'):
                    line = line.split()  # separate the line/sentence into list of words
                    line.pop(0)  # remove the first index which will just be "door"
                    temp_room = line[
                        3]  # to hold name of the room to compare if we've already made a key for it in the dict.
                    if temp_room in doors:  # check to see if the room is already in the dict
                        doors[temp_room].append([line[0], line[4], line[
                            2]])  # if so - append new door-pathway information onto the nested lists. ex: 'Bedroom': [['up1', 'Library', 'closed'], ['up2', 'Hall', 'open'], ['right', 'Bathroom', 'locked']]
                    else:
                        doors[line[3]] = [[line[0], line[4], line[
                            2]]]  # else - makes new dict entry. ex: 'Bedroom': [['up1', 'Library', 'closed']]

                # parse items
                elif line.startswith('item'):
                    temp = line.partition(':')  # to preserve item description (last index)

                    line = temp[0]  # everything before item description is in index[0]
                    line = line.split()  # split into list
                    #                     ['item', 'key', 'Library', 'USE', 'unlock']
                    #                     ['item', 'carpet', 'Living', 'MOVE']
                    # item_name = line[1] #save name of item (which is at index[1])
                    # items[line[1]] =
                    items[line[1]] = line[2:]
                    # items[line[1]] = [line[2], line[3],  #in dict - name of item is assigned as KEY: list of it's characteristics is VALUE. ex.: 'key': ['Living', 'USE', 'unlock']

                    item_description[line[1]] = temp[2].strip()  # store description into dict.

                # to get bedroom as the starting room
                elif line.startswith('start'):
                    start_room = line.split()[1]
                    # print(start_room)

    # to send inner dict of room name/room description as value of outter dict, which has int as keys
    room_count = 0
    for room in default_room_description:
        room_num[room_count] = room
        room_count += 1
    #     for key, value in default_room_description.items():
    #         room_num[room_count] = {key : value}
    #         room_count += 1

    # connect the items to where they are in the rooms
    default_items_in_rooms = {}  # new dict for where items are initially
    # go through list of items and if their location name matches a room name then make new dict entry with room name as key and item name as value
    # room description is basically dict of rooms, with room names as keys
    for room in default_room_description:
        for item, location in items.items():
            if room in location:
                if room in default_items_in_rooms:
                    temp_list = [default_items_in_rooms[room]]
                    temp_list.append(item)
                    default_items_in_rooms[room] = temp_list
                else:
                    default_items_in_rooms[room] = item
    # for room in doors:

    # now we have: 1) rooms with IDs & their names with descriptions 2) room names with description, 3) doors in each room with possible directions, neighboring rooms, status of door
    # 4) items with their location, type and optional commands 5) default location of items
    # print(f'room number - {room_num}\n\ndefault room description - {default_room_description}\n\ndoors - {doors}\n\nitems - {items}\n\ndefault item locations - {default_items_in_rooms}\n\nitem descriptions - {item_description}')
    print(room_num)


class Game(cmd.Cmd):
    # the few class variables we'll be using to affect the commnds later on:
    COMMANDS = {'go', 'take', 'release', 'open', 'open', 'show', 'holding', 'quit', 'shake',
                'unlock'}  # legal commands in this game
    directions = ['north', 'south', 'east', 'west']  # legal directions for 'go', 'open', & 'unlock' commands
    opposite_directions = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
    # start_room = ParseConfig.start_room
    inventory = []
    location = "Bedroom"

    # count = 0

    def __init__(self, room_numbers, default_room_description, doors, items, default_items_in_rooms, item_description):
        cmd.Cmd.__init__(self)
        self.items = {}
        self.rooms = {}
        self.count = 0

        # to populate self.items with items and if they're move/use/stationary
        for item in ParseConfig.items:
            if "STATIONARY" not in ParseConfig.items[item]:  # for use and move items
                if "USE" in ParseConfig.items[item]:  # for use items
                    self.items[item] = Items_Use(item, ParseConfig.items[item][2])
                else:  # for move only items
                    self.items[item] = Items_Move(item)
            else:  # for stationary items
                self.items[item] = Items(item)

        for room_name in default_room_description:  # creating objects of rooms
            if room_name in default_items_in_rooms:  # create room if the room has item
                # if room has 1 door
                if len(doors[room_name]) == 1:
                    self.rooms[room_name] = Rooms(room_name, doors[room_name][0][0], doors[room_name][0][1],
                                                  doors[room_name][0][2], default_room_description[room_name],
                                                  default_items_in_rooms[
                                                      room_name])  # passing in room name, doors, items
                # doors - Bathroom': [['west', 'Bedroom', 'open'], ['north', 'Kitchen', 'open'], ['east', 'Living', 'closed']],
                else:  # if room has more than 1 door
                    direction_list = []
                    next_rooms_list = []
                    statuses = []
                    for i in doors[room_name]:
                        direction_list.append(i[0])
                        next_rooms_list.append(i[1])
                        statuses.append(i[2])
                    self.rooms[room_name] = Rooms(room_name, direction_list, next_rooms_list, statuses,
                                                  default_room_description[room_name], default_items_in_rooms[
                                                      room_name])  # passing in room name, doors, items
            else:  # if the room doesn't have any items in it
                if len(doors[room_name]) == 1:  # if room has 1 door
                    self.rooms[room_name] = Rooms(room_name, doors[room_name][0][0], doors[room_name][0][1],
                                                  doors[room_name][0][2], default_room_description[room_name])
                else:  # if room has more than 1 door
                    direction_list = []
                    next_rooms_list = []
                    statuses = []
                    for i in doors[room_name]:
                        direction_list.append(i[0])
                        next_rooms_list.append(i[0])
                        statuses.append(i[2])
                    self.rooms[room_name] = Rooms(room_name, doors[room_name][0][0], doors[room_name][0][1],
                                                  doors[room_name][0][2],
                                                  default_room_description[room_name])  # passing in room name, doors
        # self.location = "Bedroom"
        # print(self.rooms)
        # print(self.rooms[room_name].name, self.rooms[room_name].door_direction, self.rooms[room_name].next_room, self.rooms[room_name].door_status, self.rooms[room_name].description, self.rooms[room_name].items)
        # self.location = "Library" #ParseConfig.start_room#"Library"#ParseConfig.start_room
        # print(len(doors["Bathroom"]))
        s = " "
        print(f"{self.rooms[self.location].description} Item(s) in this room: {self.rooms[self.location].items}.")

    # while True:
    # default command when user inputs an unvalid command
    def default(self, arg):
        print(
            "I do not understand that command. Type 'help' or 'commands' or 'help' for a list of specific commands or general general commands, respectively.")

    # MAIN METHODS
    # no need for if statement to check if user inputted valid command. cmd library will give SyntaxError and the game won't crash
    def do_go(self, args):
        # pseudo-code as a guideline:
        # directions = ['north', 'south', 'east', 'west']
        # if input is right ---
        # if that's a door in the room ---
        # if the room has 1 door
        # if the door is open
        # update self.location and show new room
        # elif the door is closed
        # print the door is closed
        # else the only other option is the door is the specially locked door that needs the key
        # update self.location to next room
        # if that door is open
        # update location, show room
        # else:
        # if door is closed
        # the door is closed, put the command open dir to open it
        # else: the door is locked. print this door is locked and may require a key
        # else: that's not an exit in this room, show room ---
        # else: that's not a direction, show room ---

        print(self.rooms["Bathroom"].name, self.rooms["Bathroom"].door_direction, self.rooms["Bathroom"].next_room,
              self.rooms["Bathroom"].door_status, self.rooms["Bathroom"].description, self.rooms["Bathroom"].items)
        print(self.rooms[self.location].items)
        args = args.lower().strip()
        if args in self.directions:  # if that's a possible direction
            print("yes1")
            if args in self.rooms[self.location].door_direction:
                print("yes2")
                door_index = self.rooms[self.location].door_direction.index(args)
                print(door_index)
                print(self.rooms[self.location].door_status[door_index])
                if self.rooms[self.location].door_status[door_index] == 'open':
                    print("yes3")
                    self.location = self.rooms[self.location].next_room[door_index]  # update location to next room
                    self.do_show(self.location)  # show description of new room you've just entered
                elif self.rooms[self.location].door_status[door_index] == 'closed':
                    print("yes4")
                    print("This door is closed and needs to be opened.")
                elif self.rooms[self.location].door_status[door_index] == 'locked':
                    print("yes5")
                    if "key" in self.inventory:
                        print("Use the command 'unlock' with the direction of the door to unlock this door.")
                    else:
                        print("yes9")
                        print("This door is locked.")
            else:
                print("yes10")
                print("That is not a direction in this room.")
        else:
            print("yes11")
            print("That is not a direction.")

    def do_open(self, args):
        args = args.lower().strip()
        # pseudo-code as a guideline:
        # check if it's a real door in the room ---
        # check if that door is closed ---
        # if so then change door status of the door ---
        # else: (if the door isn't closed then it can be either OPEN or LOCKED)
        # if door is open:
        # print that door is opened
        # else: that door is locked
        # else: that's not a door in this room
        if args in self.rooms[self.location].door_direction:
            door_index = self.rooms[self.location].door_direction.index(args)
            if self.rooms[self.location].door_status[door_index] == 'closed':
                self.rooms[self.location].door_status[door_index] = 'open'  # change the status of the door to open

                # you also need to change the status of the door on the "other" side to open, if you want to come back!
                corresponding_room = self.rooms[self.location].next_room[
                    door_index]  # should be = Library if you opened Bedroom's north door
                corresponding_door = self.opposite_directions[args]
                opposite_door = self.rooms[corresponding_room].door_direction.index(
                    corresponding_door)  # index of door you're entering in new room's list
                self.rooms[corresponding_room].door_status[opposite_door] = 'open'
                print("The door has been opened. You can now enter with the 'go' command.")
            else:
                if self.rooms[self.location].door_status[door_index] == 'open':
                    print("That door is already open. You can enter it using the 'go' command.")
                else:  # door must be locked
                    print("That door is locked. To enter this room you require more than the 'open' command.")
        else:
            print("That is not a door in this room.")

    def do_take(self, args):
        args = args.lower().strip()
        # if it's an item
        # if the item is in the room
        # if you can take the item (if item is of type move)
        # add item to inventory
        # remove item from room
        # print added item to inventory
        # else: print you can't move that item
        # else: print that isn't an item in this room.
        # else: print that's not an item
        if args in self.items:  # if the item is real
            if args in self.rooms[self.location].items:  # if you're in the right room
                if self.items[args].can_move == True:
                    self.inventory.append(args)
                    self.rooms[self.location].items.remove(args)
                    print(f"You have added {args} to your inventory!")
                else:
                    print("You cannot take that item. It is stationary.")
            else:
                print("That is not an item in this room.")
        else:  # the item isn't real
            print("That is not an item.")

    def do_release(self, args):
        args = args.lower().strip()
        # if it's an item
        # if the item is in your inventory
        # put item in self.location.items
        # remove item from inventory
        # show new inventory
        # else: print that isn't in your inventory
        # else: print that's not an item
        if args in self.items:
            if args in self.inventory:
                print(f"You dropped the {args} in this room. The room now has the following item(s): ")
                self.rooms[self.location].items.append(args)
                print(self.rooms[self.location].items)
                self.inventory.remove(args)
                self.do_holding(self)
            else:
                print("That is not in your inventory.")
        else:
            print("That is not an item.")

    def do_show(self, args):
        # print out description of room
        print(f"{self.rooms[self.location].description} Item(s) in this room: {self.rooms[self.location].items}.")

    def do_holding(self, args):
        if self.inventory:  # show your inventory if you have anything
            print(f"You have the following item(s) in your inventory: {self.inventory}")
        else:  # otherwise print that you don't have anything yet
            print("Nothing in your inventory yet.")

    def do_quit(self, args):
        print("Thanks for playing! Come again!")  # end of game
        return True

    # this will allow you to teleport to any random room OTHER than the Pantry where Pikachu is.
    def do_shake(self, args):
        random_room = np.random.randint(0,
                                        high=5)  # high parameter is exclusive, 5 is the ID for Pantry in the room_num variable we parsed in the ParseConfig class.
        if 'teleporter' in self.inventory:
            print("The teleporter in your inventory is making a loud noise! SpaCE iS cOlLApsiNg iN oN iTSeLF.!;./,")
            self.location = ParseConfig.room_num[random_room]
            self.do_show(self)
        else:
            print("You do not have the means for this command... yet.")

    def do_unlock(self, args):
        args = args.lower().strip()
        # if key is in your inventory
        # if args is north and self.location is Living room
        # Living room north door status = open
        # print you can go now print("This special door has been unlocked! Go ahead, Pokemon Trainer!")
        # else: print this isn't something to unlock
        # else: print you dont have the means for this command... yet
        if 'key' in self.inventory:
            if args == 'north' and self.location == 'Living':
                door_index = self.rooms[self.location].door_direction.index(
                    args)  # to get index of north door for Living room
                self.rooms[self.location].door_status[door_index] = 'open'
                print("This door has been unlocked!")
                if 'stone' in self.inventory:
                    print(self.rooms[
                              "Pantry"].description + "\nWa-Wait... something is happening?! The stone you are carying is starting to glow! It is a Thunder Stone! It is causing Pikachu to evolve! Congratulations, your Pikachu has evolved into a Raichu!")
                    sys.exit(0)
                else:
                    print(self.rooms["Pantry"].description)
                    sys.exit(0)
        else:
            print("You do not have the means for this command... yet.")

    def do_info(self, args):  # prints info on the item (args)
        # if args is an item
        # if the item is in your current room or in your inventory
        # else: that's not an item

        # item_description = {} #format will be: {item name : item description}
        if args in ParseConfig.items:
            if args in self.rooms[self.location].items or args in self.inventory:
                print(ParseConfig.item_description[args])
        else:
            print(f"{args} is not an item.")

    def do_commands(self, args):
        args = args.lower().strip()
        # required by assignment
        print("\nHere are the following commands & directions you can use to help you find Pikachu:")
        print("'go DIR' - to move to the room in direction DIR, if there is an open door in that direction")
        print(
            "'take ITEM' - let's you take the item ITEM if it's in the same room as you, and the ITEM isn't STATIONARY. The ITEM will be held by you, and no longer available in the room.")
        print(
            "'release ITEM' - let's you release item ITEM, if it's being held. The ITEM will then be in the room you're currently in, and won't be held by you.")
        print(
            "'open DIR' - opens the door in direction DIR in the current room, if there's such a door, and if that door is closed.")
        print(
            "'show' - describes the room you're currently in, i.e., gives the room's name, lists the doors, and the available items, if any.")
        print("'commands' - lists all available commands in the game")
        print("'holding' - lists all the items you're currently holding.")
        print("'quit' - ends the game")
        print("'info ITEM' - provides you with a describe of an item in the room or in your inventory")

        # extra 2 commands - that REQUIRE the player to hold an ITEM
        print("'shake ITEM' - to violently shake *ITEM*, maybe something will happen ;)")  # to activate the teleporter
        print("'unlock DIR' - to unlock a specially locked door")  # to use key to open the specially locked door

        # movement
        print("\n'north' - to move north")
        print("'south' - to move south")
        print("'east' - to move east")
        print("'west' - to move west")


# the basis for all items, default will be for stationary items
class Items():
    def __init__(self, name):
        self.name = name
        self.can_move = False


# for items that can move
class Items_Move(Items):
    def __init__(self, name):
        super().__init__(name)  # inherit from Items super-class
        self.can_move = True


# for items that can be used (i.e. with a command)
class Items_Use(Items):
    def __init__(self, name, command):
        super().__init__(name)  # inherit from Items super-class
        self.can_move = True
        self.command = command


# all room types in the game
class Rooms():
    def __init__(self, name, door_direction, next_room, door_status, description, items=None):
        self.name = name
        self.door_direction = door_direction
        self.next_room = next_room
        self.door_status = door_status
        self.description = description
        self.items = []
        self.items.append(items)


if __name__ == "__main__":
    print('Welcome to the Pokemon House! Your job is to find your missing Pikachu! Type "commands" for general help.\n')
    parse = ParseConfig()
    g = Game(parse.room_num, parse.default_room_description, parse.doors, parse.items, parse.default_items_in_rooms,
             parse.item_description)
    g.cmdloop()
