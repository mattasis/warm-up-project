class Player(object):
    def __init__(self, deck):
        self.hand = defaultdict(int)
        self.book = []
        self.deck = deck
        self.score = 0
        
    def draw(self):
        drawnCard = self.deck.pop()
        self.hand[drawnCard] += 1
        print 'You drew %s' % (drawnCard)
        self.checkBooks()
        
    def checkBooks(self):
        for i, value in self.hand.items():
            if value == 4:
                self.book.append(i)
                print 'Completed the %s book' % (i)
                self.score+=1
                del self.hand[i]
        self.checkEmpty()

    def checkEmpty(self):
        if len(self.deck)!=0 and len(self.hand)==0
            self.draw()

    def displayHand(self):
        return ' '.join(i for i, value in self.hand.iteritems())

    def playerTurn(self):
        print 'Your hand: %s' % (self.displayHand())
        askCard = raw_input('Ask for which card? ').strip()
        if askCard == 'quit':
            sys.exit(0)
        if askCard not in self.hand:
            print 'Invalid. Choose again or type "quit" to exit game.'
            askCard = self.makeTurn()
        return askCard

    def fishes(self,card):
        if card in self.hand:
            value = self.hand.pop(card)
            self.checkEmpty()
            return value
        else:
            return False
        
    def tookCard(self,card,amount):
        self.hand[card] += amount
        self.checkBooks()

class Computer(Player):
    def __init__(self,deck):
        self.hand = defaultdict(int)
        self.book = []
        self.deck = deck
        self.opponentHas = set()
        self.score = 0
 
     ##depending on difficulty, the Opponent might lie       
    def checkDeck(self, user_input):
        return self.deck.hasCard(user_input)

    ##depending on difficulty and recentCard, the opponent asks the user for a card
    def ask(self):
        #On easy difficulty, the opponent asks for a random card from its hand
        if self.difficulty==0:
            num=random.randint(0,len(self.deck)-1)
            card=self.deck[num]
            return card
            
            card=self.deck[-1]
            return card
            
            #On hard or devious difficulty, the opponent asks for the last
            #card added to its hand
        elif self.difficulty==1 or self.difficulty==2:
            card=self.deck[-1]
            return card
            
    def draw(self):
        cardDrawn = self.deck.pop()
        self.hand[cardDrawn] += 1 
        print 'Computer drew a card.' % (self.name)
        self.checkBooks()

    def compTurn(self):
        options = list(self.opponentHas & set(self.hand.i())))
        if not options:
            options = self.hand.i()
        move = random.choice(options)
        print 'Computer picks %s.' % (move)
        return move

    def fishes(self,card):
        self. opponentHas.add(card)
        if card in self:
            value = self.hand.pop(card)
            self.checkEmpty()
            return value
        else:
            return False

    def gotCard(self, card, total):
        self.hand[card] +=total
        self.opponentHas.discard(card)
        self.checkBooks()
