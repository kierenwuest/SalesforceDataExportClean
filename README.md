# Salesforce Data Export Clean

This program cleans a folder's set of .csv files, that come from the Salesforce data backup export service, with 'All Objects' checked and the ISO-8859-1 Encoding setting.   
For the purpose of archiving and easier data loading that gets rid of unused files and columns.

It attempts to:
1. Remove irrelevant files (That have no data or specific identified irrelevant objects that contain data)
2. Remove columns from the csv's that have either no data or systemmod stamps.

To run the program, ensure Pyton 3 is installed.
In the terminal, enter "python3 _cleancsvs.py" in the folder containing the files

This code was created by Kieren Wuest with Python 3.9.6 and the help of GPT-4.

v0.2 This version handles NULL bytes and replaces them with space characters.  
v0.4 This version gives better feedback and fixes History and Summary files.   
v0.5 This version creates a log file called _cleancsvs_log.txt with the outputs of the programs actions for posterity.  
v0.6 This version outputs log actions (via use of the 'logging' module) to both termial and cleancsvs_log.txt.  
