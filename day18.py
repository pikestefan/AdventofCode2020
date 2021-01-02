# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 10:35:48 2020

@author: Lucio
"""

import numpy as np
import re

brack_pattern = r'\(((\d+ ([\*,\+]\s?))* \d+)\)'
two_number_patt = r'(\d+) ([\*,\+]) (\d+)'

sum_number_patt = r'(\d+) \+ (\d+)'
mult_number_patt = r'(\d+) \* (\d+)'

def parse_operator(char):
    if char == '+':
        func = lambda a,b : a + b
    elif char == '*':
        func = lambda a,b : a * b
    return func

with open('inputs/day18.txt') as file:
    
    operation_list = []

    for line in file.readlines():
        line = line.strip()
        operation_list.append(line)
        
operation_list_orig = operation_list[:] #Copy the original array


operation_outputs_v1 = []
for operation in operation_list:

    while not operation.isdigit():
        match = re.match( two_number_patt, operation )
        if match is not None:
            a, op, b = match.groups()
            function = parse_operator(op)
            output = function(int(a), int(b))
            operation = operation.replace('{} {} {}'.format(*match.groups()),
                                          str(output), 1 )
        else:
            match = re.search( brack_pattern, operation )
            if match is not None:
                matched_pattern = match.group()
                sub_operation = matched_pattern[1:-1]
                while not sub_operation.isdigit():
                    match = re.match( two_number_patt, sub_operation )
                    a, op, b = match.groups()
                    function = parse_operator(op)
                    output = function(int(a), int(b))
                    sub_operation = sub_operation.replace('{} {} {}'.format(*match.groups()),
                                                          str(output), 1 )
                operation = operation.replace(matched_pattern, sub_operation, 1)

    operation_outputs_v1.append(int(operation))

print( sum(operation_outputs_v1) )

# Part 2
operation_outputs_v2 = []
for operation in operation_list:

    search_brackets = True
    while search_brackets:
        matched = re.findall( brack_pattern, operation )
        if len(matched) == 0:
            search_brackets = False
        else:
            for ii, match in enumerate(matched):

                sub_operation = match[0]
                
                #First look for sums
                look_for_sums = True
                while look_for_sums:
                    sums = re.search(sum_number_patt, sub_operation)
                    if sums is None:
                        look_for_sums = False
                    else:
                        a, b = sums.groups()
                        output = int(a) + int(b)
                        sub_operation = sub_operation.replace('{} + {}'.format(*sums.groups()),
                                                             str(output), 1)
                #Then look for prods
                look_for_prods = True
                while look_for_prods:
                    prods = re.search(mult_number_patt, sub_operation)
                    if prods is None:
                        look_for_prods = False
                    else:
                        a, b = prods.groups()
                        output = int(a) * int(b)
                        sub_operation = sub_operation.replace('{} * {}'.format(*prods.groups()), 
                                                              str(output), 1)
                
            operation = operation.replace( '(' + matched[ii][0] + ')',
                                          sub_operation, 1)

    #First look for sums
    look_for_sums = True
    while look_for_sums:
        sums = re.search(sum_number_patt, operation)
        if sums is None:
            look_for_sums = False
        else:
            a, b = sums.groups()
            output = int(a) + int(b)
            operation = operation.replace('{} + {}'.format(*sums.groups()),
                                          str(output), 1)
    #Then look for prods
    look_for_prods = True
    while look_for_prods:
        prods = re.search(mult_number_patt, operation)
        if prods is None:
            look_for_prods = False
        else:
            a, b = prods.groups()
            output = int(a) * int(b)
            operation = operation.replace('{} * {}'.format(*prods.groups()), 
                                          str(output), 1)

    operation_outputs_v2.append(int(operation))

print(sum(operation_outputs_v2))
        