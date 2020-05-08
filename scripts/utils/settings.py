from pathlib import Path
from configparser import ConfigParser, ExtendedInterpolation

from collections.abc import MutableMapping
import shlex
import os

BASE_DIR = Path( __file__ ).parent.parent.parent
SCRIPT_DIR = Path( __file__ ).parent.parent

env_file = BASE_DIR / ".env"


def load_config(
    include_local_path=True
):
    from itertools import chain
    parser = ConfigParser()
    parser.optionxform=str
    with open(env_file) as lines:
        lines = chain(("[config]",), lines)  # This line does the trick.
        parser.read_file(lines)
    print( "Loaded from {}:".format( env_file ) )
    for k,v in parser['config'].items() :
        print( "{k}={v}".format( k = k, v = v ) )
    print( "------------------------------" )
    config = dict(parser['config'])
    if include_local_path:
        path = os.environ['PATH']
        config = { "PATH": path, ** config }
    return config
