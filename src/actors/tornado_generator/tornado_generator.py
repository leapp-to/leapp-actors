import json

params = {}
with open('output2', 'r') as f:
    params = json.load(f)

for elem in params:
    print(elem)
