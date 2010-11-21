#!/bin/bash

export tmp_dir="./tmp/"

suspend_process()
{
#This function will suspend the original script which invoked this script

pipe=$tmp_dir$script_pid".lock"
echo $pipe

if [ -p $pipe ]; then
    rm $pipe
fi

echo "creating pipe :: "$pipe
mkfifo $pipe


while read line
do
    if [ $line = "CONTINUE" ]; then
            break
    fi
    echo $line
    echo "Resuming the process(pid) : "$pid
    echo "Deleting the pipe"
    rm $pipe
done < $pipe

}

#get_ppid()
#{
#Returns Process ID of the original shell script which invoked this script.
#}

check_status()
{
#It checks script status at the checkpoints present in the original script, and suspends/notifies in case of NZEC.

exit_code=$1
cfg_file=$2

if [ $exit_code -ne 0 ]; then
    #Possibly error, Got Non Zero Exit Code
    python notify.py -p $script_pid -e $exit_code -f $cfg_file
    if [ $? -eq 0 ]; then
	suspend_process
    fi	
	
else
    echo "Checking on the set chekpoint!!!, Everything looks Fine SO far"
fi
}

if [ ! -d $tmp_dir ]; then
    mkdir $tmp_dir;
fi

exit_code=$1
cfg_file=$2

#check number of args passed to the script
if [ $# -ne 2 ]; then 
    echo "Usage : ./check.sh <pid> <cfg file>"
    echo "exitting"
    exit 1
fi;

#check if the configuration file exists
if [ ! -e $cfg_file ]; then 
    echo "configuration file - " $cfg_file " doesn't exist, exitting"
    exit 1
fi

#ps --no-headers -o ppid -p $$
#get_ppid
#export script_pid=$?
export script_pid=`ps --no-headers -o ppid -p $$`

script_pid=`expr $script_pid`
echo "ab"$script_pid
check_status $*
