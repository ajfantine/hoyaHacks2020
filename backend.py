from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup
import random
#import main_execution

app = Flask(__name__)

pantry = ['cream cheese','bacon', 'eggs', 'olive oil', 'cheddar cheese', 'salt', 'pepper', 'milk', 'butter', 'green onions', 'spinach', 'pimento', 'dough']

def get_ingredients(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    ingredients = soup.findAll("span", {"class": "recipe-ingred_txt added"})
    ing_list = [item.text.lower() for item in ingredients]
    #print(ing_list)
    return ing_list

@app.route('/get-reccomendation/')
def get_reccomendation():
    url = "https://www.googleapis.com/customsearch/v1"
    search = "egg bacon cheese"
    exact = "recipe"
    querystring = {"key":"AIzaSyBq6hUhfOp-4e3OkajA3vSvpScPbjFkU14","cx":"008669644236061868694:5xhevflblhu","q":search,"exactTerms":exact}

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
    output = []
    #print(type(response))
    for item in response['items']:
        name = item['title']
        #print(name)
        url = item['link']
        #print(url)
        ing_list = get_ingredients(url)
        num_ing = len(ing_list)
        matches = 0
        for item in pantry:
            for ing in ing_list:
                #print(item, ing)
                if item in ing:
                    matches += 1
                    #print("there was a match!")

        if matches < num_ing:
            #print("missing", num_ing-matches, " ingredients for", name)
            pass
        else:
            name = name.replace("- Allrecipes.com", "")
            #print("have every ingredient for", name)
            #print(ing_list)
            #recipe = get_recipe(url)
            output.append({"name":name, "url":url})
            #for step in recipe:
            #    print(step)
    random.shuffle(output)
    url = output[0]["url"]
    return """<html>
    <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Lemon" />
    <head>
    <script type="text/javascript">
    function load()
    {
    window.location.href = ' """ + url + """ ';

    }
    </script>
    </head>

    <body onload="load()">
    <h1 style="padding: 10%"> ... loading your custom recipe ... </h1>
    </body>
    </html> """

    #return None
    #break #delete this break to loop through multiple, just for testing

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
    return redirect('')
    #return " ".join([item for item in pantry])

@app.route('/add-items/', methods = ['POST'])
def add_items():

    food = request.form['food']
    #print(name, number)
    #main_execution.add_user(name, number)
    pantry.append(food)
    print(pantry)
    return redirect('/scan-submission/')

if __name__ == '__main__':
    #main_execution.initialize_database()

    app.run(host='0.0.0.0', debug=True)
