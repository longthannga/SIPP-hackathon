import board
import digitalio
import random
import time


# ======================
# Hardware
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



# ======================
# Card Functions
# ======================

def shuffle(deck):
    for i in range(len(deck)-1, 0, -1):
        j = random.randint(0, i)

        temp = deck[i]
        deck[i] = deck[j]
        deck[j] = temp



def create_deck():

    deck = []

    for card in range(1, 14):

        for i in range(4):

            deck.append(card)

    shuffle(deck)

    return deck



def card_value(card):

    if card >= 10:
        return 10

    return card



def score(hand):

    total = 0
    aces = 0


    for card in hand:

        total += card_value(card)

        if card == 1:
            aces += 1


    while aces > 0 and total + 10 <= 21:

        total += 10
        aces -= 1


    return total



# ======================
# Game Start
# ======================

def new_game():

    deck = create_deck()

    player = []
    dealer = []


    player.append(deck.pop())
    player.append(deck.pop())

    dealer.append(deck.pop())
    dealer.append(deck.pop())


    return deck, player, dealer



def clear_led():

    red_led.value = False
    green_led.value = False



# ======================
# Start
# ======================

deck, player, dealer = new_game()

game_over = False

last_score = -1


print("=== BLACKJACK ===")
print("D11 = HIT")
print("D10 = STAND")



# ======================
# Main Loop
# ======================

while True:


    if game_over:


        # restart

        if not hit_button.value or not stand_button.value:

            time.sleep(0.3)

            clear_led()

            deck, player, dealer = new_game()

            game_over = False

            last_score = -1

            print("\nNew Game")


    else:


        player_score = score(player)


        # only print when score changes

        if player_score != last_score:

            print("Player Score:", player_score)

            last_score = player_score



        # Blackjack

        if player_score == 21:

            print("BLACKJACK! YOU WIN")

            green_led.value = True

            game_over = True



        # Bust

        elif player_score > 21:

            print("BUST! YOU LOSE")

            red_led.value = True

            game_over = True



        # Hit

        if not hit_button.value:


            time.sleep(0.3)


            card = deck.pop()

            player.append(card)


            print("Hit:", card)



        # Stand

        if not stand_button.value:


            time.sleep(0.3)


            print("Dealer turn")


            dealer_score = score(dealer)


            while dealer_score < 17:

                dealer.append(deck.pop())

                dealer_score = score(dealer)



            player_score = score(player)


            print("Player:", player_score)

            print("Dealer:", dealer_score)



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



    time.sleep(0.05)