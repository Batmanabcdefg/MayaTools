from maya_testing.lib import general
from maya_testing.lib import errors
import os


def get_diff(file1=None, file2=None):
    '''Given two snapshot files, return the diff as a dictionary

    File format: attr:value:type
    Dict: {'attr': [value1, value2]}

    Attributes:
        file1 -- Full path to snapshot file1. str
        file2 -- Full path to snapshot file2. str
    '''
    general.check_type(file1, 'file1', [str])
    general.check_type(file2, 'file2', [str])

    if not os.path.exists(file1):
        raise errors.InputError('file1', file1, 'File does not exist.')
    if not os.path.exists(file2):
        raise errors.InputError('file2', file2, 'File does not exist.')

    try:
        f1 = open(file1, 'r')
        f1_lines = f1.readlines()
    except Exception, e:
        raise Exception(e)
    finally:
        f1.close()

    try:
        f2 = open(file2, 'r')
        f2_lines = f2.readlines()
    except Exception, e:
        raise Exception(e)
    finally:
        f2.close()

    f1_lines.sort()
    f2_lines.sort()

    result = {}
    for l1, l2 in zip(f1_lines, f2_lines):
        elems1 = l1.split(':')
        elems2 = l2.split(':')

        if elems1[0] != elems2[0]:
            raise errors.InputError('Input files',
                                    [elems1[0], elems2[0]],
                                    'Attribute mismatch in files.')

        if elems1[1] != elems2[1]:
            result[elems1[0]] = [elems1[1], elems2[1]]

    return result
