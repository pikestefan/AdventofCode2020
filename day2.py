# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:19:26 2020

@author: Lucio
"""
from collections import OrderedDict
import numpy as np

policies = []
passwords = []
with open('inputs/day2.txt') as file:
    for line in file.readlines():
        string = line.strip()
        policy, pwd = string.split(':')
    
        passwords.append( pwd.strip() )
        
        amounts, letter = policy.split(' ')
        amount_min, amount_max = amounts.split('-')
        policies.append( {'letter' : letter,
                          'min' : int(amount_min),
                          'max' : int(amount_max)
                          } )
        

valids = [False]*len(passwords)
valid_amount = 0
for ii, pwd in enumerate(passwords):
    letter, req_min, req_max = policies[ii].values()
    how_many = pwd.count( letter )
    if (how_many >= req_min) and (how_many <= req_max):
        valids[ii] = True
        valid_amount += 1

print(valid_amount)

# Second part, new_rule: first digit gives required matching position
# second digit gives require mismatching position
        
valids = [False]*len(passwords)
valid_amount = 0
for ii, pwd in enumerate(passwords):
    letter, matching_pos, mismatching_pos = policies[ii].values()
    
    
    
    if (pwd[matching_pos - 1] == letter) ^ (pwd[mismatching_pos - 1] == letter):
        valids[ii] = True
        valid_amount += 1    
        
print(valid_amount)       
