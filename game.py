import random
import sqlite3

DATABASE = "quotes.sqlite"
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()


class Quote:
    @staticmethod
    def get_quote(id):
        cursor.execute(f"SELECT * FROM QUOTES WHERE ROWID IS {id}")
        quote = cursor.fetchall()
        return quote[0]


class Game:
    @staticmethod
    def match(quote):
        guess = input(f"{quote[1]}\nYour Guess: ")
        if guess == quote[2]:
            print("Correct!")
            return
        else:
            guess = input(f"{quote[4]}\nYour Guess: ")
            if guess == quote[2]:
                print("Correct!")
                return
            else:
                guess = input(f"{quote[5]}\nYour Guess: ")
                if guess == quote[2]:
                    print("Correct!")
                else:
                    print(quote[2])


while True:
    Game.match(Quote.get_quote(random.randint(1, 100)))
    breaker = input("Continue? (y/n)")
    if breaker != "y":
        break
