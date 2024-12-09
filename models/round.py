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
    
    def jouerCartes(self, id, numCarte,rule):
        self.plateau.append([id,numCarte])
        if len(self.plateau) == self.nb_joueur:
            self.get_res(rule)
        
    def finirRoundStrict(self):
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
    
    def finirRoundMediane(self):
        return None
    
    def finirRoundMoyenne(self):
        return None
    
    def finirRoundMajorite(self):
        return None

    def get_res(self, rule):      # faire les différentes rules
        match rule:
            case "strict":
                return self.finirRoundStrict()
            case "mediane":
                return self.finirRoundMediane()
            case "moyenne":
                return self.finirRoundMoyenne()
            case "majorite":
                return self.finirRoundMajorite()

    def __str__(self) -> str:
        output = "Round n°" + str(self.num) + " : " + self.feature + "\n"
        for i in self.subRounds:
            if isinstance(i, Round):
                output += f"SubRound n°{i.num} : {i.feature}\n"
            else:
                output += str(i)
        return output
        