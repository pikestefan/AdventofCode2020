# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 21:59:00 2020

@author: Lucio
"""
import os 
import numpy as np

with open('inputs/day4.txt') as file:
    
    keep_going = True
    
    string = ''
    passports = []
    empty_count = 0
    while keep_going:
        line = file.readline()
        line = line.strip()
        line += ' '
        if line != ' ':
            empty_count = 0
            string += line
        else:
            if string != ' ':
                string = string.strip(' ')
                entries = string.split(' ')
                dicty = dict()
                for entry in entries:
                    key, val = entry.split(':', 1)
                    dicty[key] = val
                passports.append(dicty)
            string = ' '
            empty_count += 1
        if empty_count == 2:
            keep_going = False
            
valid_pports = [False] * len(passports)

required_entries = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
req_entr_amount = len(required_entries)
for ii, passport in enumerate(passports):
    entries = list(passport.keys())
    if 'cid' in entries:
        entries.remove('cid')
        
    if len(entries) == req_entr_amount:
        valid_pports[ii] = True
        
print(np.sum(valid_pports))

#### Second part, check validity of many things

req_entr_amount = len(required_entries)

def rules(entry, value):
    
    if entry == 'byr':
        num_value = int(value)
        truth_val = 1920 <= num_value <= 2002
    if entry == 'iyr':
        num_value = int(value)
        truth_val =  2010 <= num_value <= 2020
    if entry == 'eyr':
        num_value = int(value)
        truth_val = 2020 <= num_value <= 2030
    if entry == 'hgt':
        if len(value) >= 3:
            unit = value[-2:]
            number = int(value[:-2])
            if unit == 'cm':
                truth_val = 150 <= number <= 193
            else:
                truth_val = 59 <= number <= 76
        else:
            truth_val = False
    if entry == 'hcl':
        if len(value) == 7:
            truth_val = (value[0] == '#')
            for char in value[1:]:
                num_val = ord(char)
                truth_val = truth_val and ( ord('0') <= num_val <= ord('9') or 
                                            ord('a') <= num_val <= ord('f')
                                          )
        else:
            truth_val = False
    if entry == 'ecl':
        truth_val = ( len(value) ==  3) and (value in ['amb','blu','brn',
                                                       'gry','grn','hzl','oth'])
    if entry == 'pid':
        truth_val = (len(value) == 9) and value.isdigit()
        
    return truth_val

valid_pports = [False] * len(passports)
for ii, passport in enumerate(passports):
    
    pport_entries = passport.keys()
    
    valid_entries = np.zeros(req_entr_amount).astype(bool)
    
    for jj, req_entry in enumerate(required_entries):
        if req_entry in pport_entries:
            truth_val = rules( req_entry, passport[req_entry] )
            valid_entries[jj] = truth_val
            
    valid_pports[ii] = np.all(valid_entries)
     
print(np.sum(valid_pports))
        