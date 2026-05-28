import json

inp = open('full_eln_file.json')

data = json.load(inp)
newgraph = []

for j in range(len(data['@graph'])):
    d = data['@graph'][j]
    if 'hasPart' in d.keys():
        for f in range(len(d['hasPart'])):
            for i in range(len(data['@graph'])):
                if (
                    data['@graph'][len(data['@graph']) - 1 - i]['@id']
                    == d['hasPart'][f]['@id']
                ):
                    data['@graph'][j]['hasPart'][f] = data['@graph'][
                        len(data['@graph']) - 1 - i
                    ]
    if 'variableMeasured' in d.keys():
        for f in range(len(d['variableMeasured'])):
            for i in range(len(data['@graph'])):
                if (
                    data['@graph'][len(data['@graph']) - 1 - i]['@id']
                    == d['variableMeasured'][f]['@id']
                ):
                    data['@graph'][j]['variableMeasured'][f] = data['@graph'][
                        len(data['@graph']) - 1 - i
                    ]
    if 'mentions' in d.keys():
        for f in range(len(d['mentions'])):
            for i in range(len(data['@graph'])):
                if (
                    data['@graph'][len(data['@graph']) - 1 - i]['@id']
                    == d['mentions'][f]['@id']
                ):
                    data['@graph'][j]['mentions'][f] = data['@graph'][
                        len(data['@graph']) - 1 - i
                    ]
    if d['@id'] == './':
        newgraph.append(data['@graph'][j])

data['@graph'] = newgraph

json.dump(data, open('testdump.json', 'w'))
