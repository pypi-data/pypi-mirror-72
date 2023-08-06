# Result from response = requests.options('.../api/collections/')

# response.content
content = b'{"name":"Collection List","description":"","renders":["application/json"],"parses":["application/json","application/x-www-form-urlencoded","multipart/form-data"]}'

# response.json()
json = {'name': 'Collection List', 'description': '', 'renders': ['application/json'], 'parses': ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']}
