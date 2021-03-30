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

        #
        print("'up' - to move upwards")
        print("'up' - to move upwards")
        print("'up' - to move upwards")
        print("'up' - to move upwards")
        print("'up' - to move upwards")
        print("'up' - to move upwards")
        print("'up' - to move upwards")


