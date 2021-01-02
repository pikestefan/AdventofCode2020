# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 08:51:33 2020

@author: Lucio
"""

def convert_to_bin(integer):
    
    #Could do it by hand, but python built-in function is much faster
    max_bit = 36
    
    binarized = bin(integer)
    binarized = binarized[2:]
    
    if len(binarized) < max_bit:
        binarized = '0' * ( max_bit - len(binarized) ) + binarized
        
    return binarized

def compare_bits( mask_bit, number_bit ):
    
    if mask_bit == 'X':
        output_bit = number_bit
    else:
       output_bit = mask_bit
       
    return output_bit

def compare_bits_v2( mask_bit, number_bit ):
    
    if mask_bit == '0':
        output_bit = number_bit
    else:
        output_bit = mask_bit

    return output_bit

def get_bit_combos(bit_amount):
    #Generate the list of bit combinations
    tot_combos = 2**bit_amount
    
    string_list = []
    
    multip = tot_combos//2
    glob_multip = 1
    for ii in range(0, bit_amount):
        
        stringy = ( '0' * multip + '1' * multip ) * glob_multip
        
        string_list.append(stringy)
        multip //= 2
        glob_multip *= 2
    return string_list
        

with open('inputs/day14.txt') as file:
    
    mask_list = []
    memory_addresses = []
    values_to_write = []
    
    temp_memories= []
    temp_values = []
    for line in file.readlines():
        line = line.strip().split(' = ')
        
        if line[0] == 'mask':
            mask_list.append(line[1])
            memory_addresses.append( temp_memories )
            values_to_write.append( temp_values )
            
            temp_memories = []
            temp_values = []
        else:
            address = line[0]
            address = int(address[4:-1]) # style is mem[12334923] = ...
            temp_memories.append(address)
            temp_values.append( int(line[1]) )
            
    memory_addresses.append( temp_memories )
    values_to_write.append( temp_values )
            
    memory_addresses.pop(0)
    values_to_write.pop(0)
    
memory = dict()

for mask, addresses, values in zip( mask_list, memory_addresses, values_to_write ):
    
    for address, value in zip( addresses, values ):
        
        bin_string = convert_to_bin(value)
        masked_binstring = ''.join( map( compare_bits, mask, bin_string ) )
        output_number = int(masked_binstring, base = 2)
        
        memory[address] = output_number
        
print(sum( memory.values() ))

### Part 2


memory = dict()
for mask, addresses, values in zip( mask_list, memory_addresses, values_to_write ):
    
    for address, value in zip( addresses, values ):
        
        bin_string = convert_to_bin(address)
        masked_binstring = list( map( compare_bits_v2, mask, bin_string ) )

        # Get the positions of the Xs
        x_positions = [ ii for ii in range(0, len(masked_binstring))
                        if masked_binstring[ii] == 'X' ]
        
        # Now generate all the combos for the required number of Xs
        combo_list = get_bit_combos(len(x_positions))
        
        for combo in zip(*combo_list):
            
            #For every combo, replace the Xs with the combo values
            for bit_val, pos in zip(combo, x_positions):
                masked_binstring[pos] = bit_val
            
            #Finally convert the binary array back into an integer
            mem_position = int(''.join( masked_binstring ), base = 2)
            
            memory[mem_position] = value
                
print(sum(memory.values()))  
