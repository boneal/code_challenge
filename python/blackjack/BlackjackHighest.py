import random
import functools

#Define global variables.
#List used for generating card value dict and identifying card default ranks.
CARDS = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace']
#Dict containing CARDS as keys and associated numeric value.
CARD_VALUE = {card: i + 2 if i < 9 else 11 if card == 'ace' else 10 for i, card in enumerate(CARDS)}
#List of possible card suits.
SUITS = ['hearts', 'spades', 'daimonds', 'clubs']
#Cards shared by Game, Deck and Player classes.
DECK = None
#Players shared by Game and Player classes.
PLAYERS = None

#Define a playing card. Suits are not needed for blackjack_highest function to work.
@functools.total_ordering
class Card(object):
    def __init__(self, name, value=None, suit=None, visible=True):
        self.name = name
        self.value = value
        self.suit = suit
        self.visible = visible

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
            self.__get_importance()
            self.__get_default_value()
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

    #Return whether card is visible or not
    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if isinstance(value, bool):
            self._visible = value
        else:
            raise ValueError('Value must be a boolean.')

    #Set card default value defined in CARD_VALUE dict.
    def __get_default_value(self):
        self.__default_value = CARD_VALUE[self.name]

    #Return card importance.
    @property
    def importance(self):
        return self.__importance

    #Set card importance using CARDS list index value.
    def __get_importance(self):
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
        self.__cards = self.__get_cards()
        self.__used_cards = []

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

    #Return cards in deck.
    @property
    def cards(self):
        return self.__cards

    #Set cards in deck.
    def __get_cards(self):
        deck = []
        for suit in SUITS:
            deck += map(lambda name: Card(name, None, suit), CARDS)
        if self.decks > 1:
            multi_deck = []
            for i in list(range(self.decks)):
                multi_deck = multi_deck + deck
            deck = multi_deck
        return deck

    #Merge used and unused decks then shuffle cards.
    def shuffle(self):
        self.__cards = self.__used_cards + self.__cards
        self.__used_cards = []
        random.shuffle(self.__cards)

    #Remove a card from deck
    def remove_card(self):
        if not self.cards:
            self.shuffle()
        return self.cards.pop(0)

    #Adds cards back to used card deck.
    def return_card(self, value):
        self.__used_cards.append(value)

#Define hand of cards.
class Hand(object):
    def __init__(self):
        self.__cards = []

    #Returns list of Card instances.
    @property
    def cards(self):
        return self.__cards

    #Validates input is a list of Card instances.
    def add_card(self, value):
        if isinstance(value, Card):
            self.__cards.append(value)
            self.__get_value()
            self.__get_highest()
        else:
            raise ValueError('Not a card.')

    #Return hand value.
    @property
    def value(self):
      return self.__value

    #Set value of hand.
    #Munge ace card instance values to 1 until value is no longer greater than 21.
    def __get_value(self):
        self.__cards_eval = list(self.cards)
        value = sum(map(lambda card: card.value, self.__cards_eval))
        high_ace = Card('ace')
        high_ace_index = [index for index, card in enumerate(self.__cards_eval) if card == high_ace]
        if high_ace_index:
            high_ace_index_pop = high_ace_index.pop
            high_ace_value = high_ace.value
            low_ace = Card('ace', 1)
            low_ace_value = low_ace.value
            while value > 21 and high_ace_index:
                self.__cards_eval[high_ace_index_pop(0)] = low_ace
                value += low_ace_value - high_ace_value
        self.__value = value

    #Return highest card in hand.
    @property
    def highest(self):
        return self.__highest

    #Set highest card in hand.
    def __get_highest(self):
        self.__highest = max(self.__cards_eval).name

    @property
    def bust(self):
        if self.value > 21:
            return True
        return False


#Define a player.
class Player(object):
    __Players = []

    def __init__(self):
        self.__hands = [Hand()]
        self.__name = self.__set_name()

    #Return player hands.
    @property
    def hands(self):
        return self.__hands

    #Return player name.
    @property
    def name(self):
        return self.__name

    #Set player name.
    def __set_name(self):
        player_count = len(self.__Players)
        self.__Players.append(player_count)
        return "Player %s" % (player_count)

    #Add card to current hand.
    def hit(self, hand):
        hand.add_card(DECK.remove_card())

    #Return cards in current hand to deck.
    def return_hand(self, hand):
        if hand:
            for card in hand.cards:
                DECK.return_card(card)
            self.hands[self.hands.index(hand)] = None
        if not sum(isinstance(x, Hand) for x in self.hands):
            self.__hands = [Hand()]

    #Remove player from game.
    def exit_game(self):
        for hand in self.hands:
            self.return_hand(hand)
        PLAYERS[PLAYERS.index(self)] = None

    #Split current hand.
    def split(self, hand):
        cards = hand.cards
        if len(cards) == 2 and all(card.value == cards[0].value for card in cards):
            new_hand = Hand()
            new_hand.add_card(cards.pop(-1))
            self.hands.append(new_hand)
            for hand in self.hands:
                if hand:
                    hand.add_card(DECK.remove_card())
        else:
            print "  Can only split a pair with shared card value."


#Define House. Essentially a player with different name...
class House(Player):
    @property
    def name(self):
        return "House"


