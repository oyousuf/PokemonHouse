import yaml


class ParseConfig:
    rooms = []
    doors = []
    items = []
    start_p = []

    #     def __init__(self, rooms=None, doors=None, items=None, start_p=None):
    #         self.rooms = rooms
    #         self.doors = doors
    #         self.items = items
    #         self.start_p = start_p
    @classmethod
    def yaml_open(cls):
        with open('config.yaml') as f:
            conf = yaml.load_all(f, Loader=yaml.FullLoader)
            conf = list(conf)

        cls.rooms = conf[0]['Rooms']
        cls.doors = conf[1]['Doors']
        cls.items = conf[2]['Items']
        cls.start_p = conf[3]['Starting_position']

    def add_room(self):
        if self.rooms:
            for i in self.rooms:
                Room(i['name'], i['description'])


ParseConfig.yaml_open()
# ParseConfig.doors
# ParseConfig.rooms
ParseConfig.items
# ParseConfig.start_p


COMMANDS = {'go', 'move', 'use', 'open', 'close', 'inventory', 'help'}
DIRECTIONS = ('up', 'down', 'left', 'right')


class Player:

    def __init__(self, name='Jiwoo', inventory=[], location=ParseConfig.start_p[0]['place']):
        self.name = name
        self.inventory = inventory
        self.location = location

    @property
    def location(self):
        return self.location

    @location.setter
    def location(self, room):
        self.location = room

    def add_inventory(self, item):
        self.inventory.append(item)
        return self.inventory

    def inventory(self):
        if self.inventory:
            print(f"You have {self.inventory[0]}. You may enter any room with this key. ")
        else:
            print("You have nothing. Try to find a key in the house!")

    def current_location(self):
        print(f'You are in a {self.location}.')


class Item(Player):
    def __init__(self, name=None, description=None, location=None, **kwargs):
        self.name = name
        self.description = description
        self.location = location
        self.fixed = False
        self.openable = False
        self.unlockable = False

    def get_item(self, name):
        for item in ParseConfig.items:
            if item['name'] == name:
                if item['usage'] == 'MOVE':
                    item_object = Item(item['name'], item['description'], item['place'], openable=True)

                elif item['usage'] == 'USE' and item['action'] == 'unlock':
                    item_object = Item(item['name'], item['description'], item['place'], fixed=False, openable=False,
                                       unlockable=True)
                    a = Player()
                    a.add_inventory(item['name'])
        return item_object

    def move(self):
        if self.fixed:
            print("You can't move it.")
        else:
            print("You moved a carpet and there is a key.")


class Room(Item):
    def __init__(self, name='Bedroom', description='You are in a bedroom'):
        self.name = name
        self.description = description

    def get_room(self, r):
        for room in ParseConfig.rooms:
            if room['name'] == r:
                room_object = Room(room['name'], room['description'])

        return room_object


class Door(Room):
    def __init__(self, id, _from, from_room, to, to_room, **kwargs):
        self.id = id
        self.from_ = from_
        self.from_room = from_room
        self.to = to
        self.to_room = to
        self.locked = False
        self.closed = False

#     def get_door(self, direction):
#         for door in ParseConfig.doors:
#             if door['from_'] == direction:


a = Item()
b = a.get_item('key')

a = Player()
a.location

a=Room()
a.get_room('Kitchen')