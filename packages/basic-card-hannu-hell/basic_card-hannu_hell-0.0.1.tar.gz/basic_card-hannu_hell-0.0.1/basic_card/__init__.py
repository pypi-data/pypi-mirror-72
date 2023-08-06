import pygame
import random

values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
suits = ['hearts', 'clubs', 'spades', 'diamonds']


card_images = [deck_hearts, deck_clubs, deck_spades, deck_diamonds]

deck_clubs = [pygame.image.load('Clubs 1.png'), pygame.image.load('Clubs 2.png'), pygame.image.load('Clubs 3.png'),
              pygame.image.load('Clubs 4.png'), pygame.image.load('Clubs 5.png'), pygame.image.load('Clubs 6.png'),
              pygame.image.load('Clubs 7.png'),
              pygame.image.load('Clubs 8.png'), pygame.image.load('Clubs 9.png'), pygame.image.load('Clubs 10.png'),
              pygame.image.load('Clubs 11.png'),
              pygame.image.load('Clubs 12.png'), pygame.image.load('Clubs 13.png')]
deck_diamonds = [pygame.image.load('Diamond 1.png'), pygame.image.load('Diamond 2.png'),
                 pygame.image.load('Diamond 3.png'), pygame.image.load('Diamond 4.png'),
                 pygame.image.load('Diamond 5.png'), pygame.image.load('Diamond 6.png'),
                 pygame.image.load('Diamond 7.png'), pygame.image.load('Diamond 8.png'),
                 pygame.image.load('Diamond 9.png'),
                 pygame.image.load('Diamond 10.png'), pygame.image.load('Diamond 11.png'),
                 pygame.image.load('Diamond 12.png'), pygame.image.load('Diamond 13.png')]
deck_hearts = [pygame.image.load('Hearts 1.png'), pygame.image.load('Hearts 2.png'), pygame.image.load('Hearts 3.png'),
               pygame.image.load('Hearts 4.png'), pygame.image.load('Hearts 5.png'), pygame.image.load('Hearts 6.png'),
               pygame.image.load('Hearts 7.png'),
               pygame.image.load('Hearts 8.png'), pygame.image.load('Hearts 9.png'), pygame.image.load('Hearts 10.png'),
               pygame.image.load('Hearts 11.png'), pygame.image.load('Hearts 12.png'),
               pygame.image.load('Hearts 13.png')]
deck_spades = [pygame.image.load('Spades 1.png'), pygame.image.load('Spades 2.png'), pygame.image.load('Spades 3.png'),
               pygame.image.load('Spades 4.png'), pygame.image.load('Spades 5.png'), pygame.image.load('Spades 6.png'),
               pygame.image.load('Spades 7.png'),
               pygame.image.load('Spades 8.png'), pygame.image.load('Spades 9.png'), pygame.image.load('Spades 10.png'),
               pygame.image.load('Spades 11.png'),
               pygame.image.load('Spades 12.png'), pygame.image.load('Spades 13.png')]

#------------------------------------------------------------------------------
# Classes

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} {self.suit}"

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

#------------------------------------------------------------------------------

class Deck:
    def __init__(self):
        global values, suits
        self.deck = [Card(self.value, self.suit) for self.value in values for self.suit in suits]

    def __repr__(self):
        return self.deck

    def count(self):
        return len(self.deck)

    def _deal(self, num):
        count = self.count()
        real = min([count, num])
        if count == 0:
            raise ValueError("All cards have been dealt")
        cards = self.deck[-real:]
        self.deck = self.deck[:-real]
        return cards

    def deal_card(self):
        return self._deal(1)[0]  # as its a single card we access it with its index

    def deal_hand(self, hand_size):
        return self._deal(hand_size)

    def shuffle(self):
        if self.count() < 52:
            raise ValueError("Only full decks can be shuffled")
        random.shuffle(self.deck)
        return self

