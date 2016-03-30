# coding: utf-8

"""Mastermind Game with AI
"""
__author__ = "Pierre-Victor Chaumier (chaumierpv@gmail.com)"

import random
import re


## -------------------- Functions -------------------

def compare(a, b):
    """Compare two 4 digits strings and return the number of right placed 
    and wrong placed digits.
    
    RQ: this function is symmetric. The order in which the argument are 
    provided will not change the result.
    """
    strikes = 0
    count1 = [0] * 10
    count2 = [0] * 10
    for dig1, dig2 in zip(a, b):
        if dig1 == dig2:
            strikes += 1
        else:
            count1[int(dig1)] += 1
            count2[int(dig2)] += 1
    missed = sum(map(min, count1, count2))
    return strikes, missed


## -------------------- Mastermind Computer Guess -------------------

class Agent(object):

    def __init__(self):
        self.possible = [str(dig1) + str(dig2) + str(dig3) + str(dig4)
                            for dig1 in range(10)
                            for dig2 in range(10)
                            for dig3 in range(10)
                            for dig4 in range(10)]

    def guess(self):
        guess = random.choice(self.possible)
        print('Out of {:4} possible combinations, I guess {}'
                    .format(len(self.possible), guess))
        return guess

    def update_possible(self, guess, score):
        self.possible = [p for p in self.possible if compare(p, guess) == score]


## -------------------- Mastermind Human Guess -------------------

def validate_guess(guess):
    """Check if the input given by the user is valid."""
    m = re.search('\d{4}', guess)
    assert m and m.group(0) == guess

def get_valid_guess():
    while True:
        try:
            guess = input('Please enter your guess: ')
            validate_guess(guess)
        except AssertionError:
            print('  ERROR: Please enter 4 digits')
        else:
            break
    return guess


## -------------------- Mastermind Game -------------------

def mastermind(to_find=None, human=True, max_tries=15):

    # Generation of the word to guess
    if not to_find:
        to_find = ''.join([str(random.randrange(0, 10)) for _ in range(4)])
    else:
        to_find = str(to_find)

    # if computer plays, initialize agent
    agent = Agent()

    nb_of_try = 0
    score = -1, -1
    while nb_of_try < max_tries:
        nb_of_try += 1

        # ask for the guess
        if human:
            guess = get_valid_guess()
        else:
            guess = agent.guess()

        # Checking correctness
        score = compare(guess, to_find)

        # Print result of checking
        if score[0] == 4:
            print('Result found after', nb_of_try, 'attempts:', guess)
            break
        else:
            print('  Strikes {:2}\n  Missed  {:2}'.format(*score))
            print('  {} guess left'.format(max_tries - nb_of_try))
            if not human:
                agent.update_possible(guess, score)


## -------------------- Play the Game ! -------------------

mastermind(human=False)
