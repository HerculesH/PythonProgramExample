import fileinput
import sys
# imports functions to be used
from p5Dict import printVariables, declareVar, printLabels, getLabel, getType, getValue
from p6Exec import checkForPrint, checkForAssign, checkForIf, checkForGoto

#Function which executes the operations on each variable and label
def executionFunc():
    #label dictionary
    labelErrorDic = {}
    #resets the counter to be used for execution
    count = 0
    #Tuple used for the checkForIf function
    afterIf,JumpToAfterIf = (False,"")
    #Tuple used for the checkForGoto function
    loopShouldStart,JumpToLoop = (False,"")
    #Variable which is used as an boolean to decide if the loop statements should be saved in order
    #to iterate over them
    shouldGetLoop = 0
    #Counter variable to check if an infinite loop has been triggered
    infiniteloop = 0
    #Array which saves the text fileinput loop in order to iterate over it
    getStatementArr = []
    intro = "execution begins ..."
    print(intro)
    #Iterates over the text file
    for input in fileinput.input():
        
        #Checks for label re-declaration errors in the text file
        #Uses a dicitonary to check and if found prints error message
        splitVal = input.rstrip('\n').split()[:1]
        if(':' in splitVal):
            if(splitVal in labelErrorDic):
                print('***Error: label %s appears on multiple lines: %d and %d)' % (splitVal,labelErrorDic[splitVal],count))
            labelErrorDic.update({splitVal:str(count)})
        #Checks if the first word on the text line starts with the goto statement or jump statement
        #Triggers booleans if so used for looping and executing
        if(input.rstrip('\n').startswith(JumpToLoop)):
            loopShouldStart = False
            afterIf = False
        else:
            if(input.rstrip('\n').startswith(JumpToAfterIf)):
                afterIf = False
        #Checks if loop is in the line read, if so saves the next lines to iterate over
        if("Loop" in input and "GOTO" not in input):
            getStatementArr = []
            shouldGetLoop = 1
        #If goto statement seen then stops the saving of loop lines
        if("GOTO" in input):
           shouldGetLoop = 0
           
        if(shouldGetLoop == 1):
            getStatementArr.append(input)

        #Calls each method in p6Exec in order to execute statements
        #Uses booleans to decide if should execute
        if(len(input.split()) != 0 and afterIf == False and loopShouldStart == False):
        
            try:
                #Function executions
                splitIt = input.rstrip('\n').split()[0:1]
                count += 1
                contLoop = 0
                checkForPrint(input,verbose,count)
                checkForAssign(input,verbose,count)
                afterIf,JumpToAfterIf = checkForIf(input,verbose,count)
                
                if(afterIf == False and JumpToAfterIf == ""):
                    loopShouldStart,JumpToLoop = checkForGoto(input,verbose,count)
                    if(loopShouldStart == False and JumpToLoop == "" or len(getStatementArr ) == 0):
                        afterIf = True
                        pass
                    else:
                        try:
                            #If loop encountered will start executing and iterating over saved loop
                            savedCount = count - len(getStatementArr)
                            infiniteloop = 0
                            while(contLoop == 0):
                                infiniteloop += 1
                                if(infiniteloop > 5000):
                                    raise
                                innerCount = savedCount
                                for l in getStatementArr:
                                    splitIt = l.rstrip('\n').split()[0:1]
                                    innerCount += 1
                                    checkForPrint(l,verbose,innerCount)
                                    checkForAssign(l,verbose,innerCount)
                                    afterIf,JumpToAfterIf = checkForIf(l,verbose,innerCount)
                                    #If end of loop and conditions are met then breaks out of it
                                    if(afterIf == True):
                                        afterIf = False
                                        loopShouldStart = False
                                        contLoop = 1
                                        break
                        except Exception as e:
                            print ("*** line error detected @ line:",innerCount)
                            print("Error:", e)
                            break
                        except:
                            print ("*** line error detected @ line:",innerCount)
                            traceback.print_exc()
                            break

                pass
            except Exception as e:
                print ("*** line error detected @ line:",count)
                print("Error:", e)
                break
            except:
                print ("*** line error detected @ line:",count)
                traceback.print_exc()
                break


# count variable to keep track of each number line read
start = 0
count = 0
verbose = 0
# loop which gets the input file passed and reads each line
# If count is 0 then print start statement
# checks if the line read is not a blank line or empty spaces
# Splits the line in to a list and passes it to the functions imported

#Checks if verbose mode is implemented
if(len(sys.argv) == 3):
    if(sys.argv[2] == "-v"):
         verbose = 1
         sys.argv = [sys.argv[0],sys.argv[1]]

for input in fileinput.input():
    if(start == 0):
       intro = "BEEP source code in "
       fileNameInput = fileinput.filename() + ':'
       print(intro + fileNameInput)
    start += 1
    
    if(len(input.split()) != 0):
       splitIt = input.rstrip('\n').split()[0:1]
       getType(input)
       getLabel(splitIt, input, count)
       count += 1
       p = str(count) + '. ' + input.rstrip('\n') 
       print(p)

print("Variables:")
print("    Variable     Type      Value   ")
# prints each dictonary value and key in sorted order
for (key,value), (key2,value2) in sorted(zip(printVariables().items(), declareVar().items())):
    p = ' '.ljust(4) + key.ljust(13) + value.ljust(10) + value2.ljust(10)
    print(p)

print("Labels:")
print("    Label        Statement")
for (key,value) in sorted(printLabels().items()):
    p = ' '.ljust(4) + key.ljust(13) + value.ljust(10)
    print(p)

executionFunc()