#Define blackjack game.
class Game(object):
    def __init__(self, players=1, decks=1):
        self.__house = House()
        self.__set_players(players)
        self.__set_deck(decks)

    #Get house player.
    @property
    def house(self):
        return self.__house

    #Get all the players too.
    @property
    def players(self):
        return PLAYERS

    #Set all players including house. House goes last.
    def __set_players(self, count):
        global PLAYERS
        PLAYERS = [Player() for i in list(range(count))] + [self.house]

    #Get the deck.
    @property
    def deck(self):
        return DECK

    #Set the deck and shuffle cards.
    def __set_deck(self, count):
        global DECK
        DECK = Deck(count)
        self.deck.shuffle()

    #Deal cards to all players in order. Card visibility only matters for house hole card.
    def __deal(self):
        for player in self.players:
            if player:
                for i in list(range(2)):
                    card = self.deck.remove_card()
                    card.visible = bool(i)
                    player.hands[0].add_card(card)

    #Game run logic
    def run(self):
        self.__deal()
        #Need more than one player to play.
        while sum(isinstance(x, Player) for x in PLAYERS) > 1:
            #Start round.
            for player in PLAYERS:
                #Skip players that exited the game.
                if not player:
                    continue
                #House actions.
                #House must hit until reaching at least a soft 17.
                if player is self.house:
                    #Show house's initial hand to players
                    print "House's initial hand:"
                    print_hand(self.house, self.house.hands[0])
                    hand = self.house.hands[0]
                    while hand.value < 17:
                        player.hit(hand)
                    #Show house's final hand.
                    print "House's final hand:"
                    print_hand(self.house, self.house.hands[0])
                #Player actions.
                else:
                    print "%s\'s turn:" % (player.name)
                    #Print house card visible to player.
                    print "  Visible house card:"
                    for card in self.house.hands[0].cards:
                        if card.visible:
                            print "    %s of %s" % (card.name, card.suit)
                    #Iterate player hands. Only one hand unless a split occurs.
                    for index, hand in enumerate(player.hands):
                        input = None
                        print_hand(player, hand)
                        #Continue playing hand unless player exits game.
                        while input != 'EXIT':
                            #Ask for input until a valid value is returned.
                            valid_input = False
                            while not valid_input:
                                input = raw_input("  Perform action: HIT, SPLIT, STAND or EXIT\n").upper()
                                if input == 'HIT':
                                    player.hit(hand)
                                    print_hand(player, hand)
                                elif input == 'SPLIT':
                                    player.split(hand)
                                    print_hand(player, hand)
                                elif input == 'EXIT':
                                    player.exit_game()
                                elif input == 'STAND':
                                    pass
                                else:
                                    print "Only HIT, SPLIT, STAND or EXIT are valid actions."
                                    continue
                                valid_input = True
                            #Move to next hand or player if bust or standing.
                            if input == 'STAND':
                                break
                            if hand.bust:
                                break
                    #Break player turn order only if house is left. Ends game.
                    if sum(isinstance(x, Player) for x in PLAYERS) == 1:
                        break
                print "\n"
            #Print results of round.
            #Ensures all players return cards to deck before next round.
            for player in PLAYERS:
                if not player:
                    continue
                if player != self.house:
                    print "%s:" % (player.name)
                for index, hand in enumerate(player.hands):
                    if player != self.house:
                        eval_winner(hand, index, self.house.hands[0])
                    player.return_hand(hand)
            print "\n"
            #Shuffle deck if over 75 percent consumed.
            if len(self.deck.cards) < (self.deck.decks * 13):
                print "Shuffling deck."
                self.deck.shuffle()
            #Print cards left in deck. This is mostly for sanity checking.
            print "%s cards left in deck." % len(self.deck.cards)
            #Deal new cards from deck to players
            self.__deal()

#Function for print a player's current hand.
def print_hand(player, hand):
    print "  Hand %s:" % (player.hands.index(hand) + 1)
    print "    Cards:"
    for card in hand.cards:
        print "      %s of %s" % (card.name, card.suit)
    print "    Eval: %s" % (eval_hand(hand))

#Who wins!!?!?!?
def eval_winner(player_hand, index, house_hand):
    print "  Hand %s" % (index + 1),
    if player_hand.value > 21:
        print "lost"
    elif house_hand.value > 21:
        print "won"
    elif player_hand.value < house_hand.value:
        print "lost"
    elif player_hand.value > house_hand.value:
        print "won"
    elif house_hand.value == 21 == player_hand.value:
        if len(house_hand.cards) == 2:
            if len(player_hand.cards) == 2:
                print "push"
            else:
                print "lost"
        else:
            print "lost"
    else:
        print "push"
        
#Creates a string that returns hand value, blackjack status, and highest value card.
def eval_hand(hand):
    if hand.cards:
        hand_highest = hand.highest
        hand_value = hand.value
        
        if hand_value == 21 and len(hand.cards) == 2:
            return "%s blackjack %s" % (hand_value, hand_highest)
        elif hand_value == 21:
            return "%s twenty-one %s" % (hand_value, hand_highest)
        elif hand_value > 21:
            return "%s above %s" % (hand_value, hand_highest)
        else:
            return "%s below %s" % (hand_value, hand_highest)
    else:
        return "none"

#Runs eval hand on a hand generated from user input.
def blackjack_highest(strArr):
    hand = Hand()
    cards = map(Card, strArr)
    map(hand.add_card, cards)
    return eval_hand(hand)

#Print result from input.
#print "%s\n" % (blackjack_highest(eval(str(raw_input()))))

#Run Game
#Can run game for four players with up to 8 decks like so: Game(4, 8).run()
Game().run()