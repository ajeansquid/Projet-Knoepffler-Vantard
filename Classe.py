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
        self.plateau = [] # liste de cartes jouées
        self.nb_joueur = nb_joueur
        self.prompt= ""
        
    def defPrompt(self, prompt):
        self.prompt = prompt
        
    def jouerCartes(self, id, numCarte):
        self.plateau.append([id,numCarte])
        if len(self.plateau) == self.nb_joueur:
            print("Round fini")
            self.finirRound()

    def finirRound(self):
        cache = self.plateau[0]
        door = True
        for elements in self.plateau:
            if elements[1]!= cache[1]:
                door = False
        if door == False:
            print("Nouveau rounds -> subround crée")
            self.subRounds.append(self)
            self.nb_subRound += 1
            self.plateau = []

class Game :
    def __init__(self, id, path, prompts):
        self.id = id
        self.path = path
        self.joueurs = []
        self.rounds = []
        self.prompts = prompts
        
    def add_user(self, name):
        self.joueurs.append(User(name,len(self.joueurs)))
    
    def start_round(self):
        round = Round(len(self.rounds)+1,len(self.joueurs))
        self.rounds.append(round)
        round.defPrompt(self.prompts[len(self.rounds)-1])
        
        doorv2=True
        while len(round.subRounds) < 5 and doorv2: # 5 subrounds (illimité en mode strict)
            for i in range(len(self.joueurs)):
                x = input("carte du joueur : "+self.joueurs[i].name)
                self.joueurs[i].jouer(x,round)
            if round.plateau != []:
                doorv2 = False
        
        print("Round fini")
        
        

    
        
