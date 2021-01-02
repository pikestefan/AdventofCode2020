# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 04:29:48 2020

@author: Lucio
"""

import re

def find_intersection(allergen, food_list, allergen_list):
    ingredients_per_allergen = []
    for ingredients, allergen_in_food in zip( food_list, allergen_list ):
        if allergen in allergen_in_food:
            ingredients_per_allergen.append(set(ingredients))
    intersection_per_allergen = set.intersection( * ingredients_per_allergen )
    
    return intersection_per_allergen

def remove_from_list_of_lists(element, list_of_lists):
    
    new_list = []
    for row in list_of_lists:
        new_row = [ item for item in row if item != element ]
        new_list.append(new_row)
    return new_list
    
    
with open('inputs/day21.txt') as file:
    
    food_list = []
    allergen_list = []
    
    for line in file.readlines():
        line = line.strip().split(' (')
        ingredients = line[0].split(' ')
        allergens = line[-1].replace('contains ','').replace(')','')
        allergens = allergens.split(', ')
        
        food_list.append( ingredients ) 
        allergen_list.append( allergens )
        
    flattened_allergens = []
    for listy in allergen_list:
        flattened_allergens += listy
        
    flattened_ingredients = []
    for listy in food_list:
        flattened_ingredients += listy
        
    unique_allergens = list(dict.fromkeys(flattened_allergens))
    unique_ingredients = list(dict.fromkeys(flattened_ingredients))

### Part 1
intersection_foods = [] 
for allergen in unique_allergens:
    
    all_intersec = find_intersection(allergen, food_list, allergen_list)
    intersection_foods.append(all_intersec)
    
food_w_allergens = set.union( *intersection_foods )    

without_allergens = [ingredient for ingredient in unique_ingredients
                     if not ingredient in food_w_allergens]

no_allergen_counter = 0
for ingredient in flattened_ingredients:
    
    if ingredient in without_allergens:
        no_allergen_counter += 1
print(no_allergen_counter)

### Part 2
food_list_for_id = food_list[:]

#First remove the ingredients without allergens
for no_allergen in without_allergens:
    food_list_for_id = remove_from_list_of_lists(no_allergen, food_list_for_id)
           
# Now, identify the allergens
identified_foods = {}
allergens_to_identify = unique_allergens[:]
ii = 0
while len(allergens_to_identify) > 0:
    
    ii %= len(allergens_to_identify)
    
    allergen = allergens_to_identify[ii]
    intersy = find_intersection(allergen, food_list_for_id, allergen_list)
    
    if len(intersy) == 1:
        identified_food = list(intersy)[0]
        identified_foods[allergen] = identified_food
        food_list_for_id = remove_from_list_of_lists(identified_food, 
                                                     food_list_for_id)
        allergens_to_identify.remove(allergen)
        
    ii += 1
    
sorted_allergen = []
sorted_ingredient = []
for allergen, ingredient in  sorted(identified_foods.items()):
    sorted_allergen.append(allergen)
    sorted_ingredient.append(ingredient)
    
print(','.join(sorted_ingredient))
        
        
        

 