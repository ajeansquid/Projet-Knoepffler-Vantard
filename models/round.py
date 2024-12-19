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
            if all(card[1] == "café" for card in self.plateau):
                print("Tous les joueurs ont joué 'café'. Fin de la partie.")
                return "café" # -> save 
            if any(card[1] == "?" for card in self.plateau):
                print("Nouveau subround -> un joueur a joué '?'")
                self.subRounds.append(Round(self.num, self.nb_joueur))
                self.nb_subRound += 1
                self.plateau = []
            else:
                self.ruleSplitter(rule)
    
    def getResultat(self):
        return self.resultat
        
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
        else :
            self.resultat= cache[1]
    
    def finirRoundMediane(self):
        res=[]
        for i in self.plateau:
            res.append(int(i[1]))
        self.resultat= median(res)
    
    def finirRoundMoyenne(self):
        res=[]
        for i in self.plateau:
            res.append(int(i[1]))
        self.resultat= mean(res)
    
    def finirRoundMajorite(self):
        res=[]
        for i in self.plateau:
            res.append(int(i[1]))
        
        count= Counter(res)
        resBuff, nbsBuff= count.most_common(1)[0]
        
        if nbsBuff< (len(self.plateau)/2):
            print("Nouveau rounds -> subround crée")
            self.subRounds.append(self)
            self.nb_subRound += 1
            self.plateau = []
        else :
            self.resultat= resBuff

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

    def toList(self):
        return {
            "num": self.num,
            "nb_subRound": self.nb_subRound,
            "subRounds": [subRound.toList() for subRound in self.subRounds],
            "plateau": self.plateau,
            "nb_joueur": self.nb_joueur,
            "feature": self.feature,
            "resultat": self.resultat
        }
    
    def __str__(self) -> str:
        output = "Round n°" + str(self.num) + " : " + self.feature + "\n"
        for i in self.subRounds:
            if isinstance(i, Round):
                output += f"SubRound n°{i.num} : {i.feature}\n"
            else:
                output += str(i)
        return output
        