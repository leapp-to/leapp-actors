""" Helper functions for working with OpenShift """

from subprocess import Popen, PIPE, check_output
import time


class StreamCommand(Popen):
    """ Thin wrapper around subprocess.Popen """
    def __init__(self, *args, **kwargs):
        kwargs['stdout'] = PIPE
        super(StreamCommand, self).__init__(*args, **kwargs)

    def stream_command(self):
        """ Stream the output of the command as iterable """
        while True:
            if self.poll() is not None:
                break
            line = self.stdout.readline()
            if line:
                yield line[:-1] # strip new line at the end and yield


def oc_stream(command, streaming_printer):
    """ Stream output of `command` into callable `streaming_printer`  """
    cmd = StreamCommand(['oc'] + command)
    for line in cmd.stream_command():
        streaming_printer(line)
    return cmd.wait()


def oc_exec(name, command, **kwargs):
    """ Execute `command` in a container known as `name`

        `kwargs` are passed directly to the underlying `Popen` call
    """
    return Popen(['oc', 'exec', '-i', name, '--'] + command, **kwargs).wait()


def oc(command):
    """ Call `command` using the `oc` binary """
    return check_output(['oc'] + command)


class BuildDefinition(object):
    """ Object to hold OpenShift build definition """
    def __init__(self, strategy=None, docker_image=None, to=None, args=None, from_dir=None, follow=False):
        self._strategy = strategy
        self._docker_image = docker_image
        self._to = to
        self._args = args or []
        self._from_dir = from_dir
        self._follow = follow

    def _args_append(self, args, attr):
        """ Should be static """
        try:
            attribute = getattr(self, '_' + attr)
            args += ['--{}={}'.format(attr.replace('_', '-'), attribute)]
        except AttributeError:
            pass

    def create_build(self):
        """ Create an argument set for new OpenShift build """
        args = ['new-build']
        self._args_append(args, 'strategy')
        self._args_append(args, 'to')
        self._args_append(args, 'docker_image')
        args += ['--name', self._to]
        args += [self._args]
        return args

    def create_build_and_start(self):
        """ Same as `create_build` but also create argument set for starting
            the build
        """
        build = self.create_build()

        args = ['start-build']
        self._args_append(args, 'from_dir')
        self._args_append(args, 'follow')
        args += [self._to]

        return {'build': build, 'start': args}


class BuildError(Exception):
    """ Raised on various build error events """
    pass


class sync(object):
    """ Synchronouse operations against the cluster """

    class Periodic(object):
        """ Periodic callback holder """
        def __init__(self, callback, frequency):
            assert callback and frequency > 0, 'Invalid periodic object'

            self._callback = callback
            self._frequency = frequency

        @property
        def callback(self):
            """ Function to call """
            return self._callback

        @property
        def frequency(self):
            """ Frequency with which the periodic event happens """
            return self._frequency

    class TimeoutExceededError(Exception):
        """ Error raised when the timeout specified for certain operation was exceeded """
        pass

    @staticmethod
    def NewSourceBuild(definition=None):
        """ Create a new source build from definition """

        assert isinstance(definition, BuildDefinition), "definition must be BuildDefinition"

        build_def = definition.create_build_and_start()

        oc(build_def['build'])

        if definition._follow:
            def p(x):
                print(x)
            if oc_stream(build_def['start'], p) != 0:
                raise BuildError
            return

        oc(build_def['start'])

    @staticmethod
    def Pod(name=None, timeout=None, readiness=True, periodic=None):
        """ Wait for pod `name` to become ready  """

        assert isinstance(name, str) and name, 'Name is mandatory not empty string'
        assert timeout > 0, 'Timeout must be greater than zero'
        assert isinstance(readiness, bool), 'Readiness must be bool value'
        assert isinstance(periodic, sync.Periodic), 'periodic must be of type sync.Periodic'

        delta = 0 if not periodic else periodic.frequency

        pod = None
        deadline = time.time() + timeout
        next_message = time.time() + delta

        while True:
            if time.time() >= deadline:
                raise sync.TimeoutExceededError
            if periodic.callback and time.time() >= next_message:
                periodic.callback()
                next_message = time.time() + delta
            if not pod:
                cmd = ["get", "-o", "jsonpath", "pod",
                        "--selector=name={}".format(name),
                        "--template={.items[*].metadata.name}"]
                pod = str(oc(cmd))
            time.sleep(delta)
            if pod:
                if readiness:
                    cmd = ['get', 'po', pod, '--output', 'jsonpath', '--template', '{.status.containerStatuses.*.ready}']
                    if 'true' in str(oc(cmd)):
                        return pod
                else:
                    return pod

    @staticmethod
    def ProcessApply(file_name, variables=None):
        """ Execute process -> apply template expansion  """

        assert isinstance(file_name, str) and file_name, 'File must be non empty string'

        variables = variables or []
        proc = ['oc', 'process', '-f', file_name]
        for var in variables:
            proc += ['-v', var]
        proc = Popen(proc, stdout=PIPE)
        apply_call = ['oc', 'apply', '-f', '-']
        Popen(apply_call, stdin=proc.stdout).wait()
        return proc.wait() == 0
