from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup
import random
from pymongo import MongoClient
#import main_execution

app = Flask(__name__)

my_pantry = []

def update_local_pantry():
    client = MongoClient("mongodb+srv://test:test@cluster0-3puyg.mongodb.net/test?retryWrites=true&w=majority")

    db = client.get_database('test_pantry')
    pantry = db.food_items
    print(pantry)
    pantry_items = list(pantry.find())

    for item in pantry_items:
        if item['name'] not in my_pantry:
            my_pantry.append(item['name'])

    print(my_pantry)

def get_ingredients(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    ingredients = soup.findAll("span", {"class": "recipe-ingred_txt added"})
    ing_list = [item.text.lower() for item in ingredients]
    #print(ing_list)
    return ing_list

def get_search():
    search = ""
    #meats is a good starting metric/test
    meats = ['steak','chicken','pork','beef','lamb','turkey']
    meats_in_pantry = list(set(my_pantry).intersection(set(meats)))
    random.seed()
    random.shuffle(meats_in_pantry)
    if (not len(meats_in_pantry) == 0):
        search += meats_in_pantry[0]
    #print("chosen search protein:", search)
    return search

@app.route('/get-reccomendation/')
def get_reccomendation():
    search = get_search()
    #start = 1
    print(f"Searching for recipes with {search}...")
    output = []
    start = 1
    while output == [] and start < 100:
        output = get_option(start, search)
        #output.append(single_output)
        start += 10
    if output is None:
        output = get_option(1, "bacon eggs cheese")

    return """<html>
    <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Lemon" />
    <head>
    <script type="text/javascript">
    function load()
    {
    window.location.href = ' """ + output + """ ';

    }
    </script>
    </head>

    <body onload="load()">
    <h1 style="padding: 10%"> ... loading your custom recipe ... </h1>
    </body>
    </html> """

def get_option(start, search):
    url = "https://www.googleapis.com/customsearch/v1"
    #search = "egg bacon cheese"
    exact = "recipe"
    output = []
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
    response = response.json()
    #print(type(response))
    for item in response['items']:
        name = item['title']
        #print(name)
        url = item['link']
        #print(url)
        ing_list = get_ingredients(url)
        num_ing = len(ing_list)
        matches = 0
        for item in my_pantry:
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
                #recipe = get_recipe(url)
                output.append({"name": name, "url": url})
                #recipe_chosen = True
            #for step in recipe:
            #    print(step)
    #print(output)
    #return output
    #    return None
    #break #delete this break to loop through multiple, just for testing
    random.shuffle(output)
    if len(output) > 0:
        url = output[0]["url"]
        return url
    return None


    #return None
    #break #delete this break to loop through multiple, just for testing

#probably dont need this
@app.route('/')
def index():
    return render_template('template.html')

@app.route('/scan-submission/')
def scan_submission():
    return render_template('scan_submission.html')
    #return "hello world"

@app.route('/print-pantry/', methods=['POST'])
def print_pantry():
    #must return a string or a redirect
    #return my_pantry
    update_local_pantry()
    return " ".join([item for item in my_pantry])

@app.route('/add-items/', methods = ['POST'])
def add_items():

    food = request.form['food']
    #print(name, number)
    #main_execution.add_user(name, number)
    client = MongoClient("mongodb+srv://test:test@cluster0-3puyg.mongodb.net/test?retryWrites=true&w=majority")

    db = client.get_database('test_pantry')
    pantry = db.food_items

    #check if item in dictionary and update quantitiy
    if len(list(pantry.find({'name': food}))) > 0:
        item_to_update = list(pantry.find({'name':food}))
        print(item_to_update)
        print(item_to_update[0]['quantity'])
        quantity = item_to_update[0]['quantity'] + 1
        updated = {'quantity': quantity}
        pantry.update_one({'name':food}, {'$set':updated})
    else:
        update_item = {"name": food, "quantity": 1}
        pantry.insert_one(update_item)

    #pantry.append(food)
    #print(pantry)
    update_local_pantry()
    return redirect('/scan-submission/')

@app.route('/display-database/')
def display_database():
    html_final = """
    <!DOCTYPE html>
    <html lang=en>
      <head>
        <title>My Pantry</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Lemon" />
      </head>

      <body>

        <table style="margin-left:10%;width:80%; border: solid 2px black">
          <tr style = "border: solid 2px black">
            <th style="border-right: dotted 1px black">Food Item</th>
            <th> Quantity </th>
          </tr>"""
    client = MongoClient("mongodb+srv://test:test@cluster0-3puyg.mongodb.net/test?retryWrites=true&w=majority")

    db = client.get_database('test_pantry')
    pantry = db.food_items
    pantry_items = list(pantry.find())
    for item in pantry_items:
        html = """
        <tr>
          <td style="border-right: dotted 1px black">""" + item['name'] + """</td>
          <td> """ + str(item['quantity']) + """ </td>
        </tr>"""
        html_final+= html
    html_final += """</table></body></html>"""

    return html_final


if __name__ == '__main__':
    #main_execution.initialize_database()
    update_local_pantry()
    app.run(host='0.0.0.0', debug=True)
