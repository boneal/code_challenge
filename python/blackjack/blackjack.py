#Define a playing card
class Card(object):
  card_value_dict = {
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

  int_to_string_dict = { 
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',
    '11': 'ace'
  };

  importance_list = [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace' ]

  def __init__(self, value):
    self.name = value
    self.value = None

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    if str(value).lower() in self.card_value_dict.keys():
      self._name = str(value)
    elif str(value) in self.int_to_string_dict.keys():
      self._name = self.int_to_string_dict[str(value)]
    elif str(value) == '10':
      raise ValueError('More than one face card can have a value of ' + str(value) + '.')
    else:
      raise ValueError('Could not classify ' + str(value) + ' as a playing card.')

  @property
  def value(self):
    if self._value == None:
      return self.card_value_dict[self.name]
    else:
      return self._value

  @value.setter
  def value(self, value):
    if value != None:
      if 0 < value < 12:
        self._value = value
      else:
        raise ValueError('Value can only be 1 through 11.')
    else:
      self._value = None

  @property
  def importance(self):
    return self.importance_list.index(self.name)

  def __eq__(self, other):
    if isinstance(other, Card):
      if (other.name == self.name) and (other.value == self.value):
        return True
    return False
  
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

  #Munge value if over 21 and there is at least one ace
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