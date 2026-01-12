import requests

url = "https://jsonplaceholder.typicode.com/posts/1"
data = {
    "title": "Gaurav", 
    "body": " a python developer",
    "userId": 12,
}

headers = {
    "Content-type": "application/json; charset=UTF-8"   
}

resopnse = requests.put(url, json=data, headers=headers)

print(resopnse.text)

