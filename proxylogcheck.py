##################################################
"""
  Author:      Christopher Ramirez
  Program:     Proxy Log File Analyser (Python Script)
  Version:     1.0
  Class:       3662C Develop Software
  Instructor:  John Chetcuti
  Date:        12-10-2005
  Description:  WWIT4 uses a program known as FreeProxy to crack down on users/students accessing
                forbidden sites that do not relate to their work or learning. A proxy log file is generated
                each day for the Administrators to view but it does not make it for easy readability.

                This script will solve this problem as it will open the proxy log file and only extract
                the information required (the username and forbidden website). This information will be
                then presented in a suitable format making it a better way for Administrators for viewing proxy
                logs.
"""
##################################################

#----------------------------------------
# GETTING SYSTEM TIME
#----------------------------------------

# Import time functions
# Get system day
# Get system month (full month)
# Get system month (short form)

from time import localtime, strftime           
Day = strftime("%d", localtime())               
Month = strftime("%B", localtime())
ShortMonth = strftime("%b", localtime())

#-----------------------------------------------
# CHECKING IF THE DAILY PROXY LOG FILE EXISTS
#-----------------------------------------------

# Importing the os and sys modules
# Setting up the name of the proxy log file to be read
# This checks whether the proxy log file exists
    # Opens up the proxy log for reading
# Else
    # There may be no proxy log file generated for the day
    # Generate an event to the event log

import os
import sys
import logging

ProxyLog = "access " + Day + " " + ShortMonth + ".txt"
print(ProxyLog)

if os.path.isfile(ProxyLog):
    print(f"Proxy Log for {Month} {Day}, exists and will now be read!")
    MY_FILE = open(ProxyLog, 'r')
else:
    from logging.handlers import NTEventLogHandler
    logger = logging.getLogger('ProxyLogCheck')
    handler = NTEventLogHandler("ProxyLogCheck")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info("No proxy file for today!")
    
    
#-------------------------------------------------------
# READING AND EXTRACTING INFORMATION FROM THE LOG FILE
#-------------------------------------------------------

# Read the proxy log file one line at a time
# Initialise UsernameURLList as a list

# While the proxy log file is being read
    # Initialise "Forbidden" count
    # If a Forbidden item is found in the proxy file
        # Create index point for the username
        # Initialise Naughty_User to extract username
        # These IF tests are done to find the first slash, space, colon of certain URL's
        # Initialise URL to extract URL based on the index points
        # Concatenate strings to form data structure
        # Add the string to the list
        # Read next line

proxyline = MY_FILE.readline()
UsernameURLList = []
while proxyline:                                  
    Forbiddens = proxyline.count("Forbidden")     
    if Forbiddens:                                
        IndexToUser = proxyline.find(",", 22)            
        Naughty_User = proxyline[22:IndexToUser]
        StartURL = IndexToUser + 13   
        EndURL = proxyline.find("/", StartURL)
        if EndURL != -1:
            URL = proxyline[StartURL:EndURL]
        else:
            EndURL = proxyline.find(":", StartURL)
            if EndURL != -1:
                URL = proxyline[StartURL:EndURL]
            else:
                EndURL = proxyline.find(" ", StartURL)
                URL = proxyline[StartURL:EndURL]    
                                                                                                 
        Username_URL = Day + "  " + Naughty_User + "  " + URL + "\n"     
        UsernameURLList.append(Username_URL)                             
        proxyline = MY_FILE.readline()

#_____________________________________________________________

                                   
#--------------------------------------------
# REMOVING DUPLICATE ENTRIES IN THE LOG FILE
#--------------------------------------------

# Temporarily converts the list into a dictionary and then back to a list
# Sorts the list into alphabetical order
# Prints output file with all the duplicate items removed from the list


NoDupesList = dict([(i,0) for i in UsernameURLList]).keys()
sorted(NoDupesList)
#NoDupesList.sort()                       
print(NoDupesList)


#---------------------------------------------------------
# DIRECTORY HANDLING
#---------------------------------------------------------

# Initialise path separator
# Set the main directory path to where the folders generated for each month will be stored
# Sets up the sub-directory path to where the generated user files will be stored

# If the main directory does not exist 
    # Construct the directory
    # Else, it already exists

# If the month sub-directory does not exist
    # Construct the directory
    # Else, it already exists

#____________________________________________________________
                                                
PathSep = "\\"                                           
Forbidden_Path = "C:\Forbidden"                       
ForbiddenMonthPath = Forbidden_Path + PathSep + Month    
    

if not os.path.isdir(Forbidden_Path):                        
    print
    print("Forbidden directory does not exist. Making directory now.")
    os.mkdir(Forbidden_Path)    
else:
    print
    print("Forbidden directory already exists")


if not os.path.isdir(ForbiddenMonthPath):   
    print
    print(f"{Month} directory does not exist. Making directory now.")
    os.mkdir(ForbiddenMonthPath)
else:
    print(f"{Month} directory already exists.")

#_____________________________________________________________


#-------------------------------------
# FILE HANDLING
#-------------------------------------


"""
For each user who has been accessing Forbidden sites each day, a text file is generated for that user. 
The information that is included in the text file is the date, the user and the URL that they have visited. 
If a user has visited a site a number of times, their "crime" will only be represented as one entry per unique site. 
A user may have accessed 4 websites that day which means that 4 unique entries will be added to that user file.

Example: 13 student054 www.cisco.com
         13 student054 www.hookers.com.au
         13 student054 www.chopsuey.com
         13 student054 www.mp3-mania.co.uk

"""
# Initialise the current user

# For each line in the list
    # Create index point for the user
    # Increment username length
    # Extract username from line
    # If the username value is not equal to the current user value
        # If the generated file is open
            # Close the file
        # Sets the format of the file as a text file
        # Sets the filepath as to where the generated file is to be stored
        # Generates the file, ready for writing
        # Write the lines to the user files
        # Sets the user to the current user value


#____________________________________________________________


Current_User = "snoopdogg"                    
NaughtyFile = MY_FILE
NaughtyFile.close()

for proxyline in NoDupesList:                 
    IndexUser = proxyline.find(" ", 4)        
    UsernameInLine = proxyline[4:IndexUser]   
    if UsernameInLine != Current_User:           
        if NaughtyFile is open:                        
            NaughtyFile.close()                                  
        NaughtyUserFile = Day + UsernameInLine + ".txt"                   
        Filename = ForbiddenMonthPath + PathSep + NaughtyUserFile  
        NaughtyFile = open(Filename, 'w')                                 
        WriteInfo = NaughtyFile.write(proxyline)                
        Current_User = UsernameInLine

        from logging.handlers import NTEventLogHandler
        logger = logging.getLogger("ProxyLogCheck")
        handler = NTEventLogHandler("ProxyLogCheck")
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
        Message = "A file for", UsernameInLine, "has been created as a consequence of accessing forbidden websites." 
        logger.warning(Message)                 
    else:
        WriteInfo = NaughtyFile.write(proxyline)


   
#____________________________________________________________

MY_FILE.close()         # Close the file
    







