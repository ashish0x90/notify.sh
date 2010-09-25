
'''
This is the script which will check status for last executed command and will take 
appropriate action accordingly
'''

import os,tempfile
from lib.utils import getScriptPid

def blockScript():
    '''
    Given a Process PID, block process's execution
    uses FIFO's to block on read unless someone send what to be done
    '''
    script_pid = getScriptPid()
    lockedFileName = 'check_%s.lock'%script_pid #get filename for the process to be locked
    lock_file = os.path.join(tempfile.gettempdir(),lockedFileName)

    if os.path.exists(lock_file):
        raise Exception('File %s already exists!!'%lock_file)
    os.mkfifo(lock_file) #create the Fifo file

    reader = os.open(lock_file,os.O_RDONLY) #Read from Fifo file

    while True: #Parse the commands sent by the client and work accordingly
        msg = reader.readline()[:-1].strip()
        if msg == 'continue': #Means break the lock and continue
            reader.close()
            os.unlink(lock_file) #destory Fifo

def doSomething(code):
    '''
    Depending on code parameter passed, carries out some action
    For now only supports : Blocking
    '''
    if code==1: #exit code 1
        blockScript()


if __name__=='__main__':
    try:
        exit_code = int(sys.argv[1])
    except ValueError:
        print "Something wrong with the exception sent, So NOT blocking and continuing with the script"
        sys.exit(0)

    doSomething(code) #proceed
