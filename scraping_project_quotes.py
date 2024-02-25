import requests
from bs4 import BeautifulSoup
from csv import DictWriter


BASE_URL = "http://quotes.toscrape.com"


def quotes_to_list():
    """"""
    quotes_list = []
    page_url = "/page/1/"
    while page_url:
        html = requests.get(f"{BASE_URL}{page_url}")
        soup = BeautifulSoup(html.text, 'html.parser')
        quotes = soup.find_all(class_="quote")
        for q in quotes:
            quotes_list.append({
                "quote": q.find(class_="text").get_text().replace("′", "'"),
                "author": q.find(class_="author").get_text(),
                "author_url": q.find("a")["href"]
            })
        try:
            soup.find(class_='next').find('a')['href']
        except AttributeError:
            page_url = False
        else:
            page_url = soup.find(class_='next').find('a')['href']
    return quotes_list


def write_quotes_csv(quotes_list):
    with open("quotes.csv", "w", newline="") as file:
        headers = ["quote", "author", "author_url"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for row in quotes_list:
            csv_writer.writerow(row)


all_quotes = quotes_to_list()
write_quotes_csv(all_quotes)
