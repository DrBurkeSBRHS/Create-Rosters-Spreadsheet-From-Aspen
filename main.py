"""Student Spreadsheet Creator

This program takes in a student roster that is output by Aspen 
and creates a spreadsheet of all the students in all the classes 
that a teacher has. Each line will be one student record. 

Columns: Last Name 
         First Name 
         Section number
         Class Name
         Full Class Name

The file will be tab-delimited so that it can be imported into an
Excel spreadsheet.
Once in a spreadheet, students can be sorted into classes, or into sections,
or any other way.
"""

import re

# fname is a string to contain the name of the file
fname = input("What is the name of the file? [Leave blank for 'report.csv']: ")
if (fname == ""):
  fname = "report.csv"

# file is a handle to a data file
file = open(fname)
# source_lines is a list of lines from the source file
source_lines = file.readlines()

# outfile is a handle to the output file
outfile = open("output.txt","w")
outfile.write("LNAME\tFNAME\tSECNUM\tCLASS\tFULLCLNAME\n")

# strings to hold the column data
fname = ""
lname = ""
secnum = ""
clname = ""
# fullclname is a string that contains the class name
#            including the level 
fullsecname = "" 
# minisecnum is the number for duplicate sections
minisecnum = 0

# done is a boolean to end the loop
done = False
# linecount is an integer to keep track of where we are in the source_file
linecount = -1
# temptarget is a list that will hold the regex search results temporarily
temptarget = []
# stucount is an int to hold the number of students in each section
stucount = 0
# these lists are a temporary list of students in an individual section
fnameslist = []
lnameslist = []

stutotal = 0

def getStudentLists(thesource, theplace, howmany):
  """
  Extract all student first and last names from the source
  file lines and place them in two parallel lists
  """
  #print(howmany)
  fnames = []
  lnames = []
  for count in range(theplace,theplace+howmany):
    #print(thesource[count])
    lnames.append(re.findall("\"([^,]+)",thesource[count])[0])
    fnames.append(re.findall(", ([^\"]+)",thesource[count])[0])    
  return lnames,fnames


# For every line in the source file we are going to read look for the
# class names and then for student names. For each student, several
# columns will be created, and then those records will be written to the output file
# so that there is one line per student-in-a-class

while (not done):
  while(not temptarget):
    linecount+=1
    temptarget = re.findall("Page \d+", source_lines[linecount])
  linecount+=1
  secnum = re.findall("\d{6}-\d{2}",source_lines[linecount])[0]
  minisecnum = secnum[7:9]
  fullsecname = re.findall("\d: ([^,]+)",source_lines[linecount])[0]
  clname = re.findall("[^(]+", fullsecname)[0].strip() + " " + minisecnum
  # print(secnum + " -- " + fullsecname + " -- " + clname)
  temptarget = []
  while(not temptarget):
    linecount+=1
    temptarget = re.findall("Total Students: (\d+)", source_lines[linecount])
  stucount = int(temptarget[0])
  #print(stucount)
  stutotal += stucount
  #print(stutotal)
  temptarget = []
  lnameslist,fnameslist = getStudentLists(source_lines,linecount-stucount,stucount)
  #print(fnameslist)
  #print(lnameslist)
  ct = 0
  for afname in fnameslist:
    outfile.write(lnameslist[ct] + "\t" +  afname + "\t" + secnum + "\t" + clname + "\t" + fullsecname + "\n")
    ct+=1
  print("Processed " + clname)
  if (linecount+1 == len(source_lines)):
    done = True





outfile.close()
file.close()

