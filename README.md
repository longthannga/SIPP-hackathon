# SIPP-hackathon
# CircuitPython Blackjack 🃏

A hardware Blackjack game built with CircuitPython on the **Adafruit Metro M0 Express**, made for the **UCSD SIPP Program, Summer 2026**.

Two push buttons let you **Hit** or **Stand**, and a green/red LED pair tells you whether you won, lost, or drew. All game logic (deck, dealing, scoring, dealer AI) runs on the board — output is printed over serial, so you play by watching the buttons/LEDs while reading the log from the serial console (e.g. Mu Editor).

## How It Works

1. On startup (and after each new game), a fresh 52-card deck is created and shuffled using a Fisher–Yates shuffle.
2. The player and dealer are each dealt 2 cards. The dealer's first card is hidden (shown as `?`) until the round ends.
3. **Hit button**: draws another card into your hand.
4. **Stand button**: ends your turn — the dealer then draws until reaching a score of 17 or higher, and the result is decided.
5. Aces count as 11 when possible without busting, otherwise 1 (soft/hard ace logic).
6. **Green LED** = win, **Red LED** = lose, **both** = draw.
7. After the round ends, press either button to start a new game.

`gc.collect()` is called between games and after each card draw to keep memory usage low and stable on the M0's limited RAM.

## Hardware

- **Board:** Adafruit Metro M0 Express (runs CircuitPython) (for more info: [SIPP Board Info](https://sites.google.com/view/circuitpython/board-info?authuser=0))
- **Components:**
  - 2× momentary push buttons (Hit, Stand)
  - 1× green LED
  - 1× red LED
  - 1× resistor (current-limiting, for the red LED)
  - Breadboard + jumper wires
  - USB cable (data + power)

### Pin Mapping

| Component | Board Pin | Notes |
|---|---|---|
| Hit button | `D11` | Configured as input, internal pull-up |
| Stand button | `D10` | Configured as input, internal pull-up |
| Green LED | `D4` | Digital output |
| Red LED | `D3` | Digital output |
| Button/LED grounds | `GND` | Common ground rail on breadboard |

Buttons are wired with `Pull.UP`, so they read `True` (high) when unpressed and `False` (low) when pressed — this is why the code checks `if not hit_button.value`.

⚠️ The Metro M0 Express runs at **3.3V logic** — never connect 5V signals to its I/O pins.

## Wiring Diagram

The breadboard layout (see included circuit diagram) is as follows:
- Both push buttons sit across the center gap of the breadboard, with one leg of each wired to a digital pin (D11, D10) and the other leg tied to the ground rail.
- The green LED anode connects to D4; the red LED anode connects to D3 through the resistor.
- Both LED cathodes share the ground rail, tied back to the board's GND.

## Running the Code

1. Plug the Metro M0 Express into your computer via USB — it will show up as a `CIRCUITPY` drive.
2. Copy this script onto the drive as **`code.py`** (the board only auto-runs a file with this exact name).
3. Open a serial monitor (e.g. Mu Editor's serial console) to view game output.
4. The board will auto-restart and run the game as soon as `code.py` is saved.
5. Do **not** unplug the board or press reset while it's saving — this can corrupt the `CIRCUITPY` drive. Eject it properly first.

## Team

Built at the UCSD SIPP Program hackathon, Summer 2026.
- Terrence Chou (tchou1)
- Sam Ban (SamBan2601)
- Hoang Long Nguyen (longthannga)
- James Watkins (j3watkins-star)

## Possible Future Improvements

- Add a piezo buzzer for win/lose sound effects
- Add a display (e.g. OLED) to show the full hand instead of relying on serial output
- Support betting / chip tracking
- Add a "double down" or "split" option
