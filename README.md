# Black-jack-card-counter
A full featured black jack card counting application

## setup Guide

### 1. Clone the Repository git clone https://github.com/tunetyme/black-jack-card-counter.git
cd blackjack-card-counter

2. Create a Virtual Environment (Optional)

Create a virtual environment to manage dependencies.
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies

Install the required dependencies using pip and the requirements.txt file.

pip install -r requirements.txt

4. Run the Application

   python main.py


## ALTERNATIVE INSTALL METHOD ##

1. Run pip install .

   This will install the application and its dependencies, allowing you to run it using the blackjack-counter command.


 ## User Guide
Starting the Application

Select Counting Strategy: Choose the card counting strategy (Hi-Lo, Zen, Omega II, Wong Halves) from the dropdown menu.
Number of Decks: Select the number of decks in play from the dropdown menu.
Minimum Bet: Enter the minimum bet amount in the input field.
Using the Application

Enter Cards:
Button Input: Click the buttons representing the cards dealt.
Keyboard Input: Use the number keys to input cards 2-9, '0' for 10, and 'A' for Ace.
View Statistics:
True Count: The true count is displayed prominently in the center and changes color based on its value (green for positive counts and red for negative counts).
Cards Left: Displays the number of cards left in the deck.
Kelly Bet: Shows the suggested bet multiple based on the Kelly Criterion.
Last Card: Displays the last card entered for 3 seconds.
Reset Count: Click the "Reset" button to reset the count. A confirmation dialog will appear to confirm the reset.
Advanced Features

High and Low Cards Left: Shows the number of high and low cards left in the deck.
Remaining Cards by Value: Displays the remaining cards by their value to help make informed decisions.

## Folder Structure ## 

BlackjackCardCounter/
    setup.py
    BlackjackCardCounter/
        __init__.py
        main.py
        counting.py
        # any other .py files

