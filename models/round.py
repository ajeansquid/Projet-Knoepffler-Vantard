# @author tvantard & Knoepffler

import math 
from statistics import median, mean
from collections import Counter

# Rounds nous permet de gérer plus précisément les rounds 

class Round:
    def __init__(self,num,nb_joueur):
        self.num = num
        self.nb_subRound = 0
        self.subRounds = []
        self.plateau = [] # liste de cartes jouées
        self.nb_joueur = nb_joueur
        self.feature= ""
        self.resultat= 0
            
    def defFeature(self, feature):
        self.feature = feature
    
    def jouerCartes(self, id, numCarte, rule):
        self.plateau.append([id, numCarte])
        if len(self.plateau) == self.nb_joueur:
            if any(card[1] == "?" for card in self.plateau):
                print("Nouveau subround -> un joueur a joué '?'")
                self.subRounds.append(Round(self.num, self.nb_joueur))
                self.nb_subRound += 1
                self.plateau = []
            else:
                self.ruleSplitter(rule)
    
    def getResultat(self):
        valid_cards = [x[1] for x in self.plateau if x[1] != "?"]
        if not valid_cards:
            return 0
        self.resultat = valid_cards[0]
        return self.resultat

    def finirRoundStrict(self):
        valid_cards = [card[1] for card in self.plateau if card[1] != "?"]
        if not valid_cards:
            self.resultat = 0
            return
        cache = valid_cards[0]
        door = True
        for elements in valid_cards:
            if elements != cache:
                door = False
        if door == False:
            print("Nouveau subround -> les cartes ne sont pas identiques")
            self.subRounds.append(Round(self.num, self.nb_joueur))
            self.nb_subRound += 1
            self.plateau = []
        else:
            self.resultat = cache

    
    def finirRoundMediane(self):
        valid_cards = [x[1] for x in self.plateau if x[1] != "?"]
        if not valid_cards:
            self.resultat = 0
            return
        self.resultat = median(valid_cards)
    
    def finirRoundMoyenne(self):
        valid_cards = [x[1] for x in self.plateau if x[1] != "?"]
        if not valid_cards:
            self.resultat = 0
            return
        self.resultat = mean(valid_cards)
    
    def finirRoundMajorite(self):
        valid_cards = [x[1] for x in self.plateau if x[1] != "?"]
        if not valid_cards:
            self.resultat = 0
            return
        resBuff, nbsBuff = Counter(valid_cards).most_common(1)[0]
        self.resultat = resBuff
        if nbsBuff > math.ceil(len(valid_cards) / 2):
            print("Nouveau subround -> pas de majorité")
            self.subRounds.append(Round(self.num, self.nb_joueur))
            self.nb_subRound += 1
            self.plateau = []
        else:
            self.resultat = resBuff

    def ruleSplitter(self, rule):      # faire les différentes rules
        if self.nb_subRound==0:
            return self.finirRoundStrict()
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
