import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader


BASE_URL = "http://quotes.toscrape.com"


def read_quotes_csv():
    with open("quotes.csv", newline="") as file:
        csv_reader = DictReader(file)
        quotes_list = list(csv_reader)
    return quotes_list


def start_game(quotes_list):
    chosen_element_pos = quotes_list.index(choice(quotes_list))
    chosen_quote = quotes_list[chosen_element_pos]['quote']
    chosen_author = quotes_list[chosen_element_pos]['author']
    chosen_author_url = quotes_list[chosen_element_pos]['author_url']
    guess_left = 4
    play = ""
    print(chosen_quote)
    guess = format_guess(input("Who is the author?\n"))
    while guess_left:
        if guess == format_guess(chosen_author):
            guess_left = 0
            play = input("BULL'S EYE! Wanna play again? (y/n)\n")
        else:
            guess_left -= 1
            if guess_left == 3:
                html_chosen_author = requests.get(f"{BASE_URL}{chosen_author_url}")
                soup_chosen_author = BeautifulSoup(html_chosen_author.text, 'html.parser')
                chosen_author_born_date = soup_chosen_author.find(class_="author-born-date").get_text()
                chosen_author_born_location = soup_chosen_author.find(class_="author-born-location").get_text()
                guess = format_guess(
                    input(
                        f"The author was born {chosen_author_born_location}, {chosen_author_born_date}\n"
                    )
                )
            elif guess_left == 2:
                guess = format_guess(input(f"The author's last name starts with: {chosen_author.split(' ')[-1][0]}\n"))
            elif guess_left == 1:
                guess = format_guess(input(f"The author's last name is: {chosen_author.split(' ')[-1]}\n"))
            else:
                play = input(f"It was said by {chosen_author}.\nWanna play again? (y/n)\n")
    while play != "y" and play != "n":
        play = input("Please type 'y' or 'n'.\n")
    if play == "y":
        start_game(all_quotes)


def format_guess(guess):
    amend_guess = guess.lower().replace(" ", "")
    return amend_guess


all_quotes = read_quotes_csv()
start_game(all_quotes)
