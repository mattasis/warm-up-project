class Card(object):

    suitNames = ["Hearts", "Spades", "Diamonds", "Clubs"]
    rankNames = [None, "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def toString(self):
        return '%s of %s’ % (Card.rankNames[self.rank], Card.suitNames[self.suit])

    def  compare(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return compare (t1, t2)
