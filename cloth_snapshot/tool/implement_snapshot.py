import pymel.core as pm
from maya_testing.lib import general
from maya_testing.lib import errors
import os


def get_dict(snapshot=None):
    '''Given a full path to a snapshot file,
    set the selected node to the values in the snapshot.

    Attributes:
        snapshot -- Full path to a snapshot file. str
    '''
    general.check_type(snapshot, 'snapshot', [str])

    if not os.path.exists(snapshot):
        raise errors.InputError('snapshot', snapshot, 'File does not exist.')

    lines = []
    try:
        f = open(snapshot, 'r')
        lines = f.readlines()
    except Exception, e:
        raise Exception(e)
    finally:
        f.close()

    d = {}
    for line in lines:
        elems = line.split(':')
        typ = elems[2].split("'")[1]
        if typ == 'int':
            value = int(elems[1])
        elif typ == 'float':
            value = float(elems[1])
        elif typ == 'tuple':
            value = []
            for e in elems[1][1:-1].split(','):
                try:
                    value.append(float(e))
                except:
                    value.append(e)
            value = tuple(value)
        d[elems[0]] = value

    return d


def apply_dict(node=None, d=None):
    '''Given dictionay d, apply values to attributes of node

    d format: {'aatribute': 'value'}

    Attributes:
        node -- Node to apply values to. nt.Transform | nt.Nucleus
        d -- Dictionary of attributes, values
    '''
    general.check_type(node, 'node', [pm.nt.Transform, pm.nt.Nucleus])
    general.check_type(d, 's', [dict])

    for attr in d.keys():
        try:
            a = getattr(node, attr)
            a.set(d[attr])
        except Exception, e:
            raise Exception(e)
