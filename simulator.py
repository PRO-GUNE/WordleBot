#python3
# This program simulates a number of wordle of games with the wordle bot

from wordlebot import wordleBot, readFile, readFileDict
from time import perf_counter
from itertools import product
from curses import wrapper
import curses

def genFeedback(word, guess):
    move = []
    wordcopy = [x for x in word]

    # Check for words present in the correct spot and not present at all
    try:
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

    except TypeError:
        print(f"Some Type Erro Caught word:{word}")

def printMoves(moves, stdscr, screen_row_offset):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    GREEN = curses.color_pair(1)
    YELLOW = curses.color_pair(2)
    BLACK = curses.color_pair(3)

    for i,move in enumerate(moves, screen_row_offset):
        j=0
        for letter in move:
            if letter=="R":
                stdscr.addstr(i,j,"  ",GREEN)
            elif letter=="Y":
                stdscr.addstr(i,j,"  ",YELLOW)
            elif letter=="G":
                stdscr.addstr(i,j,"  ",BLACK)
            j+=2




def simulate(stdscr:str, all_filename:str, allowed_filename:str, initial_guess:str="tares")->list:
    '''
        Simulate a number of tests with the given wordle bot
    '''
    # Get the word list from the file
    allowed = readFile(allowed_filename)
    # A list to store all the guesses
    all_guesses = []
    # All the arrangements
    arramgements = product("RYG", repeat=5)

    # Run all the tests to generate a solution 
    for j,word in enumerate(allowed):
        # Make a copy of the raw word list
        words = readFile(all_filename)
        # Frequecy data of words
        freq_list = readFileDict('./5-gram_freq.csv')

        # Data on the simulation
        simulate_data = {
                'input':genFeedback,
                'word':word,
            }

        # Get the guesses
        start = perf_counter()
        guesses = wordleBot(words=words, 
                            freq_list=freq_list,
                            arrangements=arramgements, 
                            simulate=True, 
                            simulate_data=simulate_data)
        end = perf_counter()
        all_guesses.append((guesses, word in guesses and len(guesses)<7))

        # Get the moves made
        moves = [genFeedback(word, guess) for guess in guesses]

        # Guesses will be None if the bot failed to guess correctly
        stdscr.clear()
        stdscr.addstr(0,0, f"{' Wordle Bot Simulator 🤖🏁'.center(90,'=')}")
        stdscr.addstr(2,0, f"Word: {word}")
        stdscr.addstr(3,0, f"Guesses: {guesses}")
        stdscr.addstr(4,60, f"Moves: {len(guesses)}")
        stdscr.addstr(5,70, f"Solved: {word in guesses and len(guesses)<7}")
        stdscr.addstr(6,0, f"Tests run {j+1}")
        stdscr.addstr(6,30, f"Time taken: {round(end-start,4)} s")
        printMoves(moves, stdscr, screen_row_offset=7)
        stdscr.refresh()


    return all_guesses

wrapper(simulate, './wordle.txt', './allowed.txt')

# if __name__=="__main__":
    

    # # Calculate efficiency
    # time_taken = end - start
    # print("Time taken per word: ",time_taken)

    # # Success rate
    # successes = list(filter(lambda x: x is not None, all_guesses))
    # print(f"Success Rate: {100 * len(successes)/len(all_guesses)}%", )

    # # Average number of guesses needed
    # if successes:
    #     guess_lengths = [len(guesses) for guesses in successes] 
    #     print("Average guesses made: ", sum(guess_lengths)/len(successes))