from Scripts.allCards import cards
from Scripts.input import Input
from random import choice, shuffle


# to make the upgrades more readable
class Upgrade:
    def __init__(self, name, effects, continuous=None):
        if continuous is None:
            continuous = []
        self.name = name
        self.effects = effects  # the effects to add to the card, when upgrading
        self.continuous = continuous  # same but for continuous effects

    def Apply(self, card):
        """Takes in a Card card and adds all functions from self.effects to card.effects
        does the same for continuous effects"""
        card.__effects__.extend(self.effects)
        card.__continuous__.extend(self.continuous)


# contains all the upgrades, ready to be chosen ;)
# Upgrade("name", [lambda card, user, target: user]),
upgrades = [Upgrade("strike 2", [lambda card, user, target: user.Attack(target, 2), ]),
            Upgrade("draw 1", [lambda card, user, target: user.Draw(1), ]),
            Upgrade("setup", [lambda card, user, target: user.Move_Card(card, "self.hand", "self.field")]),
            Upgrade("trap", [lambda card, user, target: user.Move_Card(card, "self.hand", "target.field")]),
            Upgrade("infect", [lambda card, user, target: user.Move_Card(card, "self.hand", "target.deck")]),
            Upgrade("bleed 1", [], [lambda card, user, target: user.Damage(1)]),
            Upgrade("trash", [lambda card, user, target: user.Move_Card(target.field[Input("Which card from your opponent's field do you want to trash ?", target.field)], "opp.field", "opp.discard")]),
            Upgrade("junker", [], [lambda card, user, target: target.Move_Card(choice(target.hand), "self.hand", "self.discard")]),
            Upgrade("heal 2", [lambda card, user, target: user.Heal(2)]),
            Upgrade("autonomous 1", [], [lambda card, user, target: target.Damage(1)])]


def LevelUp(char):
    """Takes in a Player 'char' and will ask the player to choose what to upgrade
    The 3 choices are: upgrade a card, from 3 combinations of cards and upgrades randomly chosen
    choose a new card, take 1 from 3 random, un-upgraded cards
    +10 maxhp, self-explanatory"""
    global upgrades

    print(char.name + " levels up !")
    while True is True:
        print()
        ans = Input("What do you want to do ?", ["Upgrade a card.", "Get a new card.", "get +10 max hp."])
        if ans == 0:
            options = char.metadeck[:]
            shuffle(options)
            if len(options) > 3:
                options = options[:3]
            for i in range(len(options)):
                upgrade = choice(upgrades)
                options[i] = (options[i], upgrade, (str(options[i]) + " + " + upgrade.name))
            print()
            ans = Input("Choose a card + augment combination to add to a card :", [thing[2] for thing in options])
            options[ans][1].Apply(options[ans][0])
            print("Effect added to " + str(options[ans][0]) + " !")
            return
        elif ans == 1:
            possible_cards = [cards[i]() for i in cards]
            options = [choice(possible_cards) for _ in range(3)]
            ans = Input("Choose a card to add to your deck", options)
            char.metadeck.append(options[ans])
            return
        elif ans == 2:
            char.maxhp += 10
            print(char.name + " hp were increased to " + str(char.maxhp))
            return
