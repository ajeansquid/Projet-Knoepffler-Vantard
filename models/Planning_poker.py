# @author tvantard & Knoepffler

from models.user import User
from models.round import Round
from models.game import Game

# Classe qui vas faire écran entre les classes et l'interface visuelle

class PlanningPoker:
    def __init__(self):
        self.id= 1
        self.game= Game()
