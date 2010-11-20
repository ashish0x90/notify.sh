#!/usr/bin/env python

from email.MIMEText import MIMEText
from optparse import OptionParser
import smtplib
import os,sys
from ConfigParser import ConfigParser
from utils import getProcessInfo

'''
This module notifier user, in case of error occures(script get suspended), Or any other event of interest occurs
Will require various configurable variables like ( like receiver_addrs,sender_address,sender_password,
smtp_host,smtp_port etc. etc.)

This information can be supplied as a configuration file having the required values.
'''

def parseConfiguration(cfgFile):
    config = ConfigParser()
    config.read(cfgFile)
    return config

class email:
    def __init__(self, info, cfg, script_exit_code, email_type):
        self.__validateCfg(cfg) #validate the cfg first
        self.config = cfg
        self.info = info
        self.email_type = email_type

    def __validateCfg(self, cfg):
        '''
        This function will validate that the configuration file has all the necessary options
        '''
        required_options = ['SMTP_HOST','SMTP_PORT','sender_email_addr','sender_email_passwd',
                            'recipient_email_addrs']
        for option in required_options:
            if not cfg.has_option('email',option):
                raise Exception("%s: is either missing or doesn't have a proper value, check sample cfg file"%option)

    def __getMsg(self):
        '''
        This constructs actual message to be sent out the user
        TODO: Cleanup
        '''

        if self.email_type == 'test': #A dry-run to see if the notification if working.
            subject = "Testing notification - notify.sh"
            body = "You got this message as a test run for notify.sh from %(host_name)s"%self.info

        elif self.email_type == 'error': #It's an actual error message
            subject = "Command: %(command)s, running on"\
                ": %(host_name)s had some error - notify.sh"%self.info
            args = self.prettifyArgs(self.info)            
            body = open('emailbody.txt').read()%(args, self.info['Process ID'], self.info['Process ID'])
        else:
            raise Exception('Notification can be of only following types : test,error')

        msg = MIMEText(body)
        msg['subject'] = subject
        msg['From'] = str(self.config.get('email','sender_email_addr'))
        msg['To'] = str(self.config.get('email','recipient_email_addrs'))
        
        return msg
                                 
                                 
    def prettifyArgs(self, args):
        seperator = smtplib.CRLF
        ret = ""
        for k,v in sorted(args.iteritems()):
            ret += '%-20s : %s%s'%(k.replace('_',' ').capitalize().strip(), v.strip(), seperator)
        return ret


    def notify(self):
        '''
        This code will notify the user in case the script gets suspended
        '''
        server = smtplib.SMTP(self.config.get('email','SMTP_HOST'), 
                              int(self.config.get('email','SMTP_PORT')))
        server.ehlo()
        server.starttls()
        server.ehlo()
        sender_username = self.config.get('email','sender_email_addr')
        sender_passwd = self.config.get('email','sender_email_passwd')
        
        #Login TO SMTP Server
        server.login(sender_username, sender_passwd)
        
        msg = self.__getMsg()
        print msg.as_string()
        reciepents = [each.strip() for each in msg['TO'].split(',')]
        #server.sendmail(msg['FROM'].strip(), reciepents, msg.as_string()) #Send out the email
        server.close()

    
    
def parseOptions():
    parser = OptionParser()
    parser.add_option("-p", "--pid", dest="pid", 
                      help="ID of Process which got suspended")
    parser.add_option("-f","--cfg_file", dest="cfg_file",
                      help="config file having e-mail specific options"
                      )
    parser.add_option("-e","--exit_code", dest="exit_code",
                      help="Exit Code of the last script command executed which returned None Zero Exit Code"
                      )

    options, args = parser.parse_args()
    print options.__dict__

    if not (options.pid and options.cfg_file and options.exit_code):
        print "Probably missing one or more of mandatory arguments"
        parser.print_help()
        sys.exit(1)

    return options

def notify(cfgFile, pid, exit_code, email_type="error"):
    '''
    Send out the email, when ever this function is called
    '''
    cfg = parseConfiguration(cfgFile)
    info = getProcessInfo(int(pid))
    sender = email(info, cfg, exit_code, email_type)
    sender.notify()


if __name__=='__main__':
    options = parseOptions()
    
    if not os.path.exists(options.cfg_file):
        print "Mentioned configuration file - %s doesn't exist"%options.cfg_file
        sys.exit(1)
    if not os.path.exists('/proc/%s'%options.pid): #A linuxy hack!!
        print "No Process with this PID seem to be running - %s"%options.pid
        sys.exit(1)

    notify(options.cfg_file, options.pid, options.exit_code)
