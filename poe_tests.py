"""
Simplified client implementation for testing PoE chip
"""

import sys
from time import sleep, time
from typing import (
    List,
    Callable
)
from data import RemoteConnection

# add port_status parsing about deliviring, power
# add ports ID calculated for generated PORTS MAP
# add output overload power for PD
# add output temperature
# add Progress bar

SSH_CONN = RemoteConnection().init_conn_session()
PORTS: tuple = (
    '1/1', '1/2', '1/3',
    '1/4', '1/5', '1/6',
    '1/7', '1/8',
)
# 2W on port
MIN_CONSUM: int = 2
# ret power limit on Switch(power supply) 120W
POWER_LIMIT: int = 120
# run again
NUM_REPEAT_TEST: int = 3
# test execution timer in seconds
TEST_EXEC_TIME: int = 120

TIME_UNTIL_NEXT_SURVEY: int = 5

# necessary pause for correct operation of netmiko
# for shorter pauses this may not work.
# - WARNING: not change the PAUSE constant -
PAUSE: int = 3


def wrapp_calc_curr_time() -> Callable[[], int]:
    """ Freeze the primary timestamp """
    primary_timestamp: int = int(time())
    def calculate_current_time() -> int:
        """ Calculating the current time """
        current_time: int = int(time())
        return current_time - primary_timestamp
    return calculate_current_time

def take_pause() -> None:
    """ Freeze terminal output for N seconds """
    if TIME_UNTIL_NEXT_SURVEY:
        for sec in range(1, TIME_UNTIL_NEXT_SURVEY + 1):
            print(f'next launch in {TIME_UNTIL_NEXT_SURVEY - sec}', end='\r')
            sleep(1)

def check_status_poe() -> str:
    """ Checking the status of the PoE function """
    command: str = 'show poe enable'
    poe_func_status = str(SSH_CONN.send_command(command_string=command)).split()[-1]
    return poe_func_status

def enable_poe() -> None:
    """ Enable function PoE """
    conf_command: List[str] = [ 'poe enable' ]
    SSH_CONN.send_config_set(config_commands=conf_command)

def power_supply_mode(supply_mode: str, port: str) -> None:
    """ Setting power mode """
    conf_command: List[str] = [ f'poe mode {supply_mode} port GigabitEthernet {port}' ]
    SSH_CONN.send_config_set(config_commands=conf_command)

def show_ports_status() -> List[str]:
    """ Checking the state of the ports enabled/disabled """
    command: str = 'show poe ports delivering'
    ports_delivering: List[str] = str(SSH_CONN.send_command(command_string=command)).split('\n')[1:]
    ports_status: List[str] = [ port.split()[-1] for port in ports_delivering ]
    return ports_status

def show_consum_on_port(port: str) -> int:
    """Get ports status """
    command: str = f'show poe port GigabitEthernet {port} status'
    fields: List[str] = str(SSH_CONN.send_command(command_string=command)).split()
    power: str = fields[1]
    return int(float(power))

def edit_port_status(mode: str, port: str) -> None:
    """ Enable/Disable PoE on all ports """
    conf_command: List[str] = [ f'poe enable mode {mode} port GigabitEthernet {port}' ]
    SSH_CONN.send_config_set(config_commands=conf_command)

def activate_all_channels() -> None:
    """ Execute PoE test """
    calculate_current_time: Callable[[], int] = wrapp_calc_curr_time()
    while calculate_current_time() <= TEST_EXEC_TIME:
        try:
            for index_port, status in enumerate(show_ports_status()):
                if status == 'enabled':
                    print(f'Port: {PORTS[index_port]} -> {show_consum_on_port(port=PORTS[index_port])} [W]')
                    continue
                sleep(PAUSE)
                print(f'Port: {PORTS[index_port]} -> {status}')
            take_pause()
        except KeyboardInterrupt:
            sys.exit('\nInterrupt script execution\n')

def preparatory_stage() -> None:
    """ Preliminary configuration """
    # On PoE function
    if check_status_poe() == 'disabled':
        enable_poe()
    # Set power limit 120 W
    conf_command: List[str] = [ f'poe power limit {POWER_LIMIT}' ]
    SSH_CONN.send_config_set(config_commands=conf_command)
    # Disabled PoE ports
    for id_port in PORTS:
        edit_port_status(mode='disable', port=id_port)
        sleep(PAUSE)

def sequential_activation_of_channels() -> None:
    """ 
    Sequentially On/off the port
    and power consumption output
    """
    for id_port in PORTS:
        edit_port_status(mode='enable', port=id_port)
        sleep(PAUSE)
        curr_power: int = show_consum_on_port(port=id_port)
        if MIN_CONSUM < curr_power:
            print(f'Port: {id_port} -> {curr_power} [W] [Success]')
            sleep(PAUSE)
            edit_port_status(mode='disable', port=id_port)
        else:
            print(f'Port: {id_port} -> {curr_power} [W] [Failed]')


if __name__ == '__main__':
    try:
        preparatory_stage()
        sequential_activation_of_channels()
    except Exception:
        sleep(PAUSE)
        preparatory_stage()
        sequential_activation_of_channels()
