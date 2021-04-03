import cmd
import json


class ParseConfig:
    def configparse(self):
        with open("house_description.txt") as file:
            rooms = []
            doors = []
            items = []
            starting_point = ''
            for line in file:
                line = line.partition('#')[0]
                line = line.rstrip()
                line = line.split(' ')
                if line[0] == 'room':
                    # rooms.append(line[1])
                    rooms.append(Rooms(line[1], line[2:]))
                if line[0] == 'door':
                    line[1] = line[1].split('-')
                    doors.append(line[1:])
                if line[0] == 'item':
                    items.append(line[1:])
                if line[0] == 'start':
                    starting_point = line[1]

        return ref


    def get_start(self):
        starting_point = ''


class Room:
    def __init__(self, name="Bedroom", description="This is a bedroom."):
        self.name = name
        self.description = description


class Door(Room):
    def __init__(self, exits={}):
        pass

    def exit(self, direction):
        if direction in self.exits:
            return self.exits[direction]
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
        self.loc = ParseConfig.get_room()
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
