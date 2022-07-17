import requests
from bs4 import BeautifulSoup
import sqlite3

DOMAIN = "http://quotes.toscrape.com/"


class Connections:
    def __init__(self):
        self.page_nr = 1
        self.quotes = None
        self.request = None
        self.page = []
        self.soup = None
        self.data = []
        self.quotes_counter = 0
        self.joiner = ". "

    def connect(self, page_nr):
        self.page_nr = page_nr
        self.request = requests.Session()
        self.page = self.request.get(f"{DOMAIN}page/{self.page_nr}").text

    def get_quotes(self):
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.quotes = self.soup.find_all(class_="quote")
        for quote in self.quotes:
            self.data.append(["", "", "", "", "", ""])  # id, quote, author, link, initials, dob
            self.data[self.quotes_counter][0] = self.quotes_counter + 1
            self.data[self.quotes_counter][1] = quote.find(class_="text").get_text()
            self.data[self.quotes_counter][2] = quote.find(class_="author").get_text()
            quote_in_depth = quote.find('a', href=True)
            self.data[self.quotes_counter][3] = f"{DOMAIN}{quote_in_depth['href']}"
            quote_in_depth = BeautifulSoup((self.request.get(self.data[self.quotes_counter][3])).text, "html.parser")
            self.data[self.quotes_counter][4] = self.joiner.join(
                [l[0] for l in self.data[self.quotes_counter][2].split()])
            self.data[self.quotes_counter][5] = quote_in_depth.find(class_="author-born-date").get_text()
            self.quotes_counter += 1


class MakeSQL:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def make_table():
        connection = sqlite3.connect('quotes.sqlite')
        cursor = connection.cursor()
        query = '''
        CREATE TABLE QUOTES (
        ROWID,
        QUOTE,
        AUTHOR,
        LINK,
        INITIALS,
        DATE_OF_BIRTH);
        '''
        cursor.execute(query)
        connection.commit()
        connection.close()

    def fill_table(self):
        connection = sqlite3.connect('quotes.sqlite')
        cursor = connection.cursor()
        tuple_data = [tuple(data) for data in self.data]
        for item in tuple_data:
            var_string = ', '.join('?' * len(item))
            cursor.executemany(
                '''INSERT INTO QUOTES {} VALUES ({})'''.format(("ROWID", "QUOTE", "AUTHOR", "LINK", "INITIALS", "DATE_OF_BIRTH"),
                                                               var_string), (item,))
        connection.commit()
        connection.close()


quotes = Connections()
for page_of_quotes in range(1, 11):
    quotes.connect(page_of_quotes)
    quotes.get_quotes()
print(len(quotes.data))
table = MakeSQL(quotes.data)
table.make_table()
table.fill_table()
