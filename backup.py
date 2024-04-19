#!/usr/bin/python3

import sys
import os
from datetime import datetime
from backupcfg import jobs, dspath, logPath, smtp
import pathlib
import shutil
import smtplib
    
    
def sendEmail(message):

    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + message + '\n'

    # connect to email server and send email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
                                                                                                                                                                                                                               
    except Exception as e:
        print("ERROR: An error occurred.")
    
 
def logging(errorMessage, dateTimeStamp):
    try:
    
        file = open(logPath, "a")
        
        file.write(f"Failure {errorMessage}.\n")
  
        
        file.close()
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")
    
    
    
def error(errorMessage, dateTimeStamp):
    print(f'FAILURE{errorMessage}')
    logging(f'FAILURE{errorMessage}', dateTimeStamp)
    sendEmail(errorMessage, dateTimeStamp)
    # email message
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          # write failure to log
    
    sendEmail(errorMessage)

def main():
    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S") 
    argCount = len(sys.argv)
    if argCount != 2:
        error("Error: jobname missing from command line", dateTimeStamp)
    else:
        jobname = sys.argv[1]
        if jobname not in jobs:
            error(f"ERROR: jobname {jobname} not defined.", dateTimeStamp)
        else:
            source = jobs [jobname]
            if not os.path.exists(source):
                error("ERROR: file " + source + " does not exist.", dateTimeStamp)
            else:
                if not os.path.exists(dspath):
                    error("ERROR: dirctory " + dspath + " does not exist.", dateTimeStamp)
                else:
                    pass
                    
                    srcPath = pathlib.PurePath(source)
                    
                    dstLoc = dspath + "/" + srcPath.name + "-" + dateTimeStamp
                    
                    if pathlib.Path(source).is_dir():
                        shutil.copytree(source, dstLoc)
                    else:
                        shutil.copy2(source, dstLoc)
   
   
   
   
   
if __name__== "__main__":
    main()
