#!/usr/bin/env python
"""
Python client to interface with Ublox receivers

Usage:
    pyublox -h | --help
    pyublox --version
    pyublox detect [-d <level>]
    pyublox config [ -p <serial-port>] [-f <file>] [ -r <rate> ] 
                   [ --obs-data ] [ --nav-data ] [ --llh-data ] [-d <level>]
    pyublox record [ -p <serial-port>] [ -n <name> ] [-o <dir>] 
                   [-s <periodicity>] [-d <level>]

Options:
    -h --help         Show this help
    -v --version      Show the version
    -d --debug (DEBUG | INFO | WARNING | CRITICAL)
                      Issue debug information (verbosity controlled by the given debug level) [default: CRITICAL]
    -p --serial-port  Serial port to work with (e.g. /dev/ttyACM0)
    -f --file <file>  Configure the receiver using a configuration file obtained 
                      with ublox u-center tool.
    -r --rate <rate>  Data rate at which the observable will be recorded
    --obs-data        Switch to turn on recording of observables (GNSS measurements)
    --nav-data        Switch to turn on recording of navigation data
    --llh-data        Switch to turn on recording of position estimates
    -o --output-dir <dir>
                      Record the ublox stream to a file or to stdout. If a file 
                      is specified, the periodicity  [default: .]
    -n --name <name>  Specify the receiver name, that will be used to name the 
                      receiver [default: UBLX]
    -s --slice (daily | hourly | quarterly)
                      Slice the data in chunks of given periodicity [default: daily]

Commands:
    detect  Detect ublox device attached to serial port and output basic configuration
    config  Submit configuration options to ublox
    record  Record valid binary UBX packets received from the given port to a file
"""
import docopt
import pkg_resources
import sys

from . import commands
from . import OUTPUT_DIR_STR, SLICE_STR, NAME_STR, FILE_STR, RATE_STR

from .ublox import SERIAL_PORT_STR

from roktools import logger

def main():
    """
    """

    version = pkg_resources.require("pyublox")[0].version

    args = docopt.docopt(__doc__, version=version, options_first=False)

    logger.set_level(args['--debug'])
    logger.debug(f"Start main, parsed arg\n {args}")

    command, command_args = __get_command__(args)
    logger.debug(f'Command arguments\n {command_args}')


    try:
        command(**command_args)
    except ValueError as e:
        sys.stderr.write("FATAL: " + str(e))

    return 0


def __get_command__(args):

    command = None
    command_args = {}

    if args['config']:
        command = commands.config
        command_args = __build_command_args__([SERIAL_PORT_STR, RATE_STR, FILE_STR], args)

    elif args['detect']:
        command = commands.detect
        command_args = {}

    elif args['record']:
        command = commands.record
        command_args = __build_command_args__([SERIAL_PORT_STR, OUTPUT_DIR_STR, SLICE_STR, NAME_STR], args)

    return command, command_args


def __build_command_args__(parameters, arguments):

    command_args = {}
    for arg_params in parameters:
        key = f'--{arg_params}'
        if arguments[key]:
            command_args[arg_params] = arguments[key]

    return command_args


if __name__ == "__main__":

    return_code = main()
    sys.exit(return_code)
