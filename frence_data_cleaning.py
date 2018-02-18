import json
import re


def save_to_json(dict, name):
    output = json.dumps(dict)
    f = open(name, 'w')
    f.write(output)
    f.close()
    return


f = open('./opinion_polling_french_presidential_election_2017.json')
d = json.load(f)

# Emmanuel Macron
# Marine Le Pen

tables = d['polling_data']

for table in tables:
    for key in list(table.keys()):
        if re.search('macron', key, re.IGNORECASE):
            table['Emmanuel Macron'] = table[key]
            del table[key]
        elif re.search('le pen', key, re.IGNORECASE):
            table['Marine Le Pen'] = table[key]
            del table[key]

d['polling_data'] = tables
save_to_json(d, 'cleaned_france_polling_2017.json')
