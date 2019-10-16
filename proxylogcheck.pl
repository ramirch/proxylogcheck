##################################################

# Author:      Christopher Ramirez
# Program:     Proxy Log File Analyser (PERL Script)
# Version:     1.0
# Class:       3662C Develop Software
# Instructor:  John Chetcuti
# Date:        14-10-2005

# Description:  This program will process the entries in the proxy logs 
               # generated each day and extract only the information 
               # required and present it in a suitable format.

##################################################

#------------------------
# GETTING SYSTEM TIME 
#------------------------

#_________________________________________
# Import the time functions from time module
# Get the current time
# Get the system month (full form, eg. October)
# Get the system day
# Get the system month (in short form eg. Oct)
#_________________________________________


use POSIX qw(strftime);
($Second, $Minute, $Hour, $DayOfMonth, $Month, $Year, $Weekday, $DayOfYear, $IsDST) = gmtime(time);
$Month = strftime("%B", gmtime);              
$DayOfMonth = strftime("%d", gmtime);         
$MonthDay = $Month . " " . $DayOfMonth ;       
$ShortMonth = strftime("%b", gmtime);


#-------------------------------------
# CHECKING FOR LOG FILE
#-------------------------------------

#_______________________________________________________________
# Setting the format of proxy log file as a text document
# If the proxy log file exists
    # Open the proxy file, ready for reading
# Else
    # There may be no proxy log file generated today
#_______________________________________________________________

$ProxyLog = "access " . $DayOfMonth . " " . $ShortMonth . ".txt";

if (-e $ProxyLog) {
    print "Proxy log file for ", $DayOfMonth . " " . $Month, " exists and will now be read!\n";
    print "\n";
    $OpenLog = open(PROXYLOG, "$ProxyLog");
        
}
else {
    print "No proxy log file for today."

} 


#-------------------------------------
# READING AND EXTRACTION FROM THE FILE
#-------------------------------------

#________________________________________________________________

# Read lines in the proxylog file
# sets up an output file as a list
# While the proxy log file is read
    # If "Forbidden" is found in the line
        # Create index point for start position of the username
        # Increment username length
        # Extract the username from the file
        # Increment URL start position
        # Extract the full URL from the line
#________________________________________________________________
    
$proxyline = <PROXYLOG>;         
@UsernameURLList = ();    
while ($proxyline) {             
    if ($proxyline =~ /Forbidden/i) {                      
        $IndexToUser = index($proxyline, ",", 22);         
        $Length = $IndexToUser - 22;                       
        $NaughtyUser = substr $proxyline, 22, $Length;     
        $StartURL = $IndexToUser + 13 ;                                        
        $FullURL = substr $proxyline, $StartURL;        

        
        # This section extracts a URL from the file. Some URLs differ from each other.
        # It finds the first slash, colon or space of a certain URL in the line and then extracts it
        # from the incremented URL start point to the index point.
          
        
        if (index($FullURL, "/") != -1) 
        {
            $EndURL = index($FullURL, "/");
            $URL = substr $FullURL, 0, $EndURL;
        }
        elsif (index($proxyline, ":") != -1) 
        {
            $ColonIndex = index($FullURL, ":") ;
            $URL = substr $FullURL, 0, $ColonIndex;
        } 
        elsif (index($FullURL, " ") != -1) 
        {
            $SpaceIndex = index($FullURL, " ");
            $URL = substr $FullURL, 0, $SpaceIndex;
        }

        # Concatenate strings to form a data structure to how the lines will be written to the user file
        # Create list and add the lines to the list
        # Reads the next line in the file

        $UsernameURL = $DayOfMonth ."  ". $NaughtyUser . "  " . $URL . "\n";  
        push(@UsernameURLList, $UsernameURL);                             
        $proxyline = <PROXYLOG>;                                          
    }
}

#----------------------------------------------------
# REMOVING DUPLICATE ENTRIES FROM THE LOG FILE
#----------------------------------------------------

# A hash is used to keep a record of any lines that have been seen
# Set up a list that will hold all the unique entries
# For each line in the list
    # It will then check for duplicates ignoring more than one instance of the same line
# The unique lines are added to the list
# Sort the output list into alphabetical order
# Display the output list with all the duplicates removed

%seen = ();                             
@UniqueList = ();                       
foreach $proxyline (@UsernameURLList) {
    $seen{$proxyline}++;                
}
@UniqueList = keys %seen;            
@NoDupesList = sort @UniqueList;     
print @NoDupesList;                  


#-----------------------------------------------------------
# DIRECTORY HANDLING
#-----------------------------------------------------------

# The root directory is set up
# The sub-directory in the main directory path is set up for storage of user files
           
$PathSep = "\\";
$MonthDir = $Month;
$Forbidden_Path = "C:\\Forbidden" ;                        
$ForbiddenMonthPath = $Forbidden_Path . $PathSep . $MonthDir ;   


# This checks whether the main root directory exists and if not, then it will be created.

if(-e $Forbidden_Path){
    print "--------------------------------------------------------------------------------\n";
    print "\n";
    print $Forbidden_Path, " already exists.\n";
    } 
else {
    print "--------------------------------------------------------------------------------\n";
    print "\n";
    print $Forbidden_Path, " does not exist. Constructing directory now.\n" ;   
    mkdir($Forbidden_Path);        
    }

# This checks whether the month directory exists. If not, then it will be created.

if(-e $ForbiddenMonthPath){
    print $ForbiddenMonthPath, " already exists.\n";
    } 
else {
    print $MonthDir, " directory does not exist. Constructing directory now.\n";
    mkdir($ForbiddenMonthPath);   
    }

#--------------------------------------------------------------------
# FILE HANDLING
#--------------------------------------------------------------------

# For each user who has been accessing Forbidden sites each day, a text file is generated for each user. 
# The information that is included in the text file is the date, the user and the URL that they have visited. 
# If a user has visited a site a number of times, their "crime" will only be represented as one entry per unique site. 
# A user may have accessed 5 websites which means that 5 unique entries will be added to the file.

 
# Initialise the current user
# For each line in the list
    # Create index point for username
    # Increment username length
    # Extract username from the line
    # If username is not the current user
        # Set the name of file generated under the following format
        # Set up the filepath to store the generated file
        # Generate the text file which is then ready for writing
        # Write the lines to the user files
    # Else
        # Write the Lines to the user files
    
$Current_User = "snoopdogg";                                                                                    
foreach $proxyline (@NoDupesList) {
    $IndexUser = index($proxyline, " ", 4);                              
    $Length = $IndexUser - 4;                                            
    $UsernameInLine = substr $proxyline, 4, $Length;                     
    if ($UsernameInLine ne $Current_User) {                              
        $NaughtyUserFile = $DayOfMonth . $UsernameInLine . ".txt";       
        $Filename = $ForbiddenMonthPath . $PathSep . $NaughtyUserFile;   
        $NaughtyFile = open(FILENAME, ">$Filename");                     
        $WriteInfo = print FILENAME $proxyline;                          
        $Current_User = $UsernameInLine;
    }
    else {
          $WriteInfo = print FILENAME $proxyline;
        }  
}
close(PROXYLOG);