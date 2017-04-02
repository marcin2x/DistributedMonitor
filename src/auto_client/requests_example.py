import requests


# usage examples:
root = 'https://jsonplaceholder.typicode.com'

response = requests.get(root + '/posts/1')
print(response.status_code is 200)
print(response.json())

payload = {'userId': 1, 'title': 'Lorem ipsum dolor sit amet enim.', 'body': 'Etiam ullamcorper.'}
response = requests.post(root + '/posts', payload)
print(response.status_code is 201)
print(response.json())

payload = {'title': 'Vestibulum dapibus, mauris nec malesuada fames ac turpis velit.'}
response = requests.put(root + '/posts/1', payload)
print(response.status_code is 200)
print(response.json())

response = requests.delete(root + '/posts/3')
print(response.status_code is 200)
