#! /usr/bin/env python
'''
This is the script which will check status for last executed command and will take 
appropriate action accordingly
'''

'''
Todo:
1)Needs better exception handling, remove the tmp lock files created in any case
'''

import sys,os,tempfile
from lib.utils import getScriptPid
from lib.status import addPidToStatus

import logging
import logging.config

logging.config.fileConfig("log.cfg")
log = logging.getLogger("check")

def suspendScript():
    '''
    Given a Process PID, suspends process's execution
    uses FIFO's to block on read unless someone send what to be done
    '''
    script_pid = getScriptPid() #get PID of the script which invoked 
    lockedFileName = 'check_%s.lock'%script_pid #get filename for the process to be locked
    lock_file = os.path.join(tempfile.gettempdir(),lockedFileName)
    
    if os.path.exists(lock_file):
        log.exception('File %s already exists!!'%lock_file)
        raise Exception('File %s already exists!!'%lock_file)

    try:
        os.mkfifo(lock_file) #create the Fifo file

        reader = os.open(lock_file,os.O_RDONLY) #Read from Fifo file
        addPidToStatus(script_pid) #Add Pid to status File

        while True: #Parse the commands sent by the client and work accordingly
            log.info("Script PID:%d paused"%script_pid)
            msg = reader.readline()[:-1].strip()
            if msg == 'resume': #Means break the lock and continue
                log.info("Ordered to break and lock the continue with the execution of the script")
                reader.close()
                os.unlink(lock_file) #destory Fifo
        remPidFromStatus(script_pid) #Remove this process from the list of blocked processes
    except Exception, e:
        log.info("Some Exception occured, cleanup and exit")
        cleanUp()
        
def cleanUp(lock_file):
    '''
    In case some exception does happen in this step, cleanup like for ex. deleting the FIFO file is required
    '''
    if os.path.exists(lock_file):
        os.unlink(lock_file)

if __name__=='__main__':
    try:
        exit_code = int(sys.argv[1])
    except ValueError:
        print "Something wrong with the suspending the script, So continue"
        sys.exit(0)

    if exit_code != 0: #Some step in the script seemed to have failed, so suspending process execution
        log.info('Trying to suspend the script')
        suspendScript() #Suspend
