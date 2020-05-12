#!/usr/bin/env python3

from utils.settings import BASE_DIR, load_config
# from utils.functions import exec_in_xmldb, exec_in_container, run

from argparse import ArgumentParser
import subprocess
from pathlib import Path

if __name__ == '__main__':

    config = load_config()

    subprocess.check_call(
        [ "gradle", "build" ],
        cwd = Path(config['JAVA_SRC_DIR']) / 'twitter_parser_java',
        env=config,
    )
