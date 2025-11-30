# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 18:44:12 2020

@author: Lucio
"""

with open('inputs/day6.txt') as file:
    groups = []
    group_answers = []
    file_lines = file.readlines()
    how_many_lines = len(file_lines)
    for ii, line in enumerate(file_lines):
        if line != '\n':
            line = line.strip()
            line = {letter for letter in line}
            group_answers.append(line)
            
        if line == '\n' or (ii == (how_many_lines-1)):
            groups.append(group_answers)
            group_answers = []
 

yes_answers = []
intersected_yes = []
for group in groups:
    union_answers = set()
    for answers in group:
        union_answers = union_answers.union(answers)
        
    intersection_answers = set.intersection(*group)
    
    yes_answers.append( len(union_answers) )
    intersected_yes.append( len(intersection_answers) )
    
print(sum(yes_answers))
print(sum(intersected_yes))
