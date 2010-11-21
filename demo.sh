#!/bin/bash

#The basic idea is to add this line 
#* ./check.sh $? "notification.cfg" * Wherever you want to check script status, it is analogous to a checkpoint.

#Description of the arguments
#1) $? (this is a shell variable which stores exit code of last line executed)
#2) "notification.cfg" - this is the configuration file which keeps e-mail username/pwd to be used in error notification.

#Note that this script will suspend at two steps only - when  abcde, abcd
epic_fail()
{

echo "That's the way I fail - EPIC"
return 1 #Note that this can be used to signal that some error happened.
}

epic_pass()
{
echo "Call me, I won't fail"
return 0
}

checking_a_function()
{
echo "Here I am going to track and suspend if a error occurs within a function"
#Will suspend here
abcd
./check.sh $? "notification.cfg"
echo "harmless function call"
./check.sh $? "notification.cfg"
echo "Something that doesn't need to be checked"
echo "Something that doesn't need to be checked-2"
return 0
}

echo "START"
#Will suspend here
abcde
./check.sh $? "notification.cfg"
echo "hello123"
./check.sh $? "notification.cfg"
echo "hello1234"
./check.sh $? "notification.cfg"
#Will suspend here
abcd 
./check.sh $? "notification.cfg"
echo "hello123"
./check.sh $? "notification.cfg"
echo "hello1234"
echo "END"


#Example of tracking functions for a possible error
#Will suspend here
epic_fail
./check.sh $? "notification.cfg"
epic_pass
./check.sh $? "notification.cfg"
checking_a_function
./check.sh $? "notification.cfg"
