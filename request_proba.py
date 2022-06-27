import json
import requests

# r = requests.get('http://127.0.0.1:5000/people')
# r.text
# print(r.text)
# print(r.json())

# payload = {'first_name': 'Adam', 'last_name': 'Kovacs', 'email': 'kovacs.adam@example.com'}
# r = requests.post('http://127.0.0.1:5000/people', json=payload)

payload = {'first_name': 'pETER', 'last_name': 'Kovacs', 'email': 'kovacs.PETER@example.com'}
r = requests.post('http://127.0.0.1:5000/people', data=json.dumps(payload),
                  headers={'Content-Type': 'application/json'})
print(r.status_code)
print(r.text)

r2 = requests.get('http://127.0.0.1:5000/people')
r2.text
print(r2.text)
