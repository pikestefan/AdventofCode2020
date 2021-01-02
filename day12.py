# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 16:21:58 2020

@author: Lucio
"""

with open('inputs/day12.txt') as file:
    instructions = [ [inst[0], int(inst[1:])] for inst in file.readlines() ]
    
class ship:
    
    direction_list = ['N','E','S','W']
    
    def __init__(self):
        self.position = (0,0)
        self.direction = 'E'
        self.waypoint_position = (1, 10)
        
        self.waypoint_active = False
        
    def update_direction(self, angle):
        curr_position = self.direction_list.index(self.direction)
        
        turn_angle = angle // 90
        
        self.direction = self.direction_list[ (curr_position + turn_angle) % 4 ]
        
    def update_waypoint_position(self, angle):
        curr_ii, curr_jj = self.waypoint_position
        
        abs_angle = abs(angle)
        angle_sign = angle // abs_angle
        
        if abs_angle == 90:
            new_position = - angle_sign * curr_jj, angle_sign * curr_ii
            he=2
        elif abs_angle == 180:
            new_position = -curr_ii, -curr_jj
        elif abs_angle == 270:
            new_position = angle_sign * curr_jj, - angle_sign * curr_ii
            
        return new_position

    def instruction_parse(self, instruction):
        ii, jj = self.position
        
        command, amount = instruction
        
        if command == 'F':
            command = self.direction
        
        if command == 'N':
            ii += amount
        elif command == 'S':
            ii -= amount
        elif command == 'E':
            jj += amount
        elif command == 'W':
            jj -= amount
        elif command == 'R':
            self.update_direction(amount)
        elif command == 'L':
            self.update_direction(-amount)
            
        self.position = (ii, jj)
            
    def instruction_parse_wp(self, instruction):
        ii, jj = self.position
        
        wp_ii, wp_jj = self.waypoint_position
        
        command, amount = instruction
        
        if command == 'F':
            self.position = ii + wp_ii * amount, jj + wp_jj * amount

        else:
            if command == 'N':
                wp_ii += amount
            elif command == 'S':
                wp_ii -= amount
            elif command == 'E':
                wp_jj += amount
            elif command == 'W':
                wp_jj -= amount
            elif command == 'R':
                wp_ii, wp_jj = self.update_waypoint_position(amount)
            elif command == 'L':
                wp_ii, wp_jj = self.update_waypoint_position(-amount)
            self.waypoint_position = wp_ii, wp_jj
    
    def run_instructions(self, instruction_list):
        
        if self.waypoint_active:
            interpreter = self.instruction_parse_wp
        else:
            interpreter = self.instruction_parse
        
        for instruction in instruction_list:
            interpreter(instruction)       
            
    def get_m_distance(self):
        ii, jj = self.position
        return abs(ii) + abs(jj) 
    
    def reset(self):
        self.position = (0,0)
        self.direction = 'E'
        self.waypoint_position = (1, 10)
        
        self.waypoint_active = False

shippy = ship()

## Part 1
shippy.run_instructions(instructions)
print(shippy.get_m_distance())

## Part 2
shippy.reset()
shippy.waypoint_active = True
shippy.run_instructions(instructions)
print(shippy.get_m_distance())