import os
import json

os.chdir('fixtures/new')

f = open('nodes.json')

data = json.load(f)

new_nodes = []

KNOW = 'KN'
UNDERSTAND = 'UN'
CASES = 'CS'
SKILLS = 'SK'

for n in data:
    fields = n['fields']
    del (fields['eng_title'])

    if fields['type'] == 1:
        fields['type'] = KNOW
    elif fields['type'] == 2:
        fields['type'] = UNDERSTAND
    elif fields['type'] == 3:
        fields['type'] = CASES
    elif fields['type'] == 4:
        fields['type'] = SKILLS

    new_node = {
        "model": "graph.node",
        'pk': n['pk'],
        'fields': fields
    }

    new_nodes.append(new_node)

json_string = json.dumps(new_nodes)

with open('nodes_new).json', 'w') as outfile:
    outfile.write(json_string)
