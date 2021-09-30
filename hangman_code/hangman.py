# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)
    

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    return set(letters_guessed).issuperset(set(secret_word)) 
    
  

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word = ''
    for i in secret_word:
      if i in letters_guessed:
        word += i
      else: 
        word += "_ "
    return word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
    yet been guessed.
    '''
    lett = set(string.ascii_lowercase)
    avaib = list(lett)
    avaib.sort()
    for i in letters_guessed:
        if i in avaib:
            avaib.remove(i)
    return ''.join(avaib)
    


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    turns = 6
    war = 3
    letters = []
    golosni = ['a','o','i','e','u']
    print("Welcome to the game Hangman! \nI am thinking of a word that is", len(secret_word), "letters long.\nYou have", war, " warnings left.")
    while turns > 0:
      print("-------------\nYou have", turns, " guesses left.\nAvailable letters:", get_available_letters(letters))
      while type: 
        letter = input("Please guess a letter: ").lower()
        if letter.isalpha() == False:
          print("Oops! That is not a valid letter.", end = '')
          war = war - 1
          if war >= 0:
            print("You have", war, "warnings left.")
            print(get_guessed_word(secret_word, letters))
          else:
            print("You have no warnings left so you lose one guess:")
            print(get_guessed_word(secret_word, letters))
            turns -= 1
        elif turns == 0:
          break
        else:
          break
      letters.append(letter)
      c = letters.count(letter)
      if c > 1 :
        print("Oops! You've already guessed that letter.", end = ' ')
        war = war - 1
        if war >= 0:
          print("You have", war, "warnings left.")
        else:
          print("You have no warnings left so you lose one guess:")
          print(get_guessed_word(secret_word, letters))
          if letter in golosni:
            turns = turns - 2
          else:
            turns = turns - 1
      elif letter in get_guessed_word(secret_word, letters):
        print ("Good guess:", end = ' ')
        print(get_guessed_word(secret_word, letters))
      else:
        print("Oops! That letter is not in my word:", end = ' ')
        print(get_guessed_word(secret_word, letters))
        if letter in golosni:
          turns = turns - 2
        else:
          turns = turns - 1
      if is_word_guessed(secret_word, letters) == True:
        total_score = turns * len(set(secret_word)) 
        print("-------------\nCongratulations, you won! Your total score for this game is:", total_score)
        break
        
    if turns == 0:
      print("-------------\nSorry, you ran out of guesses. The word was", secret_word)  
    


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    not_guess = my_word.count('_ ')
    my_letters = list(filter(lambda i: i != ' ', my_word))
    other_letters = list(other_word)
    right = 0
    if len(other_letters) == len(my_letters):
      ind = 0
      while ind < len(other_letters):
        if my_letters[ind] == other_letters[ind]:
          right += 1    
          ind += 1 
        else:
          ind += 1          
      if right + not_guess == len(my_letters):
        return True
      else:
        return False
    else:
      return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = []
    for i in wordlist:
      if match_with_gaps(my_word, i) == True:
        matches.append(i)
    if matches == []:   
      empty = "No matches found"
      return empty
    else:
      return ' '.join(matches)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    turns = 6
    war = 3
    letters = []
    golosni = ['a','o','i','e','u']
    print("Welcome to the game Hangman! \nI am thinking of a word that is", len(secret_word), "letters long.\nYou have", war, " warnings left.")
    while turns > 0:
      print("-------------\nYou have", turns, "guesses left.\nAvailable letters:", get_available_letters(letters))
      while type: 
        letter = input("Please guess a letter: ").lower()
        if letter == "*":
          print("Possible word matches are:", show_possible_matches(get_guessed_word(secret_word, letters)))
        elif letter.isalpha() == False:
          print("Oops! That is not a valid letter.", end = ' ')
          war = war - 1
          if war >= 0:
            print("You have", war, "warnings left.")
            print(get_guessed_word(secret_word, letters))
          else:
            print("You have no warnings left so you lose one guess:")
            print(get_guessed_word(secret_word, letters))
            turns -= 1
        elif turns == 0:
          break
        else:
          break
      letters.append(letter)
      c = letters.count(letter)
      if c > 1 :
        print("Oops! You've already guessed that letter.", end = ' ')
        war = war - 1
        if war >= 0:
          print("You have", war, "warnings left.")
        else:
          print("You have no warnings left so you lose one guess:")
          print(get_guessed_word(secret_word, letters))
          if letter in golosni:
            turns = turns - 2
          else:
            turns = turns - 1
      elif letter in get_guessed_word(secret_word, letters):
        print ("Good guess:", end = ' ')
        print(get_guessed_word(secret_word, letters))
      else:
        print("Oops! That letter is not in my word:", end = '')
        print(get_guessed_word(secret_word, letters))
        if letter in golosni:
          turns = turns - 2
        else:
          turns = turns - 1
      if is_word_guessed(secret_word, letters) == True:
        total_score = turns*len(set(secret_word)) 
        print("-------------\nCongratulations, you won! Your total score for this game is:", total_score)
        break
        
    if turns == 0:
      print("-------------\nSorry, you ran out of guesses. The word was", secret_word)  
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
