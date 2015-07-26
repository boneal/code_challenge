#Define a playing card
class Card(object):
  rank = [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace' ]
  card_value = { card: i + 1 if i < 10 else 11 if card == 'ace' else 10 for i, card in enumerate(rank) }

  def __init__(self, card, value = None):
    self.name = card
    self.value = value

  #Return card name.
  @property
  def name(self):
    return self._name

  #Set card name for class using card_value_dict as validation set.
  @name.setter
  def name(self, value):
    if str(value).lower() in self.card_value.keys():
      self._name = str(value).lower()
    else:
      raise ValueError('Could not classify ' + str(value) + ' as a playing card.')

  #Return card_value_dict defined card value if card value not set.
  @property
  def value(self):
    if self._value == None:
      return self.card_value[self.name]
    else:
      return self._value

  #Set card value. Only needed for ace when flipping between 11 default and 1.
  @value.setter
  def value(self, value):
    if value != None:
      if type(value) is int:
        self._value = value
      else:
        raise ValueError('Value must be an integer.')
    else:
      self._value = None

  #Return card rank from card_value_dict rank key value.
  #Needed for identifying highest card between several face cards with shared values.
  @property
  def importance(self):
    return self.rank.index(self.name)

  #Check if two Card classes are equal.
  #Card value gets compared to ensure a default ace and munged ace do not match.
  def __eq__(self, other):
    if isinstance(other, Card):
      if (other.name == self.name) and (other.value == self.value):
        return True
    return False

  #Allow Card class to be evaluated by max(list) when in an array.  
  def __lt__(self, other):
    if isinstance(other, Card):
      if self.value < other.value:
        return True
      if (self.value == other.value) and (self.importance < other.importance):
        return True
    return False

  def __gt__(self, other):
    if isinstance(other, Card):
      if self.value > other.value:
        return True
      if (self.value == other.value) and (self.importance > other.importance):
        return True
    return False

#Define hand of cards 
class Hand(object):
  def __init__(self, cards):
    self.cards = cards

  @property
  def cards(self):
    return self._cards

  @cards.setter
  def cards(self, value):
    if (type(value) != list) or any(True if not isinstance(x, Card) else False for x in value):
      raise ValueError('Value must be a list of cards.')
    self._cards = value

  #Return value of hand taking aces into consideration.
  @property
  def value(self):
    while self.__value() > 21:
      if Card('ace') in self.cards:
        for index in xrange(len(self.cards)):
          if self.cards[index] == Card('ace'):
            self.cards[index] = Card('ace', 1)
            break
      else:
        break
    return self.__value()

  #Return highest ranked card in hand.
  @property
  def highest(self):
    return max(self.cards).name

  #Get current hand value.
  def __value(self):
    value = 0
    for card in self.cards:
      value = value + card.value     
    return value

def BlackjackHighest(strArr):
  #Create a hand of cards
  hand = Hand([ Card(string) for string in strArr ])

  #Return result
  if hand.value == 21:
    return "blackjack " + hand.highest
  elif hand.value > 21:
    return "above " + hand.highest
  else:
    return "below " + hand.highest

#Print result
print BlackjackHighest(raw_input())