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
        self.redodd = 1
        self.blueodd = 1
        self.creator = creator
        self.matchid = len(matches) + 1

