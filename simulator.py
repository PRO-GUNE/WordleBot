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
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    GREEN = curses.color_pair(1)
    YELLOW = curses.color_pair(2)
    WHITE = curses.color_pair(3)

    for i,move in enumerate(moves, screen_row_offset):
        j=0
        for letter in move:
            if letter=="R":
                stdscr.addstr(i,j,"  ",GREEN | curses.A_DIM)
            elif letter=="Y":
                stdscr.addstr(i,j,"  ",YELLOW | curses.A_DIM)
            elif letter=="G":
                stdscr.addstr(i,j,"  ",WHITE | curses.A_DIM)
            j+=2




def simulate(stdscr:str, all_filename:str, allowed_filename:str, initial_guess:str=None)->list:
    '''
        Simulate a number of tests with the given wordle bot
    '''
    # Get the word list from the file
    allowed = readFile(allowed_filename)
    # A list to store all the guesses
    all_guesses = []
    # All the arrangements
    arramgements = product("RYG", repeat=5)
    # Make a copy of the raw word list
    words = readFile(all_filename)

    # Run all the tests to generate a solution 
    for j,word in enumerate(allowed):
        # Frequecy data of words
        freq_list = readFileDict('./5-gram_freq.csv')

        # Data on the simulation
        simulate_data = {
                'input':genFeedback,
                'word':word,
            }

        # Get the guesses
        start = perf_counter()

        # If the initial guess is to be hard coded
        guesses = wordleBot(words=words, 
                            freq_list=freq_list,
                            arrangements=arramgements,
                            last_guess=initial_guess, 
                            simulate=True, 
                            simulate_data=simulate_data)
        if initial_guess:
            guesses.insert(0, initial_guess)

        end = perf_counter()
        all_guesses.append({'guesses':guesses, 
                            'moves':len(guesses), 
                            'success':word in guesses and len(guesses)<7
                        })

        # Get the moves made
        moves = [genFeedback(word, guess) for guess in guesses]

        # Guesses will be None if the bot failed to guess correctly
        stdscr.clear()
        stdscr.addstr(f"{' Wordle Bot Simulator 🤖🏁'.center(90,'=')}")
        stdscr.addstr(2,0, f"Word: {word}")
        stdscr.addstr(3,0, f"Guesses: {guesses}")
        stdscr.addstr(4,0, f"Moves: {len(guesses)}")
        stdscr.addstr(4,40, f"Solved: {word in guesses and len(guesses)<7}")
        stdscr.addstr(6,0, f"Tests run {j+1}")
        stdscr.addstr(6,30, f"Time taken: {round(end-start,4)} s")
        printMoves(moves, stdscr, screen_row_offset=8)
        stdscr.refresh()


    return all_guesses


if __name__=="__main__":
    
    guesses = wrapper(simulate, './wordle.txt', './allowed.txt')

    # Sort the guesses by number of moves
    guesses.sort(key=lambda x:x['moves'])

    # Success rate
    successes = list(filter(lambda x:x['success'], guesses))
    success_rate = len(successes)/len(guesses)
    print(f"Success Rate: {100 * success_rate}%", )


    # Number of moves
    moves = []
    i=0
    for i in range(8):
        moves.append(len(list(filter(lambda x:x['moves']==i+1, guesses))))
    
    print(f"{'Move Analysis'.center(50, '#')}")
    print(f"Moves \t Frequency")
    for j, move in enumerate(moves,1):
        print(f"{j} \t {move}")

    total_f, total_fx = 0,0
    for i,move in enumerate(moves):
        total_fx+=(i+1)*move
        total_f+=move
    print(f"Mean number of moves: {round(total_fx/total_f, 4)}")