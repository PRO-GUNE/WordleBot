#python3
# This program simulates a number of wordle of games with the wordle bot

from wordlebot import runWordleBot, readFile
from itertools import product
from random import randint
from copy import copy
from time import perf_counter, time_ns

def genFeedback(word, guess):
    move = []
    wordcopy = [x for x in word]

    # Check for words present in the correct spot and not present at all
    for w,g in zip(word, guess):
        if w==g:
            wordcopy.remove(g)
            move.append('R')        
        else:
            move.append('G')
    
    # Check for words present in the wrong spot
    for i, g in enumerate(guess):
        if g in wordcopy and move[i]!='R':
            wordcopy.remove(g)
            move[i]='Y'

    move_str = ''.join(move)

    return move_str

def simulate(filename:str, tests:int, wordleBot, initial_guess:str="tares")->list:
    '''
        Simulate a number of tests with the given wordle bot
    '''
    # Get the word list from the file
    rawwords = readFile(filename)
    # A list to store all the guesses made
    all_guesses = []
    # A list to store all the possible arrangements
    arrangements = [''.join(arr) for arr in product("RYG", repeat=5)]
    
    # Run all the tests to generate a solution 
    for j in range(tests):
        # Make a copy of the raw word list
        words = copy(rawwords)
        # Generate a random word
        word = words[randint(0,len(words)-1)]

        last_guess = initial_guess
        guesses = []
        for _ in range(6):
            # Get the feedback from the guess
            if not last_guess:
                print(f"Bot Failed :( Answer was {word}")
                guesses = None
                break
            feedback_str = genFeedback(word, last_guess)
            guesses.append(last_guess) 
            if feedback_str=="RRRRR":
                print(f"Solved {last_guess}")
                break
            # Generate a new guess using the feedback received
            last_guess = wordleBot(words, arrangements, last_guess, feedback_str)

        else:
            print(f"Bot took too many guesses :| Answer was {word}")
            guesses = None

        # Guesses will be None if the bot failed to guess correctly
        print(f"\r{j+1} Tests run out of {tests}")
        all_guesses.append(guesses)
    
        print()
    return all_guesses

if __name__=="__main__":
    start = perf_counter()
    all_guesses = simulate('./wordle.txt', 5, runWordleBot)
    end = perf_counter()

    # Calculate efficiency
    time_taken = end - start
    print("Average time taken: ", 10/time_taken)

    # Success rate
    successes = list(filter(lambda x: x is not None, all_guesses))
    print(f"Success Rate: {100 * len(successes)/len(all_guesses)}%", )

    # Average number of guesses needed
    if successes:
        guess_lengths = [len(guesses) for guesses in successes] 
        print("Average guesses made: ", sum(guess_lengths)/len(successes))