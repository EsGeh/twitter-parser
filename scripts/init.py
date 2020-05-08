#!/usr/bin/env python3

from utils.settings import BASE_DIR, load_config
# from utils.functions import exec_in_xmldb, exec_in_container, run

from argparse import ArgumentParser
import subprocess
from pathlib import Path
from time import sleep

BASE_DIR = Path( __file__ ).parent.parent
SQLDB_WAIT_TIME=10


def create_dirs( config ):
    create_dir(
        BASE_DIR / config['DB_DATA_DIR']
    )

def init_sqldb( config ):
    try:
        subprocess.check_call(
            [ "docker-compose", "--file", BASE_DIR / "scripts/docker-compose_init_db.yaml"
            , "up", "-d", "twitter_parser_db_install"],
            env=config
        )

        print( "wait {}s for the sql database to get ready... :-P".format( SQLDB_WAIT_TIME ) )
        sleep( SQLDB_WAIT_TIME )

        src = config['DB_CONTAINER'] + ":/bitnami/postgresql"
        dst = Path(config['DB_DATA_DIR']) / "pg_conf_dir"
        subprocess.check_call(
            [ "docker", "cp", src, dst ],
            env=config
        )

        src = config['DB_CONTAINER'] + ":/opt/bitnami/postgresql"
        dst = Path(config['DB_DATA_DIR']) / "pg_opt_dir"
        subprocess.check_call(
            [ "docker", "cp", src, dst ],
            env=config
        )

        sleep( SQLDB_WAIT_TIME )

    finally:
        subprocess.check_call(
            [ "docker-compose", "--file", BASE_DIR / "scripts/docker-compose_init_db.yaml"
            , "down" ],
            env=config,
        )

# utils:

def create_dir(dir):
    print( "creating dir '{}'".format( dir ) )
    Path(dir).mkdir(
            parents = True,
            exist_ok = True
    )

if __name__ == '__main__':

    config = load_config()

    create_dirs( config )

    init_sqldb( config )
