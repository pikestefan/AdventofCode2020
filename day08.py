# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 23:05:21 2020

@author: Lucio
"""

with open('inputs/day8.txt') as file:
    instructions = []
    numbers = []
    for line in file.readlines():
        line = line.strip()
        instruction, number = line.split(' ')
        instructions.append(instruction)
        numbers.append(int(number))


def run_init(instructions):
    how_many_instructions = len(instructions)
    visited = [False] * how_many_instructions
    
    idx = 0
    accumulator = 0
    
    keep_going = True
    while keep_going:
        
        instruction, number = instructions[idx], numbers[idx]
        
        if instruction == 'nop':
            new_index = 1
        elif instruction == 'acc':
            accumulator += number
            new_index = 1
        elif instruction == 'jmp':
            new_index = number
            
        visited[idx] = True
        
        idx += new_index
        
        if idx >= how_many_instructions:
            keep_going = False
            success = True
        elif visited[idx]:
            keep_going = False
            success = False
    return accumulator, success

accumulator, _ = run_init(instructions)
print(accumulator)
     
### Part two
idx = 0
accumulator = 0

keep_going = True
visited = [False] * len(instructions)
visited_second_time = [False] * len(instructions)

#Find the commands where it gets stuck in a loop
loop_commands = []
while keep_going:
    instruction, number = instructions[idx], numbers[idx]
    
    if instruction == 'nop':
        new_index = 1
    elif instruction == 'acc':
        accumulator += number
        new_index = 1
    elif instruction == 'jmp':
        new_index = number
        
    if visited[idx] and (instruction != 'acc'):
        visited_second_time[idx] = True
        loop_commands.append([idx, instruction])
    
    visited[idx] = True
    if visited[idx + new_index] and visited_second_time[idx + new_index]:
        keep_going = False
    else:
        idx += new_index
        
#Now change the a command and re-execute
for loop_command in loop_commands:
    try_instructions = instructions[:]
    
    try_ind, try_command = loop_command
    try_command = 'nop' if (try_command == 'jmp') else 'jmp'
    try_instructions[try_ind] = try_command
    
    accumulator, success = run_init(try_instructions)
    if success:
        break

