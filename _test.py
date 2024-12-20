import unittest
from models.user import User
from models.round import Round
from models.game import Game

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User("test_user", 1)
        self.assertEqual(user.get_name(), "test_user")
        self.assertEqual(user.id, 1)

    def test_user_valid_cards(self):
        user = User("test_user", 1)
        self.assertIn("0", user.valid_cards)
        self.assertIn("café", user.valid_cards)
        self.assertIn("?", user.valid_cards)

class TestRound(unittest.TestCase):
    def test_round_creation(self):
        round = Round(1, 4)
        self.assertEqual(round.num, 1)
        self.assertEqual(round.nb_joueur, 4)
        self.assertEqual(round.feature, "")
        self.assertEqual(round.resultat, 0)

    def test_jouer_cartes(self):
        round = Round(1, 4)
        round.jouerCartes(0, "1", "strict")
        round.jouerCartes(1, "1", "strict")
        round.jouerCartes(2, "1", "strict")
        result = round.jouerCartes(3, "1", "strict")
        self.assertTrue(result)

    def test_finir_round_strict(self):
        round = Round(1, 4)
        round.jouerCartes(0, "1", "strict")
        round.jouerCartes(1, "1", "strict")
        round.jouerCartes(2, "1", "strict")
        round.jouerCartes(3, "1", "strict")
        result = round.finirRoundStrict()
        self.assertTrue(result)

class TestGame(unittest.TestCase):
    def test_game_creation(self):
        game = Game()
        self.assertEqual(game.init, 1)
        self.assertEqual(game.path, "defaultPath")
        self.assertEqual(game.joueurs, [])
        self.assertEqual(game.rounds, [])
        self.assertEqual(game.features, [])
        self.assertEqual(game.rule, "")

    def test_add_user(self):
        game = Game()
        game.add_user("test_user")
        self.assertEqual(len(game.joueurs), 1)
        self.assertEqual(game.joueurs[0].get_name(), "test_user")

    def test_add_features(self):
        game = Game()
        game.add_features(["feature1", "feature2"])
        self.assertEqual(len(game.features), 2)
        self.assertIn("feature1", game.features)
        self.assertIn("feature2", game.features)

    def test_set_rule(self):
        game = Game()
        game.set_rule("strict")
        self.assertEqual(game.get_rule(), "strict")

if __name__ == '__main__':
    unittest.main()