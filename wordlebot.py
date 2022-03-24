# python3
# This module contains the helper functions for the wordle bot
from math import log2
from itertools import product
from copy import copy

def generateGuess(words, arrangements)->str:
    '''
        Generates a guess after performing necessary calculations
    '''
    guesses = []
    num_words = len(words)
    if not num_words:
        return None

    # Get the guesses and calculate their expected values
    for i, word in enumerate(words):
        guesses.append((word, expectedInfoValue(words, arrangements, word)))
        print(f"\r{i+1} of {num_words} checked", end='')
    
    print()
    # Sort the guesses by their expected values
    guesses.sort(key=lambda x:x[1], reverse=True)

    return guesses[0][0]
    

def expectedInfoValue(words:list, arrangements:list, word: str) -> float:
    '''
        Calculates the expected information value given a word
    '''
    info_values = []
    # Calculate the different expected information values for different arrangements
    for arrangement in arrangements:
        copy_words = copy(words)
        probability = calculateInfoValue(word, copy_words, arrangement)
        value = probability*log2(1/probability) if probability else probability
        info_values.append(value)
    
    # Return the expected value for the word
    expected_value = sum(info_values)
    return expected_value


def calculateInfoValue(last_guess:str, words:list, feedback_str:str) -> float:
    '''
        Calculates the information (bits) for a given the feedback string
        The Feedback string is used to update the words list
    '''
    num_words = len(words)
    initial_num_words = num_words
    
    for j, (char, state) in enumerate(zip(last_guess, feedback_str)):
        # If the character is present and in the correct position
        if state in "RY":
            i=0
            while(i<num_words):
                if char not in words[i]:
                    words.pop(i)
                    num_words-=1
                else:
                    i+=1

        if state=="R":
            i=0
            while(i<num_words):
                if words[i][j]!=char:
                    words.pop(i)
                    num_words-=1

                else:
                    i+=1
            # If the character is present but in the wrong place
        elif state=="Y":
            i=0
            while(i<num_words):
                if words[i][j]==char:
                    words.pop(i)
                    num_words-=1

                else:
                    i+=1
        
    for char, state in zip(last_guess, feedback_str):
        if state=="G":
            i=0
            while(i<num_words):
                if shouldRemove(words[i], char, feedback_str):
                    words.pop(i)
                    num_words-=1

                else:
                    i+=1
        
    # Calculate the probability
    probability = num_words/initial_num_words
    return probability

def shouldRemove(word, letter, feedback_str):
    '''
        Checks if given letter has a Y or R value anywhere in the feedback string
    '''
    letters = [x for x in word]

    # Remove the R positions from the word
    size = len(feedback_str)
    i,j=0,0
    while j<size:
        if feedback_str[j]=="R":
            letters.pop(i)
        else:
            i+=1
        j+=1

    if letter in letters:
        return True

    return False

# Function to read the word list
def readFile(filename:str) -> list:
    with open(filename) as f:
        words = [x.strip() for x in f.readlines()]
    return words

def runWordleBot(words:list, arrangements:list, last_guess:str, feedback_str:str)->str:
    '''
        Combines the necessary functions to execute the bot
    '''

    if feedback_str=="RRRRR":
        return None

    # Update the words list in the bot
    probability = calculateInfoValue(last_guess, words, feedback_str)
    info_value = -log2(probability) if probability else 0
    print(f"Information Value of the Guess {round(info_value,2)} bits", )
    print("Number of words", len(words))        

    # Calculate the best guess
    last_guess = generateGuess(words, arrangements)
    return last_guess

    

def main() -> None:
    words = readFile('./wordle.txt')
    arrangements = [''.join(arr) for arr in product("RYG", repeat=5)]
    last_guess = "tares"
    
    print("Number of words", len(words))

    for i in range(5):
        feedback_str = input("Feedback String: ")
        guess = runWordleBot(words, arrangements, last_guess, feedback_str)

        print(words)

        if not guess:
            print(f"Success :{last_guess}")
            break
        else:
            last_guess=guess
            print(guess)


if __name__=="__main__":
    main()