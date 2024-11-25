from models.user import User
from models.round import Round
class Game :
    def __init__(self, id, path, features):
        self.id = id
        self.path = path
        self.joueurs = []
        self.rounds = []
        self.features = features
        
    def add_user(self, name):
        self.joueurs.append(User(name,len(self.joueurs)))
    
    def start_round(self):
        round = Round(len(self.rounds)+1,len(self.joueurs))
        self.rounds.append(round)
        round.defFeature(self.features[len(self.rounds)-1])
        print("question : "+round.feature)
        
        doorv2=True
        while len(round.subRounds) < 5 and doorv2: # 5 subrounds (illimité en mode strict)
            for i in range(len(self.joueurs)):
                x = input("carte du joueur : "+self.joueurs[i].name)    # pause a manage ici
                self.joueurs[i].jouer(x,round)
            if round.plateau != []:
                doorv2 = False
        
        print("Round n°"+str(round.num) +" fini")
        
    def game_start(self):
        x=0
        for i in self.features:
            x+=1
            print("question n°",x,":", i)
        