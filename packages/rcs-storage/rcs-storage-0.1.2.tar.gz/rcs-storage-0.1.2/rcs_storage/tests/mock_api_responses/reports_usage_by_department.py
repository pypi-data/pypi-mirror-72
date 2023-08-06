# Result from response = requests.get('.../api/reports/usage-by-department/')

# response.content
content = b'[{"date":"2020-06-12","used_gb":800.0,"department":"0000"},{"date":"2020-06-12","used_gb":50.0,"department":"9770"}]'

# response.json()
json = [{'date': '2020-06-12', 'used_gb': 800.0, 'department': '0000'}, {'date': '2020-06-12', 'used_gb': 50.0, 'department': '9770'}]
