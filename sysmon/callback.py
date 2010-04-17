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

    def __init__(self):
        """Creates an empty callback.
        """
        self.hooks=dict([])
    
    def hook(self,name,func):
        """Hooks the given function onto a string.

        Whenever the string is called, the given function will be
        called with a single argument (passed from the original
        caller).
        """
        if name in self.hooks:
            self.hooks[name].append(func)
        else:
            self.hooks[name]=[func]

    def call(self,name,data):
        """Calls all hooks matching the string with the given data.

        The hooks are called in the order they were created.
        """
        if name in self.hooks:
            for func in self.hooks[name]:
                func(data)
