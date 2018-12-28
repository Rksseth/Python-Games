'''
Solitaire
May 10
'''
import random
from tkinter import*
from tkinter import font

root = Tk()
root.title("Solitaire")
root.geometry("700x600")
root.configure(bg = "green")

title = Label(root,text = "Solitaire",font = ('Algerian',20),bg='green',fg = 'white').pack()

class Card(object):
    def __init__(self):
        self.val = 0
        self.suit = ""
        self.isFlipped = 0
        self.down = 0
        self.up = 0
        self.isRed = 0

        self.c = Button(root,font = "Rockwell 10",width = 7,height = 5,bd = 2,relief = RIDGE,fg = 'white')


class Game(object):
    def __init__(self):
        self.suits = ['Spades','Hearts','Clubs','Diamonds']
        self.aces = []
        self.deck = []
        self.deckFlipped = []
        self.slots = 7
        self.set = [0 for x in range(0,self.slots)]
        self.move = 0

    def setup(self):
        #FILL deck
        for suit in self.suits:
            for num in range(1,13):
                newCard = Card()
                newCard.suit = suit
                newCard.val = num

                newCard.c['command'] = lambda cardToMove = newCard:self.moveCard(cardToMove)

                if suit == 'Spades' or suit == 'Clubs':
                    newCard.isRed = 0
                else:
                    newCard.isRed = 1

                self.deck.append(newCard)

        #ASSIGN deck to positions in set
        for slot in range(0,self.slots):
            for unFlipped in range(0,slot):
                card = random.choice(self.deck)
                card.isFlipped = 0
                self.deck.remove(card)

                #CASE 1 - no card in slot
                if not self.set[slot]:
                    self.set[slot] = card
                #CASE 2 - card already in slot
                else:
                    temp = self.set[slot]
                    while temp.down:
                        temp = temp.down
                    temp.down = card
                    card.up = temp
                    
            #ADD A FLIPPED CARD AT THE END
            card2 = random.choice(self.deck)
            self.deck.remove(card2)
            card2.isFlipped = 1
            #CASE 1 - no card in slot
            if not self.set[slot]:
                self.set[slot] = card2
            #CASE 2 - card already in slot
            else:
                temp = self.set[slot]
                while temp.down:
                    temp = temp.down
                temp.down = card2
                card2.up = temp
        return True

    def printDeck(self):
        if len(self.deck) == 0:
            return 0
        card = self.deck[0]
        card.isFlipped = 1
        text = str(card.val)+" "+card.suit
        card.c['text'] = text
        if card.isRed:
            card.c['bg'] = 'red'
        else:
            card.c['bg'] = 'black'
        card.c.place(x = 600,y = 50)
        return 1
            
    def printAces(self):
        count = 0
        for item in self.aces:
            temp = item
            if temp:
                while temp.down:
                    #print(temp.val,temp.suit,end=" ")
                    temp = temp.down
                temp.c.place(x=count*50+50,y = 500)
                count += 1
        #print()
        return 1

    def printSet(self):
        for item in self.set:
                temp = item
                counter = 0
                while temp:
                    if temp.isFlipped:
                        #print(temp.val,temp.suit,end=" ")
                        text = str(temp.val)+"\n"+(temp.suit)

                        if temp.isRed:
                            temp.c['bg'] = 'red'
                        else:
                            temp.c['bg'] = 'grey20'
                    else:
                        temp.c['bg'] = 'grey'
                        #print("XXX",end=" ")
                        text = ""
                    temp.c['text'] = text
                    temp.c['command'] = lambda cardToMove = temp:self.moveCard(cardToMove)
                    temp.c.lift()
                    #WINDOWS VERSION
                    #temp.c.place(x = self.set.index(item)*70+10,y = counter*30+50)
                    #OS X 10 VERSION
                    temp.c.place(x= self.set.index(item)*80+10,y = counter*50+50)
                    temp = temp.down
                    counter += 1
                #print()

    def placeOnAces(self,card):
        if len(self.aces) == 0:
            return 0
        for item in self.set:
            temp = item
            while item.down:
                if item.down == card:
                    item.down = 0
                    return 1
                item = item.down
        for item in self.aces:
            temp = item
            while temp.down:
                temp = temp.down
            if card.val - temp.val == 1 and card.suit == temp.suit:
                temp.down = card
                card.up = temp
                return 1
        return 0
    
    def placeCard(self,card):
        #CHECK if can placed on set
        for col in range(0,self.slots):
            item = self.set[col]
            if item:
                while item.down:
                    item = item.down
                if item.val - card.val == 1 and item.isRed is not card.isRed:
                    item.down = card
                    card.up = item
                    return 1
                
        return 0
    
    def moveCard(self,card):
        #CASE 0.5 - card in deck
        if card in self.deck:
            placed = self.placeCard(card)
            onAces = self.placeOnAces(card)
            if placed or onAces:
                return 1
            self.checkDeck()
            return 0
                        
        
        #CASE 1 - card not flipped
        if not card.isFlipped:
            return False

        #CASE 2 - card flipped and is at bottom
        if not card.down:
            #CASE 2.1 - check if it can go onto aces
            if card.val == 1 and card not in self.aces:
                self.aces.append(card)
                self.flipUnFlip(card)
                self.printAces()
                return True

            #CASE 2.2 - check if it is an ace
            elif card.val == 13:
                for col in range(0,self.slots):
                    if not item:
                        self.set[col] = card
                        self.flipUnFlip(card)
                        self.printSet()
                        self.printAces()
                        return 1
            #CASE 2.3 - any other card, check if it can be added
            else:
                aces = self.placeOnAces(card)
                if aces:
                    self.flipUnFlip(card)
                    self.printSet()
                    self.printAces()
                    return 1
                for col in range(0,self.slots):
                    item = self.set[col]
                    if item:
                        temp = item
                        while temp.down:
                            temp = temp.down
                        if temp.val - card.val == 1 and temp.isRed is not card.isRed:
                            temp.down = card
                            self.flipUnFlip(card)
                            self.printSet()
                            self.printAces()
                            return 1
                        
        #CASE 3 - card has cards under it
        else:
            #CASE 3.1 - card has not been selected to move
            for col in range(0,self.slots):
                item = self.set[col]
                if item:
                    temp = item
                    while temp.down:
                        temp = temp.down
                    if temp.val - card.val == 1 and temp.isRed is not card.isRed:
                        temp.down = card
                        self.flipUnFlip(card)
                        self.printSet()
                        return 1
        return False
        
                
                

    def flipUnFlip(self,card):
        if card.up:
            upper = card.up
            upper.isFlipped = 1
            upper.down = 0
            upper.c['text'] = str(upper.val)+"\n"+upper.suit
            if upper.isRed:
                upper.c['bg'] = 'red'
            else:
                upper.c['bg'] = 'grey20'
        else:
            if card in self.set:
                x = self.set.index(card)
                self.set[x] = 0
        card.c.place_forget()
        return 1

    def checkDeck(self):
        for item in self.deck:
            if item.isFlipped:
                item.isFlipped = 0
                self.deck.remove(item)
                self.deckFlipped.append(item)

        self.printDeck()
        return 1

        
                

s = Game()
s.setup()
s.printSet()
s.printDeck()
