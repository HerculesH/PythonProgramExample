# Creates each empty dictornary
varValueD = {}
varTypeD = {}
labelD = {}
# gets a list and checks if the first item is a label
# if so creats a temporary label and removes the : character
# checks if the item exists in the dictionary and prints an statement if so
# Stores it in the label dictionary
def getLabel(splitIt, input, count):
   if(splitIt[0].endswith(':')):
       splitVal = input.rstrip('\n').split()[1:4]
       tempLabel = splitIt[0]
       tempLabel = tempLabel[:-1]
       if(tempLabel.upper() in labelD):
          print("***Error: label " + tempLabel + " appears on multiple lines: " + str(labelD.get(tempLabel.upper())) + " and " + str(count + 1))           
       labelD.update({tempLabel.upper():str(count + 1)})

# Function to get variables
# cgets an line and parses it to see if it is a variable
# if so splits the line in to a list
# Stores the type and passes the list to the Value function
def getType(input):
   if(input.rstrip('\n').startswith("VAR")):
       splitVal = input.rstrip('\n').split()[1:4]
       varTypeD.update({splitVal[1].upper():splitVal[0].upper()})
       getValue(splitVal)

# Function to get the value
# checks if there is a empty value in the value slot of the line passed
# if so stores it in the value dictionary, if not then stores it with an empty string
def getValue(splitVal):
   if(splitVal[-1] != splitVal[1]):
        varValueD.update({splitVal[1].upper():splitVal[-1]})
   else:
        varValueD.update({splitVal[1].upper():' '})

# functions to get the dictionary instances
def declareVar():
   return varValueD

def printVariables():
   return varTypeD

def printLabels():
   return labelD
