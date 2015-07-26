#Define a playing card
class Card(object):
  card_value_dict = {
    'rank': [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace' ],
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'jack': 10,
    'queen': 10,
    'king': 10,
    'ace': 11
  };

  def __init__(self, value):
    self.name = value
    self.value = None

  #Return card name.
  @property
  def name(self):
    return self._name

  #Set card name for class using card_value_dict as validation set.
  @name.setter
  def name(self, value):
    if (str(value).lower() in self.card_value_dict.keys()) and (str(value).lower() != 'rank'):
      self._name = str(value).lower()
    else:
      raise ValueError('Could not classify ' + str(value) + ' as a playing card.')

  #Return card_value_dict defined card value if card value not set.
  @property
  def value(self):
    if self._value == None:
      return self.card_value_dict[self.name]
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
    return self.card_value_dict['rank'].index(self.name)

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

#Evaluate hand value for blackjack.
#Evaluate highest card by importance and value.
def BlackjackHighest(strArr):
  #Create a hand of cards
  hand = []
  for string in strArr:
    hand.append(Card(string))
  
  #Get initial hand value
  hand_value = 0
  for card in hand:
    hand_value = hand_value + card.value

  #Munge ace card values to 1 if hand value is over 21 and there is at least one ace.
  while (Card('ace') in hand) and (hand_value > 21):
    for index in xrange(len(hand)):
      if hand[index] == Card('ace'):
        low_ace = Card('ace')
        low_ace.value = 1
        hand[index] = low_ace
        break    
    
    hand_value = 0
    for card in hand:
      hand_value = hand_value + card.value
  
  #Get highest card
  highest_card = max(hand).name
  
  #Return result
  if hand_value == 21:
    return "blackjack " + highest_card
  elif hand_value > 21:
    return "above " + highest_card
  else:
    return "below " + highest_card
  
#Print result
print BlackjackHighest(raw_input())