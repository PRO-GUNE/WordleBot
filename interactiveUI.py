# A CLI Based Wordle Game
import random as rd

def conditionalPrint(word, guess):
    move = []
    wordcopy = [x for x in word]

    # Check for words present in the correct spot and not present at all
    for w,g in zip(word, guess):
        if w==g:
            wordcopy.remove(g)
            move.append(2)        
        else:
            move.append(0)
    
    # Check for words present in the wrong spot
    for i, g in enumerate(guess):
        if g in wordcopy and move[i]!=2:
            wordcopy.remove(g)
            move[i]=1

    # print the feedback string
    for m,g in zip(move, guess):
        if m==2:
            print(f"\033[42m{g.upper()}\033[0m",  end=' ')
        elif m==1:
            print(f"\033[43m{g.upper()}\033[0m",  end=' ')
        else:
            print(f"\033[100m{g.upper()}\033[0m", end=' ')


    print()

    return move

def welcomeMsg():
    print(f"\033[92m{' Wordle CLI '.center(90,'=')}\033[0m")
    print(">>\t\033[42mA\033[0m --> A is in the word and is in the correct position\t<<")
    print(">>\t\033[43mA\033[0m --> A is in the word but is in an incorrect position\t<<")
    print(">>\t\033[100mA\033[0m --> A is not in the word\t\t\t\t<<")
    print(f"\033[1;92m{' Guess the word '.center(90,'=')}\033[0m")

def printGrid(moves):
    for move in moves:
        for m in move:
            if m==2: print("\033[42m  \033[0m", end='')
            elif m==1: print("\033[43m  \033[0m", end='') 
            else: print("\033[100m  \033[0m", end='')
        print()
        
def interactiveUI():
    welcomeMsg()

    # All the possible words
    with open('./wordle.txt') as f:
        words = [x.strip() for x in f.readlines()]

    # Select a word at random
    # word = words[rd.randint(0,len(words)-1)]
    word = 'hebes'
    guesses = 6
    moves = []

    # Get the users input for 5 chances
    i=0
    while i<guesses:
        guess = input(f"Guess {i+1}: ")

        # Check if the guess is valid
        if not 0<len(guess)<6:
            print("\033[91m>>Enter a valid guess<<\033[0m")
            continue
        # Check if the guess is correct
        if guess==word:
            print(f"\033[92mCongratulations! You have guessed the word in {i+1} guesses")
            moves.append([2]*5)
            break
        else:
            move = conditionalPrint(word, guess)
            moves.append(move)
        i+=1

    else:
        print(f"\033[90mHard Luck. The Correct guess was \033[0m{word.upper()}")

    printGrid(moves)


# Main program
if __name__=="__main__":
    interactiveUI()