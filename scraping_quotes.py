import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

# website is quotes.toscrape.com
#purpose of the project is to build a game where we scrape each quote from the website and randomly output one of them. The player must guess who is
#the author of the quote. If guesses incorrectly, he will be given a hint that was also scraped from the website. The user has 3 hints.
base_url = "http://quotes.toscrape.com"


def scrape_quotes():
    all_quotes = []
    url = "/page/1" #starting page
    while url: #loop until last page is reached. Loop searches for each quote.
        res = requests.get(f"{base_url}{url}")
        print(f"Now scraping {base_url}{url}...")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes: #adding each quote to a list called all_quotes, making a list of dictionaries with quote, author, and url of author bio
            all_quotes.append({
                "text":quote.find(class_="text").get_text(),
                "author":quote.find(class_="author").get_text(),
                "bio-link":quote.find("a")['href']
                })
        next_pg = soup.find(class_= 'next')
        url = next_pg.find("a")["href"] if next_pg else None
        #sleep(2) optional.
    return all_quotes

def start_game(quotes): #Starts the defined game above
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


quotes = scrape_quotes()
start_game(quotes)