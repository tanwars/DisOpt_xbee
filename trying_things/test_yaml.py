import yaml

fname = './trying_things/param.yaml'

with open(fname,'r') as file:
    d = yaml.full_load(file)

    # for item, doc in d.items():
    #     print(item, ":", doc)

print(bytearray(d['Xbee']['pan_id'], 'utf-8'))

