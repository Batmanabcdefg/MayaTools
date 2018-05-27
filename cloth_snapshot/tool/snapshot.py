from datetime import datetime
import pymel.core as pm
from maya_testing.lib import general
from maya_testing.lib import errors
import os


def take_snapshot(path=None):
    '''Create snapshot file for selected nodes in given path.

    Attributes:
        path -- Path to create snapshot file. str
        node -- Node to create snapshot for. nt.Transform
        typ -- Type of node. ncloth | nucleus. str
    '''
    general.check_type(path, 'path', [str])
    typs = ['transform',
            'nucleus']
    results = []
    nodes = pm.ls(sl=1)

    for node in nodes:
        typ = node.type()
        msg = ('Node: %s is of invalid type: %s' % (node, typ))
        if typ not in typs:
            pm.warning(msg)

        if typ == 'transform':
            typ = 'ncloth'
        elif typ == 'nucleus':
            typ = 'nucleus'
        else:
            pm.warning(msg)

        d = make_dict(node, typ)
        name = gen_filename(node)

        full_name = path + os.sep + name
        make_file(str(full_name), d)

        results.append('Created: %s' % full_name)
    return results


def make_dict(node=None, typ=None):  # dict: {'attr':value}
    '''Make a dictionary for the given node attributes and values.
    Expects to find: nucleus_attrs.txt or ncloth_attrs.txt file
    in directory this py file is in.

    Attributes:
        node -- Node. nt.Transform
        typ -- Type of node. ncloth | nucleus. str
    '''
    general.check_type(node, 'node', [pm.nt.Transform, pm.nt.Nucleus])
    general.check_type(typ, 'typ', [str])

    if typ not in ['ncloth', 'nucleus']:
        raise errors.InputError(typ, 'typ',
                                'Must be either: ncloth or nucleus')

    if typ == 'ncloth':
        fileName = os.path.dirname(__file__) + os.sep + 'ncloth_attrs.txt'
    elif typ == 'nucleus':
        fileName = os.path.dirname(__file__) + os.sep + 'nucleus_attrs.txt'

    if not os.path.exists(fileName):
        msg = 'File not found: ', fileName
        raise IOError(msg)

    f = open(fileName, 'r')
    attrs = f.readlines()
    f.close()

    d = {}
    if typ == 'ncloth':
        shape = node.getShape()
    elif typ == 'nucleus':
        shape = node

    for attr in attrs:
        attr = attr.strip()
        d[attr] = getattr(shape, attr).get()

    return d


def gen_filename(node=None):
    '''Given Transform node, generate a file name for a snapshot

    Format: nodeName_yyyy_mm_dd_hh_mm

    Attributes:
        node -- Transform node. nt.Transform
    '''
    general.check_type(node, 'node', [pm.nt.Transform, pm.nt.Nucleus])

    now = datetime.now()

    return node.name() + '_' + \
        str(now.year) + '-' + str(now.month) + '-' + \
        str(now.day) + '_' + \
        str(now.hour) + '-' + str(now.minute) + '.txt'


def make_file(name=None, data=None):
    '''Make a snapshot file from a given dictionary

    Format: AttributeName:value:type

    Attributes:
        name -- Full path + name for snapshot file. str
        data -- Dictionary: {'attr': value}
    '''
    general.check_type(name, 'name', [str])
    general.check_type(data, 'data', [dict])

    lines = []
    for key in data.keys():
        lines.append(str(key) + ':' +
                     str(data[key]) + ':' +
                     str(type(data[key])) + '\n')

    if not os.path.exists(os.path.dirname(name)):
        raise errors.InputError(name, 'name', 'Path does not exist.')

    try:
        f = open(name, 'w')
        f.writelines(lines)
    except Exception, e:
        raise Exception(e)
    finally:
        f.close()
