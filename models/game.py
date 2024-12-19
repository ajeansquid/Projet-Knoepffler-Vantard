# @author tvantard & Knoepffler

from models.user import User
from models.round import Round
from outils.file_op import load_features, save_session, load_session
import json

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
    
    def get_users(self):
        return self.joueurs
    
    def get_rounds(self):
        return self.rounds
    
    def get_features(self):
        return self.features
    
    def start_round(self):
        round = Round(len(self.rounds) + 1, len(self.joueurs))
        self.rounds.append(round)
        if len(self.features) > len(self.rounds) - 1:
            round.defFeature(self.features[len(self.rounds) - 1])
        else:
            print("Toutes les fonctionnalités ont été votées.")
            return "fin"

        doorv2 = True
        valid_cards = ["0", "0.5", "1", "2", "3", "5", "8", "13", "20", "40", "100", "?", "café"]
        while len(round.subRounds) < 5 and doorv2:  # 5 subrounds max
            for i in range(len(self.joueurs)):
                while True:
                    x = input("carte du joueur : " + self.joueurs[i].name + " ")
                    if x in valid_cards:
                        if x not in ["?", "café"]:
                            x = float(x) if '.' in x else int(x)
                        break
                    else:
                        print(f"Carte invalide: {x}. Veuillez entrer une carte valide.")
                result = self.joueurs[i].jouer(x, round, self.rule)
                if result == "café":
                    filename = f"session_{self.current_round_index}.json"
                    self.save_sessionP(filename)
                    print(f"Session enregistrée et arrêtée. Fichier de session créé: {filename}")
                    return "café"
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
            if y == "café":
                filename = f"session_{self.current_round_index}.json"
                print(f"Session enregistrée et arrêtée. Fichier de session créé: {filename}")
                return
            if y == "fin":
                break
            print("Niveau de difficulté : " + str(y) + " pour la tache " + i)
        self.save_final_results()
    
    def load_featuresP(self, filename="session.json"):
        return load_features(filename)
        
    def save_sessionP(self, filename=None):     
        if filename is None:
            filename = f"session_{self.current_round_index}.json"
        session_data = {
            "users": [user.__dict__ for user in self.get_users()],
            "rounds": [round.toList() for round in self.get_rounds()],
            "rule": self.rule,
            "features": [features for features in self.get_features()],
            "current_round": self.current_round_index,
            "current_feature": self.current_feature_index
        }
        save_session(filename, session_data)
    
    def load_sessionP(self, filename="session.json"):
        session_data = load_session(filename)
        if not session_data:
            print(f"Le fichier {filename} n'a pas été trouvé ou est vide.")
            return
        try:
            self.joueurs = [User(**user) for user in session_data["users"]]
            self.rounds = [Round(**round) for round in session_data["rounds"]]
            self.features = session_data["features"]
            self.rule = session_data["rule"]
            self.current_feature_index = session_data["current_feature"]
            self.current_round_index = session_data["current_round"]
        except KeyError as e:
            print(f"Clé manquante dans le fichier de session: {e}")

    def save_final_results(self, filename="final_results.json"):
        results = {feature: round.getResultat() for feature, round in zip(self.features, self.rounds)}
        try:
            with open(filename, 'w') as file:
                json.dump(results, file)
            print(f"Les résultats finaux ont été enregistrés dans {filename}.")
        except IOError:
            print(f"Erreur lors de la sauvegarde des résultats finaux dans le fichier {filename}.")
    
    def menu(self):
        while True:
            print("\nMenu Principal")
            print("1. Démarrer la partie")
            print("2. Charger une partie")
            print("3. Quitter")
            choice = input("Choisissez une option: ")

            if choice == "1":
                self.setup_game()
                self.game_start()
            elif choice == "2":
                self.charger_partie()
            elif choice == "3":
                print("Au revoir!")
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    def setup_game(self):
        self.decider_nombre_joueurs()
        self.entrer_pseudo_joueurs()
        self.choisir_regle()
        self.entrer_liste_fonctionnalites()

    def decider_nombre_joueurs(self):
        while True:
            try:
                nombre_joueurs = int(input("Entrez le nombre de joueurs: "))
                if nombre_joueurs > 0:
                    self.joueurs = [None] * nombre_joueurs
                    break
                else:
                    print("Le nombre de joueurs doit être supérieur à 0.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")

    def entrer_pseudo_joueurs(self):
        for i in range(len(self.joueurs)):
            pseudo = input(f"Entrez le pseudo pour le joueur {i + 1}: ")
            self.joueurs[i] = User(pseudo, i)

    def choisir_regle(self):
        regles = ["strict", "mediane", "moyenne", "majorite"]
        print("Règles disponibles:")
        for i, regle in enumerate(regles, 1):
            print(f"{i}. {regle}")
        while True:
            choix = input("Choisissez une règle: ")
            if choix in map(str, range(1, len(regles) + 1)):
                self.rule = regles[int(choix) - 1]
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    def entrer_liste_fonctionnalites(self):
        choix = input("Voulez-vous charger une liste de fonctionnalités depuis un fichier JSON? (oui/non): ")
        if choix.lower() == "oui":
            fichier = input("Entrez le nom du fichier JSON: ")
            self.features = self.load_featuresP(fichier)
        else:
            self.features = []
            while True:
                fonctionnalite = input("Entrez une fonctionnalité (ou 'fin' pour terminer): ")
                if fonctionnalite.lower() == "fin":
                    break
                self.features.append(fonctionnalite)

    def charger_partie(self):
        fichier = input("Entrez le nom du fichier de session: ")
        self.load_sessionP(fichier)
        self.game_start()