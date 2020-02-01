import requests

url = "https://www.googleapis.com/customsearch/v1"
search = "egg bacon cheese"
exact = "recipe"
querystring = {"key":"AIzaSyCOG5b5tRmXEmYSVZ0FwYLR1HouvyarI_E","cx":"008669644236061868694:5xhevflblhu","q":search,"exactTerms":exact}

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
print(type(response))
for item in response['items']:
    print(item['title'])
    print(item['link'])
    print()
