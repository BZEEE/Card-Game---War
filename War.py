import random
import time
from random import shuffle

class circularQueue:
    def __init__(self, capacity):
        assert isinstance(capacity, int), ("Error: Type Error: %s" % (type(capacity)))
        assert capacity >= 0, ("Error: Illegal capacity: %d" % (capacity))
        
        self.__queue = []
        self.__head = 0
        self.__tail = 0
        self.__count = 0
        self.__capacity = capacity
        
    def enqueue(self, item):
        try:
            assert self.__count != self.__capacity
            if len(self.__queue) < self.__capacity:
                self.__queue.append(item)
            else:
                self.__queue[self.__tail] = item
            self.__count += 1
            self.__tail = (self.__tail + 1) % self.__capacity
        except AssertionError:
            print("Circular Queue is at full capacity")
        
    def dequeue(self):
        try:
            assert not self.isEmpty()
            item = self.__queue[self.__head]
            self.__queue[self.__head] = None
            self.__count -= 1
            self.__head = (self.__head + 1) % self.__capacity
            return item
        except AssertionError:
            print("Circular Queue is empty, nothing to return")
        
    
    def peek(self):
        if not self.isEmpty():
            return self.__queue[self.__head]
    
    def isEmpty(self):
        return self.__count == 0   
    
    def isFull(self):
        return self.__count == self.__capacity
    
    def size(self):
        return self.__count
    
    def capacity(self):
        return self.__capacity
    
    def clear(self):
        self.__queue = []
        self.__count = 0
        self.__head = 0
        self.__tail = 0
        
    def __str__(self):
        empty = True
        str_exp = ']'
        i = self.__head
        for j in range(self.__count):
            str_exp += (self.__queue[i] + ', ')
            i = (i+1) % self.__capacity
            empty = False
        if not empty:
            str_exp = str_exp[:len(str_exp)-2]
        return str_exp + ']'
    
    
class OnTable:
    def __init__(self):
        self.__cards = []
        self.__faceUp = []
        
    def place(self, player, card, hidden):
        if player == 1:
            self.__cards.insert(0, card)
            self.__faceUp.insert(0, hidden)
        elif player == 2:
            self.__cards.append(card)
            self.__faceUp.append(hidden)
    
    def cleanTable(self):
        cards = tuple(self.__cards)
        self.__cards = []
        self.__faceUp = []
        return list(cards)
    
    def __str__(self):
        str_exp = '['
        i = 0
        while i < len(self.__cards):
            if i > 0:
                str_exp += ', '
            if self.__faceUp[i]:
                str_exp += 'XX'
            else:
                str_exp += self.__cards[i]
            i += 1
        return str_exp + ']'

    
