class opponent:
    def __init__(difficulty,ask_count):
        ask=0
        placeholder = 0
        deck=Deck(5)
        if difficulty==0:
            ##ask for random cards
            ##give card if in deck
            #in if for give, ask_count+=1
            placeholder =1
        
        elif difficulty==1:
            ##ask for last card in deck
            ##give card if in deck
            ##in if statement for giving card, ask_count += 1
            placeholder=2
        elif difficulty==2:
            
            if ask in deck and ask_count%3 != 0:
                ##give card
                placeholder =3
            elif ask in deck and ask_count%3=0:
                ##do not give card
                print "Go Fish"
            elif ask not in deck:
                print "Go Fish"