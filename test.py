import models.game as cl

Gamming = cl.Game()
Gamming.add_features(["testv1?","testv2 ?"])
Gamming.add_user("test1")
Gamming.add_user("test2")
Gamming.add_user("test3")
Gamming.add_user("test4")

Gamming.start_round()
Gamming.start_round()

for i in Gamming.rounds:
    print(i)
    print("score : ",i.get_score(""))