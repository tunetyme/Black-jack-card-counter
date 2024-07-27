class CardCounter:
    def __init__(self, strategy, decks):
        self.strategy = strategy
        self.decks = decks

    def update_running_count(self, card_value, running_count, undo=False):
        values = {
            "Hi-Lo": {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1},
            "Zen": {'2': 1, '3': 1, '4': 2, '5': 2, '6': 2, '7': 1, '8': 0, '9': 0, '10': -2, 'J': -2, 'Q': -2, 'K': -2, 'A': 0},
            "Omega II": {'2': 1, '3': 1, '4': 2, '5': 2, '6': 2, '7': 1, '8': 0, '9': -1, '10': -2, 'J': -2, 'Q': -2, 'K': -2, 'A': 0},
            "Wong Halves": {'2': 0.5, '3': 1, '4': 1, '5': 1.5, '6': 1, '7': 0.5, '8': 0, '9': -0.5, '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}
        }
        multiplier = -1 if undo else 1
        return running_count + values[self.strategy][card_value] * multiplier

    def calculate_true_count(self, running_count):
        return running_count / self.decks
