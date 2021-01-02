# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 10:57:47 2020

@author: Lucio
"""
from collections import OrderedDict
import re

rule_pattern = r'(?:\d+\s)*\d+'

with open('inputs/day19.txt') as file:
    
    rules = dict()
    
    first_block = True
    while first_block:
        line = file.readline().strip()
        if line == '':
            first_block = False
        else:
            rule_number, rule_list = line.split(': ')
            rule_list = rule_list.strip('"')
            
            if not rule_list.isalpha():
                rule_list = re.findall(rule_pattern, rule_list)
                rule_list = [ list(map(int, sublist.split(' ')))
                                    for sublist in rule_list ]
            rules[ int(rule_number) ] = rule_list
            
            
    messages = []
    second_block = True
    while second_block:
        line = file.readline().strip()
        if line == '':
            second_block = False
        else:
            messages.append(line)

def get_unique_ids(number_rules):  

    flattened_rules = []
    for numb_rule in number_rules:
        flattened_rules += numb_rule
        
    unique_ids = list(OrderedDict.fromkeys(flattened_rules))

    
    return unique_ids


def do_combos(lists):
    
    start_dims = 1
    for listy in lists:
        start_dims *= len(listy)
    
    dims = start_dims
    new_lists = []
    for ii, listy in enumerate(lists):
        sub_list = []
        dims //= len(listy)
        for string in listy:
            sub_list += [string] * dims
        new_lists.append(sub_list *( start_dims // len(sub_list) ) )
        
          
    combo_list = []
    for els in zip(*new_lists):
        combo_list.append( ''.join(els) )
        
    return combo_list


### Part 1
def translate_rules(rules):
    translated_rules = dict()
    
    # Add to the translated rules only the known 
    for rule_num, rule in rules.items():
    
        if type(rule) is str and (len(rule) == 1):
            translated_rules[rule_num] = [rule]
    
    
    ii = 0
    rule_queue = []
    rule_queue.append(0)
    while 0 not in translated_rules:
        
        rule_id =  rule_queue[-1]
        split_subrules = rules[rule_id]
        unique_ids = get_unique_ids( split_subrules )  
        
        if not all( [unique_id in translated_rules for unique_id in unique_ids ] ):
            
            new_req_rules = []
            for req_id in unique_ids:
                if (req_id not in translated_rules) and (req_id not in rule_queue):
                    new_req_rules.append(req_id)
    
            rule_queue += new_req_rules
            
        else:
            final_rules = []
            for sub_rule in split_subrules:
                lists = [translated_rules[req_id] for req_id in sub_rule]
                output_list = do_combos(lists)
                
                final_rules += output_list
            translated_rules[rule_id] = final_rules
            rule_queue.pop(-1)
    return translated_rules

# The solution is pretty slow, but what actually takes time is 
# checking if the messages are inside the rules of 0
translated_rules = translate_rules(rules)
match_counter = 0
rule_list = translated_rules[0][:]
for message in messages:
    if message in rule_list:
        match_counter += 1
        
print(match_counter)
