#!/usr/bin/env sh

export tmp_dir="./tmp/"

resume()
{
#msg="Process Paused until EXPLICITELY told to move to the next step, enter CONTINUE to move to the next step"
echo "CONTINUE" > $pid_pipe
}

pid=$1
pid_pipe=$tmp_dir$pid".lock"

if [ ! -d "/proc/"$pid ]; then
    echo "Process ("$pid") doesn't exist, are you sure?"
    exit 1
fi

if [ ! -p $pid_pipe ]; then
    echo "Process("$pid") doesn't seem to be suspended, or is not pointing to the directory having the pipe!!"
    echo "$pid_pipe should point to named pipe created by ./check.sh which suspended the process"
    exit 1
fi

resume $pid_pipe