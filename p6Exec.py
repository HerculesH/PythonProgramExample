import sys
from p5Dict import printVariables, declareVar, printLabels

#Classes to raise exceptions
class TooFewOperands(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class VarNotDefined(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class LabelNotDefined(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class InvalidExpression(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class InvalidValueType(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

#Function which checks for a print statement and if so parses the file and updates dictionary

def checkForPrint(input, verbose, count):
   if("PRINT" in input.rstrip('\n')):
        splitVal = input.rstrip('\n').split()[1:]
        if(verbose == 1):
            printStatement = "executing line " + str(count) + ": " + str(' '.join(input.rstrip('\n').split()).replace("\"",""))
            print(printStatement)
        if("PRINT" in splitVal):
           splitVal = splitVal[1:]
           
        for (key,value), (key2,value2) in sorted(zip(printVariables().items(), declareVar().items())):
            if(key.lower() in splitVal):
                   splitVal[splitVal.index(key.lower())] = value2

        if(' '.join(splitVal).replace("\"","") != ' '):
            print(' '.join(splitVal).replace("\"",""))

#Function which checks for a assign statement and if so checks to make sure every assign operator is valid before preforming the operations, stores values in dictionary

def checkForAssign(input, verbose, count):
    if("ASSIGN" in input.rstrip('\n')):
      splitVal = input.rstrip('\n').split()[1:]
      
      if(verbose == 1):
          printStatement = "executing line " + str(count) + ": " + str(' '.join(input.rstrip('\n').split()).replace("\"",""))
          print(printStatement)
      if(len(splitVal) > 2):
          try:
              if(splitVal[0] == "" or splitVal[2] == "" or splitVal[3] == ""):
                raise
              else:
                  pass
          except:
              raise TooFewOperands("Too few operands",splitVal[0],splitVal[2])

          try:
              if(splitVal[0].upper() in declareVar() and splitVal[2].upper() in declareVar()):
                pass
              else:
                raise
          except:
              raise VarNotDefined("Variable not defined",splitVal[0],splitVal[2])
      
          shouldCheckForVar = True
          try:
              if(splitVal[3].isdigit()):
                iVal = int(splitVal[3])
                shouldCheckForVar = False
                pass
          except:
                raise InvalidValueType("Invalid value",splitVal[3])

          if(shouldCheckForVar):
              try:
                  if(splitVal[3].upper() in declareVar()):
                    pass
                  else:
                    raise
              except:
                  raise VarNotDefined("Variable not defined",splitVal[3])

          try:
              if(splitVal[1] == '+' or splitVal[1] == '-' or splitVal[1] == '*' or splitVal[1] == '&'):
                pass
              else:
                print("Invalid expression")
                raise
          except:
              raise InvalidExpression("Invalid expression",splitVal[1])

          if(splitVal[1] == '+'):
             tempval = 0
             if(splitVal[3].upper() in declareVar()):
                tempval = int(declareVar().get(splitVal[2].upper())) + int(declareVar().get(splitVal[3].upper()))
             else:
               tempval = int(declareVar().get(splitVal[2].upper())) + int(splitVal[3])
          elif(splitVal[1] == '*'):
              tempval = 0
              if(splitVal[3].upper() in declareVar()):
                 tempval = declareVar().get(splitVal[2].upper()).replace("\"","") * int(declareVar().get(splitVal[3].upper()))
              else:
                 tempval = declareVar().get(splitVal[2].upper()).replace("\"","") * int(splitVal[3])
          elif(splitVal[1] == '-'):
              tempval = 0
              if(splitVal[3].upper() in declareVar()):
                 tempval = int(declareVar().get(splitVal[2].upper())) - int(declareVar().get(splitVal[3].upper()))
              else:
                 tempval = int(declareVar().get(splitVal[2].upper())) - int(splitVal[3])
          elif(splitVal[1] == '&'):

              if(splitVal[3].upper() in declareVar()):
                   tempval = declareVar().get(splitVal[2].upper()) + splitVal[3]
              else:
                tempval = declareVar().get(splitVal[2].upper()) + splitVal[3]
              
          declareVar().update({splitVal[0].upper():str(tempval)})
      else:
        
        try:
            if(splitVal[0] is "" or splitVal[1] is ""):
                raise
            else:
                pass
        except:
             raise TooFewOperands("Too few operands",splitVal[0],splitVal[1])
                            
        try:
           if(splitVal[0].upper() in declareVar() and splitVal[1].upper() in declareVar()):
             pass
           else:
             raise
        except:
           raise VarNotDefined("Variable not defined",splitVal[0],splitVal[1])
          
        tempval = declareVar().get(splitVal[1].upper())
        declareVar().update({splitVal[0].upper():str(tempval)})

#Function which checks for a if statement and makes sure it is valid if, after returns the label to jump to
def checkForIf(input, verbose, count):
    if("Loop" not in input):
        input = "Loop " + input.rstrip('\n')
    
    if("IF" in input.rstrip('\n') or "if" in input.rstrip('\n')):
        splitVal = input.rstrip('\n').split()[1:]
        if(verbose == 1):
            printStatement = "executing line " + str(count) + ": " + str(' '.join(input.rstrip('\n').split()).replace("\"",""))
            print(printStatement)
        tempval = 0
        
        try:
            if(splitVal[2] is "" or splitVal[3] is ""):
                raise
            else:
                pass
        except:
            raise TooFewOperands("Too few operands",splitVal[1],splitVal[2])
        
        shouldCheckForVar = True
        try:
            if(splitVal[2].isdigit() and splitVal[3].upper() in declareVar()):
                iVal = int(splitVal[2])
                shouldCheckForVar = False
            pass
        except:
            raise InvalidValueType("Invalid value",splitVal[2])

        if(shouldCheckForVar):
            try:
                if(splitVal[2].upper() in declareVar() and splitVal[3].upper() in declareVar()):
                    pass
                else:
                    raise
            except:
                raise VarNotDefined("Variable not defined",splitVal[2],splitVal[3])

        try:
            if(splitVal[1] == '>' or splitVal[1] == '>='):
                pass
            else:
                raise
        except:
            raise InvalidExpression("Invalid expression",val)
        
        try:
            if(splitVal[4].upper() in printLabels()):
                pass
            else:
                raise
        except:
            raise VarNotDefined("Label not defined",splitVal[4])
        try:
            if(splitVal[1] == '>'):
                if(splitVal[2].isdigit() and splitVal[3].upper() in declareVar()):
                    tempval = int(splitVal[2]) > int(declareVar().get(splitVal[3].upper()))
                elif(splitVal[2].upper() in declareVar() and splitVal[3].upper() in declareVar()):
                    tempval = int(declareVar().get(splitVal[2].upper())) > int(declareVar().get(splitVal[3].upper()))
                elif(splitVal[2].isdigit() and splitVal[3].upper() in declareVar()):
                    tempval = int(declareVar().get(splitVal[2].upper())) > int(splitVal[3])
                else:
                    tempval = int(declareVar().get(splitVal[2].upper())) > int(declareVar().get(splitVal[3].upper()))
            else:
                if(splitVal[2].isdigit() and splitVal[3].upper() in declareVar()):
                    tempval = int(splitVal[2]) > int(declareVar().get(splitVal[3].upper()))
                elif(splitVal[2].upper() in declareVar() and splitVal[3].upper() in declareVar()):
                    tempval = int(declareVar().get(splitVal[2].upper())) > int(declareVar().get(splitVal[3].upper()))
                elif(splitVal[2].isdigit() and splitVal[3].upper() in declareVar()):
                    tempval = int(declareVar().get(splitVal[2].upper())) > int(splitVal[3])
                else:
                    tempval = int(declareVar().get(splitVal[2].upper())) >= int(declareVar().get(splitVal[3].upper()))

            return(tempval,splitVal[4])
        except:
            raise InvalidValueType("Invalid value",splitVal[2],splitVal[3])
    else:
      return(False,"")

#Checks the goto statement and returns true along with the label if valid
def checkForGoto(input, verbose, count):
    if("GOTO" in input.rstrip('\n')):
      splitVal = input.rstrip('\n').split()[1:]
      if(verbose == 1):
          printStatement = "executing line " + str(count) + ": " + str(' '.join(input.rstrip('\n').split()).replace("\"",""))
          print(printStatement)
      return(True,splitVal[0] + ":")
    else:
      return(False,"")