class Game:
    def __init__(self, warCards):
        self.player1Hand = circularQueue(52)
        self.player2Hand = circularQueue(52)
        self.card_value = {'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'0': 10,'J': 11,'Q': 12,'K': 13,'A': 14}
        self.continue_game = True
        self.warCards = warCards
        self.table = OnTable()
        
    def deal_cards(self, cards):
        #player 1 or 2 is randomly selected to start receiving cards
        turn = random.choice([True, False])
        for card in cards:
            if turn:
                self.player1Hand.enqueue(card)
                turn = False
            else:
                self.player2Hand.enqueue(card)
                turn = True
        # both players now have 26 cards each in their hand
        
    def update_table(self, player1card, player2card, hidden):
        self.table.place(1, player1card, hidden)
        self.table.place(2, player2card, hidden)
                
    def play(self):
        end_session = False
        while not end_session:
            self.decide_continue()
            if self.continue_game:
                self.play_hand()
            else:
                end_session = True
            
    def play_hand(self):
        player1_card = self.player1Hand.dequeue()
        player2_card = self.player2Hand.dequeue()
        self.update_table(player1_card, player2_card, False)
        
        num = self.compare_cards(player1_card, player2_card)
        if num == 1:
            self.player1Hand.enqueue(player1_card)
            self.player1Hand.enqueue(player2_card)
            print(self.table)
            self.display_hand()            
                                    
            
        elif num == -1:
            self.player2Hand.enqueue(player1_card)
            self.player2Hand.enqueue(player2_card)
            print(self.table)
            self.display_hand()
                                    
        
        else:
            self.war(self.warCards)
                        
            
    def war(self, warCards):
       
        war = True
        while war:
                
            for version in range(warCards):
                if not self.player1Hand.isEmpty() and not self.player2Hand.isEmpty():
                    card1 = self.player1Hand.dequeue()
                    card2 = self.player2Hand.dequeue()
                    self.update_table(card1, card2, True)
                    self.decide_continue()
                
            if self.continue_game:
                player1_card = self.player1Hand.dequeue()
                player2_card = self.player2Hand.dequeue()
                self.update_table(player1_card, player2_card, False)
                num = self.compare_cards(player1_card, player2_card)
                
                if num == 1:
                    print(self.table)
                    for card in self.table.cleanTable():
                        self.player1Hand.enqueue(card)
                    self.display_hand()
                    war = False
                    
                elif num == -1:
                    print(self.table)
                    for card in self.table.cleanTable():
                        self.player2Hand.enqueue(card)
                    self.display_hand()    
                    war = False
            
            else:
                war = False
                print(self.table)
                self.display_hand()
                
            
    def compare_cards(self, player1_card, player2_card):
        if self.card_value[player1_card[0]] > self.card_value[player2_card[0]]:
            return 1
        elif self.card_value[player1_card[0]] < self.card_value[player2_card[0]]:
            return -1
        else:
            return 0
        
    def display_hand(self):
        print("Player1: {}".format(self.player1Hand.size()))
        print("Player 2: {}".format(self.player2Hand.size()))
        input("Press return key to continue")
        #pause between hands     
        self.table.cleanTable()
        print('')   
        

    def decide_continue(self):
        if self.player1Hand.isEmpty():
            self.continue_game = False
            print("Player 2 wins")
            
        elif self.player2Hand.isEmpty():
            self.continue_game = False
            print("Player 1 wins")
            


def main():
    
    # acceptable cards
    suits=["D", "C", "H", "S"]
    ranks=["K","Q","J","A","2","3","4","5","6","7","8","9","0"] 
    
    cards=[]
    for rank in ranks:
        for suit in suits:
            cards.append(rank+suit)
            
    shuffle(cards)
    try:
       cardFile= open("shuffledDeck.txt", "w")
       for card in cards:
           cardFile.write(card+"\n")
    except IOError as e:
        print ("I/O error({0}: {1}".format(e.errno, e.strerror))
    except:
        print ("Unexpected error")
    finally:
        cardFile.close()
    print("The following shuffled 52 card deck was saved in shuffledDeck.txt")    
    
    
    
    try:
        # try to open file
        file = input("Enter shuffled card file: ")
        File = open(file, 'r')
        cards = File.read().splitlines()
        #check if there is 52 cards in the deck
        assert (len(cards) == 52)
        
        #check that each card is the righ format
        cardIndex = 0
        formatted = True
        while formatted and cardIndex < 52:
            #checks that there is only two values for each card, the rank first and the suit
            if len(cards[cardIndex]) == 2:
                
                # if both values are letters, and one of them is not an acceptable rank and suit
                if cards[cardIndex].isalpha():
                    if (not cards[cardIndex][0].upper() in ranks) or (not cards[cardIndex][1].upper() in suits):
                        print("card suit or rank does not exist in the proper range of a deck of a cards")
                        formatted = False
                    
                #in case the rank is a number, and checks if the card has an acceptable rank and suit   
                else:
                    if (not cards[cardIndex][0] in ranks) and (not cards[cardIndex][1].upper() in suits):
                        print("card suit or rank does not exist in the proper range of a deck of a cards")
                        formatted = False
                    
            #means there more or less than two values for each, which is wrong formatting        
            else:
                print("Cards are not formatted properly")
                formatted = False
            
            cardIndex += 1  
        # close file
        File.close()
        
    except FileNotFoundError:
        print("file not found")
    except AssertionError:
        print("there is not 52 cards in the deck")
    else:
        # if the file is found and all cards have an acceptable form, then run the game
        valid_input = False
        while not valid_input:
            valid = ['1', '2', '3']
            warCards = input("Play a war with 1, 2, or 3 cards? ")
            if warCards in valid:
                warCards = int(warCards)
                valid_input = True
        game = Game(warCards)
        game.deal_cards(cards)
        game.play()
        input("press any key to exit")
        
main()