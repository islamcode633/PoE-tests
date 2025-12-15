"""
The module contains the necessary data for remote connection via SSH/Telnet to the switch
Using ipv4/6 protocols
"""

from netmiko import ConnectHandler


class RemoteConnection:
    """
    Contains data, commands, methods for remote connection to the switch via SSH/Telnet.
    """

    def __init__(self,
        ipv4_switch: str = '192.168.127.253',
        ipv6_switch: str = 'fe80::c1ff:fe81:3133%enp4s0',
        device_type: str = 'cisco_ios',
        username: str = 'admin',
        password: str = 'password',
        type_conn: str = ''
    ) -> None:
        self.ipv4_switch = ipv4_switch
        self.ipv6_switch = ipv6_switch
        self.device_type = device_type
        self.username = username
        self.password = password
        self.telnet_conn = '_telnet' if type_conn.lower() in ('tn', 'tel', 'telnet') else ""
        """
        :param ipv4_switch: IPv4 host address.
        :param ipv6_switch: IPv6 host address.
        :param device_type: Type OS on the host.
        :param username: Login of the user registered on the host.
        :param password: Password of the user registered on the host.
        :param telnet_conn: Flag for telnet connection.
        """

    def init_conn_session(self):
        """
        Returns SSH or Telnet connection.
        If the connection parameter is not telnet, the connection will always be via SSH.
        """
        return ConnectHandler(
                    device_type=f'{self.device_type}{self.telnet_conn}',
                    host=self.ipv4_switch,
                    username=self.username,
                    password=self.password
                )

    def get_command_ssh(self) -> str:
        """ Command for further connection via ssh """
        return f'sshpass -p {self.password} ssh -o StrictHostKeyChecking=no {self.username}@{self.ipv4_switch}'
