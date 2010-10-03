'''
A module having utility functions to like for collection information about a process, given process ID etc..
'''
import os,platform
import re
import socket
import subprocess

def getScriptPid():
    '''
    Returns PID of the script that invoked the module
    '''
    return os.getppid()


def getHostinfo():
    '''
    Returns Information about the Host
    '''
    return dict(host_name=socket.gethostname(),
                fqdn=socket.getfqdn(),
                system=platform.platform())

def getProcessInfo(pid):
    '''
    Given process ID, it returns information (as formatted string) about that process
    I couldn't find any python module/function to get details about a process, given it's PID
    So write a little hack of my own, also hoping that it would work with different flavours of Linux(Aah!!)
    
    That is parsing the output of *ps  -o user,cmd,start_time,tty=tty  --pid <PID>* to get the process info
    Which looks something like this:
    ---------------------------------------------------------
    USER     CMD                         START tty
    x90      sh test.sh                  17:21 pts/1
    ---------------------------------------------------------
    And I try to get start of each of the fields from 2nd row as index of where it's corresponding
    header starts.
    '''
    cmd_call = "ps  -o user=user_name,cmd=command,start=start_time,tt=tty  --pid %d"%pid
    process = subprocess.Popen(cmd_call,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,errors = process.communicate()
    output = output.splitlines() 
    if len(output) == 1:
        raise Exception("Looks like Process PID:%d doesn't exist!!"%pid)
    headers,output_str = output

    ##Parse the output, as given in the doc string
    header_start_idxs = [each.start() for each in re.finditer(r'\w+',headers)]
    header_start_idxs.append(None) #append None at the end, it's used in getting value of the last element.

    processInfo = {}

    for idx in range(len(header_start_idxs) - 1):
        start,end = header_start_idxs[idx],header_start_idxs[idx+1] #This header's start till next header's start is my value.
        header = headers[start:end].strip()
        value = output_str[start:end].strip()
        processInfo[header] = value

    #Update host information
    processInfo.update(getHostinfo())
    return processInfo
