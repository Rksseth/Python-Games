'''
Ravi Seth
May 26
President Card Game
'''
import random

class Card(object):
    def __init__(self,val,suit):
        self.val = val
        self.suit = suit
        self.isRed = 0
        
        self.nextC = 0

class Player(object):
    def __init__(self,name0):
        self.cards = 0
        self.name = name0

        self.nextP = 0

class Game(object):
    def __init__(self):
        self.players = 0

        self.sizeP = 0

        self.order = [3,4,5,6,7,8,9,10,11,12,13,1,2]
        
        self.suits = ['spades','hearts','clubs','diamonds']

        self.deck = 0

        self.numCardsPlayed = 0

        self.cardsSelected = []

        self.winners = []

    def print(self):
        p = self.players
        while p:
            print(p.name)
            c = p.cards
            while c:
                print((c.val,c.suit),end=" ")
                c = c.nextC
            print()
            p = p.nextP
        return 1

    def shuffleAndDeal(self):
        cards = []
        for num in self.order:
            for suit in self.suits:
                cards.append(Card(num,suit))

        numCardsPerPlayer = int(len(cards) / self.sizeP)
        extraCards = len(cards) % self.sizeP

        player = self.players
        while cards:
            card = random.choice(cards)
            cards.remove(card)
            self.insertCard(player,card)
            player = player.nextP

            if not player:
                player = self.players

        return 1           
        
    def insertPlayer(self,player):
        if not self.players:
            self.players = player
            self.sizeP += 1
            return 1

        temp = self.players
        while temp.nextP:
            temp = temp.nextP
        temp.nextP = player
        self.sizeP += 1
        return 1

    def searchPlayer(self,player):
        temp = self.players
        while temp:
            if temp.name == player.name:
                return temp
            temp = temp.nextP
        return 0
    
    def removePlayer(self,player):
        if not self.searchPlayer(player):
            return 0

        if self.players.name == player.name:
            self.players = self.players.nextP
            self.sizeP -= 1
            return 1

        temp = self.players
        while not (temp.nextP.name == player.name):
            temp = temp.nextP

        temp.nextP = temp.nextP.nextP
        self.sizeP -= 1
        return 1

    def insertCard(self,player,card):
        c = player.cards

        if not c:
            player.cards = card
            return 1

        while c.nextC:
            c = c.nextC
        c.nextC = card
        return 1

    def searchCard(self,player,card):
        temp = player.cards
        while temp:
            if temp.val == card.val and temp.suit == card.suit:
                return temp
            temp = temp.nextC
        return 0
    
    def removeCard(self,player,card):
        if not self.searchCard(player,card):
            return 0

        if player.cards.val == card.val and player.cards.suit == card.suit:
            player.cards = player.cards.nextC
            return 1
        
        temp = player.cards
        while not (temp.nextC.val == card.val and temp.nextC.suit == card.suit):
            temp = temp.nextC

        temp.nextC = temp.nextC.nextC
        return 1

    def getVal(self):
        val = input("Val : ")

        try:
            val = int(val)

            if val in self.order:
                return val
            print("NO SUCH VAL")
            return -1
        except:
            print("NOT AN INT")
            return -1

    def getSuit(self):
        suit = input("Suit : ")

        if suit in self.suits:
            return suit

        print("NO SUCH SUIT")
        return 0

    def getDone(self):
        done = input("Done Selecting (Y or N) : ")

        done = done.upper()

        if done == 'Y':
            return 1
        return 0

    def inputSelectCards(self):
        val = self.getVal()
        if not(val > 0):
            return 0

        suit = self.getSuit()
        if not suit:
            return 0

        self.selectCards(val,suit)
        return 1

    def selectCards(self,val,suit):

        card = self.searchCard(self.players,Card(val,suit))

        if not card:
            return 0

        if card in self.cardsSelected:
            self.cardsSelected.remove(card)

        else:
            self.cardsSelected.append(card)

        if self.getDone():
            #PLACE SELECTED CARDS ON DECK
            #self.placeCards()
            print(self.cardsSelected)
            return 1
        return 1

    def placeCards(self):
        #PLACE SELECTED CARDS ON DECK ONLY IF VALID
        if self.validCardAmount() and self.validCardSet() and self.validToPlace():
            self.insertToDeck()
            return 1
        return 0

    def validCardAmount(self):
        #MAKE SURE NUM CARDS TO BE PLACE FOLLOW PATTERN
        if not self.numCardsPlayed:
            return 1
        elif self.numCardsPlayed == len(self.cardsSelected):
            return 1
        return 0

    def validCardSet(self):
        #MAKE SURE THE CARDS SELECTED CAN BE PLAYED TOGETHER
        if len(self.cardsSelected) == 1:
            return 1
        val = -1
        for item in self.cardsSelected:
            if val == -1:
                val = item.val
            elif not (val == item.val):
                return 0
        return 1

    def validToPlace(self):
        #MAKE SURE CARDS SELECTED CAN BE PLACE ON DECK
        lastCardVal = self.deck.val

        newVal = self.selectedCards[0]

        validMove = False

        for val in self.order:
            if val == lastCardVal:
                validMove = True

            if validMove and newVal == val:
                return 1
        return 0

    def insertToDeck(self):
        #REMOVE SELECTED CARDS FROM PLAYERS DECK
        for card in self.selectedCards:
            self.removeCard(self.players,card)
            

        for cardIdx in range(0,len(self.selectedCards)-1):
            self.selectedCards[cardIdx].nextC = self.selectedCard[cardIdx + 1]

        #BURN
        if self.deck:
            if self.deck.val == self.selectedCards[0].val:
                self.deck = 0
                self.selectedCards = []

                if self.players.cards == 0:
                    self.winners.append(self.player)
                    self.removePlayer(self.player)
                return 1

        #NOT A BURN
        if self.deck == 0:
            self.deck = self.selectedCards[0]
        else:
            self.deck.nextC = self.selectedCards[0]
            
        if self.players.cards == 0:
            self.winners.append(self.player)
            self.removePlayer(self.player)
        return 1

    def changeTurn(self):
        self.insertPlayer(self.players)
        self.removePlayer(self.players)
        return 1
            

p = Game()

p1 = Player('Ravi')
p2 = Player('Boi')
p3 = Player('Savage')
p.insertPlayer(p1)
p.insertPlayer(p2)
p.insertPlayer(p3)

p.insertCard(p1,Card(12,'spades'))
p.insertCard(p1,Card(1,'diamonds'))

p.shuffleAndDeal()

p.print()

            


        
            

        


        

    
            

        

    
            
        

        
