# import socket programming library 
import socket
import requests
import nltk
import random
from bs4 import BeautifulSoup
  
# import thread module 
from _thread import *
import threading 
  
def get_ingredients(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    ingredients = soup.findAll("span", {"class": "recipe-ingred_txt added"})
    ing_list = [item.text.lower() for item in ingredients]
    #print(ing_list)
    return ing_list

# def get_recipe(url):
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text, 'lxml')

#     recipe = soup.findAll("span", {"class": "recipe-directions__list--item"})
#     recipe_steps = [item.text.lower() for item in recipe]
#     #print(ing_list)
#     return recipe_steps

def get_search(pantry):
    search = ""
    meats = ['steak','chicken','pork','beef','lamb','turkey']
    meats_in_pantry = list(set(pantry).intersection(set(meats)))
    random.shuffle(meats_in_pantry)
    if (not len(meats_in_pantry) == 0):
        search += meats_in_pantry[0]
    return search

def get_reccomendation(pantry, search):
    print(f"Searching for recipes with {search}...")
    url = "https://www.googleapis.com/customsearch/v1"
    exact = "recipe"
    querystring = {"key": "AIzaSyDZUfQlDisHb2oYpJxwHLUjXA9qC7Zhqoo",
                   "cx": "009003825059138050829:hczen1dhoxr", "q": search, "exactTerms": exact}

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
    #print(response)
    output = []
    recipes = []
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
            continue
        else:
            name = name.replace("- Allrecipes.com", "").strip()
            #print("have every ingredient for", name)
            #print(ing_list)
            output.append({"name": name, "url": url})
            #for step in recipe:
            #    print(step)
            recipes.append(name)
    print(f"Found recipes: {recipes}")
    return output
  

# thread function 
def on_new_client(client_socket):
    pantry = []

    while True: 
  
        # data received from client 
        data = client_socket.recv(8192)
        if not data:
            print('Bye') 
            
            # lock released on exit 
            #print_lock.release() 
            break

        pantry_str = str(data.decode('ascii'))
        pantry = eval(pantry_str)
        search = get_search(pantry)
        recipes = get_reccomendation(pantry, search)

        data = str(recipes)
        client_socket.sendall(data.encode('ascii','ignore'))

    # connection closed 
    client_socket.close()
  
  
def Main(): 
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)
    print("Hostname :  ", host_name)
    print("IP : ", host)
    port = 5056
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to port", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 
  
    # a forever loop until client wants to exit 
    while True: 
  
        # establish connection with client 
        c, addr = s.accept() 
  
        # lock acquired by client 
        #print_lock.acquire() 
        print('Connected to :', addr[0], ':', addr[1]) 
  
        # Start a new thread and return its identifier 
        start_new_thread(on_new_client, (c,))
    s.close() 
  
  
if __name__ == '__main__': 
    Main() 
