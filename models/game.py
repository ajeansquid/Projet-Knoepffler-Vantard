# @author tvantard & Knoepffler

from models.user import User
from models.round import Round
from outils.file_op import load_features, save_session, load_session

# Cette classe nous permet un accès rapide aux classes Rounds and Users
# égalmement, elle permet une overview globale du jeu en cour

class Game :
    def __init__(self):
        self.init=1
        self.path="defaultPath"
        self.joueurs = []
        self.rounds = []
        self.features = []
        self.rule=""
        self.current_feature_index = 0
        self.current_round_index = 0
        
    def add_user(self, name):
        self.joueurs.append(User(name,len(self.joueurs)))
    def add_path(self, path):
        self.path = path
    def add_features(self, features):
        for i in features:
            self.features.append(i)
            
    def set_rule(self, rule):
        self.rule = rule
    def set_index(self, index):
        self.current_feature_index = index
    def set_round_index(self, index):
        self.current_round_index = index
    
    def incr_index(self):
        self.current_feature_index += 1
    def incr_round_index(self):
        self.current_round_index += 1
    
    def start_round(self):
        round = Round(len(self.rounds) + 1, len(self.joueurs))
        self.rounds.append(round)
        round.defFeature(self.features[len(self.rounds) - 1])

        doorv2 = True
        valid_cards = ["0", "0.5", "1", "2", "3", "5", "8", "13", "20", "40", "100", "?", "café"]
        while len(round.subRounds) < 5 and doorv2:  # 5 subrounds max
            for i in range(len(self.joueurs)):
                while True:
                    x = input("carte du joueur : " + self.joueurs[i].name + " ")
                    if x in valid_cards:
                        if x == "café":
                            self.save_sessionP()
                            print("Session enregistrée et arrêtée.")
                            return
                        if x not in ["?", "café"]:
                            x = float(x) if '.' in x else int(x)
                        break
                    else:
                        print(f"Carte invalide: {x}. Veuillez entrer une carte valide.")
                self.joueurs[i].jouer(x, round, self.rule)
            if any(card[1] != "?" for card in round.plateau):
                doorv2 = False

        print("Round n°" + str(round.num) + " fini")
        return round.getResultat()
        
    def game_start(self):
        x = 0
        for i in self.features:
            x += 1
            print("Tache n°", x, ":", i)
            y = self.start_round()
            print("Niveau de difficulté : " + str(y) + " pour la tache " + i)
    
    def load_featuresP(self, filename="session.json"):
        return load_features(filename)
        
    def save_sessionP(self, filename="session.json"):     
        session_data = {
            "users": [user.__dict__ for user in self.get_users()],
            "rounds": [round.toList() for round in self.get_rounds()],
            "rule": self.rule,
            "features": [features for features in self.get_features()],
            "current round": self.current_round_index,
            "current feature": self.current_feature_index
        }
        save_session(filename, session_data)
    
    def load_sessionP(self, filename="session.json"):
        session_data = load_session(filename)
        self.users = [User(**user) for user in session_data["users"]]
        self.rounds = [Round(**round) for round in session_data["rounds"]]
        self.features = self.load_featuresP(filename)
        self.current_feature_index = session_data["current_feature_index"]
        self.current_round_index = session_data["current_round_index"]