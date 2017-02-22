import random
import math

class Board:
    #first value in each ordered pair is the tile number, second is the probability of spawning
    starting_tiles = ((2,.9),(4,.1))
    
    def __init__(self,w,h):
        self.width = w
        self.height = h
        self.score = 0
        self._generate_table()

    def _generate_table(self):
        #Creates table full of 0's
        table = []
        for i in range(self.width):
            column = []
            for j in range(self.height):
                column.append(0)
            table.append(column)
            
        self.table = table

    def get_table(self):
        return self.table

    def get_score(self):
        return self.score

    def display(self):
        #displays the board]
        print('\nScore - {}\n'.format(self.score))
        max_len = []
        for i in range(self.width):
            max_len.append(0)
            for j in range(self.height):
                max_len[i] = max([len(str(self.table[i][j])),max_len[i]])
        for j in range(self.height):
            row = ''
            for i in range(self.width):
                value = self.table[i][j]
                len_diff = max_len[i] - len(str(value)) if value != 0 else max_len[i]
                #Makes all tiles the same width and attempts to center values
                row += '[{0}{2}{1}]'.format(' ' * math.floor(len_diff/2), ' ' * math.ceil(len_diff/2), value if value != 0 else '')
            print(row)
        print('\n')

    def random_blank_space(self):
        #Returns None if there are no blanks
        #otherwise coordinates of a blank space
        is_full = True
        
        for i in range(self.width):
            if 0 in self.table[i]:
                is_full = False

        if is_full:
            return None
        
        while True:
            x = random.randint(0,self.width-1)
            y = random.randint(0,self.height-1)
            value = self.table[x][y]
            if value == 0:
                return (x,y)
            
    def random_tile_value(self):
        #Returns starting tile value set in Board.starting_tiles
        values = ([A[0] for A in self.starting_tiles])
        weights = ([A[1] for A in self.starting_tiles])
        return random.choices(values,weights)[0]

    def spawn_tile(self):
        #Spawns a tile in a blank space
        space = self.random_blank_space()
        if space == None:
            return
        x,y = space
        self.table[x][y] = self.random_tile_value()


    def shift_up(self):
        #shifts all tiles with a blank spot above them one space up
        table_changed = False
        for i in range(self.width):
            for j in range(self.height - 1):
                current = self.table[i][j+1]
                destination = self.table[i][j]

                if destination == 0 and current != 0:
                    self.table[i][j+1] , self.table[i][j] = destination , current
                    table_changed = True

        return table_changed

    def merge_up(self):
        #shifts tiles with equal tile above them up and adds them together
        table_changed = False
        for i in range(self.width):
            for j in range(self.height - 1):
                current = self.table[i][j+1]
                destination = self.table[i][j]

                if destination == current and current != 0:
                    self.table[i][j] = current * 2
                    self.table[i][j+1] = 0
                    self.score += current*2
                    table_changed = True

        return table_changed

    def swipe_up(self):
        #shifts and merges tiles up.
        changed = False
        while self.shift_up():
            changed = True

        if self.merge_up():
            changed = True

        while self.shift_up():
            changed = True

        if changed:
            self.spawn_tile()

    def swipe_down(self):
        #shifts and merges tiles down
        for i in range(self.width):
            self.table[i] = self.table[i][::-1]

        self.swipe_up()
        
        for i in range(self.width):
            self.table[i] = self.table[i][::-1]

    def swipe_left(self):
        #shifts and merges tiles left
        self.table  = [[x[i] for x in self.table] for i in range(len(self.table[0]))]
        self.swipe_up()
        self.table  = [[x[i] for x in self.table] for i in range(len(self.table[0]))]

    def swipe_right(self):
        #shifts and merges tiles right
        self.table  = [[x[i] for x in self.table] for i in range(len(self.table[0]))]
        self.swipe_down()
        self.table  = [[x[i] for x in self.table] for i in range(len(self.table[0]))]

    def game_over_check(self):
        #Checks if there are any possible moves left
        for column in self.table:
            if 0 in column:
                return

        for i in range(self.width):
            for j in range(self.height):
                try:
                    if self.table[i][j] == self.table[i-1][j] and i != 0:
                        return
                except:
                    pass
                try:
                    if self.table[i][j] == self.table[i+1][j]:
                        return
                except:
                    pass
                try:
                    if self.table[i][j] == self.table[i][j-1] and j != 0:
                        return
                except:
                    pass
                try:
                    if self.table[i][j] == self.table[i][j+1]:
                        return
                except:
                    pass

        print('u lose, loser! Your score was {}.'.format(self.score))
        while True:
            input('')
        
if __name__ == '__main__':
    BOARD_WIDTH = 4
    BOARD_HEIGHT = 4

    board = Board(BOARD_WIDTH,BOARD_HEIGHT)
    board.spawn_tile()
    board.display()

    control_dict = {'w':board.swipe_up,
                    's':board.swipe_down,
                    'a':board.swipe_left,
                    'd':board.swipe_right}

    while True:
        direction = input(': ')
        if direction not in control_dict:
            print('invalid input - WASD only')
            continue
        control_dict[direction]()
        board.display()
        board.game_over_check()

