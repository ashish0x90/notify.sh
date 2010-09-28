'''
A module having utility functions to like for collection information about a process, given process ID etc..
'''
import os

def getScriptPid():
    '''
    Returns PID of the script that invoked the module
    '''
    return os.getppid()


def getProcessInfo(pid):
    '''
    Given process ID, it returns information (as formatted string) about that process
    '''
    return '' #returns empty string for now
