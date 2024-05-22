#!/usr/bin/python3

"""
Connor Ede Copyright 2024

This program is to test and send an email with either an error or success message.
"""
import sys
import os
from datetime import datetime
from backupcfg import jobs, dspath, logPath, smtp
import pathlib
import shutil
import smtplib
    
"""
This is to send the email to the receipient.
"""
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
    
"""
When logging in.
"""
def logging(errorMessage, dateTimeStamp):
    try:
    
        file = open(logPath, "a")
         
        file.write(f"{errorMessage}.\n")
  
        
        file.close()
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")
    
"""
When error happens, date/time and error message will appear.
"""
def error(errorMessage, dateTimeStamp):
    print(f'FAILURE {errorMessage}')
    logging(f'FAILURE {errorMessage}', dateTimeStamp)    
    sendEmail(errorMessage)
    # email message
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          # write failure to log
    
"""
This is the main function.
"""
def main():
    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S") 
    argCount = len(sys.argv)
    
    if argCount != 2:
        error ("Error: jobname missing from command line", dateTimeStamp)
    else:
        jobname = sys.argv[1]
        
        if jobname not in jobs:
            error (f"ERROR: jobname {jobname} not defined.", dateTimeStamp)
        else:
            for source in jobs [jobname]:
                
                """
                If file source does not exist.
                """
                if not os.path.exists(source):
                    error("ERROR: file " + source + " does not exist.", dateTimeStamp)
                else:
                    
                    """
                    If directory destination does not exist.
                    """
                    if not os.path.exists(dspath):
                        error("ERROR: dirctory " + dspath + " does not exist.", dateTimeStamp)
                    else:
                        pass
                        
                        srcPath = pathlib.PurePath(source)
                        
                        dstLoc = dspath + "/" + srcPath.name + "-" + dateTimeStamp
                        
                        
                        if pathlib.Path(source).is_dir():
                            
                            """
                            When directory is copied.
                            """
                            shutil.copytree(source, dstLoc)
                            
                            """
                            When file is copied.
                            """
                            
                        else:
                            shutil.copy2(source, dstLoc)
                        logging(f'SUCCESS copied {source} to {dstLoc} ', dateTimeStamp)
   
   
   
   
   
if __name__== "__main__":
    main()
