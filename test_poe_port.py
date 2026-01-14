#!/usr/bin/env python3

"""
Enable and disable the PoE port for log collection
"""

import sys
from time import sleep
from typing import (
    List,
    Union
)
import re

from data import RemoteConnection


SSH_CONN = RemoteConnection().init_conn_session()

PORTS: tuple = ('1/1', '1/9')
PAUSE: int = 3


def enable_poe() -> None:
    """ Enable function PoE """
    conf_command: List[str] = [ 'poe enable' ]
    SSH_CONN.send_config_set(conf_command)

def show_consum_on_port(port: str) -> Union[int, None]:
    """Get ports status """
    command: str = f'show poe port GigabitEthernet {port} status'
    fields: List[str] = str(SSH_CONN.send_command(command)).split()
    pattern = r"(\d+)[.]"
    match = re.search(pattern, fields[1])
    if match:
        return int(match.group(1))
    return None

def edit_port_status(mode: str, port: str) -> None:
    """ Enable/Disable PoE on all ports """
    conf_command: List[str] = [ f'poe enable mode {mode} port GigabitEthernet {port}' ]
    print(f'mode: {mode}')
    SSH_CONN.send_config_set(conf_command)


if __name__ == '__main__':
    try:
        enable_poe()
        print("Starting PoE test")
        while (symbol := input()) == ' ':
            edit_port_status(mode='enable', port=PORTS[0])
            sleep(PAUSE)
            print(f'{PORTS[0]} <-> {show_consum_on_port(port=PORTS[0])}W')
            sleep(PAUSE)
            edit_port_status(mode='disable', port=PORTS[0])
            print()
    except Exception as e:
        print(f'Error {e.args}')
        sys.exit(1)
    finally:
        SSH_CONN.disconnect()
