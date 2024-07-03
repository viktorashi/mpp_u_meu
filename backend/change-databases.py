import json
import pandas as pd
import csv
import re
from collections import Counter


#change the file to only contain the name, category, atomic_number, appearance, discovered_by, named_by, phase, bohr_model_image and summary of the elements
def convert_dicts_to_tuples():
    file = json.load(open('app/static/periodic-table.json','r'))
    new_data = []
    for item in file:
        new_item = (
            item['name'],
            item['category'],
            item['number'],
            item['appearance'],
            item['discovered_by'],
            item['named_by'],
            item['phase'],
            item['bohr_model_image'],
            item['summary'],
            item['symbol']
        )
        new_data.append(new_item)
    print(new_data)
    #write the new data to the file, overwriting the old data

    with open('app/static/periodic-table.json', 'w') as file:
        json.dump(new_data, file, indent=4)

def parse_formula(formula):
    # Regular expression to match elements and their counts
    element_pattern = re.compile(r'([A-Z][a-z]{0,2})(\d*)')

    # Find all matches in the formula
    matches = element_pattern.findall(formula)
    
    # Create a list to store elements considering their counts
    elements = []
    
    for (element, count) in matches:
        if count == '':
            count = 1
        else:
            count = int(count)
        elements.extend([element] * count)

    return elements

def most_common_element(formula):
    elements = parse_formula(formula)
    element_counts = Counter(elements)
    most_common = element_counts.most_common(1)
    return most_common[0] if most_common else None


def manipulate_molecules():
    elements = []
    with open('app/static/molecules.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            formula = row[0]
            primary_element = most_common_element(formula)
            elements.append(primary_element[0])
            # print(primary_element[0])
    # print(elements)
    df = pd.read_csv('app/static/molecules.csv')
    df["primary_element"] = pd.Series(elements) 
    df.to_csv('app/static/molecules.csv', index=False, index_label=False)

def add_atiomic_number_of_primary_element():
    elements = json.load(open('app/static/periodic-table.json','r'))
    molecules = pd.read_csv('app/static/molecules.csv')
    for index, row in molecules.iterrows():
        primary_element = row[2]
        for element in elements:
            if element[9] == primary_element:
                atomic_number = element[2]
                #this writes them with a float, so we need to convert them to int
                #it dont work it still writes them as a float

                molecules.at[index, 'atomic_number'] = int(atomic_number)
    molecules.to_csv('app/static/molecules.csv', index=False, index_label=False)

# manipulate_molecules()

# convert_dicts_to_tuples()

# add_atiomic_number_of_primary_element()