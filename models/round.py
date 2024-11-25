class Round:
    def __init__(self,num,nb_joueur):
        self.num = num
        self.nb_subRound = 0
        self.subRounds = []
        self.plateau = [] # liste de cartes jouées
        self.nb_joueur = nb_joueur
        self.feature= ""
        
    def defFeature(self, feature):
        self.feature = feature
    
    def jouerCartes(self, id, numCarte):
        self.plateau.append([id,numCarte])
        if len(self.plateau) == self.nb_joueur:
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

    def get_score(self):
        if not self.plateau:
            return None
        return self.plateau[0][1]

