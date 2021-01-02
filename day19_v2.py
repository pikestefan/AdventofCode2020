# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 10:57:47 2020

@author: Lucio

Alternative version, realizing the neat trick of using regexp
to go through the message list faster. Here one checks that the messages
matches a string regexp given by the rules, and doesn't check that the string 
is found inside in the list of possible strings (see day19).
Inspired from 
https://github.com/marcodelmastro/AdventOfCode2020
"""
from collections import OrderedDict
#import re
from math import ceil
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
            
            rules[ int(rule_number) ] = rule_list
            
            
    messages = []
    second_block = True
    while second_block:
        line = file.readline().strip()
        if line == '':
            second_block = False
        else:
            messages.append(line)

def translate_rules( rules, starting_rule = 0 ):
    translated_rules = dict()
    
    # Add to the translated rules only the ones known from the beginning
    rules_to_translate = []
    for rule_num, rule in rules.items():
        if len(rule) == 1:
            translated_rules[rule_num] = rule
        else:
            rules_to_translate.append(rule_num)
        
    rule_queue = []
    while len(rules_to_translate) > 0:
        
        if len(rule_queue) == 0:
            rule_queue.append( rules_to_translate[0] )
        rule_id =  rule_queue[-1]
        rule_string = rules[rule_id]
        
        matched_ids = list( map( int, re.findall('\d+', rule_string) ) )
        
        #You need to have all the sub rules, before translating.
        #If you don't, wait until then
        if not all( [req_id in translated_rules for req_id in matched_ids ] ):
            
            for req_id in matched_ids:
               if (req_id not in translated_rules) and (req_id not in rule_queue):
                   rule_queue.append(req_id)
                
        else:
            for req_id in matched_ids:
                trans_rule = translated_rules[req_id]
                if '|' in trans_rule:
                    trans_rule = '(' + trans_rule + ')'
                
                rule_string = re.sub( r'\b' + str(req_id) + r'\b', 
                                      trans_rule,
                                      rule_string)
                
            translated_rules[rule_id] = rule_string.replace(' ','')
            rule_queue.pop(-1)
            rules_to_translate.remove(rule_id)
            
    return translated_rules


def apply_rules_part2(rules, messages):
    
    # Rule 0 is just '8 11'
    mod_rules = dict(rules)
    mod_rules[8] =' 42 | 42 8'
    mod_rules[11] = '42 31 | 42 11 31'
    
    # The affected rules are 8 and 11
    #First get the unaffected ones
    unaffected_rules = dict()
    for rule, rule_string in mod_rules.items():
        rule_ids = list( map(int, re.findall('\d+', rule_string)) )
        if not ( (rule == 8) or (rule == 11) or
                 (8 in rule_ids) or (11 in rule_ids)  ):
            unaffected_rules[rule] = rule_string
            
    unaffected_translated = translate_rules(unaffected_rules)
    
    rule42 = unaffected_translated[42]
    rule31 = unaffected_translated[31]
    
    len42 = get_minimum_matchable_length(rule42)
    len31 = get_minimum_matchable_length(rule31)
    
    rule8 = r'({})+'.format(rule42) 
    rule11 = r'({})'.format(rule42) + '{x}' + r'({})'.format(rule31) + '{x}'
    
    rule0 = '^{}{}$'.format(rule8, rule11)
    
    # The following func is to tell the while loop to stop when
    # the pattern which it's trying to match is longer than 
    # the actual string.
    min_patt_len = lambda message, repeat:  len42 + repeat* (len42 + len31)
    
    match_counter = 0
    for message in messages:
        
        keep_searching = True
        
        rep = 1
        patt_len = min_patt_len(message, rep)
        while keep_searching and (patt_len <= len(message)):
            match = re.match( rule0.replace('x', str(rep)), message )
            if match is not None:
                keep_searching = False
                match_counter += 1
            rep += 1
            patt_len = min_patt_len(message, rep)
        
    return match_counter  

def get_minimum_matchable_length(string):
    
    pattern = r'\(([a-z]+)\|([a-z]+)\)'
    
    keep_matching = True
    
    while keep_matching:
        match = re.search(pattern, string)
        if match is not None:
            left_term, right_term = match.groups()
            min_length = min( len(left_term), len(right_term) )
            string = string.replace(match.group(0), 'x'*min_length)
            string = re.sub(r'\(([a-z]+)\)',r'\1',string)
        else:
            keep_matching = False
            
    minimum_len = min( list( map(len, string.split('|') ) ) )
    
    return minimum_len

### Part 1
translated_rules = translate_rules(rules)
match = sum([ 1 if re.fullmatch(translated_rules[0], message) else 0
               for message in messages ] )
print(match)
### Part 2
part2_matches = apply_rules_part2(rules, messages)
print(part2_matches)