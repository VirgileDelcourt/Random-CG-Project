class Card:
    def __init__(self, name, cost, effects, desc, **kwargs):
        assert type(name) == str, "Card's name must be str"
        assert type(cost) == int, "Card's cost must be int"
        assert type(effects) == list, "Card's effects must be a list"
        assert len([True for _ in effects if not type(_) == type(lambda: "")]) == 0, "Card's effects must be a list of functions"
        
        self.name = name
        self.cost = cost
        # /!\ all effects must be like : (lambda card, user, target: pass)
        self.__effects__ = effects
        if "continuous" in kwargs:  # continuous effects are triggered at each round start, if the card is on the player's field
            self.__continuous__ = kwargs["continuous"]
            del kwargs["continuous"]
        else:
            self.__continuous__ = []
        self.description = desc

        self.mod = 0  # it's supposed to show how much a card has been upgraded
        
    def Use(self, user, target):
        """Call this function to, well, use the card
        Will simply call every function giving in the card, and the user and target you put in"""
        for effect in self.__effects__:
            effect(self, user, target)
            
    def Start_Turn(self, user, target):
        """This function is called by the player at each round start
        Will activate the continuous effect of the card"""
        for effect in self.__continuous__:
            effect(self, user, target)
            
    def Add(self, *args):
        """Takes in any number of functions (effects, that means they look like 'lambda card, user, target: pass')
        and adds those to this card's effects"""
        for effect in args:
            if type(effect) != type(lambda: ""):
                raise TypeError("tried to add " + type(effect).__name__ + ", instead of function, as effect to card " + self.name)
            self.__effects__.append(effect)
            self.mod += 1

    def Create_Copy(self):
        """Create and returns a copy of this card.
        Used to create an exact copy of the cards from the player's meta deck into the real deck
        although that doesn't really work well when cards add effects on play"""
        new = Card(self.name, self.cost, self.__effects__, self.description, continuous=self.__continuous__)
        new.mod = self.mod  # I don't know why this doesn't work
        return new
            
    def __repr__(self):
        if self.mod > 0:
            return self.name + "+" + str(self.mod) + " (" + str(self.cost) + ")"
        else:
            return self.name + " (" + str(self.cost) + ")"
