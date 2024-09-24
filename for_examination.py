import sys
import random


def readlines(filename):
    with open(filename) as file:
        return file.readlines()


def choose_word(wordbank):
    return random.choice(wordbank).strip()


def identical(let1, let2):
    if let1 == let2:
        return True
    return False


def in_there(let1, secret_word):
    if let1 in secret_word:
        return True
    return False


def letter_found(letter, word):
    num = 0
    for c in word:
        if c == letter:
            num += 1
    return num


def num_occurrences(secret_word):
    first_list = []
    for letter in "abcdefghijklmnopqrstuvwxyz":
        num = letter_found(letter, secret_word)
        if num != 0:
            first_list.append((letter, num))
    return first_list


def ax_others(num_list, let1):
    new_num_list = []
    for letter, num in num_list:
        if let1 == letter and num - 1 >= 0:
            new_num_list.append((letter, num - 1))
        else:
            new_num_list.append((letter, num))
    return new_num_list


def is_not_zero(num_list, let1):
    for letter, num in num_list:
        if let1 == letter and num != 0:
            return True
    return False


def compare(guess, secret_word):
    output = ["", "", "", "", ""]
    num_list = num_occurrences(secret_word)
    output, num_list, indexes = exclaim(guess, secret_word, output, num_list)
    return fill_holes(guess, secret_word, output, num_list), indexes


def exclaim(guess, secret_word, output, num_list):
    indexes = []
    for i in range(5):
        let1 = guess[i]
        let2 = secret_word[i]
        if identical(let1, let2):
            output[i] = "!"
            num_list = ax_others(num_list, let1)
            indexes.append((let1, int(i)))
    return output, num_list, indexes


def fill_holes(guess, secret_word, output, num_list):
    dont_use = ""
    for i in range(5):
        let1 = guess[i]
        let2 = secret_word[i]
        if in_there(let1, secret_word) and is_not_zero(num_list, let1) and not identical(let1, let2):
            output[i] = "?"
            num_list = ax_others(num_list, let1)
        else:
            if not identical(let1, let2):
                output[i] = "*"
                dont_use += let1
    return "".join(output), dont_use


def did_you_win(guess, secret_word):
    if guess == secret_word:
        print("Way to go!")
        return True


def neat_string(in_string, last_out):
    out_string = ""
    for c in "abcdefghijklmnopqrstuvwxyz":
        if c in in_string or c in last_out:
            out_string += c
    return out_string


def gen_knowledge(known, last_output):
    output = last_output
    if len(known) == 0:
        return "".join(output)
    for letter, number in known:
        output[number] = letter
    return "".join(output)


def start_game(secret_word, guesses):
    i = 1
    last_output = ["_", "_", "_", "_", "_"]
    last_out = ""
    while i <= guesses:
        guess = input(f"Guess #{i}: \n")
        print(compare(guess, secret_word)[0][0])
        if did_you_win(guess, secret_word):
            return
        if i != guesses + 1:
            print(f"These letters are not in the answer: {neat_string(compare(guess, secret_word)[0][1], last_out)}")
            print(f"This is the word as you know it: {gen_knowledge(compare(guess, secret_word)[1], last_output)}")
            last_output = list(gen_knowledge(compare(guess, secret_word)[1], last_output))
            last_out = neat_string(compare(guess, secret_word)[0][1], last_out)
            i += 1
        if i == 7:
            print(f"Maybe next time. The answer is {secret_word}.")
            i += 1


def main(infile, guesses):
    wordbank = readlines(infile)
    secret_word = choose_word(wordbank)
    start_game(secret_word, guesses)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
