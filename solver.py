import random

class Solver:
    def __init__(self, wordlist):
        self.wordlist = wordlist

    def generate_guess(self, prev_guess_result=None):
        guess = random.choice(self.wordlist)
        return guess
