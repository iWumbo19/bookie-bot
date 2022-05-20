import ah
import json

matches = []
author = ""
max_bet = 10000
lowest_bet = 1


def clean_author(a):
    b = a.split('#')
    author = b[0]


class Match:
    def __init__(self, redcorner, bluecorner, creator):
        self.redcorner = redcorner
        self.bluecorner = bluecorner
        self.redpot = 0
        self.bluepot = 0
        self.redodd = 1.00
        self.blueodd = 1.00
        self.creator = creator
        self.matchid = len(matches) + 1
        self.closed = False
        self.redbetters = {}
        self.bluebetters = {}

    def update_odds(self):
        if self.redpot > self.bluepot:
            self.redodd = self.redpot / self.bluepot
            self.blueodd = 1
        else:
            self.blueodd = self.bluepot / self.redpot
            self.redodd = 1

    def payout_match(self, winner):
        f = open('accounts.json')
        accounts = json.load(f)
        for key in self.redbetters:
            for account in accounts['Accounts']:
                if key == account['name']:
                    if winner == 'red':
                        account['coin'] += self.redbetters[key]
                        account['wins'] += 1
                        account['profit'] += self.redbetters[key]
                    else:
                        account['coin'] -= self.redbetters[key]
                        account['losses'] += 1
                        account['profit'] -= self.redbetters[key]
        for key in self.bluebetters:
            for account in accounts['Accounts']:
                if key == account['name']:
                    if winner == 'blue':
                        account['coin'] += self.bluebetters[key]
                        account['wins'] += 1
                        account['profit'] += self.bluebetters[key]
                    else:
                        account['coin'] -= self.bluebetters[key]
                        account['losses'] += 1
                        account['profit'] -= self.bluebetters[key]
        with open('accounts.json', 'w') as json_file:
            json.dump(accounts, json_file,
                      indent=4)
        f.close()