"""
Docstring for excepts_poe
"""


class AuthException(Exception):
    """ Failed to log in """

class EnablePoeException(Exception):
    """ Error activating the poe function """

class SetPowerLimitException(Exception):
    """ Error setting power limit """

class InitErrorException(Exception):
    """ Error initializing required parameters """
