import requests
from bs4 import BeautifulSoup
import random

pantry = ['chicken', 'pork', 'steak', 'cream cheese','bacon', 'eggs', 'olive oil', 'cheddar cheese', 'salt', 'pepper', 'milk', 'butter', 'green onions', 'spinach', 'pimento', 'dough']

def get_search():
    search = ""
    meats = ['steak','chicken','pork','beef','lamb','turkey']
    meats_in_pantry = list(set(pantry).intersection(set(meats)))
    random.seed()
    random.shuffle(meats_in_pantry)
    if (not len(meats_in_pantry) == 0):
        search += meats_in_pantry[0]
    #print("chosen search protein:", search)
    return search

def get_ingredients(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    ingredients = soup.findAll("span", {"class": "recipe-ingred_txt added"})
    ing_list = [item.text.lower() for item in ingredients]
    #print(ing_list)
    return ing_list

def get_recipe(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    recipe = soup.findAll("span", {"class": "recipe-directions__list--item"})
    recipe_steps = [item.text.lower() for item in recipe]
    #print(ing_list)
    return recipe_steps
def get_reccomendation(start, search):
    url = "https://www.googleapis.com/customsearch/v1"
    #search = "egg bacon cheese"
    exact = "recipe"
    output = []
    #recipe_chosen = False
    #while(not recipe_chosen):
    querystring = {"key":"AIzaSyBq6hUhfOp-4e3OkajA3vSvpScPbjFkU14","cx":"008669644236061868694:5xhevflblhu","q":search,"exactTerms":exact, "start":start}

    headers = {
        'User-Agent': "PostmanRuntime/7.17.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "9858fb58-0434-47f1-9582-e37df8b1258e,989b61c7-1892-450c-9e35-d73c24e4b1c0",
        'Host': "www.googleapis.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response)

    response = response.json()
    #print(type(response))
    #next_start = response['queries']['nextPage'][0]['startIndex']
    #print("next start index:", next_start)
    #start = next_start
    for item in response['items']:
        name = item['title']
        #print(name)
        url = item['link']
        print(url)
        #print(url)
        ing_list = get_ingredients(url)
        print(ing_list)
        num_ing = len(ing_list)
        matches = 0
        for item in pantry:
            for ing in ing_list:
                #print(item, ing)
                if item in ing:
                    matches += 1
                    #print("there was a match!")

        if num_ing < 1:
            print("no ingredients found for", name, ", invalid recipe")
            print()

        else:
            if num_ing - matches > 2:
                print("missing", num_ing-matches, " ingredients for", name)
                print()
            else:
                name = name.replace("- Allrecipes.com", "")
                print("have almost every ingredient for", name)
                print(ing_list)
                recipe = get_recipe(url)
                output.append({"name": name, "url": url})
                recipe_chosen = True
            #for step in recipe:
            #    print(step)
    print(output)
    return output
    #    return None
    #break #delete this break to loop through multiple, just for testing

search = get_search()
#start = 1
print(f"Searching for recipes with {search}...")
output = []
start = 1
while output == [] and start < 100:
    output = get_reccomendation(start, search)
    #output.append(single_output)
    start += 10

print("FINAL OUTTPUT:")
print(output)
