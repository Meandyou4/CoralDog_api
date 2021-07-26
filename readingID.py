import json
with open('labels.json') as f:
    data = json.load(f)

name_by_id = dict([(str(p['id']), p['breed']) for p in data])
id_by_name = dict([(p['breed'], p['id']) for p in data])

print(id_by_name['Akita'])