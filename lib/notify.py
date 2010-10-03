from email.MIMEText import MIMEText
from email.Message import Message
import smtplib
import os,sys
from ConfigParser import ConfigParser

'''
This module notifier user, in case of error occures(script get suspended), Or any other event of interest occurs
Will require various configurable variables like ( like receiver_addrs,sender_address,sender_password,
smtp_host,smtp_port etc. etc.)

This information can be supplied as a configuration file having the required values.
'''

def parseConfiguration(cfgFile):
    config = ConfigParser()
    config.parse(cfgFile)
    return config

class email:
    def __init__(self,info,cfg):
        self.__validateCfg(cfg) #validate the cfg first
        self.config = cfg
        self.info = info

    def __validateCfg():
        '''
        This function will validate that the configuration file has all the necessary options
        '''
        required_options = ['SMTP_HOST','SMTP_PORT','sender_email_addr','sender_email_passwd',
                'recipient_email_addrs','test_message_title','title']
        for option in required_options:
            if not self.config.has_option('email',option):
                raise Exception("%s: is either missing or doesn't have a proper value, check sample cfg file"%option)

    def __getMsg(self):
        '''
        This constructs actual message to be sent out the user
        '''
        msg = Message()
        msg['From'] = self.config.get('email','sender_email_addr')
        msg['To'] = self.config.get('email','recipient_email_addrs')

        if self.info.get('type') == 'test': #If this is a test email to check if everything will work.
            msg['Subject'] = self.config.get('message','test_message_title')
        elif self.info.get('type') == 'error': #It's an actual error message
            msg['Subject'] = self.config.get('message','message_title')%info
        else:
            raise Exception('Notification can be of only following types : test,error')
        body = self.co
        msg.attad
        return msg

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
        reciepents = [each.strip() for each in msg['TO'].split(',')]
        print msg.as_string()
        #server.sendmail(msg['FROM'].strip(), recipients, msg.as_string()) #Send out the email
        server.close()

    
def notify(cfgFile,info):
    '''
    Send out the email, when ever this function is called
    '''
    cfg = parseConfiguration(cfgFile)
    sender = email(info,cfgFile)
    sender.notify()
    

