""" Script that launches a server.

Normally, this is meant to be invoked from within a Launcher object (see launcher.py).
However, you can also call this directly, with command-line arguments:
:arg --logport: port number of log server
:arg --serverport: (optional) port number to use for server. Notes:
    (1) if not provided, the user will be prompted to enter a port number in the commandline
    (2) this script does not explicitly provide ConnectionRefusedError handling. Two (non-exclusive) options:
        (i) Implement in server.launch() method
        (ii) Implement in launcher.py module (DONE)
:arg --server: (optional) the name of the server module. Notes:
    (1) should be the name of the module from which the desired server can be instantiated
    (2) module must explicitly be imported in this script
            (we could consider adding auto-import functionality for selected/all modules at a later time)
    (3) module must have a launch(**kwargs) method for instantiating server (and prerequisites) with parameters
        :param logger: instance of LogClient class to use for logging
        :param port: (int) port number
"""

import importlib

from pylabnet.utils.helper_methods import parse_args, show_console, hide_console
from pylabnet.utils.logging.logger import LogClient


def main():

    # parse command line arguments
    args = parse_args()
    try:
        log_port = int(args['logport'])
    except IndexError:
        raise IndexError('Please provide command line arguments in the form\n"'
                         'python launch_gui.py --logport 1234 --serverport 5678 --server servername')
    if 'serverport' in args:
        server_port = int(args['serverport'])
    else:
        show_console()
        server_port = int(input('Please enter a server port value: '))
        hide_console()
    if 'server' in args:
        server = args['server']
    else:
        show_console()
        server = input('Please enter a server module name: ')
        hide_console()
    if 'logip' in args:
        host = args['logip']
    else:
        host = 'localhost'

    # Instantiate logger
    server_logger = LogClient(
        host=host,
        port=log_port,
        module_tag=server+'_server',
        server_port=server_port
    )

    # Retrieve debug flag.
    debug = int(args['debug'])

    # Halt execution and wait for debugger connection if debug flag is up.
    if debug:
        import ptvsd
        import os
        # 5678 is the default attach port in the VS Code debug configurations
        server_logger.info(f"Waiting for debugger to attach to PID {os.getpid()} (pylabnet_server)")
        ptvsd.enable_attach(address=('localhost', 5678))
        ptvsd.wait_for_attach()
        breakpoint()

    # Instantiate module
    try:
        mod_inst = importlib.import_module(f'servers.{server}')
    except ModuleNotFoundError:
        server_logger.error(f'No module found in pylabnet.launchers.servers named {server}.py')
        raise

    mod_inst.launch(logger=server_logger, port=server_port)


if __name__ == '__main__':
    main()
