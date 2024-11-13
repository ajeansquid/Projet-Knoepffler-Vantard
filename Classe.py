class User :
    def __init__(self, name, id):
        self.name = name
        self.id = id
    def jouer (self,num_carte,actual_round):
        actual_round.jouerCartes(self.id,num_carte)


class Round :
    def __init__(self,num,nb_joueur):
        self.num = num
        self.nb_subRound = 0
        self.subRounds = []
        plateau = [] # liste de cartes jouées
        self.nb_joueur = nb_joueur
        self.prompt =""
        
    def prompt(self, prompt):
        self.prompt = prompt
        
    def jouerCartes(self, id, numCarte):
        self.plateau.append([id,numCarte])
        if len(self.plateau) == self.nb_joueur:
            self.finirRound()
            
    def finirRound(self):
        cache = self.plateau[0[1]]
        door = True
        for elements in self.plateau:
            if elements[1]!= cache:
                door = False
        if door == False:
            self.nb_subRound += 1
            self.subRounds.append(self)
            self.plateau = []
        
            
        
    

class Game :
    def __init__(self, id, path):
        self.id = id
        self.path = path
        self.joueurs = []
        self.rounds = []
        self.prompt = []
    

    
        
