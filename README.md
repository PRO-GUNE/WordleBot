# Wordle Bot - Python 3
This is a wordle bot designed using the principles of entropy in information theory.

# How to Use This Repo
There are two ways to use this repository:

## Use the bot to play wordle
To have the bot play wordle, you can use the `wordle_bot.py` file while playing the actual wordle game on the [Wordle website](https://www.nytimes.com/games/wordle/index.html). The bot will give you the next word to guess and you can use that to play the game.

- Start the bot with `python wordle_bot.py`
- Enter the initial guess the bot gives in the Wordle site
- You will get the feedback of which letters are correct and which are in the wrong position.
- Enter the feedback in the bot using the following format
  - `Correct letters in the right position: R`
  - `Correct letters in the wrong position: Y`
  - `Incorrect letters: G`
- Then it would give you its prediction to the next word

## Simulation mode

In this mode the robot will run on a simulated wordle game and will give you the next word to guess and the feedback. You can use this to test the bot's performance. It will simulate all the words given in the `allowed.txt` file.

### Calculations
* Expected Value / Entropy : Calculate the matching words for a given arrangement and then use the frequecy data of those words to calculate the overall probability of that arrangement. Use this probability to calculate the Entropy value
* Score: The score is calculated using the following function
*Score = P(word)x(number_of_moves) + (1-P(word))x(F(current_uncertainity-expected_value_of_word))*
The Function *F* is a function that gives how likely it is to move to the next guess without the current guess being the correct guess

### Results
When checked upon the valid wordle dataset, this bot can execute with 96% success rate and mean score of 4.21