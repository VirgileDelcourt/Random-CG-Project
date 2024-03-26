from Scripts.cards import Card
from Scripts.allCards import cards
from Scripts.players import Player
from Scripts.upgrades import LevelUp
from Scripts.input import Input

from time import sleep
from random import choice

# 'importing' cards for easier access
strike = cards["Strike"]
heavy = cards["Heavy"]
bleed = cards["Bleed"]
recover = cards["Recover"]
drawback = cards["Drawback"]
care = cards["Care"]
rune = cards["Rune"]

# creating the characters
starter_deck = [strike(), strike(), strike(), heavy(), recover(), recover(), recover(), recover(), rune()]
pap = Player("Pap", starter_deck + [strike(), drawback()])
fet = Player("Fet", starter_deck + [bleed(), bleed()])
pip = Player("Pip", starter_deck + [care(), care()])

# player selection 'screen'
participants = [pap, fet, pip]
hro = participants[Input("Who do you want to play as ?", participants)]
participants.remove(hro)
opponents = participants
print()

# main loop
while hro.hp > 0:
    opp = choice(opponents)  # choosing a random opponent
    print("Your opponent is " + str(opp) + " !")
    sleep(2)
    print("Game Start !", end="\n\n")
    sleep(2)
    hro.Init_Game(opp)
    opp.Init_Game(hro)

    # combat loop
    while hro.hp > 0 and opp.hp > 0:
        if hro.hp > 0:
            hro.Turn()
            sleep(2)
            print()
        if opp.hp > 0:
            opp.Auto_Turn()
            sleep(2)
            print()

    # handling winning and losing
    if hro.hp > 0:
        sleep(2)
        print(hro.name + " won.")
        LevelUp(hro)
    else:
        sleep(2)
        print(opp.name + " won.")
    print(end="\n\n")
