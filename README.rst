::


	    _   __        __   _  ____                 __  
	   / | / /____   / /_ (_)/ __/__  __    _____ / /_ 
	  /  |/ // __ \ / __// // /_ / / / /   / ___// __ \
	 / /|  // /_/ // /_ / // __// /_/ /_  (__  )/ / / /
	/_/ |_/ \____/ \__//_//_/   \__, /(_)/____//_/ /_/ 
	                           /____/                  


Notify.sh 
=========

Notify.sh adds better error handling/notification ability to the otherwise vanilla shell scripts.(**Linux Only**)


The Idea
--------
::

  While it's easy to know when a error occurs while a shell script is running, 
  when that error happens though we can pretty much do only one thing - cleanup and terminate the script.
  This is even worse when you are running a script which has to do a LOT OF WORK.
  In that case I don't want to restart the process from stratch when a error occurs, 
  and it would be AWESOME if I had a tool which can monitor the script and if a error occured can:
  1. Suspend the script immediately.
  2. Send out an e-mail notifying me about the error and also how to resume/terminate that script.
  Now in this case I can manually either correct/redo the step at which error occured and can resume the script.
  Well this was pretty much the basic idea that led me to implement the solution.


Use cases
---------
It is particularly helpful in cases when you want to monitor scripts and don't want to keep looking at the screen all the time.
Optionally if a error occurs you want to suspend/terminate the process and be notified in real-time.

- Enable runtime checkpoints for scripts to check if a step passed/failed.
- If a step fails (tested on the basis of NZEC), send out a notification e-mail and suspend the process.
- The suspended process can be resumed/terminated later.

Getting started
---------------

  Notify.sh can be integrated with existing shell scripts in following k simple steps.

#. Download the latest copy of notify.sh code, and copy your scripts(s) in the same directory which has notify.sh contents.
#. Update the notification.cfg template file provided, with approproiate settings.
#. Run demo.sh to see if notification.cfg file is valid. You should get error email, also try to resume the suspended demo.sh process. If this works, then you are all good so far.
#. Now one very important thing to be noted before we move any further is that - 
   notify.sh DOESN'T make catching the shell script errors any easier,
   but only can help you on *HOW TO HANDLE* a error if it occurs.
   In other words you *NEED* to provide some sort of status code everytime you invoke the check.sh script using which
   check.sh can then determine if some error has occured. A relevant analogy would be exit code returned by the processes.
   So, at whichever step you need to check status, you need to invoke check.sh and pass a integer value as follows.
   Status flag - 0 (No error happened)
   Status flag - anything else (Something went wrong, suspend the process)
   
   It's particularly easier to do in shell scripts, because the pre-defined shell variable **$?** 
   stores exit code for last statement executed.
   So most of the times you can just invoke it as 

::   

     ./check.sh $? "notification.cfg"

Refer to *demo.sh* for detailed use cases, as in what all situations this can be used.
     

Runtime Dependencies
--------------------
- python 2.5

ToDo
----
- Add the Non Zero exit code on which the process got suspended to the notification(e-mails) sent.
