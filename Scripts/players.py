from Scripts.cards import Card
from Scripts.input import Input
from random import shuffle, choice
from time import sleep


class Player:
    def __init__(self, name, deck, hp=20):
        assert type(name) == str, "Player's name must be str"
        assert type(hp) == int, "Player's hp must be int"
        assert type(deck) == list, "Player's deck must be a list"
        assert len([True for _ in deck if not issubclass(type(_), Card)]) == 0, "Player's deck must be a list of Cards"

        self.name = name
        self.metadeck = deck  # contains the base cards, which are copied at the start of battle into the actual deck
        self.maxhp = hp
        self.hp = self.maxhp

        self.deck = []
        self.hand = []
        self.discard = []
        self.field = []  # cards on the field will activate their continuous effect at the start of each turn

        self.mana = 0  # used to play cards, set to maxmana at the start of each turn
        self.maxmana = 0  # increased by 1 at the start of each turn, resets to 0 at the end of the fight

        self.opponent = None  # you can only fight on opponent at once, that's where they're stored

    def Damage(self, dmg, mes=None):
        """Takes in an int (dmg) and lowers the player's hp by that amount.
        You can also give it a message to print after the attack"""
        print(self.name + " took " + str(dmg) + " damage.", end="")
        if mes != None:
            print(mes)
        else:
            print()
        self.hp -= dmg
        print(self.name + " now has " + str(self.hp) + " hp.")

    def Attack(self, target, dmg):
        """Takes in a Player (target) and an int (dmg) and calls target.Damage(dmg)"""
        print(self.name + " attacked " + target.name + ".")
        target.Damage(dmg)

    def Heal(self, pwr):
        """takes in an int (pwr) and increases Player's hp by that amount."""
        print(self.name + " recovered " + str(pwr) + " hp.")
        self.hp += pwr

    def Init_Game(self, opp):
        """Takes in a Player (opp) to be the next opponent.
        Then, sets the game up (shuffle deck, draw starting hand, reset mana and hp)"""
        self.opponent = opp

        self.hand = []
        self.discard = []
        self.field = []
        self.deck = [card.Create_Copy() for card in self.metadeck]
        shuffle(self.deck)

        self.hp = self.maxhp
        self.maxmana, self.mana = 0, 0

        if self.opponent.opponent is None:  # since the player is always initiated before the enemy,
            self.Draw(5, True)              # we can know if we should show the cards drawn
        else:
            self.Draw(5, False)             #or not

        print()

    def Draw(self, n=1, show=True):
        """Can take in an int (n) that is the number of cards to be drawn (1 otherwise)
        Will add the top n cards of the draw pile to the Player's hand.
        Will automatically stop if there are no cards left to draw"""
        for _ in range(n):
            if len(self.deck) <= 0:
                print(self.name + " has no cards left to draw.")
                sleep(1)
                return
            card = self.deck.pop(0)
            self.hand.append(card)
            if show:
                print(self.name + " drew " + str(card) + ".")
            else:
                print(self.name + " drew a card.")
            sleep(1)

    def Prep_Turn(self, main_char=True):
        """Handles all the start of turn routine / logic
        Like mana gain, draw, activating continuous effects, etc."""
        print("It is " + self.name + "'s turn.")
        print("They have " + str(self.hp) + " hp left.")
        sleep(2)
        self.maxmana += 1
        self.mana = self.maxmana
        if len(self.deck) <= 0:
            self.Shuffle_Deck()
        if len(self.field) > 0:
            print(self.name + " continuous effect(s) activate.")
            sleep(2)
            for card in self.field:
                card.Start_Turn(self, self.opponent)
                sleep(2)
        if len(self.hand) <= 0:
            self.Draw(1, main_char)
        self.Draw(1, main_char)
        sleep(2)

    def Turn(self):
        """When called, makes the player take a turn (by player I do mean main character)
        basically only asks them what they want to play and play the cards wanted"""
        self.Prep_Turn()
        while self.mana > 0:
            print()
            print("You have " + str(self.mana) + " / " + str(self.maxmana) + " mana.")
            if len(self.hand) > 0:
                choice = Input("Choose what to do :", self.hand + ["End your turn"],
                               "(type in 1, 2, ... to chose an option)")
                print()
                if choice < len(self.hand):
                    card = self.hand[choice]
                    print(self.name + " used " + str(card) + ".")
                    card.Use(self, self.opponent)
                    sleep(2)
                    self.mana -= card.cost
                    if card in self.hand:
                        self.Move_Card(card, "self.hand", "self.discard")
                else:
                    self.mana = 0
            else:
                print("You have no cards left in your hand, your turn ends.")
                self.mana = 0
            if self.opponent.hp <= 0:
                self.mana = 0
        print(self.name + " ends their turn.")

    def Auto_Turn(self):
        self.Prep_Turn(False)
        while self.mana > 0 and len(self.hand) > 0:
            options = [card for card in self.hand if card.cost <= self.mana]
            to_play = choice(options)
            print(self.name + " used " + str(to_play) + ".")
            sleep(1)
            to_play.Use(self, self.opponent)
            self.mana -= to_play.cost
            self.Move_Card(to_play, "self.hand", "self.discard")
            sleep(3)
            print()
        print(self.name + " end their turn.")

    def Shuffle_Deck(self):
        """Shuffle Player's discard pile into their deck."""
        self.deck.extend(self.discard)
        self.discard = []
        print(self.name + " shuffles their discard into their deck.")

    def Move_Card(self, card, start, end):
        """Moves 'card' give (if it is in 'start') into 'end', removing it from 'start'
        start and end must be like: self.hand (= this player's hand), or opp.deck (= this player's opponent's deck), etc.
        Will not return an error when the card isn't found, but it will simply print an error message"""
        try:
            owner, place = start.split(".")
            target, destination = end.split(".")
        except:
            raise

        if owner == "self":
            owner = self
        else:
            owner = self.opponent
        if target == "self":
            target = self
        else:
            target = self.opponent

        try:
            if place == "hand":
                owner.hand.remove(card)
            elif place == "field":
                owner.field.remove(card)
            elif place == "discard":
                owner.discard.remove(card)
            elif place == "hand":
                owner.hand.remove(card)
            else:
                raise RuntimeError("place wasn't correct (got " + place + ")")

            if destination == "hand":
                target.hand.append(card)
            elif destination == "field":
                target.field.append(card)
            elif destination == "discard":
                target.discard.append(card)
            elif destination == "hand":
                target.hand.append(card)
            else:
                raise RuntimeError("destination wasn't correct (got " + destination + ")")

            print(self.name + " moved " + str(card) + " from " + owner.name + "'s " + place + " to " + target.name + "'s " + destination + ".")
        except:
            print(self.name + " tried to moved " + str(card) + " to " + target.name + "'s " + destination + " but didn't succeed.")

    def __repr__(self):
        return self.name + " (" + str(self.hp) + "/" + str(self.maxhp) + ")"
