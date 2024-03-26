from Scripts.cards import Card
from Scripts.input import Input


class Strike(Card):
    def __init__(self):
        super().__init__("Strike!", 1, [lambda card, user, target: user.Attack(target, 3)],
                         "Deal 3 damage to opp.")

# This card made a bug where its growth wouldn't be reset between battles, and I can't figure why
# It's because the card played was adding the function to the meta card (in the meta deck)
# but I even added a card parameter instead of just putting self, and it didn't change a thing
"""
class Scale(Card):
    def __init__(self):
        super().__init__("Scale", 1, [lambda card, user, target: user.Attack(target, 1),
                                      lambda card, user, target: card.Add(lambda _card, _user, _target: _user.Attack(_target, 1))],
                         "Deal 1 damage to opp. Increase Strike number by 1 when played.")
"""


class Bleed(Card):
    def __init__(self):
        super().__init__("Bleed", 1, [lambda card, user, target: user.Attack(target, 1),
                                      lambda card, user, target: user.Move_Card(card, "self.hand", "opp.field")],
                         "Deal 1 damage to opp, then 1 again everytime their turn start.",
                         continuous=[lambda card, user, target: user.Damage(1)])


class Summon(Card):
    def __init__(self):
        super().__init__("Summon", 1, [lambda card, user, target: user.Move_Card(card, "self.hand", "self.field")],
                         "Summons a minion that deals 2 damage to opp each turn.",
                         continuous=[lambda card, user, target: target.Damage(2)])


class Rune(Card):
    def __init__(self):
        super().__init__("Rune", 2, [lambda card, user, target: user.Move_Card(card, "self.hand", "self.field")],
                         "Get a Rune that allows you to draw one more at turn start.",
                         continuous=[lambda card, user, target: user.Draw(1)])


class Recover(Card):
    def __init__(self):
        super().__init__("Recover", 1, [lambda card, user, target: user.Heal(2)],
                         "Recover 2 hp.")


class Prepare(Card):
    def __init__(self):
        super().__init__("Prepare", 0, [lambda card, user, target: user.Draw(1)],
                         "Draw a card.")


class Drawback(Card):
    def __init__(self):
        super().__init__("Drawback", 1, [lambda card, user, target: user.Attack(target, 5),
                                         lambda card, user, target: user.Move_Card(card, "self.hand", "self.field")],
                         "Deals 5 damage to opponent, but then deals 1 damage to you every other turn at round start.",
                         continuous=[lambda card, user, target: user.Damage(1)])


class Benefit(Card):
    def __init__(self):
        super().__init__("Benefit", 0, [lambda card, user, target: user.Move_Card(user.field[Input("Which card do you want to give to your opponent ?", user.field)], "self.field", "opp.field"),
                                        lambda card, user, target: user.Draw(1)],
                         "Give 1 of your active cards to your opponent to draw 1.")


class Steal(Card):
    def __init__(self):
        super().__init__("Steal", 1, [lambda card, user, target: user.Move_Card(target.field[Input("Which card do you want to steal from your opponent ?", target.field)], "opp.field", "self.field")],
                         "Steal one of your opponent's active card.")


class Care(Card):
    def __init__(self):
        super().__init__("Care", 1, [lambda card, user, target: user.Move_Card(card, "self.hand", "self.field")],
                         "Will heal you for 1 at the start of each of your turns.",
                         continuous=[lambda card, user, target: user.Heal(1)])
        
class Heavy(Card):
    def __init__(self):
        super().__init__("Heavy Slash!", 2, [lambda card, user, target: user.Attack(target, 5)],
                         "Deal 5 damage to opp.")


# all cards are packed in here, ready to be exported :)
cards = {"Strike": Strike, "Bleed": Bleed, "Summon": Summon, "Rune": Rune, "Recover": Recover, "Prepare": Prepare,
         "Drawback": Drawback, "Benefit": Benefit, "Steal": Steal, "Care": Care, "Heavy": Heavy}
