import json
import match

# Function to retrieve balance from file
def get_balance():
    f = open('accounts.json')
    accounts = json.load(f)
    for account in accounts['Accounts']:
        if account['name'] == match.author:
            return f"{match.author} has {account['coin']} shtickcoin"
    return "You don't have an account yet dawg"
    f.close()


# Function to retrieve wins from file
def get_wins():
    f = open('accounts.json')
    accounts = json.load(f)
    for account in accounts['Accounts']:
        if account['name'] == match.author:
            return f"{match.author} has {account['wins']} wins"
    return "You don't have an account yet dawg"
    f.close()


# Function to retrieve losses from file
def get_losses():
    f = open('accounts.json')
    accounts = json.load(f)
    for account in accounts['Accounts']:
        if account['name'] == match.author:
            return f"{match.author} has {account['losses']} losses"
    return "You don't have an account yet dawg"
    f.close()


# Function to add new account to file
def create_account():
    f = open('accounts.json')
    accounts = json.load(f)
    for account in accounts['Accounts']:
        if account['name'] == match.author:
            return "You look familiar my guy"
    new = Account(match.author)
    accounts['Accounts'].append(new.dict_form())
    with open('accounts.json', 'w') as json_file:
        json.dump(accounts, json_file,
                  indent=4)
    f.close()
    return f"Created account for {match.author}!\nHere's 10000 shtickcoin to start"


def has_funds(amount):
    f = open('accounts.json')
    accounts = json.load(f)
    for account in accounts['Accounts']:
        if account['name'] == match.author:
            if account['coin'] < amount:
                return False
    with open('accounts.json', 'w') as json_file:
        json.dump(accounts, json_file,
                  indent=4)
    f.close()


def remove_funds(amount):
    f = open('accounts.json')
    accounts = json.load(f)
    for account in accounts['Accounts']:
        if account['name'] == match.author:
            account['coin'] -= amount
    with open('accounts.json', 'w') as json_file:
        json.dump(accounts, json_file,
                  indent=4)
    f.close()


# Class to help with json object formatting
class Account:
    def __init__(self, name):
        self.name = name
        self.coin = 10000
        self.wins = 0
        self.losses = 0
        self.profit = 0
        self.backrupt = 0

    def win(self, amount):
        self.coin += amount
        self.wins += 1
        self.profit += amount

    def lose(self, amount):
        self.coin -= amount
        self.losses += 1
        self.profit -= amount

    def bailout(self):
        self.coin = 10000
        self.backrupt += 1

    def dict_form(self):
        out = {"name": self.name,
                "coin": self.coin,
                "wins": self.wins,
                "losses": self.losses,
                "profit": self.profit,
                "bankrupt": self.backrupt}
        return out
