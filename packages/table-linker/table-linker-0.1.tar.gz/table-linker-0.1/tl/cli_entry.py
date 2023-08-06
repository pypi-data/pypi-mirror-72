import sys
import importlib
import pkgutil
import itertools
from io import StringIO
import signal
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from tl import cli
from tl.exceptions import tl_exception_handler, TLArgumentParseException
from tl import __version__
import sh

handlers = [x.name for x in pkgutil.iter_modules(cli.__path__)
            if not x.name.startswith('__')]

pipe_delimiter = '/'

signal.signal(signal.SIGPIPE, signal.SIG_DFL)


class TLArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('formatter_class'):
            kwargs['formatter_class'] = RawDescriptionHelpFormatter

        super(TLArgumentParser, self).__init__(*args, **kwargs)


def cmd_done(cmd, success, exit_code):
    # cmd.cmd -> complete command line
    global ret_code
    ret_code = exit_code


def cli_entry(*args):
    """
    Usage:
        tl <command> [options]
    """
    global ret_code
    parser = TLArgumentParser()
    parser.add_argument(
        '-V', '--version',
        action='version',
        version='TL %s' % __version__,
        help="show tl version and exit."
    )

    parser.add_argument(
        '--url',
        action='store',
        type=str,
        dest='url',
        required=False,
        help='URL of the Elasticsearch server containing the items in the KG')

    parser.add_argument(
        '--index',
        action='store',
        type=str,
        dest='index',
        required=False,
        help='name of the Elasticsearch index')

    parser.add_argument(
        '-U',
        action='store',
        type=str,
        dest='user',
        required=False,
        help='the user id for authenticating to the ElasticSearch index')

    parser.add_argument(
        '-P',
        action='store',
        type=str,
        dest='password',
        required=False,
        help='the password for authenticating to the ElasticSearch index')

    sub_parsers = parser.add_subparsers(
        metavar='command',
        dest='cmd'
    )
    sub_parsers.required = True

    # load parser of each module
    # TODO: need to optimize with lazy loading method
    for h in handlers:
        mod = importlib.import_module('.{}'.format(h), 'tl.cli')
        sub_parser = sub_parsers.add_parser(h, **mod.parser())
        mod.add_arguments(sub_parser)

    if not args:
        args = tuple(sys.argv)
    if len(args) == 1:
        args = args + ('-h',)
    args = args[1:]

    # parse internal pipe
    pipe = [tuple(y) for x, y in itertools.groupby(args, lambda a: a == pipe_delimiter) if not x]
    if len(pipe) == 1:
        cmd_args = pipe[0]
        args = parser.parse_args(cmd_args)

        # load module
        func = None
        if args.cmd:
            mod = importlib.import_module('.{}'.format(args.cmd), 'tl.cli')
            func = mod.run
            kwargs = vars(args)
            del kwargs['cmd']

        # run module
        ret_code = tl_exception_handler(func, **kwargs)
    else:
        concat_cmd_str = None
        global_cmd_options = {}
        if '--url' in args:
            i = args.index('--url')
            global_cmd_options['--url'] = args[i + 1]

        if '--index' in args:
            i = args.index('--index')
            global_cmd_options['--index'] = args[i + 1]

        if '-U' in args:
            i = args.index('-U')
            global_cmd_options['-U'] = args[i + 1]

        if '-P' in args:
            i = args.index('-P')
            global_cmd_options['-P'] = args[i + 1]

        for idx, cmd_args in enumerate(pipe):
            _ = list(cmd_args)
            for k in global_cmd_options:
                _.insert(0, global_cmd_options[k])
                _.insert(0, k)

            cmd_args = tuple(_)

            # parse command and options
            cmd_str = ', '.join(['"{}"'.format(c) for c in cmd_args])

            # add common arguments
            cmd_str += ', _bg_exc=False, _done=cmd_done'  # , _err=sys.stdout
            # add specific arguments
            if idx == 0:  # first command
                concat_cmd_str = 'sh.tl({}, _in=sys.stdin, _piped=True)'.format(cmd_str)
            elif idx + 1 == len(pipe):  # last command
                concat_cmd_str = 'sh.tl({}, {}, _out=sys.stdout)'.format(concat_cmd_str, cmd_str)
            else:
                concat_cmd_str = 'sh.tl({}, {}, _piped=True)'.format(concat_cmd_str, cmd_str)
        try:
            # print(concat_cmd_str)
            process = eval(concat_cmd_str)
            process.wait()
        except sh.SignalException_SIGPIPE:
            pass
        except sh.ErrorReturnCode as e:
            # mimic parser exit
            parser.exit(TLArgumentParseException.return_code, e.stderr.decode('utf-8'))
    return ret_code
