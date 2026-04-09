import json
import numpy as np


def main(temp_json, heating_json, rules_json, current_temp):
    temp_data = json.loads(temp_json)
    heating_data = json.loads(heating_json)
    rules = json.loads(rules_json)
    
    temp_terms = {term['id']: term['points'] for term in temp_data['температура']}
    heating_terms = {term['id']: term['points'] for term in heating_data['температура']}
    
    def membership_degree(value, points):
        points = sorted(points, key=lambda p: p[0])
        
        if value <= points[0][0]:
            return points[0][1]
        if value >= points[-1][0]:
            return points[-1][1]
        
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            if x1 <= value <= x2:
                if x2 == x1:
                    return y1
                return y1 + (y2 - y1) * (value - x1) / (x2 - x1)
        
        return 0.0
    
    input_memberships = {}
    for term_id, points in temp_terms.items():
        input_memberships[term_id] = membership_degree(current_temp, points)
    
    output_memberships = {}
    for rule in rules:
        if len(rule) >= 2:
            input_term = rule[0] 
            output_term = rule[1]  
            
            activation = input_memberships.get(input_term, 0.0)
            
            if output_term not in output_memberships:
                output_memberships[output_term] = activation
            else:
                output_memberships[output_term] = max(output_memberships[output_term], activation)
    
    numerator = 0.0
    denominator = 0.0
    
    all_x = []
    for points in heating_terms.values():
        for point in points:
            all_x.append(point[0])
    
    x_min, x_max = min(all_x), max(all_x)
    
    num_points = 1000
    x_range = np.linspace(x_min, x_max, num_points)
    
    for x in x_range:
        aggregated_membership = 0.0
        
        for term_id, activation in output_memberships.items():
            if term_id in heating_terms:
                term_membership = membership_degree(x, heating_terms[term_id])
                clipped_membership = min(activation, term_membership)
                aggregated_membership = max(aggregated_membership, clipped_membership)
        
        numerator += x * aggregated_membership
        denominator += aggregated_membership
    
    if denominator == 0:
        return (x_min + x_max) / 2
    
    return numerator / denominator
