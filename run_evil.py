import evilhangman
import pandas as pd

dictionary = pd.read_csv("dict_en.txt", sep = '\n').iloc[:, 0].values.tolist()
# dictionary = ['abba', 'acca', 'efeu']

game = evilhangman.Evilhangman(dictionary)


print(game.initialize(4))

while True:

    print(game.status)

    # Determine initial word

    # I have to update the remaining_words!
    
    guess = raw_input('Please guess a letter: ')

    letter_in_word = game.update_family(guess)
    
    game.create_families(guess)

    status = game.get_status()

    # Determine game status
    if status == 0:
        print("Loser")
        break
    if status == 1:
        print("Winner")
        break
    if status == 2:
        pass

    