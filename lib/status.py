'''
A module to read/write list of processes IDs for currently locked processes

For now, it stores all the Process IDS in a text file in temp dir

ToDo: Change to a more process safe, concurrent access datastore instead of a text file.
      Or , enable file locking for exclusive access at process level for a less effecient but safer access
'''
import os,tempfile

import logging
import logging.config

logging.config.fileConfig("log.cfg")
log = logging.getLogger("status")

status_file = os.path.join(tempfile.gettempdir(),'status_list') #File 

def getStatusFilePath():
    return status_file

def addPidToStatus(ppid):
    '''
    Updates Status file with the script pids currently locked
    TODO: workaround for concurrent access, use fnctl or something
    '''
    processList = getSuspendedProcesses()
    f = open(status_file,'w')
    
    processList.append(str(ppid)) #Add ppid to status file
    log.debug("Added ppid %s to status_file : %s"%(ppid, getStatusFilePath()))
    f.writelines(['%s\n'%ppid for pid in processList])
    f.close()

def remPidFromStatus(ppid):
    '''
    Updates Status file with the script pids currently locked
    TODO: workaround for concurrent access, use fnctl or something
    '''
    if os.path.exists(getStatusFilePath()):
        processList = getSuspendedProcesses()
        f = open(getStatusFilePath(),'w')
        processList = ['%s\n'%pid for pid in processList if pid != int(ppid)] #remove the entry
        log.debug("removed ppid %s to status_file : %s"%(ppid, getStatusFilePath()))
        f.writelines(processList)
        f.close()
    else:
        raise Exception("Can't remove remove process pid %s, from file : %s which doesn't exist"%(ppid,status_file))

def getSuspendedProcesses():
    '''
    Reads Status file having list of script Process IDS currently Locked
    TODO: workaround for concurrent access, use fnctl or something
    '''
    if os.path.exists(getStatusFilePath()):
        f = open(getStatusFilePath(),'r')
        processList = [int(pid.strip()) for pid in f.readlines()]
        f.close()
        return processList
    else: #Status File doesn't exist yet, return empty list
        return []
