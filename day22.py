# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 18:12:58 2020

@author: Lucio
"""

from collections import deque, defaultdict

def apply_win(winner, winning_card, losing_card):
    
    winner += [winning_card, losing_card]
    
class recursive_combat_game:
    
    def __init__(self, deck1, deck2, gameID, DEBUG = False):
        
        self.player1 = deck1[:]
        self.player2 = deck2[:]
        self.gameID = gameID
        
        self.round = 1
        self.card1 = 0
        self.card2 = 0
        
        self.game_finished = False
        self.paused = False
        self.game_winner = None
        
        self.previous_rounds_pl1 = []
        self.previous_rounds_pl2 = []
        
        self.DEBUG = DEBUG
        
    def play_round( self, previous_winner = None ):
        
        if not self.game_finished:
            
            previous_1 = self.player1[:]
            previous_2 = self.player2[:]
            
            if self.DEBUG:
                print("\n===== Game {:.0f}, round {:.0f} =====".format(self.gameID, 
                                                                       self.round))
            
            if previous_winner is not None:
                # This means that there was a recursive game won earlier
                if previous_winner == 1:
                    self.do_win(self.player1, self.card1, self.card2)
                    winner = 1
    
                elif previous_winner == 2:
                    self.do_win(self.player2, self.card2, self.card1)
                    winner = 2
                    
                if self.DEBUG:
                    print("Determining round with previous game winner...")
                    print("Player 1 has {:.0f} and Player 2 has {:.0f}".format(self.card1,
                                                                               self.card2))
                    print("Player {:.0f} wins the round!".format(winner))
                    
            else:
                if ( (self.player1 in self.previous_rounds_pl1) or
                     (self.player2 in self.previous_rounds_pl2) ):
                    
                    winner = 1
                    self.game_finished = True
                    if self.DEBUG:
                         print("Player 1:", self.player1)
                         print("Player 2:", self.player2)
                         print("One of the two decks was identical!")
                    
                else:
                    
                    if self.DEBUG:
                        print("Player 1:", self.player1)
                        print("Player 2:", self.player2)
                    self.card1 = self.player1.pop(0)
                    self.card2 = self.player2.pop(0)
                    
                    if self.DEBUG:
                        print("Player 1 draws:", self.card1)
                        print("Player 2 draws:", self.card2)
                    
                    
                    if (len(self.player1)>=self.card1) and (len(self.player2)>=self.card2):
                       
                        self.paused = True
                        
                        if self.DEBUG:
                            print("Starting new game to determine round winner")
                        
                    else:
                        if self.card1 > self.card2:
                            self.do_win(self.player1, self.card1, self.card2)
                            winner = 1
                        elif self.card2 > self.card1:
                            self.do_win(self.player2, self.card2, self.card1)
                            winner = 2
                        else:
                            print("Equal value?")
                            
                        if self.DEBUG:
                            print("Player {:.0f} wins the round!".format(winner))
            
            if len(self.player1) == 0 or len(self.player2) == 0:
                self.game_finished = True
            
            if self.game_finished:
                if self.DEBUG:
                    print("Game finished and won by:", winner)
                return winner
            elif self.paused:
                return self.player1[0:self.card1], self.player2[:self.card2]
            else:
                self.round += 1
                if previous_1 != self.player1:
                    self.previous_rounds_pl1.append(previous_1)
                if previous_2 != self.player2:
                    self.previous_rounds_pl2.append(previous_2)
                return None
                        
    def do_win(self, winner, winning_card, losing_card):
        winner += [winning_card, losing_card]
                    

    
with open('inputs/day22.txt') as file:
    listy =  file.readlines() 
    
    sep_idx = listy.index('\n')
    
    deck1 = listy[:sep_idx]
    deck1 = [int(card) for card in deck1[1:]]
    deck2 = listy[sep_idx+1:]
    deck2 = [int(card) for card in deck2[1:]]
    
    player1 = deck1[:]
    player2 = deck2[:]
    
### Part 1
while player1 and player2:
    
    card1 = player1.pop(0)
    card2 = player2.pop(0)
    
    if card1 > card2:
       apply_win(player1, card1, card2)
    elif card2 > card1:
        apply_win(player2, card2, card1)
    else:
        print("Equal value?")
        
if player1:
    winning_deck = list(player1)
    print("Winner is 1")
else:
    winning_deck = list(player2)
    print("Winner is 2")
    
points = [ card*(ii+1) for ii, card in enumerate(winning_deck[::-1]) ]
print(sum(points))
       

### Part 2
game_queue = []

glob_counter = 1
DEBUG = False

first_game = recursive_combat_game(deck1, deck2, glob_counter, DEBUG= DEBUG)

game_queue.append(first_game)

previous_winner = None
ii = 0
while not first_game.game_finished:
    
    curr_game = game_queue[-1]
    
    round_result = curr_game.play_round(previous_winner)
    
    if curr_game.paused and not curr_game.game_finished:
        glob_counter += 1
        new_game = recursive_combat_game(round_result[0], round_result[1], glob_counter,
                                         DEBUG = DEBUG)
        
        game_queue.append(new_game)
        
    elif curr_game.game_finished and len(game_queue) > 1:
        previous_winner = round_result
        game_queue.pop(-1)
        game_queue[-1].paused = False
        
    else:
        previous_winner = None
    
    ii+=1
    
winner = round_result

if winner == 1:
    winning_deck = first_game.player1
else:
    winning_deck = first_game.player2
        
points = [ card*(ii+1) for ii, card in enumerate(winning_deck[::-1]) ]
print(sum(points))