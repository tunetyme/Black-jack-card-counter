import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
                             QComboBox, QLineEdit, QPushButton, QTextEdit, QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtCore import Qt, QTimer

class CardCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack Card Counter")

        self.counting_strategy = "Hi-Lo"
        self.deck_count = 1
        self.min_bet = 1.0
        self.running_count = 0
        self.cards_counted = 0
        self.card_history = []
        self.card_buttons = {}
        self.card_count = {str(i): 0 for i in range(2, 11)}
        self.card_count.update({"10": 0, 'A': 0})

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        top_layout = QGridLayout()
        layout.addLayout(top_layout)

        # Counting Strategy Selection
        strategy_label = QLabel("Select Counting Strategy:")
        strategy_label.setStyleSheet("font-size: 16px;")
        strategy_label.setToolTip("Select the counting strategy to use.")
        top_layout.addWidget(strategy_label, 0, 0)
        self.strategy_combobox = QComboBox()
        self.strategy_combobox.addItems(["Hi-Lo", "Zen", "Omega II", "Wong Halves"])
        self.strategy_combobox.setStyleSheet("font-size: 16px;")
        self.strategy_combobox.setToolTip("Choose the card counting strategy.")
        self.strategy_combobox.currentIndexChanged.connect(self.strategy_changed)
        top_layout.addWidget(self.strategy_combobox, 0, 1)

        # Deck Count Input
        deck_label = QLabel("Number of Decks:")
        deck_label.setStyleSheet("font-size: 16px;")
        deck_label.setToolTip("Select the number of decks in play.")
        top_layout.addWidget(deck_label, 1, 0)
        self.deck_combobox = QComboBox()
        self.deck_combobox.addItems([str(i) for i in range(1, 9)])
        self.deck_combobox.setStyleSheet("font-size: 16px;")
        self.deck_combobox.setToolTip("Choose the number of decks.")
        self.deck_combobox.currentIndexChanged.connect(self.deck_changed)
        top_layout.addWidget(self.deck_combobox, 1, 1)

        # Minimum Bet Input
        min_bet_label = QLabel("Minimum Bet:")
        min_bet_label.setStyleSheet("font-size: 16px;")
        min_bet_label.setToolTip("Enter the minimum bet amount.")
        top_layout.addWidget(min_bet_label, 2, 0)
        self.min_bet_entry = QLineEdit("1.0")
        self.min_bet_entry.setStyleSheet("font-size: 16px;")
        self.min_bet_entry.setToolTip("Specify the minimum bet amount.")
        self.min_bet_entry.textChanged.connect(self.min_bet_changed)
        self.min_bet_entry.returnPressed.connect(self.clear_focus)
        top_layout.addWidget(self.min_bet_entry, 2, 1)

        # Help Button
        help_button = QPushButton("Help")
        help_button.setStyleSheet("font-size: 16px; padding: 10px;")
        help_button.setToolTip("Click for help on how to use the app.")
        help_button.clicked.connect(self.show_help)
        top_layout.addWidget(help_button, 0, 2, 1, 2)

        # Card Buttons
        button_layout = QGridLayout()
        layout.addLayout(button_layout)
        card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
        positions = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2)  # Adjusted positions for 10 and A
        ]
        self.card_buttons = {}
        for index, value in enumerate(card_values):
            button = QPushButton(value)
            button.setStyleSheet("font-size: 18px; padding: 10px;")
            button.clicked.connect(lambda _, v=value: self.update_count(v))
            row, col = positions[index]
            button_layout.addWidget(button, row, col)
            self.card_buttons[value] = button

        # Reset Button
        reset_button = QPushButton("Reset")
        reset_button.setStyleSheet("font-size: 18px; padding: 10px;")
        reset_button.setToolTip("Reset the count.")
        reset_button.clicked.connect(self.reset_count)
        layout.addWidget(reset_button)

        # Count Displays
        self.true_count_label = QLabel("True Count: 0")
        self.true_count_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        self.true_count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.true_count_label, alignment=Qt.AlignCenter)

        self.cards_left_label = QLabel("Cards Left: 0")
        self.cards_left_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.cards_left_label)

        self.kelly_label = QLabel("Kelly Bet (multiple of min): 0")
        self.kelly_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.kelly_label)

        self.last_card_label = QLabel("")
        self.last_card_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.last_card_label)

        # Statistics Display
        stats_layout = QGridLayout()
        layout.addLayout(stats_layout)

        self.high_cards_label = QLabel("High Cards Left: 0")
        self.high_cards_label.setStyleSheet("font-size: 16px;")
        stats_layout.addWidget(self.high_cards_label, 0, 0)

        self.low_cards_label = QLabel("Low Cards Left: 0")
        self.low_cards_label.setStyleSheet("font-size: 16px;")
        stats_layout.addWidget(self.low_cards_label, 0, 1)

        self.remaining_cards_label = QLabel("Remaining Cards by Value")
        self.remaining_cards_label.setStyleSheet("font-size: 16px;")
        stats_layout.addWidget(self.remaining_cards_label, 1, 0, 1, 2)

        self.remaining_cards_text = QTextEdit()
        self.remaining_cards_text.setReadOnly(True)
        self.remaining_cards_text.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.remaining_cards_text)

        # Event Filters for minimum bet field focus handling
        self.centralWidget().installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:
            self.clear_focus()
        return super().eventFilter(obj, event)

    def strategy_changed(self, index):
        self.counting_strategy = self.strategy_combobox.currentText()

    def deck_changed(self, index):
        self.deck_count = int(self.deck_combobox.currentText())

    def min_bet_changed(self, text):
        try:
            self.min_bet = float(text)
        except ValueError:
            self.min_bet_entry.setText("1.0")
            self.min_bet = 1.0

    def clear_focus(self):
        self.centralWidget().setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_0:
            self.update_count('10')
        elif event.key() == Qt.Key_A:
            self.update_count('A')
        elif Qt.Key_2 <= event.key() <= Qt.Key_9:
            self.update_count(str(event.key() - Qt.Key_0))

    def update_count(self, card_value):
        try:
            # Calculate the running count based on the selected strategy
            if self.counting_strategy == "Hi-Lo":
                if card_value in ['2', '3', '4', '5', '6']:
                    self.running_count += 1
                elif card_value in ['10', 'A']:
                    self.running_count -= 1
            elif self.counting_strategy == "Zen":
                if card_value in ['2', '3', '7']:
                    self.running_count += 1
                elif card_value in ['4', '5', '6']:
                    self.running_count += 2
                elif card_value in ['10', 'A']:
                    self.running_count -= 2
                elif card_value == '9':
                    self.running_count -= 1
            elif self.counting_strategy == "Omega II":
                if card_value in ['2', '3', '7']:
                    self.running_count += 1
                elif card_value in ['4', '5', '6']:
                    self.running_count += 2
                elif card_value == 'A':
                    self.running_count -= 1
                elif card_value in ['10']:
                    self.running_count -= 2
                elif card_value in ['8']:
                    self.running_count -= 1
            elif self.counting_strategy == "Wong Halves":
                if card_value in ['2', '7']:
                    self.running_count += 0.5
                elif card_value in ['3', '4', '6']:
                    self.running_count += 1
                elif card_value == '5':
                    self.running_count += 1.5
                elif card_value in ['10', 'A']:
                    self.running_count -= 1

            self.cards_counted += 1
            self.card_history.append(card_value)
            self.card_count[card_value] += 1

            total_cards = self.deck_count * 52
            cards_left = total_cards - self.cards_counted

            if cards_left > 0:
                true_count = self.running_count / (cards_left / 52)
            else:
                true_count = self.running_count  # If no cards are left, just use running count

            self.true_count_label.setText(f"True Count: {true_count:.2f}")
            self.cards_left_label.setText(f"Cards Left: {cards_left}")
            self.update_kelly(true_count)
            self.display_last_card(card_value)
            self.update_statistics()
            self.update_strategy_indicator(true_count)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def update_kelly(self, true_count):
        if true_count > 0:
            p = 0.5 + (0.1 * true_count)
            b = 1
            kelly_fraction = (p * (b + 1) - 1) / b
            kelly_multiple = kelly_fraction * self.min_bet
            self.kelly_label.setText(f"Kelly Bet (multiple of min): {kelly_multiple:.2f}")
        else:
            self.kelly_label.setText("Kelly Bet (multiple of min): 0")

    def update_statistics(self):
        total_cards = self.deck_count * 52

        high_cards = self.card_count["10"] + self.card_count["A"]
        low_cards = sum(self.card_count[str(i)] for i in range(2, 7))

        high_cards_left = (total_cards * 4 // 13) - high_cards
        low_cards_left = (total_cards * 5 // 13) - low_cards

        self.high_cards_label.setText(f"High Cards Left: {high_cards_left}")
        self.low_cards_label.setText(f"Low Cards Left: {low_cards_left}")

        self.remaining_cards_text.clear()
        remaining_cards = {str(i): total_cards // 13 - self.card_count[str(i)] for i in range(2, 10)}
        remaining_cards.update({"10": total_cards * 4 // 13 - self.card_count["10"], 'A': total_cards // 13 - self.card_count['A']})

        for card, count in remaining_cards.items():
            self.remaining_cards_text.append(f"{card}: {count}")

    def display_last_card(self, card_value):
        self.last_card_label.setText(card_value)
        QTimer.singleShot(3000, self.clear_last_card)

    def clear_last_card(self):
        self.last_card_label.setText("")

    def update_strategy_indicator(self, true_count):
        if true_count > 0:
            self.true_count_label.setStyleSheet("color: green; font-size: 24px; font-weight: bold;")
        else:
            self.true_count_label.setStyleSheet("color: red; font-size: 24px; font-weight: bold;")

    def reset_count(self):
        reply = QMessageBox.question(self, 'Reset Count', 'Are you sure you want to reset the count?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.running_count = 0
            self.cards_counted = 0
            self.card_history = []
            self.card_count = {str(i): 0 for i in range(2, 11)}
            self.card_count.update({"10": 0, 'A': 0})
            self.true_count_label.setText("True Count: 0")
            self.cards_left_label.setText("Cards Left: 0")
            self.kelly_label.setText("Kelly Bet (multiple of min): 0")
            self.high_cards_label.setText("High Cards Left: 0")
            self.low_cards_label.setText("Low Cards Left: 0")
            self.remaining_cards_text.clear()
            self.update_strategy_indicator(0)

    def show_help(self):
        help_text = (
            "Welcome to the Blackjack Card Counter App!\n\n"
            "Features:\n"
            "- Select a card counting strategy: Hi-Lo, Zen, Omega II, Wong Halves\n"
            "- Choose the number of decks in play\n"
            "- Enter cards using either buttons or keyboard input\n"
            "- View real-time statistics including true count, cards left, and distribution of remaining cards\n"
            "- Reset the count at any time\n\n"
            "How to Use:\n"
            "1. Select a counting strategy from the dropdown menu.\n"
            "2. Choose the number of decks in play.\n"
            "3. Enter the cards dealt by clicking the card buttons or using keyboard input.\n"
            "4. The true count and other statistics will update automatically.\n"
            "5. Use the reset button to start over when a new shoe is used.\n"
            "6. For keyboard input, use the numbers for cards 2-9 and '0' for 10. Use 'A' for Ace.\n"
            "7. The last card entered will be displayed for 3 seconds.\n\n"
            "Advanced Features:\n"
            "- The app will show the remaining cards by value to help you make more informed decisions.\n"
            "- The true count is color-coded: green for positive counts and red for negative counts.\n"
            "- The Kelly Criterion is used to suggest the optimal bet fraction based on the current count.\n\n"
            "Enjoy and good luck!"
        )
        QMessageBox.information(self, "User Guide", help_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardCounterApp()
    window.show()
    sys.exit(app.exec_())
