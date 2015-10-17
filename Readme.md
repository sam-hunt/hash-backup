# myBackup Readme!

###Member information###

 * number of members: 1
 * member name: **Samuel Hunt**
 * member ID: **14216618**
 * bitbucket user: [s14216618](https://bitbucket.org/s14216618/)
 * repo name: [251-A2-Hunt-Sam](https://bitbucket.org/s14216618/251-a2-hunt-sam)


###How to run the program###

 1. Run from the command line e.g. _**'"Python" "mybackup.py" "Command" "Argument"'**_ where:
    * _**"Python"**_ is your local installed version of Python 3.4 (I used Anaconda)
    * _**"mybackup.py"**_ is the absolute or relative path to my program's main module on your machine
    * _**"Command"**_ is one of my program's valid commands. If you get this wrong, my program will set you right though!
    * _**"Argument"**_ is specific to which myBackup Command you invoke. e.g. a directory or file pattern. Help is available on this.

 2. Or from Pycharm with a run configuration set up from run->edit configurations,   
    and with _**"Command" "Argument"'**_ in the script parameters text-box

 3. Valid commands are:
    * init
    * store `<directory`>
    * list [pattern]
    * test
    * get `<filename-or-pattern>`
    * restore [destination-directory]
    * help 

 4. Entering an invalid command will prompt you to what the valid commands are and terminate the program

 5. Entering a valid command with invalid argument will also tell you why it was invalid, then terminate the program

 6. Init should be used before other commands, however ignoring this will just prompt you to do this


###Folders###
 * The program consists of 3 modules: mybackup.py, mkfilsig.py, and logger.py

 * Also there is this read-me file. There are no other files/folders.

 * The program output folder is hardcoded to '~/myArchive' where '~' is the expanded current user home directory

   * There is only one instance of this hard-coded path at the top of the mybackup.py folder.   
     Feel free to change this at your leisure as all other paths which operate on the archive are relative to this  
   * You should ensure the program has elevated privileges or sufficient permissions to write to specified directories

 * The program will tell you where it outputs files (current working directory etc) if you don't specify an optional one


###Interesting commits (?)###
 * [b437596](https://bitbucket.org/s14216618/251-a2-hunt-sam/commits/b437596701ed078cf20cc464227d877a2accca11) **test command implemented.**    
   I also made changes to the store function so that re-adding inconsistent files will fix them.   

 * [a045525](https://bitbucket.org/s14216618/251-a2-hunt-sam/commits/a04552535d790dc28fdcf8b896cf90ef87c69ea0) **restore command implemented.**    
   Code is clean, succinct and functional.   

 * Disclaimer: as was similarly mentioned on the discussion forum, I also decided to break my commits into much smaller  
   chunks, so that rollback would be easier should it be required, and so that individual commits were more focused on   
   particular features. Anyway I did all of the work so it must count as a 'significant chunk' haha      

 * Also as I was working alone, I chose to just use the single master branch for commits. The reason for this was that alone the work is largely linear,    
   and I didn't think it would simplify the audit trail by have lots of commits across multiple branches for small bug fixes on a solo project.


###Notable features###
*  My descriptive help function.      
*  Switch construct in main rather than if-else ladder.      
*  Re-adding inconsistent files fixes them.      
*  Invalid commands reroutes to help.      
*  Many exceptions are instead handled further up the stack in main.     


###Future Improvements###

I would further improve the program by making the ARCHIVE_PATH variable rather than hard-coded and storing the path in a     
text file in the program folder etc.
Also adding compression using python's gzip lib functinos before hashing would make it more useful as a backup program,    
although you would have to ensure that the specific algorithm used isn't likely to become deprecated/removed anytime soon      
rendering all backups unrecoverable in newer python versions...     

Thanks for taking the time to read my readme and mark my assignment.   
Cheers, Sam