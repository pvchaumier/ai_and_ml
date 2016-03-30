# coding: utf-8

"""
Python command line implementation of the 2048 game.

TODO:
    - 
"""

import random
import unittest

## -------------------- Game -------------------

class GameException(Exception):
    pass

class Game(object):
    """2048 game implementation.

    The probability of having a four are defined as a class variable.
    """

    proba_four = 0.1

    def __init__(self, grid_size=4):
        self.grid_size = grid_size
        self.score = 0
        self.grid = [[0 for _ in range(self.grid_size)] 
                        for _ in range(self.grid_size)]
        self.add_number()


    def __str__(self):
        """Game formatted as follow (with a grid of size 2):

         ---------------------
        |          |          |
        |---------------------|
        |          |    2     |
         ---------------------
        score = 0
        """
        first = True
        for row in self.grid:
            if first:
                str_game = ' ' + '-' * (11 * self.grid_size - 1) + '\n'
                first = False
            else:
                str_game += '|' + '-' * (11 * self.grid_size - 1) + '|\n'
            str_game += ('|' + '|'.join(['{:^10}'.format(el) if el != 0 
                                          else ' '* 10 for el in row]) 
                         + '|\n')
        str_game += ' ' + '-' * (11 * self.grid_size - 1) + '\n'
        str_game += 'score = ' + str(self.score)
        return str_game


    @property
    def free_positions(self):
        """Return an list of tuples (i, j) of available positions."""
        positions = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    positions.append((i, j))
        if positions == []:
            raise GameException('Game Over. No free position left.')
        return positions


    def is_game_over(self):
        if max([max(row) for row in self.grid]) == 2 ** (self.grid_size ** 2):
            raise GameException('Congrats, You won !')

        # If there is a zero then the game is not over
        for row in self.grid:
            if 0 in row:
                return False

        # Check if two consecutive number (vertically or horizontally) are 
        # equal. In this case the game is not over.
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # horizontal check
                if (i < self.grid_size - 1 and 
                    self.grid[i][j] == self.grid[i + 1][j]):
                    return False
                # vertical check
                if (j < self.grid_size - 1 and 
                    self.grid[i][j] == self.grid[i][j + 1]):
                    return False
        
        return True


    def add_number(self):
        """Add a number (two or four with probability proba_four) at random
        within the free prositons of grid ."""
        # take one of the free positions in the grid at random 
        x, y = random.choice(self.free_positions)
        # with the probability of Game.proba_four, put a 4 in the box. Else
        # put a 2
        if random.random() < Game.proba_four:
            self.grid[x][y] = 4
        else:
            self.grid[x][y] = 2


    def sum_row(self, row):
        """Returns the list as if there was only a left mouvement.

        For instance, [2, 2, 8, 0] will return [4, 8, 0, 0]
        """
        # Start by removing the zeros as they do not have any effect
        row_trimmed = [el for el in row if el != 0]
        # if the row has zero or one element, it stays identical
        if len(row_trimmed) == 0 or len(row_trimmed) == 1:
            new_row = row_trimmed
        # else if the row has more than two elements
        else:
            new_row = []
            # the points will be added if the element is equal to the next one.
            # We thus need to know if the current position was already added at 
            # the previous iteration or if it needs to be added now
            already_added = False
            for i in range(len(row_trimmed[:-1])):
                if already_added:
                    already_added = False
                else:
                    if row_trimmed[i] == row_trimmed[i + 1]:
                        # here we alse add the next element
                        new_row.append(2 * row_trimmed[i])
                        self.score += 2 * row_trimmed[i]
                        already_added = True
                    else:
                        new_row.append(row_trimmed[i])
            # As we loop until the second to last element, one needs to check
            # whether the last element was added or not
            if not already_added:
                new_row.append(row_trimmed[-1])

        # we might need to add zeros for the new_row to be of the right size
        return new_row + [0] * (self.grid_size - len(new_row))


    def sum_grid(self, grid):
        """Takes a grid and sums all its row as if the movement was towards the 
        left."""
        new_grid = []
        for i in range(self.grid_size):
            new_grid.append(self.sum_row(grid[i]))
        return new_grid


    # 
    # Mouvements
    # 

    # The idea is to define one function and then reuse it by manipulating the 
    # grid.

    @staticmethod
    def transpose(grid):
        return [list(row) for row in zip(*grid)]

    @staticmethod
    def miror(grid):
        return [[box for box in reversed(row)] for row in grid]

    def check_change(self, new_grid):
        if new_grid != self.grid:
            self.grid = new_grid
            self.add_number()
        if self.is_game_over():
            raise GameException('Game Over. No free position or mouvement'
                                ' left.')


    def left(self):
        # new_grid let us check if the movement changed something
        new_grid = self.sum_grid(self.grid)
        self.check_change(new_grid)

    def right(self):
        miror_grid = self.miror(self.grid)
        new_miror_grid = self.sum_grid(miror_grid)
        new_grid = self.miror(new_miror_grid)
        self.check_change(new_grid)

    def up(self):
        transposed_grid = self.transpose(self.grid)
        new_transposed_grid = self.sum_grid(transposed_grid)
        new_grid = self.transpose(new_transposed_grid)
        self.check_change(new_grid)

    def down(self):
        miror_transposed_grid = self.miror(self.transpose(self.grid))
        new_miror_transposed_grid = self.sum_grid(miror_transposed_grid)
        new_grid = self.transpose(self.miror(new_miror_transposed_grid))
        self.check_change(new_grid)


## -------------------- Unittest -------------------

class GameTestCase(unittest.TestCase):

    def setUp(self):
        # to be sure that the grid is of the good size
        self.game = Game(grid_size=4)

    # 
    # Test sum on a line
    # 

    def test_sum_empty(self):
        self.assertEqual(self.game.sum_row([]), 
                         [0] * self.game.grid_size)

    def test_sum_one_element(self):
        self.assertEqual(self.game.sum_row([1]), 
                         [1] + [0] * (self.game.grid_size - 1))

    def test_sum_multiple_elements(self):
        self.assertEqual(self.game.sum_row([2, 2, 8, 0]),
                         [4, 8, 0, 0])

    def test_sum_all_same(self):
        self.assertEqual(self.game.sum_row([2, 2, 2, 2]),
                         [4, 4, 0, 0])

    def test_sum_all_different(self):
        self.assertEqual(self.game.sum_row([2, 4, 8, 16]),
                         [2, 4, 8, 16])

    # 
    # Test Game Over
    # 

    def test_game_over_false_zero(self):
        self.game.grid_size = 2
        self.game.grid = [[2, 0], [0, 0]]
        self.assertFalse(self.game.is_game_over())

    def test_game_over_false_two_neighbor_equal(self):
        self.game.grid_size = 2
        self.game.grid = [[2, 4], [2, 16]]
        self.assertFalse(self.game.is_game_over())
    
    def test_game_over_true(self):
        self.game.grid_size = 2
        self.game.grid = [[2, 4], [8, 16]]
        self.assertTrue(self.game.is_game_over())


if __name__ == '__main__':
    unittest.main()
