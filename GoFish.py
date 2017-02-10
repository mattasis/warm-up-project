class Opponent():
    def __init__(self, deck, difficulty, laidDown):
        self.deck = deck
        self.difficulty = difficulty
        self.laidDown = laidDown
        self.books = 0
        self.recentCard = None

    ##depending on difficulty, the Opponent might lie       
    def checkDeck(self, user_input):
        return self.deck.hasCard(user_input)

    ##depending on difficulty and recentCard, the opponent asks the user for a card
    def ask():
        return 2
    
class Card():
    
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    
    SPADES = 0
    CLUBS = 1
    HEARTS = 2
    DIAMONDS = 3
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def checkEquals(self, otherRank):
        return self.rank == otherRank
    
    def toString(self):
        formated_suit = ""
        if (self.suit == Card.SPADES):
            formated_suit = "Spades"
        elif (self.suit == Card.CLUBS):
            formated_suit = "Clubs"
        elif (self.suit == Card.HEARTS):
            formated_suit = "Hearts"
        elif (self.suit == Card.DIAMONDS):
            formated_suit = "Diamonds"
        else:
            formated_suit = "what"

        formated_rank = ""
        if (self.rank >= Card.JACK):
            if (self.rank == Card.JACK):
                formated_rank = "Jack"
            elif (self.rank == Card.QUEEN):
                formated_rank = "Queen"
            elif (self.rank == Card.KING):
                formated_rank = "King"
            else:
                formated_rank = "Ace"
        else:
            formated_rank = self.rank
        output = str(formated_rank) + " of " + str(formated_suit)
        return output
                
class Player():
    def __init__(self, deck):
        self.deck = deck
        self.books = 0
    def addBook(self):
        self.books += 1

#This class has list of cards, which it can manipulate with various methods.
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
            
    def hasCard(self, rank):
        for i in range(len(self.cards)):
            if(self.cards[i].checkEquals(rank)):
                return True
        return False
        
    def printDeck(self):
        for i in range(len(self.cards)):
            print(self.cards[i].toString())

    ##removes all instances of rank and returns them in a list
    def removeAll(self, rank):
        return
    
    ##append newCards to this Deck's cards
    def addCards(self, newCards):
        return

    ##checks to see if this Deck has four of the same rank card
    def hasBook(self, rank):
        return
    ##count the occurrence of rank Card in the deck and returns it
    def count(self, rank):
        return
    ##shuffle the deck
    def shuffle(self):
        return
    
SENTINEL = "stop"
HAND_SIZE = 7

def main():
    #get the difficulty
    difficulty = int(input("Enter user difficulty (0 = easy, 1 = smart, 2 = devious): "))
    print("HI")
    #start creating all the objects
    stock = Deck()
    stock.shuffle() #implement
    laidDown = []
    playerCards = []
    opponentCards = []
    for i in range(HAND_SIZE):
        playerCards.append(stock.cards.pop())
    for i in range(HAND_SIZE):
        opponentCards.append(stock.cards.pop())
        
    #make two more decks out of the card lists
    playerHand = Deck(playerCards)
    opponentHand = Deck(opponentCards)

    player = Player(playerHand)
    opponent = Opponent(opponentHand, difficulty, laidDown)

    #just to make sure it's working
    print("Player Hand: ")
    player.deck.printDeck()
    
    print("Opponent Hand: ")
    opponent.deck.printDeck() 
    
    #print("Rest of deck: ")
    #deck.printDeck()
    
    
    
    gameGoing = True
    while(gameGoing):
        hotStreak = True
        #Player's turn
        print("Your turn!")
        while(hotStreak):
            request = input("Take your guess: ")
            if (request != SENTINEL):
                formated_request = parseInput(request)
                while (request != SENTINEL and not formated_request):
                    request = input("Invalid input, please try again: ")
                    formated_request = parseInput(request)
                if (request != SENTINEL):
                    #get rid of the question mark so it can be printed
                    request = request[0:-1]
                    if (opponent.checkDeck(formated_request)):
                        print("The opponent has a ", request, "! You will get to go again.", sep = "")
                        player.deck.addCards(opponent.deck.removeAll(formated_request))
                        #check for a book
                        if (player.deck.hasBook(formated_request)):
                            print("You have four ", request, "s! +1 point", sep = "")
                            laidDown.append(player.deck.removeAll(formated_request))
                            player.addBook()
                            
                    #Go fish!
                    else:
                        print("The opponent does not have any ", request,"s. Go fish!", sep = "")
                        newCard = stock.cards.pop()
                        print("You picked up a", newCard.toString(), ".")
                        player.deck.cards.append(newCard)
                        
                        #got the card you asked for originally
                        if (newCard.checkEquals(formated_request)):
                            print("You picked up the card you originally asked for! You will get to go again.")
                            if (player.deck.hasBook(formated_request)):
                                print("You have four ", request, "s! +1 point", sep = "")
                                laidDown.append(player.deck.removeAll(formated_request))
                                player.addBook()
                        else:
                            hotStreak = False
                else:
                    gameGoing = False
                    hotStreak = False
            else:
                gameGoing = False
                hotStreak = False
        #Opponent's turn
        if (gameGoing):
            hotStreak = True
            while(hotStreak):
                print("Opponent's turn.")
                #request = opponent.ask()
                hotStreak = False
    #print(playerCards.contains
    #for i in range(52):
        #print(deck.cards[i].rank, "is the rank, ", deck.cards[i].suit, " is the suit.")
    #card = deck.cards.pop()
        
# this method should take the user's input and return a value that can be checked, or false if it's invalid
# for example, user_input = kings? should return 13
def parseInput(user_input):
    if (user_input == "2?"):
        return 2
    elif (user_input == "3?"):
        return 3
    elif (user_input == "4?"):
        return 4
    elif (user_input == "5?"):
        return 5
    elif (user_input == "6?"):
        return 6
    elif (user_input == "7?"):
        return 7
    elif (user_input == "8?"):
        return 8
    elif (user_input == "9?"):
        return 9
    elif (user_input == "10?"):
        return 10
    elif (user_input == "jack?"):
        return Card.JACK
    elif (user_input == "queen?"):
        return Card.QUEEN
    elif (user_input == "king?"):
        return Card.KING
    elif (user_input == "ace?"):
        return Card.ACE
    else:
        return False
main()
