import random

import json

matches = []
author = ""
max_bet = 10000
lowest_bet = 1


# Method to separate name from #DiscordID and sets match.author
def clean_author(a):
    b = a.split('#')
    author = b[0]


def in_matches(temp_id):
    for match in matches:
        if match.matchid == temp_id:
            return False
    return True


def generate_id():
    x = random.randint(0,255)
    while in_matches(x):
        x = random.randint(0,255)
    return x


# Match object that holds all needed information for match handling
class Match:
    def __init__(self, redcorner, bluecorner, creator):
        self.redcorner = redcorner
        self.bluecorner = bluecorner
        self.redpot = 0
        self.bluepot = 0
        self.redodd = 1.00
        self.blueodd = 1.00
        self.creator = creator
        self.matchid = generate_id()
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

    async def payout_match(self, ctx, winner):
        f = open('accounts.json')
        accounts = json.load(f)
        self.update_odds()
        for key in self.redbetters:
            for account in accounts['Accounts']:
                if key == account['name']:
                    if winner == 'red':
                        account['coin'] += self.redbetters[key] * (self.blueodd/self.redodd)
                        account['wins'] += 1
                        account['profit'] += self.redbetters[key] * (self.blueodd/self.redodd)
                        await ctx.send(f"{account['name']} wins {self.redbetters[key] * (self.blueodd/self.redodd)}"
                                       f" shtickcoin!")
        for key in self.bluebetters:
            for account in accounts['Accounts']:
                if key == account['name']:
                    if winner == 'blue':
                        account['coin'] += self.bluebetters[key] * (self.redodd/self.blueodd)
                        account['wins'] += 1
                        account['profit'] += self.bluebetters[key] * (self.redodd/self.blueodd)
                        await ctx.send(f"{account['name']} wins {self.bluebetters[key] * (self.redodd/self.blueodd)}"
                                       f" shtickcoin!")
        with open('accounts.json', 'w') as json_file:
            json.dump(accounts, json_file,
                      indent=4)
        f.close()
