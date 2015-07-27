#Define a playing card.
#Suits are not needed for BlackjackHighest to work.
class Card(object):
    RANK = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace']
    CARD_VALUE = {card: i + 1 if i < 10 else 11 if card == 'ace' else 10 for i, card in enumerate(RANK)}

    def __init__(self, card, value=None):
        self.name = card
        self.value = value

    #Return card name.
    @property
    def name(self):
        return self._name

    #Set card name for class using CARD_VALUE dict as validation set.
    @name.setter
    def name(self, value):
        if str(value).lower() in self.CARD_VALUE.keys():
            self._name = str(value).lower()
        else:
            raise ValueError('Could not classify ' + str(value) + ' as a playing card.')

    #Return card value defined in CARD_VALUE dict if not set.
    @property
    def value(self):
        if self._value is None:
            return self.CARD_VALUE[self.name]
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

    #Return card importance using RANK list index value.
    @property
    def importance(self):
        return self.RANK.index(self.name)

    #Check if two Card class instances are equal. Both name and value must be equal.
    def __eq__(self, other):
        if isinstance(other, Card):
            if other.name == self.name and other.value == self.value:
                return True

    #Allow list of Card class instances to be evaluated by max(list).
    #Card value takes precedence over importance unless card values are equal.
    def __gt__(self, other):
        if isinstance(other, Card):
            if ((self.importance > other.importance and self.value == other.value) or
                    self.value > other.value):
                return True


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
        if (not isinstance(value, list) or
               any(False if isinstance(card, Card) else True for card in value)):
            raise ValueError('Value must be a list of cards.')
        self._cards = value

    #Return value of hand taking aces into consideration.
    @property
    def value(self):
        normal_ace = Card('ace')
        low_ace = Card('ace', 1)
        ace_index = [index for index, card in enumerate(self.cards) if card == normal_ace]
        pop_an_ace = ace_index.pop
        while self.__value() > 21 and ace_index:
            self.cards[pop_an_ace(0)] = low_ace
        return self.__value()

    #Called by value property getter to detect current hand value.
    def __value(self):
        return sum(map(lambda card: card.value, self.cards))

    #Return highest card in hand.
    @property
    def highest(self):
        return max(self.cards).name


def blackjack_highest(strArr):
    #Create a hand of cards.
    hand = Hand(map(Card, strArr))
    hand_value = hand.value
    hand_highest = hand.highest

    #Return result.
    if hand_value == 21:
        return "blackjack " + hand_highest
    elif hand_value > 21:
        return "above " + hand_highest
    else:
        return "below " + hand_highest

#Print result
print blackjack_highest(raw_input())