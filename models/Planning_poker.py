from models.user import User
from models.round import Round
from utils.file_op import load_features, save_session, load_session
# from models.game import Game

class PlanningPoker:
    def __init__(self):
        self.users = []
        self.rounds = []
        self.features = []
        self.current_feature_index = 0
        self.current_round_index = 0
        
    def load_features(self, filename):
        self.features = load_features(filename)
        
    def save_session(self, filename):
        session_data = {
            "users": [user.__dict__ for user in self.users],
            "rounds": [round.__dict__ for round in self.rounds],
            "current_feature_index": self.current_feature_index,
            "current_round_index": self.current_round_index
        }
        save_session(filename, session_data)
    
    def load_session(self, filename):
        session_data = load_session(filename)
        self.users = [User(**user) for user in session_data["users"]]
        self.rounds = [Round(**round) for round in session_data["rounds"]]
        self.current_feature_index = session_data["current_feature_index"]
        self.current_round_index = session_data["current_round_index"]
    
    def add_user(self, name):
        user_id = len(self.users) + 1
        self.users.append(User(name, user_id))
    
    def start(self):
        num_users = int(input("Combien de joueurs ? "))
        for _ in range(num_users):
            name = input("Nom du joueur : ")
            self.add_user(name)
        print("Les joueurs sont : ", [user.name for user in self.users])
        self.rule = input("Choisissez la règle (stricte, moyenne, etc.) : ")
        
    def vote(self):
        while self.current_feature_index < len(self.features):
            feature = self.features[self.current_feature_index]
            print("Fonctionnalité : ", feature['name'])
            round = Round(self.current_round_index + 1, len(self.users))
            self.rounds.append(round)
            self.current_round_index += 1
            round.defFeature(feature)
            for user in self.users:
                card = input(f"Carte du joueur {user.name} : ")
                user.jouer(card, round)
            round.finirRound()
            score = round.get_score()
            if score is not None:
                feature['score'] = score
            self.current_feature_index += 1
        self.save_session('session.json')
