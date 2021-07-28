import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter
from csv import DictReader
# website is quotes.toscrape.com
#purpose of the project is to build a game where we scrape each quote from the website, store them in a csv file for efficiency (not scraping each time
#we play) and randomly output one of the quotes in the file. The player must guess who is the author of the quote.
#If he or she guesses incorrectly, he or she will be given a hint that was also scraped from the website and stored in the file. The user has 3 hints.

# http://quotes.toscrape.com
base_url = "http://quotes.toscrape.com"
### BELOW: Must only be run once in a while ######
def scrape_quotes():
    all_quotes = []
    url = "/page/1"
    while url:
        res = requests.get(f"{base_url}{url}")
        print(f"Now scraping {base_url}{url}...")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            all_quotes.append({
                "text":quote.find(class_="text").get_text(),
                "author":quote.find(class_="author").get_text(),
                "bio-link":quote.find("a")['href']
                })
        next_pg = soup.find(class_= 'next')
        url = next_pg.find("a")["href"] if next_pg else None
        sleep(1)
    return all_quotes

quotes = scrape_quotes()
#write quotes to csv file
def write_quotes(quotes):
    with open("quotes.csv", "w") as file:
        headers = ['text','author','bio-link']
        csv_writer = DictWriter(file, fieldnames= headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)
### ^^^^^^^^ Must only be run once in a while ^^^^^^^^^


# Reading the csv file
def read_quotes(filename):
    with open(filename, 'r') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)

def start_game(quotes):
    quote = choice(quotes)

    remaining_guesses = 4

    print("Here's a quote:")
    print(quote["text"])


    guess = ''

    while guess.lower() != quote['author'].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}")
        remaining_guesses -= 1
        if guess.lower() == quote['author'].lower():
            print("YOU GOT IT RIGHT!")
            break
        if remaining_guesses == 3:
            res = requests.get(f"{base_url}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, 'html.parser')
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
        elif remaining_guesses == 2:
            print(f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
        elif remaining_guesses==1:
            last_initial = quote['author'].split(" ")[1][0]
            print(f"Here's a hint: The author's first name starts with: {last_initial}")
        else:
            print(f"Sorry you ran outh of guesses. The answer was {quote['author']}")

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y/n)?")

    if again.lower() in ('yes', 'y'):
        print("Ok YOU PLAY AGAIN\n")
        return start_game()
    else:
        print('Ok Goodbye')


quotes = read_quotes("quotes.csv")
start_game(quotes)