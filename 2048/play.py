# coding: utf-8

import os

from game import Game, GameException

g = Game(grid_size=2)

actions = {
    'q':    g.left,
    'd':    g.right,
    'z':    g.up,
    's':    g.down
}

while 1:
    os.system('clear')
    print(g)
    action = input('continue ? ')

    try:
        actions[action]()
    except GameException as e:
        os.system('clear')
        print(g)
        print(e)
        break
    except KeyError:
        if action == 'quit':
            break
