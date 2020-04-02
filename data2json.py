import os
from prase import prase
import json

def data2json(base_url, data):
    jsondata = []
    for item in data['file']:
        jsondata += [{
            't': '<' + item['name'] + '>',
            'd': str(item['namespace']) + '::' + str(item['name']),
            'p': os.path.join(base_url, str(item['filename']) + '.html')
            }]

    for item in data['class']:
        jsondata += [{
            't': item['name'],
            'd': str(item['name']),
            'p': os.path.join(base_url, str(item['filename']) + '.html')
            }]
        for function in item['functions']:
            jsondata += [{
                't': function['name'],
                'd': str(item['name']) + '::' + str(function['name']),
                'p': os.path.join(base_url, str(function['anchorfile']))
                }]

    for item in data['namespace']:
        for function in item['functions']:
            jsondata += [{
                't': function['name'],
                'd': str(item['name']) + '::' + str(function['name']),
                'p': os.path.join(base_url, str(function['anchorfile']))
                }]

    return jsondata


if __name__ == '__main__':
    filename = 'cppreference-doxygen-local.tag.xml'
    data = prase(filename)

    base_url = 'reference/zh'
    jsondata = data2json(base_url, data)
    with open('public/indexes-cn.json', 'w') as f:
        json.dump(jsondata, f)

    base_url = 'reference/en'
    jsondata = data2json(base_url, data)
    with open('public/indexes-en.json', 'w') as f:
        json.dump(jsondata, f)
    print('write json completed')

