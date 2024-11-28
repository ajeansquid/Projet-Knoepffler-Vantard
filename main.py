from models.Planning_poker import PlanningPoker
from models import game


if __name__ == "__main__":
    planning_poker = PlanningPoker()
    planning_poker.start()
    #planning_poker.load_features('features.json')
    planning_poker.vote()
    #planning_poker.save_session('session.json')
    