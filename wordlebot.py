# python3
# This module contains the helper functions for the wordle bot
from math import log2
from itertools import product

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
    size = len(words)
    # Calculate the different expected information values for different arrangements
    for arrangement in arrangements:
        matching = getMatchingWords(word, words, arrangement)
        value = calculateInfoValue(size, len(matching))
        info_values.append(value)
    
    # Return the expected value for the word
    expected_value = sum(info_values)
    return expected_value

def calculateInfoValue(size:int, matching_size:int)->float:
    '''
        Calculates the information value
    '''
    probability = matching_size/size
    value = -log2(probability) if probability else 0

    return value


def getMatchingWords(last_guess:str, words:list, feedback_str:str) -> set:
    '''
        Calculates the information (bits) for a given the feedback string
    '''
    possible_words = set(words)
    contains_only_elsewhere = set()
    must_not_contain = set()
    exact_letter_match = set()
    
    for i, (letter,state) in enumerate(zip(last_guess, feedback_str)):
        # letter is present but not in the correct position
        if state=="Y":
            contains_only_elsewhere.update({word for word in possible_words if 
                                            letter not in word or word[i]==letter})
        
        # letter is present and in the correct position
        elif state=="R":
            exact_letter_match.update({word for word in possible_words if 
                                        letter!=word[i]})
        
        # letter is not present in the word
        else:
            must_not_contain.update({word for word in possible_words if
                                        letter==word[i]})
    
    # remove unwanted words from the possible set of words
    possible_words -= contains_only_elsewhere
    possible_words -= must_not_contain
    possible_words -= exact_letter_match

    return possible_words

# Function to read the word list
def readFile(filename:str) -> list:
    with open(filename) as f:
        words = [x.strip() for x in f.readlines()]
    return words

def runWordleBot(input=input)->list:
    '''
        Combines the necessary functions to execute the bot
    '''
    words = readFile('./wordle.txt')
    arrangements = [''.join(arr) for arr in product("RYG", repeat=5)]
    last_guess = "tares"

    guesses = []

    for i in range(5):
        # Get Feedback on last guess
        feedback_str = input("Feedback String: ")
            
        # Check if guessed correctly    
        if feedback_str=="RRRRR":
            print(f"Success :{last_guess}")
            break

        # Update the words list in the bot
        size = len(words)
        words = getMatchingWords(last_guess, words, feedback_str)
        info_value = calculateInfoValue(size, len(words))
        print(f"Information Value of the Guess {round(info_value,2)} bits")        

        # Calculate the best guess
        last_guess = generateGuess(words, arrangements)
        print(f"Next Guess: {last_guess}")
        guesses.append(last_guess)

    else:
        print(f"Bot Failed :| on {last_guess}")
    
    return guesses


if __name__=="__main__":
    runWordleBot()