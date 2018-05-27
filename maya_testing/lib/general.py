import errors
import pymel.core as pm
import logging


def logSetup(level='debug', name=None):
    '''Setup logging for this module

    Attributes:
        level -- Logging level for this module. Int
        name -- Name for log file. Str
    '''
    if level not in ['debug', 'info', 'warning', 'error', 'critical']:
        raise ValueError('Invalid log level: %s' % level)
    numeric_level = getattr(logging, level.upper(), None)

    if not isinstance(name, str):
        raise ValueError('Invalid log file name: %s' % name)

    logging.basicConfig(filename='transforms.log', level=numeric_level)

logSetup(level='info', name='general')


def check_type(obj=None, attr=None, types=[]):
    ''' Check an objects type

    Attributes:
        obj -- Object to check
        attr -- Attribute that object is passed into. String
        types -- List of types that obj needs to be
    '''
    for t in types:
        if isinstance(obj, t):
            return True
    raise errors.InputError(attr, type(obj), types)


def assertAlmostEquals(a=None, b=None, res=5, log=False):
    '''Compare two lists, element by element

    Attributes:
        a -- List a
        b -- List b
        res -- Resolution for rounding used for float comparisons. Int
    '''
    check_type(a, 'a', [list, pm.dt.Point, pm.dt.Vector])
    check_type(b, 'b', [list, pm.dt.Point, pm.dt.Vector])
    check_type(res, 'res', [int])

    if len(a) != len(b):
        return False

    for elem_a, elem_b in zip(a, b):
        if log:
            a_str = 'A: ', elem_a
            b_str = 'B: ', elem_b
            logging.debug(a_str)
            logging.debug(b_str)

        if isinstance(elem_a, list):
            if not assertAlmostEquals(elem_a, elem_b):
                if log:
                    logging.debug('Fail')
                return False
            else:
                continue

        elif isinstance(elem_a, float):
            if round(elem_a, res) == round(elem_b, res):
                continue
            else:
                if log:
                    logging.debug('Fail')
                return False

        elif isinstance(elem_a, int):
            if elem_a == elem_b:
                continue
            else:
                if log:
                    logging.debug('Fail')
                return False

        elif isinstance(elem_a, str):
            if elem_a == elem_b:
                continue
            else:
                if log:
                    logging.debug('Fail')
                return False

        else:
            if log:
                logging.debug('Fail')
            return False

    if log:
        logging.debug('Pass')
    return True
