import random
import functools

#Define global variables.
CARDS = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace']
CARD_VALUE = {card: i + 2 if i < 9 else 11 if card == 'ace' else 10 for i, card in enumerate(CARDS)}
SUITS = ['hearts', 'spades', 'daimonds', 'clubs']

#Define a playing card. Suits are not needed for blackjack_highest function to work.
@functools.total_ordering
class Card(object):
    def __init__(self, name, value=None, suit=None):
        self.name = name
        self.value = value
        self.suit = suit

    #Return card name.
    @property
    def name(self):
        return self._name

    #Set card name for class using CARDS list as validation set.
    @name.setter
    def name(self, value):
        value = str(value).lower()
        if value in CARDS:
            self._name = value
            self.get_importance()
            self.get_default_value()
        else:
            raise ValueError('Could not classify \'' + value + '\' as a playing card.')

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

    #Return card suit.
    @property
    def suit(self):
        if self._suit is None:
            return SUITS[0]
        else:
            return self._suit

    #Set card suit.
    @suit.setter
    def suit(self, value):
        if value is not None:
            value = str(value)
            if value in SUITS:
                self._suit = value
            else:
                raise ValueError('Value \'' + value + '\' not a valid suit.')
        else:
            self._suit = None

    #Set card default value defined in CARD_VALUE dict.
    def get_default_value(self):
        self.__default_value = CARD_VALUE[self.name]

    #Return card importance.
    @property
    def importance(self):
        return self.__importance

    #Set card importance using CARDS list index value.
    def get_importance(self):
        self.__importance = CARDS.index(self.name)

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

#Define deck of cards
class Deck(object):
    def __init__(self, decks=1):
        self.decks = decks

    #Return number of decks.
    @property
    def decks(self):
        return self._decks

    #Set number of decks.
    @decks.setter
    def decks(self, value):
        if isinstance(value, int) and value < 9:
            self._decks = value
        else:
            raise ValueError('Value must be an integer less than nine.')
        self.get_cards()

    #Return cards in deck.
    @property
    def cards(self):
        return self.__cards

    #Set cards in deck.
    def get_cards(self):
        deck = []
        for suit in SUITS:
            deck += map(lambda name: Card(name, None, suit), CARDS)
        if self.decks > 1:
            multi_deck = []
            for i in list(range(self.decks)):
                multi_deck = multi_deck + deck
            deck = multi_deck
        self.__cards = deck

    #Shuffle cards in deck.
    def shuffle(self):
        random.shuffle(self.__cards)

def House(object):
    pass

def Player(object):
    pass        

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

    if hand_value == 21 and len(hand.cards) == 2:
        return "blackjack " + hand_highest
    elif hand_value == 21:
        return "twenty-one " + hand_highest
    elif hand_value > 21:
        return "above " + hand_highest
    else:
        return "below " + hand_highest

#Print result from input.
#print blackjack_highest(eval(str(raw_input())))

deck = Deck()
for card in deck.cards:
   print card.name + " of " + card.suit

deck.shuffle()
print "###SHUFFLE###"
for card in deck.cards:
   print card.name + " of " + card.suit
