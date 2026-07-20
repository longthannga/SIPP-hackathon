import board
import digitalio
import random
import time
import gc

# ======================
# Card helpers
# ======================
SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
NAMES = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}


def card_str(card):
    suit, value = card
    name = NAMES.get(value, str(value))
    return "{} of {}".format(name, suit)


def card_value(card):
    v = card[1]
    return 10 if 11 <= v <= 13 else v


def card_is_ace(card):
    return card[1] == 1


# ======================
# Player
# ======================
class Player:
    __slots__ = ("hand", "score")

    def __init__(self):
        self.hand = []
        self.score = 0

    def add_card(self, card):
        self.hand.append(card)
        self.score = self.calculate_score()

    def calculate_score(self):
        total = 0
        aces = 0
        for card in self.hand:
            total += card_value(card)
            if card_is_ace(card):
                aces += 1
        while aces > 0 and total + 10 <= 21:
            total += 10
            aces -= 1
        return total

    def show_hand(self):
        for card in self.hand:
            print(" -", card_str(card))

    def get_score(self):
        return self.score


# ======================
# Hardware setup
# ======================
red_led = digitalio.DigitalInOut(board.D3)
green_led = digitalio.DigitalInOut(board.D4)
red_led.direction = digitalio.Direction.OUTPUT
green_led.direction = digitalio.Direction.OUTPUT

hit_button = digitalio.DigitalInOut(board.D11)
stand_button = digitalio.DigitalInOut(board.D10)
hit_button.direction = digitalio.Direction.INPUT
stand_button.direction = digitalio.Direction.INPUT
hit_button.pull = digitalio.Pull.UP
stand_button.pull = digitalio.Pull.UP


def clear_led():
    red_led.value = False
    green_led.value = False


# ======================
# Deck helpers
# ======================
def create_deck():
    deck = []
    for suit in SUITS:
        for value in range(1, 14):  # 1..13, Jack=11 Queen=12 King=13 Ace=1
            deck.append((suit, value))
    shuffle(deck)
    return deck


def shuffle(deck):
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]


def new_game():
    gc.collect()  # free previous game's objects BEFORE allocating the new deck
    deck = create_deck()
    player = Player()
    dealer = Player()
    player.add_card(deck.pop())
    player.add_card(deck.pop())
    dealer.add_card(deck.pop())
    dealer.add_card(deck.pop())
    return deck, player, dealer


# ======================
# Start
# ======================
print("Free memory:", gc.mem_free())

deck, player, dealer = new_game()
gc.collect()
game_over = False
last_score = -1
last_hand_size = 0

print("=== BLACKJACK ===")

# ======================
# Main Loop
# ======================
while True:
    if game_over:
        # restart on either button press
        if not hit_button.value or not stand_button.value:
            time.sleep(0.3)
            clear_led()
            # drop references before rebuilding, then collect inside new_game()
            deck = None
            player = None
            dealer = None
            deck, player, dealer = new_game()
            game_over = False
            last_score = -1
            last_hand_size = 0
            print("\nNew Game")
    else:    
        player_score = player.get_score()

        # determine if you got blackjack
        got_blackjack = (player_score == 21 and len(player.hand) == 2 and last_score != 21)

        # print when score or hand changes
        if player_score != last_score or len(player.hand) != last_hand_size:
            print("Dealer Hand:")
            print(" - ?")
            print(" -", card_str(dealer.hand[1]))
            print("Player Hand:")
            player.show_hand()
            print("Player Score:", player_score, "\n")
            last_score = player_score
            last_hand_size = len(player.hand)

        # Blackjack
        if got_blackjack:
            print("BLACKJACK\n")
            time.sleep(.5)

        # Bust
        elif player_score > 21:
            print("BUST! YOU LOSE")
            red_led.value = True
            game_over = True

        # Hit
        if not game_over and not hit_button.value:
            time.sleep(0.3)
            card = deck.pop()
            player.add_card(card)
            print("Hit:", card_str(card))
            gc.collect()

        # Stand
        if not game_over and (not stand_button.value or got_blackjack):
            time.sleep(0.3)
            print("Dealer turn")
            while dealer.get_score() < 17:
                dealer.add_card(deck.pop())

            player_score = player.get_score()
            dealer_score = dealer.get_score()
            print("Player:", player_score)
            player.show_hand()
            print("Dealer:", dealer_score)
            dealer.show_hand()

            if dealer_score > 21:
                print("Dealer Bust - YOU WIN")
                green_led.value = True
            elif player_score > dealer_score:
                print("YOU WIN")
                green_led.value = True
            elif player_score < dealer_score:
                print("YOU LOSE")
                red_led.value = True
            else:
                print("DRAW")
                red_led.value = True
                green_led.value = True

            game_over = True
            gc.collect()

    time.sleep(0.05)
