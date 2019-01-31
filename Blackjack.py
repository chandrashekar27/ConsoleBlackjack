import random
import time
global card_suits, card_ranks, card_values
card_suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
card_ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
              'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
card_values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
               'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
               'Queen': 10, 'King': 10,
               'Ace': 11}

# some basic functions

def print_decks(deck1):
    print("Dealer's Hand")
    if len(comp_hand) == 1:
        print("<<HIDDEN>>")
    comp_hand.show()
    print('\n')
    print("Player's Hand")
    deck1.show()


def user_bust():
    global won
    won = 'comp'
    money.money_lose()
    print(f'BUST. You lost {money.bet} chips!')


def user_win():
    global won
    won = 'user'
    money.money_win()
    print(f'Success! You win {money.bet} chips!')


def comp_win():
    global won
    won = 'comp'
    money.money_lose()
    print(f'You lose! You lost {money.bet} chips!')


def comp_bust():
    global won
    won = 'user'
    money.money_win()
    print(f'Dealer Busts! You win {money.bet} chips!')


class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = card_values[self.rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Chips():
    def __init__(self, start_value=100):
        self.value = start_value
        self.bet = 1000

    def __str__(self):
        return f'You have {self.value} chips left !!'

    def bet_money(self):
        self.bet=1000
        while self.bet > self.value:
            try:
                self.bet = int(input('Enter the amount you want to bet:- '))
            except TypeError:
                print('INPUT INVALID')
        print(f'You have bet {self.bet} chips!')

    def money_win(self):
        self.value += self.bet

    def money_lose(self):
        self.value -= self.bet
class Deck():
    def __init__(self):
        self.deck = []
        for suit in card_suits:
            for rank in card_ranks:
                self.deck.append(Card(suit, rank))

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def get_card(self):
        return self.deck.pop()


class Hand():
    def __init__(self, player):
        self.player=player
        self.hand = []
        # deal 2 cards to user or 1 card to comp
        self.hand.append(the_deck.get_card())
        if self.player == 'user':
            self.hand.append(the_deck.get_card())

    def show(self):
        for card in self.hand:
            print(f'{card.rank} of {card.suit}')

    def __len__(self):
        return len(self.hand)

    def get_value(self):
        sum = 0
        for card in self.hand:
            sum += card.value
        if sum > 21 and self.ace():
            sum -= 10
        return sum

    def ace(self):
        for value in self.hand:
            if value.value == 11:
                return True
        return False

    def add_card(self):
        self.hand.append(the_deck.get_card())

    def destroy(self):
        for card in self.hand:
            del card


# GAME running cell
running = True
money = Chips(100)
while running:
# starting variables and objects
    the_deck = Deck()
    user_state = 'none'
    comp_state = 'none'
    global won
    won = 'none'
# display remaining money and ask for bet amount
    print('Welcome to blackjack')
    print(money)
    money.bet_money()
# shuffle the deck
    the_deck.shuffle_deck()
# create user and comps hands
    user_hand = Hand('user')
    comp_hand = Hand('comp')
# inner game loop 1(until player loses or holds)
    while user_state != 'hold':
        print_decks(user_hand)
# check for blackjack
        if user_hand.get_value() == 21:
            break
# check for player lose
        if user_hand.get_value() > 21:  # player bust
            user_bust()
            break
# ask player to hit or hold
        user_state = 'none'
        while user_state != 'hold' and user_state != 'hit':
            user_state = input('Do you wish to hit or hold? ')
            if user_state == 'hit':  # if player chooses to hit , add a card
                user_hand.add_card()
# inner game loop 2(for dealer)
    while won == 'none':
        # print the decks
        print("Dealer's move....")
        print('\n')
        time.sleep(2)
        print_decks(user_hand)
# check if dealer won or lost or tie(end loop if won or lost)
        if comp_hand.get_value() > 21:  # comp bust
            comp_bust()
        if comp_state == 'hold':
            if user_hand.get_value() > comp_hand.get_value():  # player win
                user_win()
            elif user_hand.get_value() == comp_hand.get_value():  # tie game
                won = 'tie'
                print(f'Its a TIE!')
            else:  # comp win
                comp_win()
# decide to hit or hold
        if user_hand.get_value() > comp_hand.get_value():
            comp_state = 'hit'
        elif user_hand.get_value() == comp_hand.get_value():
            if comp_hand.get_value() < 16:
                comp_state = 'hit'
            else:
                comp_state = 'hold'
        else:
            comp_state = 'hold'
        if comp_state == 'hit':  # if comp chooses to hit , add a card
            comp_hand.add_card()
            time.sleep(1)
# if money available,continue
    print(money)
# if not broke,DELETE VARIABLES, ask if they want to play again(playing variable)
    if money.value > 0:
        again = 'none'
        while again != 'yes' and again != 'no':
            again = input('Do you wish to another hand? enter yes or no:- ')
        if again == 'no':
            running = False
        else:
            print("Starting another round...")
            del the_deck
            user_hand.destroy()
            comp_hand.destroy()
            del user_hand
            del comp_hand
            time.sleep(1)
    else:
        print('You are BROKE! GAME OVER!')
        running = False
