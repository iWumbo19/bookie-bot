import json
import match


def get_balance():
    f = open('accounts.json')
    accounts = json.load(f)
    for account in accounts['Accounts']:
        if account['name'] == match.author:
            return f"{match.author} has {account['coin']} shtickcoin"
    return "You don't have an account yet dawg"
    f.close()


def get_wins():
    f = open('accounts.json')
    accounts = json.load(f)
    for account in accounts['Accounts']:
        if account['name'] == match.author:
            return f"{match.author} has {account['wins']} wins"
    return "You don't have an account yet dawg"
    f.close()


def get_losses():
    f = open('accounts.json')
    accounts = json.load(f)
    for account in accounts['Accounts']:
        if account['name'] == match.author:
            return f"{match.author} has {account['losses']} losses"
    return "You don't have an account yet dawg"
    f.close()


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
        dict = {"name": self.name,
                "coin": self.coin,
                "wins": self.wins,
                "losses": self.losses,
                "profit": self.profit,
                "bankrupt": self.backrupt}
        return dict
