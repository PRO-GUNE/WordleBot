# Wordle Bot - Python 3
This is a wordle bot designed using the principles of entropy in information theory.

## Bot v1.0 - Naive bot
This bot takes the probability of choosing each letter for a given position of a word to be equally likely

## Bot v2.0 - FrequencyData Bot
This bot uses data about the frequency of usage of words to predict the probable words

### Calculations
* Expected Value / Entropy : Calculate the matching words for a given arrangement and then use the frequecy data of those words to calculate the overall probability of that arrangement. Use this probability to calculate the Entropy value
* Score: The score is calculated using the following function
*Score = P(word)x(number_of_moves) + (1-P(word))x(F(current_uncertainity-expected_value_of_word))*
The Function *F* is a function that gives how likely it is to move to the next guess without the current guess being the correct guess

### Results
When checked upon the valid wordle dataset, this bot can execute with 96% success rate and mean score of 4.21