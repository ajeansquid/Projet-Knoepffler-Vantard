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
                return "café" # -> save and stop game
            if all(card[1] == "?" for card in self.plateau):
                return "Les conditions des règles ne sont pas remplies, nouveau vote !"
            if rule == "strict" and any(card[1] == "?" for card in self.plateau):
                return "Les conditions des règles ne sont pas remplies, nouveau vote !"
            else:
                result = self.ruleSplitter(rule)
                if result != True:
                    return "Les conditions des règles ne sont pas remplies, nouveau vote !"
        return False

    def getResultat(self):
        return self.resultat
        
    def finirRoundStrict(self):
        if not self.plateau:
            return "Le plateau est vide. Impossible de terminer le round."

        cache = self.plateau[0]
        door = True
        for elements in self.plateau:
            if elements[1] == "?":
                return "Les conditions des règles ne sont pas remplies, nouveau vote !"
            if elements[1] != cache[1]:
                door = False
        if not door:
            return "Les conditions des règles ne sont pas remplies, nouveau vote !"
        else:
            self.resultat = cache[1]
            return True
    
    def finirRoundMediane(self):
        if not self.plateau:
            return "Le plateau est vide. Impossible de terminer le round."

        res = [int(i[1]) for i in self.plateau if i[1] not in ["?", "café"]]
        if not res:
            return "Les conditions des règles ne sont pas remplies, nouveau vote !"
        self.resultat = median(res)
        return True
    
    def finirRoundMoyenne(self):
        if not self.plateau:
            return "Le plateau est vide. Impossible de terminer le round."

        res = [int(i[1]) for i in self.plateau if i[1] not in ["?", "café"]]
        if not res:
            return "Les conditions des règles ne sont pas remplies, nouveau vote !"
        self.resultat = mean(res)
        return True
    
    def finirRoundMajorite(self):
        if not self.plateau:
            return "Le plateau est vide. Impossible de terminer le round."

        res = [int(i[1]) for i in self.plateau if i[1] not in ["?", "café"]]
        if not res:
            return "Les conditions des règles ne sont pas remplies, nouveau vote !"
        
        count = Counter(res)
        resBuff, nbsBuff = count.most_common(1)[0]
        
        if nbsBuff < (len(res) / 2):
            return "Les conditions des règles ne sont pas remplies, nouveau vote !"
        else:
            self.resultat = resBuff
            return True

    def ruleSplitter(self, rule):
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
