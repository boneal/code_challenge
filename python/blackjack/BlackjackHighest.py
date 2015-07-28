#Define a playing card.
#Suits are not needed for blackjack_highest function to work.
class Card(object):
    __RANK = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace']
    __CARD_VALUE = {card: i + 2 if i < 9 else 11 if card == 'ace' else 10 for i, card in enumerate(__RANK)}

    def __init__(self, card, value=None):
        self.name = card
        self.value = value

    #Return card name.
    @property
    def name(self):
        return self._name

    #Set card name for class using __RANK list as validation set.
    @name.setter
    def name(self, value):
        value = str(value).lower()
        if value in self.__RANK:
            self._name = value
            self.get_importance()
            self.get_default_value()
        else:
            raise ValueError('Could not classify ' + value + ' as a playing card.')

    #Return card value.
    @property
    def value(self):
        if self._value is None:
            return self.__default_value
        else:
            return self._value

    #Set card value. Accepts None or an integer value.
    @value.setter
    def value(self, value):
        if value is not None:
            if isinstance(value, int):
                self._value = value
            else:
                raise ValueError('Value must be an integer.')
        else:
            self._value = None

    #Set card default value defined in __CARD_VALUE dict.
    def get_default_value(self):
        self.__default_value = self.__CARD_VALUE[self.name]

    #Return card importance.
    @property
    def importance(self):
        return self.__importance

    #Set card importance using __RANK list index value.
    def get_importance(self):
        self.__importance = self.__RANK.index(self.name)

    #Check if two Card class instances are equal. Both name and value must be equal.
    def __eq__(self, other):
        if isinstance(other, Card):
            if other.name == self.name and other.value == self.value:
                return True
        return False

    #Allow list of Card class instances to be evaluated by max(list).
    #Card value takes precedence over importance unless card values are equal.
    def __gt__(self, other):
        if isinstance(other, Card):
            if ((self.importance > other.importance and self.value == other.value) or
                    self.value > other.value):
                return True
        return False


#Define hand of cards.
class Hand(object):
    def __init__(self, cards):
        self.cards = cards

    #Returns list of Card instances.
    @property
    def cards(self):
        return self._cards

    #Validates input is a list of Card instances.
    @cards.setter
    def cards(self, value):
        if (not isinstance(value, list) or not value or
               any(False if isinstance(card, Card) else True for card in value)):
            raise ValueError('Value must be a list of cards.')
        elif any(True if value.count(card) > 32 else False for card in value):
            raise ValueError('Hand can not contain more than thirty-two of any single card.')
        self._cards = value
        self.get_value()
        self.get_highest()

    #Return hand value.
    @property
    def value(self):
      return self.__value

    #Set value of hand.
    #Munge ace card instance values to 1 until value is no longer greater than 21.
    def get_value(self):
        value = sum(map(lambda card: card.value, self.cards))
        high_ace = Card('ace')
        high_ace_index = [index for index, card in enumerate(self.cards) if card == high_ace]
        if high_ace_index:
            high_ace_index_pop = high_ace_index.pop
            high_ace_value = high_ace.value
            low_ace = Card('ace', 1)
            low_ace_value = low_ace.value
            while value > 21 and high_ace_index:
                self.cards[high_ace_index_pop(0)] = low_ace
                value += low_ace_value - high_ace_value
        self.__value = value

    #Return highest card in hand.
    @property
    def highest(self):
        return self.__highest

    #Set highest card in hand.
    def get_highest(self):
        self.__highest = max(self.cards).name

def blackjack_highest(strArr):
    #Create a hand of cards and return result.
    hand = Hand(map(Card, strArr))
    hand_highest = hand.highest
    hand_value = hand.value

    if hand_value == 21:
        return "blackjack " + hand_highest
    elif hand_value > 21:
        return "above " + hand_highest
    else:
        return "below " + hand_highest

#Print result
#Below allows both local and coderbyte script execution.
print blackjack_highest(eval(str(raw_input())))