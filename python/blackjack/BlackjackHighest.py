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

  #Set card name for class using card_value dict as validation set.
  @name.setter
  def name(self, value):
    if str(value).lower() in self.card_value.keys():
      self._name = str(value).lower()
    else:
      raise ValueError('Could not classify ' + str(value) + ' as a playing card.')

  #Return card value defined in card_value dict if not set.
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

  #Return card rank from rank list index.
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

  #Allow Card class to be evaluated by max(list) when in a list.  
  def __lt__(self, other):
    if isinstance(other, Card):
      if (self.importance < other.importance) and (self.value == other.value):
        return True
      if (self.value < other.value):
        return True

  def __gt__(self, other):
    if isinstance(other, Card):
      if (self.importance > other.importance) and (self.value == other.value):
        return True
      if (self.value > other.value):
        return True

  #Implemented for sum(list) to work on cards.
  def __radd__(self, other):
    return other + self.value

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
    if (type(value) != list) or any(True if not isinstance(x, Card) else False for x in value):
      raise ValueError('Value must be a list of cards.')
    self._cards = value

  #Return value of hand taking aces into consideration.
  @property
  def value(self):
    ace_index = [ index for index, card in enumerate(self.cards) if card == Card('ace')]
    while sum(self.cards) > 21 and ace_index:
      self.cards[ace_index.pop(0)] = Card('ace', 1)
    return sum(self.cards)

  #Return highest ranked card in hand.
  @property
  def highest(self):
    return max(self.cards).name

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