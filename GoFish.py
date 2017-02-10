from data_ball import DataBall
from Game_Utilities import Card
from Game_Utilities import Deck
from Game_Utilities import Opponent
from Game_Utilities import Player
SENTINEL = "stop"
HAND_SIZE = 7

def main():
    #get the difficulty
    difficulty = int(input("Enter user difficulty (0 = easy, 1 = smart, 2 = devious): "))
    #dataBall = DataBall(difficulty)
    #dataBall.update()
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
