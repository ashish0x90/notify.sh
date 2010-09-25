'''
A module to read/write list of processes IDs for currently locked processes

For now, it stores all the Process IDS in a text file in temp dir

ToDo: Change to a more process safe, concurrent access datastore instead of a text file.
      Or , enable file locking for exclusive access at process level for a less effecient but safer access
'''

status_file = os.path.join(tempfile.gettempdir(),'status_list') #File 

def getFilePath():
    return status_file

def UpdateStatus(ppid,remove=False):
    '''
    Updates Status file with the script pids currently locked
    TODO: workaround for concurrent access, use fnctl or something
    '''
    current_list = readStatusFile()
    f = open(status_file,'w')
    
    if remove:
        current_list = [each.strip() for each in current_list if each.strip() != str(ppid).strip()] #remove the entry
    else:
        current_list.append(str(ppid))
    f.writelines(current_list)
    f.close()

def readStatus():
    '''
    Reads Status file having list of script Process IDS currently Locked
    TODO: workaround for concurrent access, use fnctl or something
    '''
    f = open(status_file,'r')
    data = f.readlines()
    f.close()
    return data
