import board
import digitalio
import random
import time

# set up leds
red_led = digitalio.DigitalInOut(board.D5)
blue_led = digitalio.DigitalInOut(board.D4)
green_led = digitalio.DigitalInOut(board.D3)
yellow_led = digitalio.DigitalInOut(board.D2)

leds = [red_led, blue_led, green_led, yellow_led]

for led in leds:
    led.direction = digitalio.Direction.OUTPUT
    led.value = False

# set up buttons
red_button = digitalio.DigitalInOut(board.D11)
blue_button = digitalio.DigitalInOut(board.D10)
green_button = digitalio.DigitalInOut(board.D9)
yellow_button = digitalio.DigitalInOut(board.D8)

buttons = [red_button, blue_button, green_button, yellow_button]

for button in buttons:
   button.direction = digitalio.Direction.INPUT
   button.pull = digitalio.PULL.UP

sequence = []

# show the sequence
def show_sequence():
    for color in sequence:
        leds[color].value = True
        time.sleep(0.5)
        leds[color].value = False

# add a random color to sequence
def add_to_sequence():
    sequence.append(random.randint(0, 3))

# check player's input
def check_player_input():
    for correct_color in sequence:
        if press_color() != correct_color:
            return False

    return True

def press_button():
    # code for pressing button

# main game
while True:
    add_to_sequence()

    show_sequence()

    # check player's answer

    # if wrong end game






