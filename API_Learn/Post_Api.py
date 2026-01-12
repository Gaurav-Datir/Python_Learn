import requests

url = "https://jsonplaceholder.typicode.com/posts"

data = {
    "title": "Gaurav", 
    "body": " a python developer",
    "userId": 12,
} 

headers = {
    "Content-type": "application/json; charset=UTF-8"   
}

resopnse = requests.post(url, json=data, headers=headers)

print(resopnse.text)