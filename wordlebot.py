# python3
# This module contains the helper functions for the wordle bot
from math import log2
from itertools import product
from re import match
from csv import DictReader

def generateGuess(words:list, freq_list:dict)->str:
    '''
        Generates a guess after performing necessary calculations
    '''
    guesses = []
    num_words = len(words)

    # Get the guesses and calculate their expected values
    for i, word in enumerate(words):
        probability = freq_list.get(word) if freq_list.get(word) else 0
        guesses.append((word, probability))
        print(f"\r{i+1} of {num_words} checked", end='')
    
    print()
    # Sort the guesses by their expected values
    guesses.sort(key=lambda x:x[1], reverse=True)

    return guesses[0][0]
    

def uncertainity(words:list, freq_list:dict) -> float:
    '''
        Calculates the expected information value given a word
    '''
    # Calculate the different expected information values for different arrangements
    value = 0.0
    for word in words:
        value += calculateInfoValue(word, freq_list)
    
    # Return the expected value for the word
    return value

def calculateInfoValue(word:str, freq_list:dict, )->float:
    '''
        Calculates the information value
    '''
    return freq_list.get(word)*log2(1/freq_list.get(word)) if freq_list.get(word) else 0


def getMatchingWords(last_guess:str, words:list, feedback_str:str) -> float:
    '''
        Calculates the information (bits) for a given the feedback string
    '''
    matching = []
    
    for word in words:

        if isValid(last_guess, feedback_str, word):
            matching.append(word)

    return matching

def genRegex(last_guess:str, feedback_str:str) -> str:
    '''
        Generate a regex string using the last guess and the feedback
    '''
    # list of tokens to merge to get the final regex string
    regex_tokens = []

    # The token for letters not in the word
    G_letters = set()
    Y_letters = set()
    for l,f in zip(last_guess, feedback_str):
        if f=="G":
            G_letters.add(l)
        elif f=="Y":
            Y_letters.add(l)

    # Check if copies exist in pairs i.e. the two sets are equal
    G_letters = list(G_letters - Y_letters)

    if not G_letters:
        for l,f in zip(last_guess, feedback_str):
            # If the letter is in the right position
            if f=='R':
                regex_tokens.append(l)
            elif f=='Y':
                regex_tokens.append(f'[^{l}]')
            elif f=="G":
                regex_tokens.append('[a-z]')

    else:    
        # If no copies are present
        G_string = ''.join(G_letters)

        for l,f in zip(last_guess, feedback_str):
            # If the letter is in the right position
            if f=='R':
                regex_tokens.append(l)
            elif f=='Y':
                regex_tokens.append(f'[^{l}{G_string}]')
            elif f=="G":
                regex_tokens.append(f'[^{G_string}]')
    
    regex = ''.join(regex_tokens)
    return regex

def isValid(last_guess:str, feedback_str:str, word:str):
    '''
        Checks if the given string is a valid match
    '''
    # Generate the regex string
    regex = genRegex(last_guess, feedback_str)

    if match(regex, word):
        # Letters that should be present in the word
        Y_letters = [l for l,f in zip(last_guess, feedback_str) if f=="Y"]
        for letter in Y_letters:
            if letter not in word:
                return False

        # word has all characters that should be present
        return True
    
    # Word does not match the regex
    return False



# Function to read the word list
def readFile(filename:str) -> list:
    with open(filename) as f:
        words = [x.strip() for x in f.readlines()]
    return words

def readFileDict(filename:str) -> dict:
    with open(filename, newline='') as f:
        data = DictReader(f)
        words = {}
        for row in data:
            words[row['word']] = float(row['probability'])

    return words

def runWordleBot(input=input)->list:
    '''
        Combines the necessary functions to execute the bot
    '''
    words = readFile('./wordle.txt')
    freq_list = readFileDict('./5-gram_freq.csv')
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
        words = getMatchingWords(last_guess, words, feedback_str)
        info_value = uncertainity(words, freq_list)
        print(f"Remaining Uncertainity: {info_value}")      

        # Calculate the best guess
        last_guess = generateGuess(words, freq_list)
        print(f"Next Guess: {last_guess}")
        guesses.append(last_guess)

    else:
        print(f"Bot Failed :| on {last_guess}")
    
    return guesses


if __name__=="__main__":
    runWordleBot()