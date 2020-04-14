from requests import get

print(get('http://localhost:8080/api/news').json())

print(get('http://localhost:8080/api/v2/news/2').json())

print(get('http://localhost:8080/api/v2/news').json())