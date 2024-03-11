# python3
# This module contains the helper functions for the wordle bot
from math import log2
from itertools import product
from re import match
from csv import DictReader


def generateGuess(
    words: list,
    freq_list: dict,
    arrangements: list,
    uncertainity: float,
    current_score: int,
) -> str:
    """
    Generates a guess after performing necessary calculations
    """
    guesses = []

    # Get the guesses and calculate the overall probability of their possible matches
    for i, word in enumerate(words):
        expectedValues = []

        # If the word is not likely to occur i.e. not in the frequency data, skip that word
        if not freq_list.get(word):
            continue

        for arrangement in arrangements:
            matching = getMatchingWords(word, words, arrangement)

            # Calculate the overall probability of the matching words
            probability = 0
            for word in matching:
                probability += freq_list.get(word) if freq_list.get(word) else 0

            # Add to the expected values list
            value = probability * log2(1 / probability) if probability else 0
            expectedValues.append(value)

        # If the word is not probable then no need to consider its score
        if freq_list.get(word):
            score = freq_list.get(word) * current_score + (1 - freq_list.get(word)) * (
                uncertainity - current_score
            )
            # Add the word to the list
            guesses.append((word, score))

    # Sort the guesses by their expected values
    guesses.sort(key=lambda x: x[1], reverse=True)

    return guesses[0][0] if guesses else None


def uncertainity(words: list, freq_list: dict) -> float:
    """
    Calculates the expected information value given a word
    """
    # Calculate the different expected information values for different arrangements
    value = 0.0
    for word in words:
        value += (
            freq_list.get(word) * log2(1 / freq_list.get(word))
            if freq_list.get(word)
            else 0
        )

    # Return the expected value for the word
    return value


def getMatchingWords(last_guess: str, words: list, feedback_str: str) -> float:
    """
    Calculates the information (bits) for a given the feedback string
    """
    matching = []

    for word in words:

        if isValid(last_guess, feedback_str, word):
            matching.append(word)

    return matching


def genRegex(last_guess: str, feedback_str: str) -> str:
    """
    Generate a regex string using the last guess and the feedback
    """
    # list of tokens to merge to get the final regex string
    regex_tokens = []

    # The token for letters not in the word
    G_letters = set()
    Y_letters = set()
    for l, f in zip(last_guess, feedback_str):
        if f == "G":
            G_letters.add(l)
        elif f == "Y":
            Y_letters.add(l)

    # Check if copies exist in pairs i.e. the two sets are equal
    G_letters = list(G_letters - Y_letters)

    if not G_letters:
        for l, f in zip(last_guess, feedback_str):
            # If the letter is in the right position
            if f == "R":
                regex_tokens.append(l)
            elif f == "Y":
                regex_tokens.append(f"[^{l}]")
            elif f == "G":
                regex_tokens.append("[a-z]")

    else:
        # If no copies are present
        G_string = "".join(G_letters)

        for l, f in zip(last_guess, feedback_str):
            # If the letter is in the right position
            if f == "R":
                regex_tokens.append(l)
            elif f == "Y":
                regex_tokens.append(f"[^{l}{G_string}]")
            elif f == "G":
                regex_tokens.append(f"[^{G_string}]")

    regex = "".join(regex_tokens)
    return regex


def isValid(last_guess: str, feedback_str: str, word: str):
    """
    Checks if the given string is a valid match
    """
    # Generate the regex string
    regex = genRegex(last_guess, feedback_str)

    if match(regex, word):
        # Letters that should be present in the word
        Y_letters = [l for l, f in zip(last_guess, feedback_str) if f == "Y"]
        for letter in Y_letters:
            if letter not in word:
                return False

        # word has all characters that should be present
        return True

    # Word does not match the regex
    return False


# Function to read the word list
def readFile(filename: str) -> list:
    with open(filename) as f:
        words = [x.strip() for x in f.readlines()]
    return words


def readFileDict(filename: str) -> dict:
    with open(filename, newline="") as f:
        data = DictReader(f)
        words = {}
        for row in data:
            words[row["word"]] = float(row["probability"])

    return words


def wordleBot(
    words: list,  # The list of possible words
    freq_list: list,  # The frequency list data
    arrangements: list,  # All possible feedback strings
    current_score: int = 1,  # Current score of the game
    last_guess: str = None,  # The previous guess made and passed down to the function
    feedback_str: str = None,  # The Feedback given for the last guess
    simulate: bool = False,  # Simulation Mode is ON or off
    simulate_data: dict = None,  # If simualtion mode is ON, then this dictionary should
    # carry the input function with the parameters, word and last_guess
    # and the correct word
) -> list:
    """
    The Logic of the wordle bot using all the helper functions
    """
    # Check if guessed correctly
    if feedback_str == "RRRRR":
        return None

    # Calculate the best guess
    current_uncertainity = uncertainity(words, freq_list)
    last_guess = generateGuess(
        words, freq_list, arrangements, current_uncertainity, current_score
    )

    # Get Feedback on last guess
    if simulate:
        input_func = simulate_data["input"]
        feedback_str = input_func(word=simulate_data["word"], guess=last_guess)
    else:
        print("Next Guess: ", last_guess)
        feedback_str = input("Feedback String: ")

    # Update the words list in the bot if a valid last guess is made
    if last_guess:
        words = getMatchingWords(last_guess, words, feedback_str)
    else:
        return None

    # Recursive call down the next function
    next_guess = wordleBot(
        words,
        freq_list,
        arrangements,
        current_score + 1,
        last_guess,
        feedback_str,
        simulate,
        simulate_data,
    )

    # Check if the recursion has reached the answer
    if isinstance(next_guess, list):
        newlist = [last_guess]
        newlist.extend(next_guess)
        return newlist
    elif next_guess:
        return [last_guess, next_guess]

    return last_guess


def main() -> list:
    """
    Combines the necessary functions to execute the bot
    """
    words = readFile("./data/wordle.txt")
    freq_list = readFileDict("./data/5-gram_freq.csv")
    arramgements = product("RYG", repeat=5)

    guesses = wordleBot(words, freq_list, arramgements)

    print(guesses)


def welcomeMsg():
    print(f"\033[92m{' Wordle BOT 🤖'.center(90,'=')}\033[0m")
    print(
        ">>\t\033[42mA\033[0m --> A is in the word and is in the correct position\t<<"
    )
    print(
        ">>\t\033[43mA\033[0m --> A is in the word but is in an incorrect position\t<<"
    )
    print(">>\t\033[100mA\033[0m --> A is not in the word\t\t\t\t<<")
    print(f"\033[1;92m{' Guess the word '.center(90,'=')}\033[0m")


if __name__ == "__main__":
    welcomeMsg()
    main()
