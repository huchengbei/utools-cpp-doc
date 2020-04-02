def prase(filename):
    from xml.dom.minidom import parse
    dt = parse(filename)
    bl = dt.documentElement
    nodes = bl.childNodes
    file_list = []
    namespace_list = []
    class_list = []
    for node in nodes:
        if node.nodeName == 'compound'and node.hasAttribute('kind'):
            if node.getAttribute('kind') == 'file':
                node_info = node.childNodes
                info = {
                        'name': '',
                        'filename': '',
                        'namespace': ''
                }
                for item in node_info:
                    if item.nodeName == 'name':
                        if item.childNodes.length > 0:
                            info['name'] = item.childNodes[0].data
                    if item.nodeName == 'filename':
                        if item.childNodes.length > 0:
                            info['filename'] = item.childNodes[0].data
                    if item.nodeName == 'namespace':
                        if item.childNodes.length > 0:
                            info['namespace'] = item.childNodes[0].data
                if info['name'] != '' and info['filename'] != '':
                    file_list += [info]
            if node.getAttribute('kind') == 'namespace':
                node_info = node.childNodes
                info = {
                        'name': '',
                        'filename': '',
                        'functions': []
                }
                for item in node_info:
                    if item.nodeName == 'name':
                        if item.childNodes.length > 0:
                            info['name'] = item.childNodes[0].data
                    if item.nodeName == 'filename':
                        if item.childNodes.length > 0:
                            info['filename'] = item.childNodes[0].data
                if info['name'] != '':
                    for item in node_info:
                        if item.nodeName == 'member'and item.hasAttribute('kind'):
                            item_info = item.childNodes
                            function_info = {
                                    'name': '',
                                    'namespace_id': len(namespace_list) + 1,
                                    'class_id': '',
                                    'belong': 'namespace',
                                    'type': '',
                                    'anchorfile': '',
                                    'anchor': '',
                                    'arglist': ''
                            }
                            for item in item_info:
                                if item.nodeName == 'name':
                                    if item.childNodes.length > 0:
                                        function_info['name'] = item.childNodes[0].data
                                if item.nodeName == 'type':
                                    if item.childNodes.length > 0:
                                        function_info['type'] = item.childNodes[0].data
                                if item.nodeName == 'anchorfile':
                                    if item.childNodes.length > 0:
                                        anchorfile = item.childNodes[0].data
                                        pos = anchorfile.find('/')
                                        function_info['anchorfile'] = anchorfile[pos+1:]
                                if item.nodeName == 'anchor':
                                    if item.childNodes.length > 0:
                                        function_info['anchor'] = item.childNodes[0].data
                                if item.nodeName == 'arglist':
                                    if item.childNodes.length > 0:
                                        function_info['arglist'] = item.childNodes[0].data
                            info['functions'] += [function_info]
                    namespace_list += [info]

            if node.getAttribute('kind') == 'class':
                node_info = node.childNodes
                info = {
                        'name': '',
                        'filename': '',
                        'functions': []
                }
                for item in node_info:
                    if item.nodeName == 'name':
                        if item.childNodes.length > 0:
                            info['name'] = item.childNodes[0].data
                    if item.nodeName == 'filename':
                        if item.childNodes.length > 0:
                            info['filename'] = item.childNodes[0].data
                if info['name'] != '':
                    for item in node_info:
                        if item.nodeName == 'member'and item.hasAttribute('kind'):
                            item_info = item.childNodes
                            function_info = {
                                    'name': '',
                                    'namespace_id': '',
                                    'class_id': len(class_list) + 1,
                                    'belong': 'class',
                                    'type': '',
                                    'anchorfile': '',
                                    'anchor': '',
                                    'arglist': ''
                            }
                            for item in item_info:
                                if item.nodeName == 'name':
                                    if item.childNodes.length > 0:
                                        function_info['name'] = item.childNodes[0].data
                                if item.nodeName == 'type':
                                    if item.childNodes.length > 0:
                                        function_info['type'] = item.childNodes[0].data
                                if item.nodeName == 'anchorfile':
                                    if item.childNodes.length > 0:
                                        anchorfile = item.childNodes[0].data
                                        pos = anchorfile.find('/')
                                        function_info['anchorfile'] = anchorfile[pos+1:]
                                if item.nodeName == 'anchor':
                                    if item.childNodes.length > 0:
                                        function_info['anchor'] = item.childNodes[0].data
                                if item.nodeName == 'arglist':
                                    if item.childNodes.length > 0:
                                        function_info['arglist'] = item.childNodes[0].data
                            info['functions'] += [function_info]
                    class_list += [info]

    prase_data = {
            'file': file_list,
            'namespace': namespace_list,
            'class': class_list
    }

    return prase_data

def data2sql(table_name, fields, data):
    sql = "insert into " +  str(table_name) + ' ('  + ', '.join(fields) + ') values ' 
    values = tuple(data[item] for item in fields)
    return sql + str(values) + ';'

def prase2sql(filename):
    sqls = []
    prase_data = prase(filename)
    for item in prase_data['file']:
        fields = ('name', 'filename', 'namespace')
        sql = data2sql('file', fields, item)
        sqls += [sql]
    for item in prase_data['namespace']:
        fields = ('name', 'filename')
        sql = data2sql('namespace', fields, item)
        sqls += [sql]
        for info in item['functions']:
            fields = ('namespace_id', 'belong', 'type', 'name', 'anchorfile', 'anchor', 'arglist')
            sql = data2sql('function', fields, info)
            sqls += [sql]
    for item in prase_data['class']:
        fields = ('name', 'filename')
        sql = data2sql('class', fields, item)
        sqls += [sql]
        for info in item['functions']:
            fields = ('class_id', 'belong', 'type', 'name', 'anchorfile', 'anchor', 'arglist')
            sql = data2sql('function', fields, info)
            sqls += [sql]
    return sqls

def write2sql(filename, host, user, passwd, db):
    import MySQLdb
    from tqdm import tqdm
    sqls = prase2sql(filename)
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    cur = db.cursor()
    for sql in tqdm(sqls):
        cur.execute(sql)
    cur.close()
    db.commit()
    db.close()


if __name__ == '__main__':
    filename = r'cppreference-doxygen-local.tag.xml'
    fields = ('a', 'b')
    data = {'b': 1, 'a': 2}

    # print(data2sql('table', fields, data))
    # print(prase2sql(filename)[:10])
    var = 'cppreference'
    write2sql(filename, '127.0.0.1', var, var, var)

