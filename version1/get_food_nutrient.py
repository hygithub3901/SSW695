import requests
import json

def call_API(foodName, apiKey):
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={apiKey}&query={foodName}&requireAllWords=True'
    res = requests.get(url)
    print(res.status_code)
    return res.json()

def obtain_energy(foodNutrientlist):
    energy = 0
    for i in foodNutrientlist:
        if i['nutrientName'] == 'Energy':
            energy = i['value']
    return energy

def format_food(foodname,foodCategory,foodNutrientList):
    protein = 0
    fat = 0
    carbohydrate = 0
    energy = 0
    sugre = 0 
    va = 0
    vc = 0
    for i in foodNutrientList:
        if i['nutrientName'] == 'Protein':
            protein = i['value']

        if i['nutrientName'] == 'Total lipid (fat)':
            fat = i['value']

        if i['nutrientName'] == 'Carbohydrate, by difference':
            carbohydrate = i['value']

        if i['nutrientName'] == 'Energy':
            energy = i['value']

        if i['nutrientName'] == 'sugre':
            sugre = i['value']
        
        if i['nutrientName'] == 'va':
            va = i['value']
        
        if i['nutrientName'] == 'vc':
            vc = i['value']

    data = {
        'foodName': foodname,
        'foodType': foodCategory,
        'protein': protein,
        'fat':fat,
        'carbohydrate':carbohydrate,
        'energy':energy,
        'sugar':sugre,
        'va':va,
        'vc':vc,
    }
    return data