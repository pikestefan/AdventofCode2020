# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 19:20:48 2020

@author: Lucio
"""

import re
from collections import deque
import numpy as np

rule_dictionary = {}

match_rule = "(\d+) (\w+\s\w+) bag"



with open('inputs/day7.txt') as file:
    
    for line in file.readlines():
        line = line.strip('.\n')
        bag, contained_bags = line.split(' contain ')
        
        bag = bag.replace(' bags', '')
        
        matching_string = re.findall(match_rule, contained_bags)
        if matching_string:
            bag_types = []
            amounts = []
            for match in matching_string:
                amount, bag_type = match
                bag_types.append(bag_type)
                amounts.append(int(amount))
            
            contained_bags = dict(zip(bag_types, amounts))
        elif contained_bags == 'no other bags':
            contained_bags = {'none':0} 
        else:
            print("No match")
        rule_dictionary[bag] = contained_bags
        
        
look_for_bag = deque()
look_for_bag.append('shiny gold')

bag_in_rules = rule_dictionary.keys()
can_contain_bags = []
while look_for_bag:
    look_for_this = look_for_bag.popleft()
    for bag in bag_in_rules:
        contained_bags = rule_dictionary[bag].keys()
        if look_for_this in contained_bags:
            can_contain_bags.append(bag)
            look_for_bag.appendleft(bag)
        
print(len(np.unique(can_contain_bags)))
        
##### Part 2
bag_queue = deque()
bag_queue.append([1, 'shiny gold'])

bags_required = 0

while bag_queue:
    
    multiplier, bag = bag_queue.popleft()
    
    bags_in_bag = rule_dictionary[bag]
    
    for colour, amount in bags_in_bag.items():
        if amount !=0:
            bags_required += multiplier * amount
            bag_queue.appendleft([multiplier * amount, colour])
        
print(bags_required)
    
    
        
        
        