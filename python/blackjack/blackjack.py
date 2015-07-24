def BlackjackHighest(strArr):
  #Down case strings in strArr.
  for i in range(len(strArr)):
    strArr[i]= strArr[i].lower()

  #Create a dict with order key to define highest card by index. 
  #Ace will be an exception if sum of cards is greater than 21 when its integer value equals 11.
  blackjack_dict = {
    'list': [ 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace' ],
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
  
  #Make sure we're playing blackjack.
  for card in strArr:
    if card not in blackjack_dict['list']:
      return card + " is not a playable blackjack card!"
  
  #Add the hand up but don't go over 21 if possible!
  hand = 0
  
  for card in strArr:
    hand = hand + blackjack_dict[card]
    if hand > 21 and ('ace' in strArr):
      blackjack_dict['ace'] = 1
      hand = hand - 11 + blackjack_dict['ace']

  #What is the highest card in the hand?
  highest_card = 'one'
  
  for card in strArr:
    if blackjack_dict[card] > blackjack_dict[highest_card]:
      highest_card = card
      
    if blackjack_dict[card] == blackjack_dict[highest_card]:
      if blackjack_dict['list'].index(card) > blackjack_dict['list'].index(highest_card):
        highest_card = card
    
  #Return result.
  if hand == 21:
    return "blackjack " + highest_card
  elif hand > 21:
    return "above " + highest_card
  else:
    return "below " + highest_card

#Print result
print BlackjackHighest(raw_input())