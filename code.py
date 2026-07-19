import board
import digitalio
import random
import time

# Cards
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        if self.value == 11:
            return f"Jack of {self.suit}"
        elif self.value == 12:
            return f"Queen of {self.suit}"
        elif self.value == 13:
            return f"King of {self.suit}"
        elif self.value == 1:
            return f"Ace of {self.suit}"
        else:
            return f"{self.value} of {self.suit}"
    
    def get_value(self):
        if 11 <= self.value <= 13:
            return 10
        else:
            return self.value

    def is_ace(self):
        return self.value == 1
    
# Players
class Player:
    def __init__(self):
        self.hand = []
        self.score = 0

    def add_card(self, card):
        self.hand.append(card)
        self.score = self.calculate_score()


    def calculate_score(self):
        total = sum(card.get_value() for card in self.hand)
        aces = sum(card.is_ace() for card in self.hand)

        #Ace can be 1 or 11 favorably, so if adding 10 doesn't bust the player, we add it
        while aces > 0 and total + 10 <= 21: 
            total += 10
            aces -= 1

        return total

    def show_hand(self):
        for card in self.hand:
            print(card)

    def get_score(self):
        return self.score


def main():
    # create a deck of cards
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] # Jack=11, Queen=12, King=13, Ace=1
    deck = [Card(suit, value) for suit in suits for value in values]
    random.shuffle(deck)

    dealer = Player()
    player = Player()


    # set up leds
    red_led = digitalio.DigitalInOut(board.D3)
    green_led = digitalio.DigitalInOut(board.D4)

    leds = [red_led, green_led,]

    for led in leds:
        led.direction = digitalio.Direction.OUTPUT
        led.value = False

    # set up buttons
    hit_button = digitalio.DigitalInOut(board.D11)
    stop_button = digitalio.DigitalInOut(board.D10)
    

    buttons = [hit_button, stop_button]

    for button in buttons:
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.PULL.UP

def player_choice():
    .#code for player's choice

# main game

while player.score() < 21:

print("hit or stay")

if player_choice() == "hit":
    player.add_card(deck.pop())
    print(player.hand[len(player.hand) - 1])
elif player_choice() == "stay":
    . #code for staying





