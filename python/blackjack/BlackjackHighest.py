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

    #Set card value. Only needed for ace when flipping between 11 default and 1.
    @value.setter
    def value(self, value):
        if value is not None:
            if isinstance(value, int):
                self._value = value
            else:
                raise ValueError('Value must be an integer.')
        else:
            self._value = None

    #Return card rank from RANK list index.
    #Needed for identifying highest card between several face cards with shared values.
    @property
    def importance(self):
        return self.RANK.index(self.name)

    #Check if two Card classes are equal.
    #Card value gets compared to ensure a default ace and munged ace do not match.
    def __eq__(self, other):
        if isinstance(other, Card):
            if other.name == self.name and other.value == self.value:
                return True

    #Allow Card class to be evaluated by max(list) when in a list.
    def __gt__(self, other):
        if isinstance(other, Card):
            if ((self.importance > other.importance and self.value == other.value) or
                    self.value > other.value):
                return True


#Define hand of cards.
class Hand(object):
    def __init__(self, cards):
        self.cards = cards

    #Returns list of cards in hand.
    @property
    def cards(self):
        return self._cards

    #Performs input validation when adding list of cards.
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

    def __value(self):
        return sum(map(lambda card: card.value, self.cards))

    #Return highest ranked card in hand.
    @property
    def highest(self):
        return max(self.cards).name


def blackjack_highest(strArr):
    #Create a hand of cards
    hand = Hand(map(Card, strArr))

    #Return result
    if hand.value == 21:
        return "blackjack " + hand.highest
    elif hand.value > 21:
        return "above " + hand.highest
    else:
        return "below " + hand.highest

#Print result
print blackjack_highest(raw_input())