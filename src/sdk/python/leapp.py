''' Leapp Python SDK '''

from json import dumps, load
from sys import stdin
from collections import defaultdict
from subprocess import check_output, Popen, CalledProcessError
from os import devnull


DEV_NULL = open(devnull, 'w')


class Severity(object):
    ''' Severity of event '''
    (Log, Debug, Fatal) = ['log', 'debug', 'fatal']


def bail(severity, message, data=None, code=-1):
    ''' End the execution and emit diagnostics message

        :param severity: Severity of the message
        :type severity:  Severity
        :param message:  Message to bail out with
        :type message:   str
        :param data:     Additional structured data
        :type data:      dict
        :param code:     Error code to exit with
        :type code:      int
    '''
    print(dumps({'errors':
                 {
                     'source': {
                         'severity': severity,
                         'message': message,
                         'data': data
                     }
                 }
                 }))
    exit(code)


def get_value(obj, pathspec, default=None, strict=False):
    ''' Get value from `obj` as defined by `pathspec`

        TODO: Decide about `strict` and exception throwing here in general
    '''
    if '.' not in pathspec and pathspec not in obj:
        if strict:
            raise ValueError('pathspec: "{}" is invalid'.format(pathspec))
        return default

    bound = obj
    for item in pathspec.split('.'):
        if item in bound:
            bound = bound[item]
        else:
            if strict:
                raise ValueError('pathspec: "{}" is invalid'.format(pathspec))
            return default

    return bound


def get_items(obj, *items):
    ''' Get named `items` from an `obj` object '''
    ret = []
    for item in items:
        ret.append(getattr(obj, item))
    return ret


def object_with_parent(obj, parent):
    obj['_rid'] = parent['_id']


def get_command_output(command, **kwargs):
    return check_output(command, **kwargs)


def call_command_with_input(command, input, **kwargs):
    p = Popen(command, **kwargs)
    p.communicate(input)
    return p


class ActorHelper(object):
    def __init__(self):
        self.error_return_code = -1
        self._output = defaultdict(list)
        self.input = load(stdin)

    def get_dependent_result(self, rid):
        return

    def get_input(self, channel):
        return self.input[channel]

    def output(self, channel, data):
        self._output[channel].append(data)

    def error(self, data, fatal=True):
        # LOG ERROR somewher
        exit(self.error_return_code)

    def done(self):
        print(dumps(self.output))


Actor = ActorHelper()
