#def get_room() was made to parse the house description and put them in variables we can pass into classes later
def start():
    room_num = {}  # format will be: {#number : {Room Name: Room Description}, {}, {}, etc.}
    room_description = {}  # format will be: {Room Name: Room Description}
    doors = {}  # format will be: {starting_room : [[direction, end_room, door status], [direction, end_room, door status]]}
    items = {}  # format will be: {item name : [room location, type of item, optional command]} 'MOVE']}
    item_description = {}  # format will be: {item name : item description}
    with open("Users/User/PokemonHouse/house_description.txt") as file:  # read in house_description file
        for line in file:  # iterate over each line
            if not line.startswith('#') and not line.startswith('\n'):  # exclude parsing of # or new lines
                temp = line[5:]  # all categories (rooms, doors, item) begin their information after the 5th element

                # to make inner dict of room name:room description
                if line.startswith('room'):
                    room_description[temp.partition(':')[0]] = temp.partition(':')[2].strip()

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
                    item_name = line[1]  # save name of item (which is at index[1])
                    items[item_name] = line[
                        2]  # in dict - name of item is assigned as KEY: list of it's characteristics is VALUE. ex.: 'key': ['Living', 'USE', 'unlock']

                    item_description[item_name] = temp[2].strip()  # store description into dict.

    # to send inner dict of room name/room description as value of outter dict, which has int as keys
    room_count = 0
    for key, value in room_description.items():
        room_num[room_count] = {key: value}
        room_count += 1

    # connect the items to where they are in the rooms
    default_items_in_rooms = {}  # new dict for where items are initially
    # go through list of items and if their location name matches a room name then make new dict entry with room name as key and item name as value
    # room description is basically dict of rooms, with room names as keys
    for room in room_description:
        for item, location in items.items():
            if room in location:
                if room in default_items_in_rooms:
                    temp_list = [default_items_in_rooms[room]]
                    temp_list.append(item)
                    default_items_in_rooms[room] = temp_list
                else:
                    default_items_in_rooms[room] = item

                    # now we have: 1) rooms with IDs & their names with descriptions 2) room names with description, 3) doors in each room with possible directions, neighboring rooms, status of door
                # 4) items with their location, type and optional commands 5) default location of items
    print(
        f'room number - {room_num}\n\nroom description - {room_description}\n\ndoors - {doors}\n\nitems - {items}\n\ndefault item locations - {default_items_in_rooms}\n\nitem descriptions - {item_description}')


class Room:
    def __init__(self, name):
        self.name = name

class Items:
    def __init__(self, name, room, type, effect):
        self.name = name
        self.room = room
        self.type = type
        self.effect = effect

class Doors:
    def __init__(self, status, current_room, end_room):
        self.status = status
        self.current_room = current_room
        self.end_room = end_room

class PokeHouse:
    def __init__(self):
        pass

    def play(self, opening_message = "Welcome to the Pokemon House, where you'll try to find Pikachu."):
        print(opening_message)
        self.help()

    def help(self):
        #required by assignment
        print("Here are the following commands you can use to help you find Pikachu:")
        print("'go DIR' - to move to the room in direction *DIR*, if there is n open door in that direction")
        print("'take ITEM' - let's you take the item ITEM if it's in the same room as you, and the ITEM isn't STATIONARY. The ITEM will be held by you, and no longer available in the room.")
        print("'release ITEM' - let's you release item ITEM, if it's being held. The ITEM will then be in the room you're currently in, and won't be held by you.")
        print("'open DIR' - opens the door in direction DIR in the current room, if there's such a door, and if that door is closed.")
        print("'show' - describes the room you're currently in, i.e., gives the room's name, lists the doors, and the available items, if any.")
        print("'commands' - lists all available commands in the game")
        print("'holding' - lists all the items you're currently holding.")
        print("'quit' - ends the game")

        #extra 2 commands - that REQUIRE the player to hold an ITEM
        print("'shake ITEM' - to violently shake the item *ITEM*, maybe something will happen :)") #to activate the teleporter
        print("'unlock DIR' - to unlock a specially locked door") #to use key to open the specially locked door

        #movement
        print("'up' - to move up")
        print("'up1' - to move to the first door ahead of you if you're in a room with 2 doors.")
        print("'up1' - to move to the second door ahead of you if you're in a room with 2 doors.")
        print("'down' - to move down")
        print("'right' - to move right")
        print("'left' - to move left")


import cmd
import json


def get_room(name):
    ret = None
    with open("house_description.txt") as file:
        starting_point = ''
        for line in file:
            line = line.partition('#')[0]
            line = line.rstrip()
            line = line.split(' ')
            if line[0] == 'start':
                starting_point = line[1]
                name = starting_point
                exits = {"up": "Library", "down": "Hall", "left": "Bathroom"}
                ret = Room(exits=exits)
    return ret


class Room:
    def __init__(self, name="Bedroom", description="This is a bedroom.", exits={}):
        self.name = name
        self.description = description
        self.exit = exit

    def exit(self, direction):
        if direction in self.exit:
            return self.exit[direction]
        else:
            return None

    def up(self):
        return self.exit('up')

    def down(self):
        return self.exit('down')

    def left(self):
        return self.exit('left')

    def right(self):
        return self.exit('right')


class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.loc = get_room('Bedroom')
        self.look()

    def move(self, dir):
        newroom = self.loc.exit(dir)
        if newroom is None:
            print("You can't go that way. Try another direction.")
        else:
            self.loc = get_room(newroom)
            self.look()

    def look(self):
        print(self.loc.name)
        print("")
        print(self.loc.description)

    def do_up(self, args):
        self.move('up')

    def do_down(self, args):
        self.move('down')

    def do_left(self, args):
        self.move('left')

    def do_right(self, args):
        self.move('right')

    def do_quit(self, args):
        print("Thank you for playing!")
        return True


if __name__ == "__main__":
    g = Game()
    g.cmdloop()

#####
def get_room():
    i = 0
    room_num = {}
    room_description = {}
    with open("Users/User/PokemonHouse/house_description.txt") as file:
        for line in file:
            # to parse rooms
            if not line.startswith('#') and not line.startswith('\n'):
                # or line.startswith('door') or line.startswith('item'):
                temp = line[5:]
                if line.startswith('room'):
                    room_description[temp.partition(':')[0]] = temp.partition(':')[2].strip()
                    i += 1
                elif line.startswith('door'):
                    pass
                elif line.startswith('item'):
                    pass

    room_count = 0
    for key, value in room_description.items():
        room_num[room_count] = {key: value}
        room_count += 1
    print(f'room num: {room_num}')