# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 18:22:52 2020

@author: Lucio
"""

def do_round(input_list, curr_idx):
    
    list_len = len(input_list)
    curr_cup = input_list[curr_idx]
    
    min_val, max_val = min(input_list), max(input_list)
    
    picked_cups = []
    
    new_list = input_list[:]
    
    for ii in range(1,4):
        
        pick_idx = (curr_idx + ii) % list_len
        
        picked_cups.append( input_list[pick_idx] )
        new_list.remove(input_list[pick_idx])
        
    destination_cup = curr_cup
    find_destination  = True
    while find_destination:
        
        destination_cup -= 1
        if destination_cup < min_val:
            destination_cup = max_val
            
        if (destination_cup not in picked_cups):
            find_destination = False
    destination_idx = new_list.index(destination_cup)
    
    new_list_len = len(new_list)
    for ii, cup in zip( range(destination_idx+1, destination_idx + 4), 
                        picked_cups):
        new_list.insert(ii, cup)
    
    new_curr_cup_idx = new_list.index(curr_cup)
    
    output_list = []
    for ii in range( new_curr_cup_idx - curr_idx,
                    new_curr_cup_idx - curr_idx + list_len ):
       output_list.append(new_list[ii % list_len])
    
    return output_list, destination_cup, picked_cups

def do_round_v2(cup_dictionary, curr_cup):
    
    pick_first = cup_dictionary[curr_cup]
    pick_mid = cup_dictionary[pick_first]
    pick_last = cup_dictionary[pick_mid]
    
    next_cup = cup_dictionary[pick_last]
    
    destination_cup = curr_cup
    find_destination  = True
    while find_destination:
        
        destination_cup -= 1
        if destination_cup < 1:
            destination_cup = 1000000
            
        if destination_cup not in [pick_first, pick_mid, pick_last]:
            find_destination = False
          
    cup_after_destination = cup_dictionary[ destination_cup ]
    
    cup_dictionary[ curr_cup ] = next_cup
    cup_dictionary[ destination_cup ] = pick_first
    cup_dictionary[ pick_last ] =  cup_after_destination
    
    return next_cup
    
def print_cup_dict(cup_dictionary):
    
    cuppy = min(cup_dictionary)
    cup_list = []
    for ii in range(len(cup_dictionary)):
        cuppy = cup_dictionary[cuppy]
        cup_list.append(str(cuppy))
    
    print(','.join(cup_list))
    

puzzle_input = '712643589'

puzzle_input = [int(numb) for numb in puzzle_input]

"""
### Part 1
input_list = puzzle_input[:]
input_list_len = len(input_list)
curr_index = 0
for ii in range(0, 100):
    #print(" -- Move {:d} --".format(ii+1))
    #print("Current cup:", input_list[curr_index])
    #print("Cups:", input_list)
    input_list, destination_cup, picked = do_round(input_list, curr_index)
    #print("Picked cups:", picked)
    #print("Destination:", destination_cup)
    #print('\n')
    curr_index += 1
    curr_index %= input_list_len

one_index = input_list.index(1)

final_list = []
for ii in range(1, input_list_len):
    final_list.append(input_list[(ii + one_index) % input_list_len])

print(''.join(map(str,final_list) ) )
"""
### Part 2
correct_list = puzzle_input[:]
max_input = max(puzzle_input)
correct_list += [ii for ii in range(max_input + 1, 1000000 + 1)]
list_len = len(correct_list)

following_el = [ correct_list[ (ii + 1) % list_len ] for ii in range(list_len)]

cup_dictionary = dict(zip(correct_list, following_el))

curr_cup = correct_list[0]
for ii in range(0, 10000000):
    curr_cup = do_round_v2(cup_dictionary, curr_cup)
    
cup_after_one = cup_dictionary[1]
print(cup_after_one * cup_dictionary[cup_after_one])



