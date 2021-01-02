# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 07:56:29 2020

@author: Lucio
"""

with open('inputs/day16.txt') as file:

    rules = dict()
    nearby_addresses = []
    for line in file.readlines():
        line = line.strip()
        
        if line and line[0].isalpha():
            
            if 'your' in line:
                get_my_address = True
                get_nearby_address = False
            elif 'nearby' in line:
                get_my_address = ~get_my_address
                get_nearby_address = ~get_my_address
            else:
                rule_name, ranges = line.split(': ')
                ranges = ranges.split(' or ')
                
                nums_in_range = []
                for ii, rangey in enumerate(ranges):
                    rangey = rangey.split('-')
                    rangey = list( map(int, rangey) )
                    rangey = [ ii for ii in range(rangey[0], rangey[1] + 1)]
                    nums_in_range += rangey

                rules[rule_name] = nums_in_range
                
        elif line and line[0].isdigit():
            line = list(map( int, line.split(',') ) )
            if get_nearby_address:
                nearby_addresses.append(line)
            elif get_my_address:
                my_address = line

all_valid_ranges = []
for valid_range in rules.values():
    all_valid_ranges += valid_range

invalid_counter = 0
valid_tickets = [True] * len(nearby_addresses)

for ii, address in enumerate(nearby_addresses):
    for number in address:
        if number not in all_valid_ranges:
            invalid_counter += number
            valid_tickets[ii] = False
            
print(invalid_counter)

### Part 2

filtered_tickets = [ticket for ticket, valid in zip(nearby_addresses, valid_tickets) if valid]
filtered_tickets = [ my_address ] + filtered_tickets
how_many_tickets = len( filtered_tickets )

columns = len( filtered_tickets[0] )
fields_to_check = list( rules.keys() )

possible_fields = [0] * columns
for col in range(columns):

    valid_fields = []
    for field in fields_to_check:
        
        value_is_valid = True
        keep_looping = True
        
        row = 0
        while keep_looping and row < how_many_tickets:
            value_is_valid = value_is_valid and ( filtered_tickets[row][col] in rules[field] )
            
            if not value_is_valid:
                keep_looping = False
            row += 1
        if value_is_valid:
            valid_fields.append(field)
    possible_fields[col] = valid_fields
        
#All the lists in possible fields must have length == 1, so the sum is columns
while sum( (map(len, possible_fields) ) ) > columns: 
    
    determined_fields = []
    
    for field in possible_fields:
        if len(field) == 1:
            determined_fields.append(field[0])
            
    for possible_field_list in possible_fields:
        for det_field in determined_fields:

            if det_field in possible_field_list and len(possible_field_list) > 1:
                possible_field_list.remove(det_field)
    
determined_fields = [ field[0] for field in possible_fields ]

departure_valsum = 1
for ii, det_field in enumerate(determined_fields):
    if 'departure' in det_field:
        departure_valsum *= my_address[ii]
print(departure_valsum)