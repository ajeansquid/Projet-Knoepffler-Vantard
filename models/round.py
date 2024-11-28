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

    def get_score(self, rule):      # faire les différentes rules
        match rule:
            case "":
                return
            case "":
                return
            case "":
                return
            case "":
                return

    def toList(self):
        print(self)
        liste = {}
        liste["num"]= self.num
        liste["nb_subRound"]= self.nb_subRound
        liste["plateau"]= self.plateau
        liste["nb_joueur"]= self.nb_joueur
        liste["feature"]= self.feature