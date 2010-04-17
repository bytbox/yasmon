"""Provides a flexible and extensible callback class for the system
monitor.

"""

class SysmonCallback:
    """A flexible and extensible callback class for sysmon.

    Callback functions are registered with a unique identifying
    string, usually of the form part1.part2.specific. 

    Callback functions are called with a single argument, usually a
    dictionary. Callback functions are called in the order they were
    registered.
    """
    def __init__():
        pass
    
    def hook(name,func):
        pass

    def call(name,data):
        pass
