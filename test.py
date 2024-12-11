import models.game as cl

Gamming = cl.Game()
Gamming.set_rule("strict")
Gamming.add_features(["testv1?","testv2 ?"])
Gamming.add_user("test1")
Gamming.add_user("test2")
Gamming.add_user("test3")
Gamming.add_user("test4")

Gamming.game_start()