#------------------------------------------------------------------------------

def compare_cards(c1, c2):
    k = ["A", "K", "Q", "J"]
    if c1.value == "A" and c2.value == "A":
        return c1
    if c1.value == "A" and c2.value == "K":
        return c1
    if c1.value == "A" and c2.value == "Q":
        return c1
    if c1.value == "A" and c2.value == "J":
        return c1
    if c1.value == "K" and c2.value == "A":
        return c2
    if c1.value == "K" and c2.value == "K":
        return c1
    if c1.value == "K" and c2.value == "Q":
        return c1
    if c1.value == "K" and c2.value == "J":
        return c1
    if c1.value == "Q" and c2.value == "A":
        return c2
    if c1.value == "Q" and c2.value == "K":
        return c2
    if c1.value == "Q" and c2.value == "Q":
        return c1
    if c1.value == "Q" and c2.value == "J":
        return c1
    if c1.value == "J" and c2.value == "A":
        return c2
    if c1.value == "J" and c2.value == "K":
        return c2
    if c1.value == "J" and c2.value == "Q":
        return c2
    if c1.value == "J" and c2.value == "J":
        return c1
    if c1.value not in k and c2.value not in k:
        if int(c1.value) > int(c2.value):
            return c1
        if int(c1.value) == int(c2.value):
            return c1
        if int(c1.value) < int(c2.value):
            return c2
    if c1.value in k and c2.value not in k:
        return c1
    if c1.value not in k and c2.value in k:
        return c2

#------------------------------------------------------------------------------

def match_card(i, x, y):
    k = 0
    j = 0
    for s in suits:
        if i.suit == s:
            for v in values:
                if i.value == v:
                    win.blit(card_images[j][k], (x, y))
                if k <= 12:
                    k += 1
        if j <= 3:
            j += 1

#------------------------------------------------------------------------------

def have_suits(hand, s):
    for i in hand:
        if i.suit == s:
            return True
    return False

#------------------------------------------------------------------------------

def least_high_card(c, hand):
    n = 0
    for s in suits:
        for m in range(13):
            if c.suit == s and c.value == values[n]:
                for k in range(13):
                    for i in hand:
                        if n == 0:
                            return None
                        elif n == 12:
                            if i.suit == s and i.value == 'A':
                                return i
                        elif 0 < n < 12:
                            if i.suit == s and i.value == values[n + 1]:
                                return i
                    if n == 12:
                        break
                    n += 1
                    if n > 12:
                        n = 0
                        break
            if n == 12:
                break
            n += 1
        n = 0

#------------------------------------------------------------------------------

def lowest_valueCard_of_suit(hand, s):
    n = 0
    for k in range(13):

        for i in hand:
            if i.suit == s:
                if i.value == values[n + 1]:
                    return i
        n += 1
        if n == 12:
            for j in hand:
                if j.suit == s:
                    if j.value == 'A':
                        return j
        if n > 12:
            return None

#------------------------------------------------------------------------------

def lowest_valueCard(hand):
    n = 0
    for k in range(13):
        for i in hand:
            if i.value == values[n + 1]:
                return i
        n += 1
        if n == 12:
            for j in hand:
                if j.value == 'A':
                    return j
        if n > 12:
            return None

#------------------------------------------------------------------------------

def highest_valueCard_of_suit(hand, s):
    n = 13
    for j in hand:
        if j.suit == s:
            if j.value == "A":
                return j
    for k in range(13):

        for i in hand:
            if i.suit == s:
                if i.value == values[n - 1]:
                    return i
        n -= 1
        if n < 2:
            return None

#------------------------------------------------------------------------------

def highest_valueCard(hand):
    n = 13
    for j in hand:
        if j.value == "A":
            return j
    for k in range(13):
        for i in hand:
            if i.value == values[n - 1]:
                return i
        n -= 1
        if n < 2:
            return None
#------------------------------------------------------------------------------




