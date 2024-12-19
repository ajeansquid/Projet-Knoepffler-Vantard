# @author tvantard & Knoepffler

from models.user import User
from models.round import Round
from outils.file_op import load_features, save_session, load_session
import json

# Cette classe nous permet un accès rapide aux classes Rounds and Users
# égalmement, elle permet une overview globale du jeu en cour

class Game :
    def __init__(self,init=1):
        self.init=init
        self.path="defaultPath"
        self.joueurs = []
        self.rounds = []
        self.features = []
        self.rule=""
        self.current_feature_index = 0
        self.current_round_index = 0
    
    # Base
    
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
    def get_rule(self):
        return self.rule
    
    # Functions
    
    def start_round(self):
        round = Round(len(self.rounds)+1,len(self.joueurs))
        self.rounds.append(round)
        round.defFeature(self.features[len(self.rounds)-1])
        
        doorv2=True
        while len(round.subRounds) < 5 and doorv2: # 5 subrounds max
            for i in range(len(self.joueurs)):
                x = input("carte du joueur : "+self.joueurs[i].name+ " ")
                if x == "café":
                    filename = f"session_{self.init}_{self.current_round_index}.json"
                    self.save_sessionP()
                    print(f"Session enregistrée et arrêtée. Fichier de session créé: {filename}")
                    break
                self.joueurs[i].jouer(x,round,self.rule)
            if round.plateau != []:
                doorv2 = False
        
        print("Round n°"+str(round.num) +" fini")
        return round.getResultat()
        
    def game_start(self):
        x=0
        for i in self.features:
            x+=1
            print("Tache n°",x,":", i)
            y= self.start_round()
            print("Niveau de difficulté : "+ str(y) +" pour la tache " + i)
        self.save_final_results()
    
    def load_featuresP(self, filename="session.json"):
        return load_features(filename)
        
    def save_sessionP(self, filename="session_{self.init}_{self.current_round_index}.json"):     
        session_data = {
            "init": self.init,
            "users": [user.__dict__ for user in self.joueurs],
            "rounds": [round.toList() for round in self.rounds],
            "rule": self.rule,
            "features": [features for features in self.features],
            "current round": self.current_round_index,
            "current feature": self.current_feature_index
        }
        save_session(filename, session_data)
    
    def load_sessionP(self, filename="session.json"):
        session_data = load_session(filename)
        if not session_data:
            print(f"Le fichier {filename} n'a pas été trouvé ou est vide.")
            return
        try:
            self.init= session_data["init"]
            self.joueurs= [User(**user) for user in session_data["users"]]
            self.rounds= [Round(**round) for round in session_data["rounds"]]
            self.features= session_data["features"]
            self.rule= session_data["rule"]
            self.current_feature_index= session_data["current_feature"]
            self.current_round_index= session_data["current_round"]
        except KeyError as e:
            print(f"Clé manquante dans le fichier de session: {e}")
    
    def save_final_results(self, filename="final_results_{self.init}.json"):
        results = {feature: round.getResultat() for feature, round in zip(self.features, self.rounds)}
        try:
            with open(filename, 'w') as file:
                json.dump(results, file)
            print(f"Les résultats finaux ont été enregistrés dans {filename}.")
        except IOError:
            print(f"Erreur lors de la sauvegarde des résultats finaux dans le fichier {filename}.")