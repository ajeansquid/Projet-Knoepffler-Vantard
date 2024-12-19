# @author tvantard & Knoepffler

class User : 
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def jouer(self, num_carte, actual_round, rule):
        valid_cards = ["0", "0.5", "1", "2", "3", "5", "8", "13", "20", "40", "100", "?", "café"]
        if str(num_carte) in valid_cards:
            actual_round.jouerCartes(self.id, num_carte, rule)
        else:
            print(f"Carte invalide: {num_carte}")

