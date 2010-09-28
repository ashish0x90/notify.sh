#! /usr/bin/env python
'''
This is the script which will resume a previously suspended process
cmd line params needed : process PID
'''

import os,tempfile
from lib.status import getSuspendedProcesses
from lib.utils import getProcessInfo

import logging
import logging.config

logging.config.fileConfig("log.cfg")
log = logging.getLogger("resume")

def resumeScript(pid):
    '''
    Given a Process PID, block process's execution
    uses FIFO's to block on read unless someone send what to be done
    '''
    lockedFileName = 'check_%s.lock'%pid #get filename for the process to be locked
    lock_file = os.path.join(tempfile.gettempdir(),lockedFileName)

    writer = os.open(lock_file, os.O_WRONLY)
    os.write(writer, 'resume\n') #This will resume the process
 
    

def getBlockedProcesses():
    '''
    It gathers diagnostic information about all the processes currently blocked 
    which can be shown to the user, who can then decide what has to be done
    returns {pid1:<Information Str>,
             pid2:<Information Str>
             }
    '''
    return dict([ [pid, getProcessInfo(pid)] for pid in getSuspendedProcesses()])

if __name__=='__main__':
    processList = getBlockedProcesses()
    if not processList:
        print "All the processes seem to be running just fine!!"

    ##Pretty Print Process List
    print 'Number of processes currently blocked : %s\n'%len(processList)
    for pid,information in processList.iteritems():
        print "PID: %s"%pid
        print information
        print '\n\n'

    #Get PID of the process to be unblocked
    pid = None
    while pid not in getBlockedProcesses():
        print "Enter PID of the script process from the list given above, which you want to be continued."
        pid = raw_input('PID :')
        try:
            pid = int(pid)
        except:
            continue
        
    resumeScript(pid=pid)
