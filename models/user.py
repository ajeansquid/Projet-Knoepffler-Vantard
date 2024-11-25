
class User : 
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def jouer (self,num_carte,actual_round):
        actual_round.jouerCartes(self.id,num_carte)

