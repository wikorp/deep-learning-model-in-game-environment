from utils import floors_group_on_screen, extra_floors_groups, extra_fininsh_floors_groups, floors_in_group
import random


class Map:
    def __init__(self):
        self.layout = []
        self.init_map()

    def init_map(self):
        for i in range(extra_fininsh_floors_groups - 1):
            self.layout.append('X                   X')
            self.layout.append('X                   X')
            self.layout.append('X                   X')
            self.layout.append('X                   X')
            self.layout.append('X                   X')
        self.layout.append('X                   X')
        self.layout.append('X                   X')
        self.layout.append('X                   X')
        self.layout.append('X       FFFFF       X')
        self.layout.append('X                   X')

        parity = 1
        for i in range(floors_group_on_screen - 1 + extra_floors_groups):
            for j in range(floors_in_group - 1):
                self.layout.append('X                   X')

            if parity % 2 == 1:
                space = 21
                space = space - 4 * 2 - 2
                l = random.randint(0, 2)
                r = random.randint(0, 2)
                space = space - l
                level = "X"
                for ll in range(l):
                    level += " "
                level += "XXXX"
                for s in range(space - r):
                    level += " "
                level += "XXXX"
                for rr in range(r):
                    level += " "
                level += "X"
                self.layout.append(level)
            else:
                space = 21
                space = space - 5 - 2 - 5
                c = random.randint(0, 4)
                space = space - c
                level = "X     "
                for cc in range(c):
                    level += " "
                level += "XXXXX"
                for s in range(space):
                    level += " "
                level += "X"
                self.layout.append(level)

            parity += 1
        
        self.layout.append('X                   X')
        self.layout.append('X                   X')
        self.layout.append('X                   X')
        self.layout.append('X         P         X')
        self.layout.append('X       XXXXX       X')
