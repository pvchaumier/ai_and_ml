# Mastermind Game to be played

## Motivation

After watching Raymond Hettinger's [video](https://www.youtube.com/watch?v=M9V1e-rG7VA)
on AI with Python, I wanted to give it a try and implement my own version 
of both the game and the solver.


## Description

This program contains two mastermind game
- one that makes you guess the combination
- one that tries to guess automatically the combination you invented


## How the solver works

The solver keeps a list of all possible combinations, chooses one at random
and then update the list with the received feedback.

Usually it takes 6 or 7 tries for the computer to find the right 
combination.


## Rules

Mastermind is a game in which you have to discover a combination of digits
based on feedbacks given by your opponent.

Given a combination, the types of feedback you can obtain are:
- number of digits rightly placed
- number of digits rightly guessed by misplaced

The game ends either when you found the right combination or when you tried
too many times (usually the maximum number of tries is 15).

e.j. : if the combination to guess is 1234 and you give 2131
the feedback will be: 2 badly placed and 1 well placed.
