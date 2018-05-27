
class InputError(Exception):
    '''Invalid argument data passed by caller of method

    Attributes:
        attr -- Attribute that raised error
        value -- Invalid data passed in
        expected -- Message: expected data
    '''
    def __init__(self, attr, value, expected):
        self.attr = attr
        self.value = value
        self.expected = expected

    def __str__(self):
        return "%s passed %s. Expected %s." % (self.attr,
                                               self.value,
                                               self.expected)


class BuildError(Exception):
    '''Something went wrong during build

    Attributes:
        method -- Name of method that raised the error
        msg -- Error message
    '''
    def __init__(self, method, msg):
        self.method = method
        self.msg = msg

    def __str__(self):
        return "%s(): %s" % (self.method, self.msg)


class ObjectError(Exception):
    '''Some aspect of passed in object is not as expected

    Attributes:
        obj -- Object that raised the error
        expected -- What was expected
        value -- Value found instead of expected
    '''
    def __init__(self, obj, expected, value):
        self.obj = obj
        self.expected = expected
        self.value = value

    def __str__(self):
        return "Object: %s Expecting: %s Got: %s" % (self.obj,
                                                     self.expected,
                                                     self.value)
