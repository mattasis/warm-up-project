#This class has list of cards, and methods for creating, viewing, and manipulating the list
#in various ways important to how Go Fish is played
from random import shuffle
class Deck():
    #this allows default construction, where 52 cards are added to a list, or it allows a list to be passed in
    def __init__(self, i = None):
        if i is None:
            self.cards = []
            for i in range(Card.DIAMONDS + 1):
                for j in range(2, Card.ACE + 1):
                    self.cards.append(Card(i, j))
        else:
            self.cards = i
            
    #Checks through the deck to see if it contains a certain card   
    def hasCard(self, rank):
        for i in range(len(self.cards)):
            if(self.cards[i].checkEquals(rank)):
                return True
        return False
    
    #Prints the deck as a string list, showing the cards in the deck
    def printDeck(self):
        for i in range(len(self.cards)):
            print(self.cards[i].toString())

    #removes all instances of rank and returns them in a list
    def removeAll(self, rank):
        removed = []
        for i in range(len(self.cards)):
            if i==rank:
                self.cards.remove(i)
                removed.add(i)
        return removed
    
    #adds newCards to this Deck's cards
    def addCards(self, newCards):
        self.cards.append(newCards)

    #checks to see if this Deck has four of the same rank card
    def hasBook(self, rank):
        counter=0
        for i in range(len(self.cards)):
            if i==rank:
                counter+=1
        if counter==4:
            return True
        else:
            return False
            
    #counts the occurrence of rank Card in the deck and returns it
    def count(self, rank):
        counter1=0
        for j in range(len(self.cards)):
            if j==rank:
                counter1+=1
        return counter1
        
    #randomizes the order of cards in the deck
    def shuffle(self):
        self.cards=shuffle(self.cards)
        return self.cards
        
    #removes the top n=size cards from the deck and returns them as a list
    def deal(self,size):
        dealt = []
        for i in range(size):
            dealt[i]=self.cards.pop()
        return dealt
    #removes only the top card from the deck and returns it
    def dealTop(self):
        card=self.cards.pop()
        return card
    