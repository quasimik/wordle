import argparse
import random
import string

from termcolor import colored

from solver import Solver

def format_guess_result(guess, guess_result):
    result_text = ''
    for g, r in zip(guess, guess_result):
        if r == 2:
            color = 'green'
        elif r == 1:
            color = 'blue'
        else:
            color = 'red'
        result_text += colored(g, color)
    return result_text

class Wordle:
    def __init__(self, wordlist, word, max_guesses=6):
        self.wordlist = wordlist
        self.word = word
        self.word_length = len(word)
        self.n_guesses = 0
        self.max_guesses = max_guesses
        self.history = []

    def get_history(self, mode='color'):
        hidden = ['🟥', '🟦', '🟩']
        if mode == 'color':
            return '\n'.join(format_guess_result(word, self.check_guess(word, count=False)[1]) for word in self.history) + '\n'
        elif mode == 'hidden':
            return '\n'.join(''.join(hidden[r] for r in self.check_guess(word, count=False)[1]) for word in self.history) + '\n'
        else:
            return '\n'.join(self.history) + '\n'

    def check_guess(self, guess, count=True):
        """
        :param guess: A guess
        :returns guess_result: List[int] as such:
            2: letter is in correct position
            1: letter exists, in wrong position
            0: letter does not exist
        """
        if count:
            if not (
                len(guess) == args.word_length and
                guess in self.wordlist and
                self.n_guesses < self.max_guesses
            ):
                return 'invalid', None
            self.n_guesses += 1
            self.history.append(guess)

        guess_result = [0 for _ in range(self.word_length)]
        unseen = list(self.word)
        for i, (g, w) in enumerate(zip(guess, self.word)):
            if g == w:
                unseen.remove(g)
                guess_result[i] = 2
        for i, (g, w) in enumerate(zip(guess, self.word)):
            if guess_result[i] == 0 and g in unseen:
                unseen.remove(g)
                guess_result[i] = 1
        win = sum((r == 2) for r in guess_result) == self.word_length
        status = 'win' if win else 'continue'
        return status, guess_result

class InteractiveSolver:
    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.word_length = len(wordlist[0])

    def generate_guess(self, prev_guess_result=None):
        guess = input(f'type a guess ({self.word_length} letters): ')
        return guess

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wordlist', default='wordlist_letterpress.txt')
    parser.add_argument('--word-length', type=int, default=5)
    parser.add_argument('--word', default=None)
    parser.add_argument('--seed', default=None)
    parser.add_argument('--max-guesses', type=int, default=6)
    parser.add_argument('--interactive', action='store_true', default=False)
    args = parser.parse_args()

    with open(args.wordlist) as f:
        wordlist = [w.strip() for w in f]
        wordlist = [w for w in wordlist if len(w) == args.word_length]
    if args.word is None:
        random.seed(args.seed)
        args.word = random.choice(wordlist)

    wordle = Wordle(wordlist=wordlist, word=args.word, max_guesses=args.max_guesses)
    if not args.interactive:
        solver = Solver(wordlist)
    else:
        solver = InteractiveSolver(wordlist)

    status = None
    n_guesses = 0
    guess_result = None
    while status != 'win' and n_guesses < args.max_guesses:
        n_guesses += 1
        status = None
        while status in (None, 'invalid'):
            guess = solver.generate_guess(guess_result)
            status, guess_result = wordle.check_guess(guess)
        print(f'''guess {n_guesses:>2}  {format_guess_result(guess, guess_result)}''')

    if status == 'win':
        print('win')
    else:
        print(f'''lose, word is {colored(args.word, 'green')}''')
    print(wordle.get_history(mode='hidden'))
