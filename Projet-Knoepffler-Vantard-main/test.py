import models.game as cl

Gamming = cl.Game()

Gamming.set_rule("moyenne")
Gamming.add_features(["test v1?"])
Gamming.add_user("test1")
Gamming.add_user("test2")
Gamming.add_user("test3")

Gamming.game_start()


Gamming2 = cl.Game()
Gamming2.set_rule("mediane")
Gamming2.add_features(["test v2?"])
Gamming2.add_user("test12")
Gamming2.add_user("test22")
Gamming2.add_user("test32")

Gamming2.game_start()


Gamming3 = cl.Game()
Gamming3.set_rule("majorite")
Gamming3.add_features(["test v3?"])
Gamming3.add_user("test13")
Gamming3.add_user("test23")
Gamming3.add_user("test33")

Gamming3.game_start()
