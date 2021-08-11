
#The Assembler for the Femto-4 found on CircuitVerse.
#Refer to Developer Guide.txt if you want to understand what this is for. 

debug = True
if debug:
  print("Running")


#This thing was not programmed to be robust. 

#Useful lists for coversions 
HexAddOn = "0x"
hexConv = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

supportedChars = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
charConvertor = {" ": 32, "!": 33, "\"": 34, "#": 35, "$": 36, "%": 37, "&": 38, "\'": 39, "(": 40, ")": 41, "*": 42, "+": 43, ",": 44, "-": 45, ".": 46, "/": 47, "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57, ":": 58, ";": 59, "<": 60, "=": 61, ">": 62, "?": 63, "@": 64, "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74, "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84, "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "[": 91, "\\": 92, "]": 93, "^": 94, "_": 95, "`": 96, "a": 97, "b": 98, "c": 99, "d": 100, "e": 101, "f": 102, "g": 103, "h": 104, "i": 105, "j": 106, "k": 107, "l": 108, "m": 109, "n": 110, "o": 111, "p": 112, "q": 113, "r": 114, "s": 115, "t": 116, "u": 117, "v": 118, "w": 119, "x": 120, "y": 121, "z": 122, "{": 123, "|": 124, "}": 125, "~": 126}

#Adds two hexadecimal digits together. Does not handle overflows
def hex_digit_add(a,b):
  return hexConv[(hexConv.index(a) + hexConv.index(b)) % 16]

#Combines the two parts of an ALU instruction into one opcode
def add_ALU_codes(opcode, ALUcode):
  global hexReplace
  return opcode[0] + hex_digit_add(opcode[1],ALUcode[0]) + ALUcode[1:3]

#Combines the two parts of a JPF instruction into one opcode
def add_JPF_codes(opcode, FLAGcode):
  global hexReplace
  return opcode[0:2] + hex_digit_add(opcode[2],FLAGcode[0]) + FLAGcode[1]

#Converts decimal values (as integers) to hexadecimal values (as strings). 
def decimal_to_hex(x):
  out = ""
  while x != 0:
    out = hexConv[x % 16] + out
    x = x//16
  return out

def formattedDecimalToHex(x):
  out = ""
  while x != 0:
    out = hexConv[x % 16] + out
    x = x//16
  if len(out) > 4:
    out = out[len(out)-4:len(out)]
  elif len(out) < 4:
    out = "0" * (4-len(out)) + out
  return out

#Converts hexadecimal values (as strings) to decimal values (as integers).
def hex_to_decimal(x):
  out = 0
  for digit in x:
    out *= 16
    out += hexConv.index(digit)
  return out

def convertCharIntoDecimal(character):
  if len(character) != 2:
    raise Exception("Invalid char in: " + character)
  elif character[0] != "\'":
    raise Exception("Invalid char in: " + character)
  else:
    return charConvertor[character[1]]

def assembler():
  #Basic opcodes
  AssemblyCodes1 = {"PWS": "0000", "GRF": "0001", "NOP": "0002", "LDV": "1000", "LDD": "1001", "LDI": "1002", "LDP": "1004", "LDA": "1005", 
                    "LIV": "1008", "LID": "1009", "LII": "100a", "LIP": "100c", "LIA": "100d", "PSV": "4000", "PSD": "4001", 
                    "PPD": "4002", "PSI": "4003", "PPI": "4004", "JMP": "5000", "JPD": "5001"}
  #ALU opcodes
  AssemblyCodes2 = {"ANR": "20", "ANV": "24", "AND": "28", "ANB": "2c", "ALR": "30", "ALV": "34", "ALD": "38", "ALB": "3c"}
  ALUCodes = {"ADD": "0a8", "SBA": "198", "SBB": "168", "ICA": "188", "ICB": "128", "DCA": "0b8", "DCB": "0e8", "NGA": "148", 
              "NGB": "118", "NTA": "040", "NTB": "010", "ORR": "0ad", "NOR": "051", "AND": "0a1", "NND": "05d", "XOR": "0a0", 
              "XNR": "0ac", "SLA": "0ba", "SLB": "0ca", "INA": "080", "INB": "020", "HGH": "0c0", "LOW": "000", "SRA": "200", 
              "SRB": "201", "MLT": "202", "DVA": "204", "DVB": "205", "LSA": "208", "LSB": "209", "RSA": "20c", "RSB": "20d", 
              "XAD": "210", "XSA": "211", "XSB": "212", "CAD": "220", "CSA": "221", "CSB": "222", "CSL": "223", "CNG": "224", 
              "CAT": "230", "CSR": "231"}
  #Flag jump opcodes
  AssemblyCodes3 = {"JPF": "504", "JDF": "508"}
  #Bit test jump opcodes
  AssemblyCodes4 = {"JPB": "50c", "JDB": "50e"}
  #Clock jump opcodes
  AssemblyCodes5 = {"JPC": "5100", "JDC": "5102"}
  #Expected number of data chunks for each opcode
  AssemblyNumber = {"PWS": 1, "GRF": 1, "LDV": 3, "LDD": 3, "LDI": 3, "LDP": 2, "LDA": 2, "LIV": 3, "LID": 3, "LII": 3, "LIP": 2, 
                    "LIA": 2, "PSV": 2, "PSD": 2, "PSI": 2, "PPD": 2, "PPI": 2, "JMP": 2, "JPD": 2, "ANR": 3, "ANV": 4, "AND": 4, 
                    "ANB": 4, "ALR": 4, "ALV": 5, "ALD": 5, "ALB": 5, "JPF": 3, "JDF": 3, "JPB": 3, "JDB": 3, "JPC": 3, "JDC": 3}

  #Flag jump opcodes. Not really that useful since a direct compare operation doesn't exist
  FlagJumpCodes = {"SGR": "0a", "EQL": "03", "ELS": "0c", "SLS": "0e", "NQL": "02", "CRY": "0c", "NCY": "08"}

  #List of preset variables, mostly of ASCII characters. 
  addresses = {"TTY": "3200", "OUTPUT": "3201", "CTRLR1P": "3000", "CTRLR1H": "3001", "CTRLR2P": "3002", "CTRLR2H": "3003", 
               "KYBD": "3004", "RND": "00ff", "MODE": "00ca", "PRCT": "00cb", "SELECT": "00cc", "STKPNTR": "00b0", "ACC2": "00c7", 
               "FLG": "00c8", "BinaryToBCD": "c000" , "BCDToASCII": "c01d", 
               "SPR0COORD": "33c0", "SPR0CLR": "33c1", "SPR1COORD": "33c2", "SPR1CLR": "33c3", "SPR2COORD": "33c4", "SPR2CLR": "33c5", 
               "SPR3COORD": "33c6", "SPR3CLR": "33c7", "SPR4COORD": "33c8", "SPR4CLR": "33c9", "SPR5COORD": "33ca", "SPR5CLR": "33cb", 
               "SPR6COORD": "33cc", "SPR6CLR": "33cd", "SPR7COORD": "33ce", "SPR7CLR": "33cf", "SPR8COORD": "33d0", "SPR8CLR": "33d1", 
               "SPR9COORD": "33d2", "SPR9CLR": "33d3", "SPR10COORD": "33d4", "SPR10CLR": "33d5", "SPR11COORD": "33d6", "SPR11CLR": "33d7",
               "SPR12COORD": "33d8", "SPR12CLR": "33d9", "SPR13COORD": "33da", "SPR13CLR": "33db", "SPR14COORD": "33dc", "SPR14CLR": "33dd",  
               "SPR15COORD": "33de", "SPR15CLR": "33df", "SPR16COORD": "33e0", "SPR16CLR": "33e1", "SPR17COORD": "33e2", "SPR17CLR": "33e3",
               "SPR18COORD": "33e4", "SPR18CLR": "33e5", "SPR19COORD": "33e6", "SPR19CLR": "33e7", "SPR20COORD": "33e8", "SPR20CLR": "33e9",
               "SPR21COORD": "33ea", "SPR21CLR": "33eb", "SPR22COORD": "33ec", "SPR22CLR": "33ed", "SPR23COORD": "33ee", "SPR23CLR": "33ef", 
               "SPR24COORD": "33f0", "SPR24CLR": "33f1", "SPR25COORD": "33f2", "SPR25CLR": "33f3", "SPR26COORD": "33f4", "SPR26CLR": "33f5",
               "SPR27COORD": "33f6", "SPR27CLR": "33f7", "SPR28COORD": "33f8", "SPR28CLR": "33f9", "SPR29COORD": "33fa", "SPR29CLR": "33fb",
               "SPR30COORD": "33fc", "SPR30CLR": "33fd", "SPR31COORD": "33f3", "SPR31CLR": "33ff", 
               "\'0": "0030", "\'1": "0031", "\'2": "0032", "\'3": "0033", "\'4": "0034", "\'5": "0035", "\'6": "0036", 
               "\'7": "0037", "\'8": "0038", "\'9": "0039", "\'a": "0061", "\'b": "0062", "\'c": "0063", "\'d": "0064", 
               "\'e": "0065", "\'f": "0066", "\'g": "0067", "\'h": "0068", "\'i": "0069", "\'j": "006a", "\'k": "006b", 
               "\'l": "006c", "\'m": "006d", "\'n": "006e", "\'o": "006f", "\'p": "0070", "\'q": "0071", "\'r": "0072", 
               "\'s": "0073", "\'t": "0074", "\'u": "0075", "\'v": "0076", "\'w": "0077", "\'x": "0078", "\'y": "0079", 
               "\'z": "007a", "\'A": "0041", "\'B": "0042", "\'C": "0043", "\'D": "0044", "\'E": "0045", "\'F": "0046", 
               "\'G": "0047", "\'H": "0048", "\'I": "0049", "\'J": "004a", "\'K": "004b", "\'L": "004c", "\'M": "004d", 
               "\'N": "004e", "\'O": "004f", "\'P": "0050", "\'Q": "0051", "\'R": "0052", "\'S": "0053", "\'T": "0054", 
               "\'U": "0055", "\'V": "0056", "\'W": "0057", "\'X": "0058", "\'Y": "0059", "\'Z": "005a", "\'_": "0020", 
               "\'exclamation": "0021", "\'\"": "0022", "\'hash": "0023", "\'$": "0024", "\'percent": "0025", "\'&": "0026", 
               "\'\'": "0027", "\'(": "0028", "\')": "0029", "\'*": "002a", "\'+": "002b", "\',": "002c", "\'-": "002d", 
               "\'.": "002e", "\'/": "002f", "\':": "003a", "\';": "003b", "\'<": "003c", "\'=": "003d", "\'>": "003e", 
               "\'?": "003f", "\'@": "0040", "\'[": "005b", "\'\\": "005c", "\']": "005d", "\'^": "005e", "\'__": "005f", 
               "\'{": "007b", "\'|": "007c", "\'}": "007d", "\'~": "007e"}

  print("Starting")

  assem = open("Assembly.txt", "r")
  inter = open("Intermediate.txt", "w")

  #Step 1: convert the assembly into an intermediate form

  #Set default address, 0x4000
  address = 16384
  startAddress = 0
  lineNum = 1

  #Converts the assembly line by line
  for line in assem:
    if "!" in line:
      address = hex_to_decimal(line.split("!")[-1].strip())

    line = line.split("#")[0]
    
    #Get the actual instruction
    instruction = (" " + line).split("#")[0].split("//")[0].split("/>")[0].split("%")[0].split("!")[0].split()

    #Check to see if variable being assigned
    splitLine = line.split("%")
    if len(splitLine) > 1:
      var = splitLine[-1].split("=")
      addresses[var[0].strip()] = var[1].strip()
    
    #Convert the instruction
    if len(instruction) != 0 and line[0] != "#":

      #Check to see if variable being assigned to this address
      splitLine = line.split("//")
      if len(splitLine) > 1:
        addressNameList = splitLine[-1].strip().split(" ")
        for i in addressNameList:
          addresses[i] = decimal_to_hex(address)
      startAddress = address

      i = 0
      while i < len(instruction):

        #Clean up instruction
        data = instruction[i].strip()

        #Deals with basic instructions
        if data.upper() in AssemblyCodes1.keys():
          inter.write(AssemblyCodes1[data.upper()] + " ")
          if(len(instruction) != AssemblyNumber[data.upper()]):
            raise Exception("Assembly instruction " + str(instruction) + " at " + str(lineNum) + " expected " + str(AssemblyNumber[data.upper()]) + " data chunks. Got " + str(len(instruction)) + " instead. ")

        #Deals with ALU instructions
        elif data.upper() in AssemblyCodes2.keys():
          data2 = instruction[i+1].upper()
          i+=1
          if data2 in ALUCodes.keys():
            inter.write(add_ALU_codes(AssemblyCodes2[data.upper()], ALUCodes[data2]) + " ")
          else:
            inter.write(add_ALU_codes(AssemblyCodes2[data.upper()], data2) + " ")
          if(len(instruction) != AssemblyNumber[data.upper()]):
            raise Exception("Assembly instruction " + str(instruction) + " at " + str(lineNum) + " expected " + str(AssemblyNumber[data.upper()]) + " data chunks. Got " + str(len(instruction)) + " instead. ")

        #Deals with flag jump instructions
        elif data.upper() in AssemblyCodes3.keys():
          data2 = instruction[i+1]
          i+=1
          if data2.upper() in FlagJumpCodes.keys():
            inter.write(add_JPF_codes(AssemblyCodes3[data.upper()], FlagJumpCodes[data2.upper()]) + " ")
          else:
            inter.write(add_JPF_codes(AssemblyCodes3[data.upper()], data2) + " ")
          if(len(instruction) != AssemblyNumber[data.upper()]):
            raise Exception("Assembly instruction " + str(instruction) + " at " + str(lineNum) + " expected " + str(AssemblyNumber[data.upper()]) + " data chunks. Got " + str(len(instruction)) + " instead. ")

        #Deals with bit jump instructions
        elif data.upper() in AssemblyCodes4.keys():
          opcode = AssemblyCodes4[data.upper()]
          data2 = instruction[i+1]
          i+=1
          inter.write(opcode[0:2] + hex_digit_add(opcode[2], data2[0]) + data2[1] + " ")
          if(len(instruction) != AssemblyNumber[data.upper()]):
            raise Exception("Assembly instruction " + str(instruction) + " at "+ str(lineNum) + " expected " + str(AssemblyNumber[data.upper()]) + " data chunks. Got " + str(len(instruction)) + " instead. ")

        #Deals with clock jump instructions
        elif data.upper() in AssemblyCodes5.keys():
          opcode = AssemblyCodes5[data.upper()]
          data2 = instruction[i+1]
          i+=1
          inter.write(opcode[0:3] + hex_digit_add(opcode[3], data2) + " ")
          if(len(instruction) != AssemblyNumber[data.upper()]):
            raise Exception("Assembly instruction " + str(instruction) + " at " + str(lineNum) + " expected " + str(AssemblyNumber[data.upper()]) + " data chunks. Got " + str(len(instruction)) + " instead. ")

        #Assume data is either variable or raw hexdecimal
        else:
          inter.write(data + " ")

        #Update address
        i+=1
        address += 1
      inter.write("#" + decimal_to_hex(startAddress))
      inter.write("\n")
      
      splitLine = line.split("/>")
      if len(splitLine) > 1:
        addressNameList = splitLine[-1].strip().split(" ")
        for i in addressNameList:
          addresses[i] = decimal_to_hex(address)
          
    lineNum += 1

  assem.close()
  inter.close()

  print("Intermediate Finished")

  inter = open("Intermediate.txt", "r")
  code = open("MachineCode.txt", "w")

  #Step 2: convert the intermediate into machine code

  numData = 0

  lineNum = 1
  for line in inter:

    #Get rid of addresses in intermediate
    instruction = line.split("#")[0].split()
    for i in instruction:

      #If variable, add in varaible's value
      if i.strip() in addresses.keys():
        code.write(HexAddOn + addresses[i.strip()] + " ")

      #If not variable assume it is raw hex value
      else:
        #Ensure that the hex value is valid
        if len(i) != 4:
          raise Exception("Invalid hex value of " + i + " at line " + str(lineNum))
        for j in i:
          if j not in hexConv:
            raise Exception("Invalid hex value of " + i + " at line " + str(lineNum))
        code.write(HexAddOn + i.strip() + " ")
      numData += 1

      #Ensure that each line contains 1024 data chunks, allowing it to be copied directly into the EEPROM banks
      if(numData > 1023):
        code.write("\n")
        numData = 0
    lineNum += 1
  inter.close()
  code.close()

  print("Machine Code Finished")
        
class StatementTree ():
  
  def __init__ (self, left, right, operator):
    self.left = left
    self.right = right
    self.operator = operator
    
  def __str__ (self):
    return "(" + str(self.left) + " " + str(self.operator) + " " + str(self.right) + ")"
  
  def __repr__ (self):
    return self.__str__ ()
  
  def cleanPrint(self):
    leftString = ""
    rightString = ""
    operatorString = ""
    if isinstance(self.left, StatementTree):
      leftString = self.left.cleanPrint()
    elif isinstance(self.left, list):
      if len(self.left) != 0:
        leftString = str(self.left[0])
    if self.operator[1] == "PARAMETERS":
      for i in self.right:
        if isinstance(i, StatementTree):
          rightString += i.cleanPrint() + ","
        elif isinstance(i, list):
          rightString += i[0] + ","
    elif isinstance(self.right, StatementTree):
      rightString = self.right.cleanPrint()
    elif isinstance(self.right, list):
      if len(self.right) != 0:
        rightString = str(self.right[0])
    if isinstance(self.operator[0], list):
      for i in self.operator[0]:
        if isinstance(i, StatementTree):
          operatorString += i.cleanPrint()
        elif isinstance(i, list):
          if len(i) != 0:
            operatorString += i[0]
    else:
      operatorString = self.operator[0]
    #print(leftString, "|", operatorString, "|", rightString)
    #print(type(leftString), "|", type(operatorString), "|", type(rightString))
    return "(" + leftString + " " + operatorString + " " + rightString + ")"

#StateMachine for interpreting text
class StateMachine ():

  def __init__ (self, stateMap, initState):
    #StateMaps maps which characters in which states map to which other states
    self.stateMap = stateMap
    self.state = initState

  def setState (self, state):
    self.state = state

  def updateState (self, nextChar):
    if self.state in self.stateMap.keys():
      if nextChar in self.stateMap[self.state].keys():  
        self.state = self.stateMap[self.state][nextChar]
      else:
        self.state = "ERROR"
    else:
      self.state = "ERROR"
      
class VariableScope ():
  
  #Scope stores it in identifier, type, tokenName
  def __init__ (self, superScope):
    self.scope = []
    self.superScope = superScope
    
  def addVariable(self, identifier, varType, number):
    if not self.variableInScope(identifier):
      self.scope.append([identifier, varType, varType + str(number)])
      return varType + str(number)
    else:
      raise Exception(identifier + " already declared.")
    
  def addSpecialVariable(self, identifier, varType, tokenName):
    if not self.variableInScope(identifier):
      self.scope.append([identifier, varType, tokenName])
      return tokenName
    else:
      raise Exception(identifier + " already declared.")
    
  def getVariable(self, identifier):
    for i in self.scope:
      if i[0] == identifier:
        return i
    if self.superScope != None:
      result = self.superScope.getVariable(identifier)
      if result != None:
        return result
      raise Exception(identifier + " not declared.")
      
  def variableInScope(self, identifier):
    for i in self.scope:
      if i[0] == identifier:
        return True
    return False
  
  def variableFindable(self, identifier):
    for i in self.scope:
      if i[0] == identifier:
        return True
    if self.superScope != None:
      return self.superScope.variableFindable(identifier)
    return False
  
  def flattenScope(self):
    result = []
    for i in self.scope:
      result.append([i[2], i[1], 1, [], []])
    return result
      
class ArrayScope ():
  
  #Scope stores it in identifier, type, length, tokenName
  def __init__ (self, superScope):
    self.scope = []
    self.superScope = superScope
    
  def addArray(self, identifier, arrayType, length, number):
    if not self.arrayInScope(identifier):
      self.scope.append([identifier, arrayType, length, arrayType + str(number)])
      return arrayType + str(number)
    else:
      raise Exception(identifier + " already declared.")
    
  def getArray(self, identifier):
    for i in self.scope:
      if i[0] == identifier:
        return i
    if self.superScope != None:
      result = self.superScope.getArray(identifier)
      if result != None:
        return result
      raise Exception(identifier + " not declared.")
      
  def arrayInScope(self, identifier):
    for i in self.scope:
      if i[0] == identifier:
        return True
    return False
  
  def arrayFindable(self, identifier):
    for i in self.scope:
      if i[0] == identifier:
        return True
    if self.superScope != None:
      return self.superScope.arrayFindable(identifier)
    return False
  
  def flattenScope(self):
    result = []
    for i in self.scope:
      result.append([i[3], i[1], i[2], [], []])
    return result
      
class FunctionScope ():
  
  #Scope stores it in identifier, returnType, parameters, tokenName, length, parameterNames
  #Parameters in the form [type, length]
  def __init__ (self, superScope):
    self.scope = []
    self.superScope = superScope
    
  def addFunction(self, identifier, returnType, parameters, number, parameterNames, length = 1):
    if not self.functionInScope(identifier, parameters):
      tokenIdentifier = "f" + returnType + str(number)
      if returnType == "NONE":
        returnType = ""
        length = 0
      elif returnType in ["INT", "CHAR", "BOOLEAN"]:
        length = 1
      self.scope.append([identifier, returnType, parameters, tokenIdentifier, length, parameterNames])
      return tokenIdentifier
    else:
      raise Exception(identifier + " already declared.")
    
  def getFunction(self, identifier, parameters):
    for i in self.scope:
      if i[0] == identifier:
        if len(i[2]) == len(parameters):
          returning = True
          for j in range(len(i[2])):
            if i[2][j][0] != parameters[j][0]:
              returning = False
          if returning:
            return i
    if self.superScope != None:
      result = self.superScope.getFunction(identifier, parameters)
      if result != None:
        return result
      raise Exception(identifier + str(parameters) + " not declared.")
      
  def functionInScope(self, identifier, parameters):
    for i in self.scope:
      if i[0] == identifier and i[2] == parameters:
        return True
    return False
  
  def functionFindable(self, identifier, parameters):
    for i in self.scope:
      if i[0] == identifier and i[2] == parameters:
        return True
    if self.superScope != None:
      return self.superScope.functionFindable(identifier)
    return False
  
  def flattenScope(self):
    result = []
    for i in self.scope:
      result.append([i[3], i[1], i[4], i[2], i[5]])
    return result
  
class CodeLine():
  
  def __init__(self, assemblyCode, operands, nextLine, name = None):
    self.assemblyCode = assemblyCode
    self.operands = operands
    self.nextLine = nextLine
    if name == None:
      self.name = []
    else:
      self.name = [name]
    self.nextLineCode = nextLine
    
  def __str__(self):
    result = self.assemblyCode
    for i in self.operands:
      result += " " + str(i)
    if self.name != []:
      resultName = ""
      for i in self.name:
        resultName += " " + i
      result += " />" + resultName
    return result
  
  def __repr__(self):
    return self.__str__()
    
  def setNextLine(self, nextLine):
    self.nextLine = nextLine
    if self.nextLineCode == None:
      self.nextLineCode = nextLine
    
  def setNextLineCode(self, nextLineCode):
    self.nextLineCode = nextLineCode
    
  def setLastLine(self, lastLine):
    if self.nextLine == None:
      #print("Set Last Line")
      self.nextLine = lastLine
      if self.nextLineCode == None:
        self.nextLineCode = lastLine
    else:
      #print("Sending on request")
      self.nextLine.setLastLine(lastLine)
    
  def getLastLine(self):
    if self.nextLine != None:
      return self.nextLine.getLastLine()
    else:
      return self
    
  def setName(self, name):
    if name == None:
      self.name = []
    else:
      self.name = [name]
      
  def removeName(self, name):
    if name in self.name:
      self.name.remove(name)
    
  def addName(self, name):
    if name != None:
      self.name.append(name)
      
  def convertToACCDLoad(self, newOperand):
    global debug
    if self.assemblyCode[0:2] == "AN" and self.assemblyCode[2] in "RVBD":
      self.assemblyCode = "AL" + self.assemblyCode[2:7]
      self.operands.append(newOperand)
      if debug:
        print(self, self.nextLine)
    else:
      raise Exception("Attempted to convert line", self, "into ALU load line")
      
  def convertToACCILoad(self, newOperand):
    global debug
    if self.assemblyCode[0:2] == "AN" and self.assemblyCode[2] in "RVBD":
      self.nextLine = CodeLine("LIA", [newOperand], self.nextLine)
      self.nextLineCode = self.nextLine
      if debug:
        print(self, self.nextLine, self.nextLine.nextLine)
    else:
      raise Exception("Attempted to convert line", self, "into ALU load line")
      
  def convertToACC2DLoad(self, newOperand):
    global debug
    if self.assemblyCode[0:2] == "AN" and self.assemblyCode[2] in "RVBD":
      self.nextLine = CodeLine("LDD", ["ACC2", newOperand], self.nextLine)
      self.nextLineCode = self.nextLine
      if debug:
        print(self, self.nextLine, self.nextLine.nextLine)
    else:
      raise Exception("Attempted to convert line", self, "into ALU load line")
      
  def convertToACC2ILoad(self, newOperand):
    global debug
    if self.assemblyCode[0:2] == "AN" and self.assemblyCode[2] in "RVBD":
      self.nextLine = CodeLine("LDI", ["ACC2", newOperand], self.nextLine)
      self.nextLineCode = self.nextLine
      if debug:
        print(self, self.nextLine, self.nextLine.nextLine)
    else:
      raise Exception("Attempted to convert line", self, "into ALU load line")
    
  def printAllCode(self):
    #print("Called print all on ", self)
    result = self.assemblyCode
    for i in self.operands:
      result += " " + str(i)
    if self.name != []:
      resultName = ""
      for i in self.name:
        try:
          resultName += " " + i
        except:
          raise Exception("Invalid name in", i)
      result += " />" + resultName
    if self.nextLine != self.nextLineCode:
      result += " #-> " + str(self.nextLine)
    if self.nextLineCode != None:
      result += "\n"
      result += self.nextLineCode.printAllCode()
    #print("result: ",result)
    #print("------")
    return result
    
  def printAll(self):
    #print("Called print all on ", self)
    result = self.assemblyCode
    for i in self.operands:
      result += " " + str(i)
    if self.name != []:
      resultName = ""
      for i in self.name:
        resultName += " " + i
      result += " />" + resultName
    if self.nextLine != None:
      result += "\n"
      result += self.nextLine.printAll()
    #print("result: ",result)
    #print("------")
    return result

class ConditionalLine(CodeLine):
  
  def __init__(self, assemblyCode, operands, nextLine, nextLineFalse):
    super().__init__(assemblyCode, operands, nextLine)
    self.nextLineFalse = nextLineFalse
    
  def setNextLineFalse(self, nextLineFalse):
    self.nextLineFalse = nextLineFalse
    
  def printAllCode(self):
    #print("Called print all on ", self)
    result = self.assemblyCode
    for i in self.operands:
      result += " " + str(i)
    if self.name != []:
      resultName = ""
      for i in self.name:
        resultName += " " + i
      result += " />" + resultName
    if self.nextLineFalse != None:
      result += " #=> " + str(self.nextLineFalse)
    if self.nextLineCode != self.nextLine:
      result += "\n#|-> " + str(self.nextLine)
    if self.nextLineCode != None:
      result += "\n"
      result += self.nextLineCode.printAllCode()
    #print("result: ",result)
    #print("------")
    return result
    
  def printAll(self):
    #print("Called print all on ", self)
    result = self.assemblyCode
    for i in self.operands:
      result += " " + str(i)
    if self.name != []:
      resultName = ""
      for i in self.name:
        resultName += " " + i
      result += " />" + resultName
    if self.nextLineFalse != None:
      result += "->" + str(self.nextLineFalse)
    if self.nextLine != None:
      result += "\n"
      result += self.nextLine.printAll()
    #print("result: ",result)
    #print("------")
    return result

def convertToNumber(stringInt):
  if len(stringInt) >= 2:
    if stringInt[0] == "0":
      if stringInt[1] == "x":
        total = 0
        for i in stringInt[2:len(stringInt)]:
          total *= 16
          total += hexConv.index(i.lower())
        return total
      elif stringInt[1] == "b":
        total = 0
        for i in stringInt[2:len(stringInt)]:
          total *= 2
          total += int(i)
        return total
      else:
        return int(stringInt) #Denary
    else:
      return int(stringInt) #Denary
  else:
    return int(stringInt) #Denary

def constructTree(line):
  global debug
  #print(line)
  keyOperator = -1
  #keyOperatorEnd = -1
  keyOperatorType = "NONE"
  operatorType = "NONE"
  priorityArray = ["KEYWORD", "ASSIGNER", "MODIFIER", "TYPE", "ARRAY_TYPE", "BOOLEAN_OPERATOR", "COMPARATOR", "SUBSCRIPT", "OPERATOR", "NEGATOR", "SLICE", "NUMBER", "CHAR", "STRING", "IDENTIFIER", "EXPRESSION", "ARRAY", "PARAMETERS", "NONE"]
  #operatorPriorityArray = [["&", "|", "^", ">>", "<<"], ["+", "-"], ["*", "/", "%"], "NONE"]
  operatorPriorityDictionary = {"&": 1, "|": 1, "^": 1, ">>": 1, "<<": 1, "+": 2, "-": 2, "*": 3, "/":3, "%":3, "NONE": 4}
  if len(line) == 0:
    return []
  elif len(line) == 1:
    if line[0][1] == "EXPRESSION":
      return constructTree(line[0][0])
    elif line[0][1] == "CODE":
      codeTree = []
      for i in line[0][0]:
        codeTree.append(constructTree(i))
      return codeTree
    elif line[0][1] == "SUBSCRIPT":
      if debug:
        print(line)
        pass
      return StatementTree([], constructTree(line[0][0]),["[]", "SUBSCRIPT"])
    return line[0]
  else:
    for i in range(len(line)):
      if debug:
        #print("Line:", line[i])
        pass
      if line[i][1] == "KEYWORD" and priorityArray.index(keyOperatorType) > priorityArray.index("KEYWORD"):
        keyOperator = i
        keyOperatorType = "KEYWORD"
      elif line[i][1] == "ASSIGNER" and priorityArray.index(keyOperatorType) > priorityArray.index("ASSIGNER"):
        keyOperator = i
        keyOperatorType = "ASSIGNER"
      elif line[i][1] == "MODIFIER" and priorityArray.index(keyOperatorType) > priorityArray.index("MODIFIER"):
        keyOperator = i
        keyOperatorType = "MODIFIER"
      elif line[i][1] == "TYPE" and priorityArray.index(keyOperatorType) > priorityArray.index("TYPE"):
        keyOperator = i
        keyOperatorType = "TYPE"
      elif line[i][1] == "BOOLEAN_OPERATOR" and priorityArray.index(keyOperatorType) >= priorityArray.index("BOOLEAN_OPERATOR"):
        keyOperator = i
        keyOperatorType = "BOOLEAN_OPERATOR"
      elif line[i][1] == "COMPARATOR" and priorityArray.index(keyOperatorType) > priorityArray.index("COMPARATOR"):
        keyOperator = i
        keyOperatorType = "COMPARATOR"
      elif line[i][1] == "SUBSCRIPT" and priorityArray.index(keyOperatorType) > priorityArray.index("SUBSCRIPT"):
        keyOperator = i
        keyOperatorType = "SUBSCRIPT"
      elif line[i][1] == "ARRAY_TYPE" and priorityArray.index(keyOperatorType) > priorityArray.index("ARRAY_TYPE"):
        keyOperator = i
        keyOperatorType = "ARRAY_TYPE"
      elif line[i][1] == "OPERATOR" and priorityArray.index(keyOperatorType) >= priorityArray.index("OPERATOR"):
        if operatorPriorityDictionary[operatorType] >= operatorPriorityDictionary[line[i][0]]:
          keyOperator = i
          operatorType = line[i][0]
          keyOperatorType = "OPERATOR"
      elif line[i][1] == "NEGATOR" and priorityArray.index(keyOperatorType) > priorityArray.index("NEGATOR"):
        keyOperator = i
        keyOperatorType = "NEGATOR"
      elif line[i][1] == "SLICE" and priorityArray.index(keyOperatorType) > priorityArray.index("SLICE"):
        keyOperator = i
        keyOperatorType = "SLICE"
      elif line[i][1] == "PARAMETERS" and priorityArray.index(keyOperatorType) > priorityArray.index("PARAMETERS"):
        keyOperator = i
        keyOperatorType = "PARAMETERS"
      elif line[i][1] == "ARRAY" and priorityArray.index(keyOperatorType) > priorityArray.index("ARRAY"):
        keyOperator = i
        keyOperatorType = "ARRAY"
    if keyOperator == -1:
      print(line)
      raise Exception("Failed to find operator in: " + str(line))
    if keyOperatorType == "SUBSCRIPT":
      if debug:
        print("SUBSCRIPT line:", line)
        pass
      if keyOperator == 0:
        return StatementTree(constructTree(line[keyOperator+1:len(line)]), constructTree(line[keyOperator][0]),["[]", "SUBSCRIPT"])
      elif keyOperator == len(line) - 1:
        return StatementTree(constructTree(line[0:keyOperator]), constructTree(line[keyOperator][0]), ["[]", "SUBSCRIPT"])
      else:
        print(keyOperator, len(line) - 1)
        raise Exception("Unaccounted case in: ", line)
    elif keyOperatorType == "PARAMETERS":
      if keyOperator == len(line) - 1:
        #print(line[keyOperator])
        parametersTree = []
        for i in line[keyOperator][0]:
          parametersTree.append(constructTree(i))
        return StatementTree(constructTree(line[0:keyOperator]), parametersTree, ["()", "PARAMETERS"])
      else:
        raise Exception("Unaccounted case in: ", line)
    elif keyOperatorType == "ARRAY":
      if keyOperator == len(line) - 1:
        #print(line[keyOperator])
        parametersTree = []
        for i in line[keyOperator][0]:
          parametersTree.append(constructTree(i))
        return StatementTree(constructTree(line[0:keyOperator]), parametersTree, ["[]", "ARRAY"])
      else:
        raise Exception("Unaccounted case in: ", line)
    else:
      return StatementTree(constructTree(line[0:keyOperator]), constructTree(line[keyOperator+1:len(line)]), line[keyOperator])
    
def sortIntoLines(tokenList):
  tokensByLine = []
  tokenLine = []
  tokenBracket = []
  curlyCount = 0
  squareCount = 0
  roundCount = 0
  gettingBracket = "NONE"
  previousType = "NONE"
  for i in tokenList:
    if gettingBracket == "NONE":
      if i[1] == "RETURN":
        #tokenLine.append(i)
        tokensByLine.append(tokenLine)
        tokenLine = []
      elif i[1] == "OPERATOR":
        if i[0] == "-":
          if previousType == "ASSIGNER" or previousType == "OPERATOR":
            i[1] = "NEGATOR"
            tokenLine.append(i)
            previousType = "NEGATOR"
          else:
            tokenLine.append(i)
            previousType = "OPERATOR"
        elif i[0] == "not":
          i[1] = "NEGATOR"
          tokenLine.append(i)
          previousType = "NEGATOR"
        else:
          tokenLine.append(i)
          previousType = "OPERATOR"
      elif i[1] == "OPEN CURLY":
        curlyCount += 1
        gettingBracket = "CURLY"
        tokensByLine.append(tokenLine)
        tokenLine = []
        tokenBracket = []
        tokenBracket.append(i)
      elif i[1] == "CLOSE CURLY":
        curlyCount -= 1
        raise Exception("Found unpaired }")
      elif i[1] == "OPEN SQUARE":
        squareCount += 1
        gettingBracket = "SQUARE"
        tokenBracket = []
        tokenBracket.append(i)
      elif i[1] == "CLOSE SQUARE":
        squareCount -= 1
        raise Exception("Found unpaired ]")
      elif i[1] == "OPEN ROUND":
        roundCount += 1
        gettingBracket = "ROUND"
        tokenBracket = []
        tokenBracket.append(i)
      elif i[1] == "CLOSE ROUND":
        roundCount -= 1
        raise Exception("Found unpaired )")
      else:
        tokenLine.append(i)
        previousType = i[1]
        
    elif gettingBracket == "CURLY":
      if i[1] == "OPEN CURLY":
        curlyCount += 1
        tokenBracket.append(i)
      elif i[1] == "CLOSE CURLY":
        curlyCount -= 1
        tokenBracket.append(i)
        if curlyCount == 0:
          temp = sortIntoLines(tokenBracket[1:-1])
          tokensByLine.append([[temp, "CODE"]])
          tokenLine = []
          gettingBracket = "NONE"
          previousType = "NONE"
      else:
        tokenBracket.append(i)
        
    elif gettingBracket == "SQUARE":
      if i[1] == "RETURN":
        raise Exception("EOL without closing bracket")
      elif i[1] == "OPEN SQUARE":
        squareCount += 1
        tokenBracket.append(i)
      elif i[1] == "CLOSE SQUARE":
        squareCount -= 1
        tokenBracket.append(i)
        if squareCount == 0:
          if previousType in ["IDENTIFIER", "KEYWORD", "ARRAY_TYPE"]:
            temp = sortBracket(tokenBracket[1:-1])
            tokenLine.append([temp,"SUBSCRIPT"])
            previousType = "SUBSCRIPT"
            previousType = "SUBSCRIPT"
          elif previousType in ["OPERATOR", "ASSIGNER", "NEGATOR"]:
            temp = sortParameter(tokenBracket[1:-1])
            tokenLine.append([temp,"ARRAY"])
            previousType = "ARRAY"
            previousType = "ARRAY"
          else:
            raise Exception("Invalid sqaure bracket")
          gettingBracket = "NONE"
      else:
        tokenBracket.append(i)
    
    elif gettingBracket == "ROUND":
      if i[1] == "RETURN":
        raise Exception("EOL without closing bracket")
      elif i[1] == "OPEN ROUND":
        roundCount += 1
        tokenBracket.append(i)
      elif i[1] == "CLOSE ROUND":
        roundCount -= 1
        tokenBracket.append(i)
        if roundCount == 0:
          if previousType == "IDENTIFIER":
            temp = sortParameter(tokenBracket[1:-1])
            tokenLine.append([temp, "PARAMETERS"])
            previousType = "PARAMETERS"
          else:
            temp = sortBracket(tokenBracket[1:-1])
            tokenLine.append([temp, "EXPRESSION"])
            previousType = "EXPRESSION"
          gettingBracket = "NONE"
      else:
        tokenBracket.append(i)
  if (len(tokenLine) != 0):
    tokensByLine.append(tokenLine)
        
  return tokensByLine
  
def sortBracket(tokenList):
  tokensByLine = []
  tokenBracket = []
  curlyCount = 0
  squareCount = 0
  roundCount = 0
  gettingBracket = "NONE"
  previousType = "NONE"
  for i in tokenList:
    if gettingBracket == "NONE":
      if i[1] == "RETURN":
        raise Exception("EOL without closing bracket")
      elif i[1] == "OPEN CURLY":
        raise Exception("EOL without closing bracket")
      elif i[1] == "CLOSE CURLY":
        curlyCount -= 1
        raise Exception("Found unpaired }")
      elif i[1] == "OPEN SQUARE":
        squareCount += 1
        gettingBracket = "SQUARE"
        tokenBracket = []
        tokenBracket.append(i)
      elif i[1] == "CLOSE SQUARE":
        squareCount -= 1
        raise Exception("Found unpaired ]")
      elif i[1] == "OPEN ROUND":
        roundCount += 1
        gettingBracket = "ROUND"
        tokenBracket = []
        tokenBracket.append(i)
      elif i[1] == "CLOSE ROUND":
        roundCount -= 1
        raise Exception("Found unpaired )")
      else:
        tokensByLine.append(i)
        previousType = i[1]
        
    elif gettingBracket == "SQUARE":
      if i[1] == "RETURN":
        raise Exception("EOL without closing bracket")
      elif i[1] == "OPEN SQUARE":
        squareCount += 1
        tokenBracket.append(i)
      elif i[1] == "CLOSE SQUARE":
        squareCount -= 1
        tokenBracket.append(i)
        if squareCount == 0:
          temp = sortBracket(tokenBracket[1:-1])
          if previousType in ["IDENTIFIER", "KEYWORD"]:
            temp = sortBracket(tokenBracket[1:-1])
            tokensByLine.append([temp, "SUBSCRIPT"])
            previousType = "SUBSCRIPT"
            previousType = "SUBSCRIPT"
          elif previousType in ["OPERATOR", "ASSIGNER", "NEGATOR"]:
            temp = sortParameter(tokenBracket[1:-1])
            tokensByLine.append([temp, "ARRAY"])
            previousType = "ARRAY"
            previousType = "ARRAY"
          else:
            raise Exception("Invalid square bracket")
          gettingBracket = "NONE"
      else:
        tokenBracket.append(i)
    
    elif gettingBracket == "ROUND":
      if i[1] == "RETURN":
        raise Exception("EOL without closing bracket")
      elif i[1] == "OPEN ROUND":
        roundCount += 1
        tokenBracket.append(i)
      elif i[1] == "CLOSE ROUND":
        roundCount -= 1
        tokenBracket.append(i)
        if roundCount == 0:
          if previousType == "IDENTIFIER":
            temp = sortParameter(tokenBracket[1:-1])
            tokensByLine.append([temp,"PARAMETERS"])
            previousType = "PARAMTERS"
          else:
            temp = sortBracket(tokenBracket[1:-1])
            tokensByLine.append([temp,"EXPRESSION"])
            previousType = "EXPRESSION"
          gettingBracket = "NONE"
      else:
        tokenBracket.append(i)
        
  return tokensByLine

def sortParameter(tokenList):
  global debug
  tokensByLine = []
  tokenLine = []
  tokenBracket = []
  curlyCount = 0
  squareCount = 0
  roundCount = 0
  gettingBracket = "NONE"
  previousType = "NONE"
  for i in tokenList:
    if debug:
      print("Paramters i:", i)
    if gettingBracket == "NONE":
      if i[1] == "RETURN":
        raise Exception("EOL without closing bracket")
      elif i[1] == "COMMA":
        tokensByLine.append(tokenLine)
        tokenLine = []
      elif i[1] == "OPEN CURLY":
        curlyCount += 1
        gettingBracket = "CURLY"
        tokensByLine.append(tokenLine)
        tokenLine = []
        tokenBracket = []
        tokenBracket.append(i)
      elif i[1] == "CLOSE CURLY":
        curlyCount -= 1
        raise Exception("Found unpaired }")
      elif i[1] == "OPEN SQUARE":
        squareCount += 1
        gettingBracket = "SQUARE"
        tokenBracket = []
        tokenBracket.append(i)
      elif i[1] == "CLOSE SQUARE":
        squareCount -= 1
        raise Exception("Found unpaired ]")
      elif i[1] == "OPEN ROUND":
        roundCount += 1
        gettingBracket = "ROUND"
        tokenBracket = []
        tokenBracket.append(i)
      elif i[1] == "CLOSE ROUND":
        roundCount -= 1
        raise Exception("Found unpaired )")
      else:
        tokenLine.append(i)
        previousType = i[1]
        
    elif gettingBracket == "SQUARE":
      if i[1] == "RETURN":
        raise Exception("EOL without closing bracket")
      elif i[1] == "OPEN SQUARE":
        squareCount += 1
        tokenBracket.append(i)
      elif i[1] == "CLOSE SQUARE":
        squareCount -= 1
        tokenBracket.append(i)
        if squareCount == 0:
          temp = sortBracket(tokenBracket[1:-1])
          if previousType in ["IDENTIFIER", "KEYWORD", "ARRAY_TYPE"]:
            temp = sortBracket(tokenBracket[1:-1])
            tokenLine.append([temp,"SUBSCRIPT"])
            previousType = "SUBSCRIPT"
            previousType = "SUBSCRIPT"
          elif previousType in ["OPERATOR", "ASSIGNER", "NEGATOR"]:
            temp = sortParameter(tokenBracket[1:-1])
            tokenLine.append([temp,"ARRAY"])
            previousType = "ARRAY"
            previousType = "ARRAY"
          else:
            raise Exception("Invalid square bracket")
          gettingBracket = "NONE"
      else:
        tokenBracket.append(i)
    
    elif gettingBracket == "ROUND":
      if i[1] == "RETURN":
        raise Exception("EOL without closing bracket")
      elif i[1] == "OPEN ROUND":
        roundCount += 1
        tokenBracket.append(i)
      elif i[1] == "CLOSE ROUND":
        roundCount -= 1
        tokenBracket.append(i)
        if roundCount == 0:
          if previousType == "IDENTIFIER":
            temp = sortParameter(tokenBracket[1:-1])
            tokenLine.append([temp, "EXPRESSION"])
            previousType = "EXPRESSION"
          else:
            temp = sortBracket(tokenBracket[1:-1])
            tokenLine.append([temp, "PARAMETERS"])
            previousType = "PARAMETERS"
          gettingBracket = "NONE"
      else:
        tokenBracket.append(i)
  if (len(tokenLine) != 0):
    tokensByLine.append(tokenLine)
        
  if debug:
    print("Parameter tokenList: ", tokenList)
    print("Parameter tokenLine: ", tokenLine)
    print("Parameter tokensByLine: ", tokensByLine)
    pass
  return tokensByLine

def determineTypeOfCode(tree, varScope, arrayScope, funcScope, number, totalScope):
  global debug
  if isinstance(tree, list):
    nextScope = None
    nextArrayScope = None
    for i in range(len(tree)):
      #print(tree[i])
      if isinstance(tree[i], list):
        if len(tree[i]) == 2:
          if tree[i][1] in ["KEYWORD", "ASSIGNER", "MODIFIER", "TYPE", "ARRAY_TYPE", "COMPARATOR", "SUBSCRIPT", "OPERATOR", "BOOLEAN_OPERATOR", "NEGATOR", "NUMBER", "CHAR", "STRING", "IDENTIFIER", "PARAMETERS"]:
            temp, varScope, arrayScope, funcScope, number, tree[i], nextScope, nextArrayScope = determineType(tree[i], varScope, arrayScope, funcScope, number)
          else:
            if nextScope == None:
              tree[i], tempVarScope, tempArrayScope, tempFuncScope, number, tempScope = determineTypeOfCode(tree[i], VariableScope(varScope), ArrayScope(arrayScope), FunctionScope(funcScope), number, totalScope)
              totalScope = tempScope
            else:
              tree[i], tempVarScope, tempArrayScope, tempFuncScope, number, tempScope = determineTypeOfCode(tree[i], nextScope, nextArrayScope, FunctionScope(funcScope), number, totalScope)
              nextScope = None
              nextArrayScope = None
              totalScope = tempScope
        else:
          if nextScope == None:
            tree[i], tempVarScope, tempArrayScope, tempFuncScope, number, tempScope = determineTypeOfCode(tree[i], VariableScope(varScope), ArrayScope(arrayScope), FunctionScope(funcScope), number, totalScope)
            totalScope = tempScope
          else:
            tree[i], tempVarScope, tempArrayScope, tempFuncScope, number, tempScope = determineTypeOfCode(tree[i], nextScope, nextArrayScope, FunctionScope(funcScope), number, totalScope)
            nextScope = None
            nextArrayScope = None
            totalScope = tempScope
      elif isinstance(tree[i], StatementTree):
        temp, varScope, arrayScope, funcScope, number, tree[i], nextScope, nextArrayScope = determineType(tree[i], varScope, arrayScope, funcScope, number)
      #print("--RESULT--")
      #print(tree[i], number)
    return tree, varScope, arrayScope, funcScope, number, varScope.flattenScope() + arrayScope.flattenScope() + funcScope.flattenScope() + totalScope

def determineType(tree, varScope, arrayScope, funcScope, number):
  if isinstance(tree, StatementTree):
    #ASSIGNER
    if tree.operator[1] == "ASSIGNER":
      leftTemp = determineType(tree.left, varScope, arrayScope, funcScope, number)
      number = leftTemp[4]
      varScope = leftTemp[1]
      arrayScope = leftTemp[2]
      funcScope = leftTemp[3]
      rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
      number = rightTemp[4]
      leftType = leftTemp[0]
      rightType = rightTemp[0]
      tree.left = leftTemp[5]
      tree.right = rightTemp[5]
      if (leftType in ["CHAR", "INT", "BOOLEAN"]) and (rightType in ["CHAR", "INT", "BOOLEAN", "CHAR_CONST", "INT_CONST", "BOOLEAN_CONST"]):
        return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
      elif (leftType in ["ARRAY", "STRING"] and rightType in ["ARRAY", "STRING", "ARRAY_CONST", "STRING_CONST"]):
        return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
      else:
        print(leftType, rightType)
        print(tree.right)
        print(funcScope.scope)
        raise Exception("Invalid types around operator in: " + tree.cleanPrint())
        
    #MODIFIER
    elif tree.operator[1] == "MODIFIER":
      if tree.operator[0] == "++" or tree.operator[0] == "--":
        if tree.right == []:
          leftTemp = determineType(tree.left, varScope, arrayScope, funcScope, number)
          number = leftTemp[4]
          varScope = leftTemp[1]
          arrayScope = leftTemp[2]
          funcScope = leftTemp[3]
          leftType = leftTemp[0]
          tree.left = leftTemp[5]
          if (leftType in ["CHAR", "INT", "BOOLEAN"]):
            return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
          elif (leftType in ["ARRAY", "STRING"]):
            return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            raise Exception("Invalid types around operator in: " + tree.cleanPrint())
        else:
          raise Exception()
      else:
        leftTemp = determineType(tree.left, varScope, arrayScope, funcScope, number)
        number = leftTemp[4]
        varScope = leftTemp[1]
        arrayScope = leftTemp[2]
        funcScope = leftTemp[3]
        rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
        leftType = leftTemp[0]
        rightType = rightTemp[0]
        tree.left = leftTemp[5]
        tree.right = rightTemp[5]
        if (leftType in ["CHAR", "INT", "BOOLEAN"]) and (rightType in ["CHAR", "INT", "BOOLEAN", "CHAR_CONST", "INT_CONST", "BOOLEAN_CONST"]):
          return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
        elif (leftType in ["ARRAY", "STRING"] and rightType in ["ARRAY", "STRING", "ARRAY_CONST", "STRING_CONST"]):
          return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
        else:
          raise Exception("Invalid types around operator in: " + tree.cleanPrint())
          
    #TYPE
    elif tree.operator[1] == "TYPE":
      if tree.left != []:
        raise Exception("Invalid declaration in: " + tree.cleanPrint())
      else:
        if not isinstance(tree.right, list):
          raise Exception("Invalid declaration in: " + tree.cleanPrint())
        elif not tree.right[1] == "IDENTIFIER":
          raise Exception("Invalid declaration in: " + tree.cleanPrint())
        elif not arrayScope.arrayInScope(tree.right[0]):
          if tree.operator[0] == "int":
              tree.right[0] = varScope.addVariable(tree.right[0], "INT", number)
              number += 1
              return "INT", varScope, arrayScope, funcScope, number, tree, None, None
          elif tree.operator[0] == "char":
            tree.right[0] = varScope.addVariable(tree.right[0], "CHAR", number)
            number += 1
            return "CHAR", varScope, arrayScope, funcScope, number, tree, None, None
          elif tree.operator[0] == "bool":
            tree.right[0] = varScope.addVariable(tree.right[0], "BOOLEAN", number)
            number += 1
            return "BOOLEAN", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            raise Exception("Invalid declaration in: " + tree.cleanPrint())
        else:
          raise Exception("Identifier " + tree.right[0] + "already used in: " + tree.cleanPrint())
          
    #ARRAY_TYPE
    elif tree.operator[1] == "ARRAY_TYPE":
      if tree.left != []:
        raise Exception("Invalid declaration in: " + tree.cleanPrint())
      elif not isinstance(tree.right, StatementTree):
        raise Exception("Invalid declaration in: " + tree.cleanPrint())
      elif tree.right.operator[1] != "SUBSCRIPT":
        raise Exception("Invalid declaration in: " + tree.cleanPrint())
      elif not varScope.variableInScope(tree.right.left[0]):
        #print(tree.operator)
        if tree.operator[0] == "array":
          rightTemp = determineType(tree.right.right, varScope, arrayScope, funcScope, number)
          if rightTemp[0] != "INT_CONST":
            raise Exception("Non-constant list size in: " + tree.cleanPrint())
          #length = convertToNumber(tree.right.right[0])
          tree.right.left[0] = arrayScope.addArray(tree.right.left[0], "ARRAY", convertToNumber(tree.right.right[0]), number)
          number += 1
          return "ARRAY", varScope, arrayScope, funcScope, number, tree, None, None
        elif tree.operator[0] == "string":
          rightTemp = determineType(tree.right.right, varScope, arrayScope, funcScope, number)
          if rightTemp[0] != "INT_CONST":
            raise Exception("Non-constant list size in: " + tree.cleanPrint())
          #length = convertToNumber(tree.right.right[0])
          tree.right.left[0] = arrayScope.addArray(tree.right.left[0], "STRING", convertToNumber(tree.right.right[0]), number)
          number += 1
          return "STRING", varScope, arrayScope, funcScope, number, tree, None, None
      else:
        raise Exception("Identifier " + tree.right[0] + "already used in: " + tree.cleanPrint())
        
    #SUBSCRIPT
    elif tree.operator[1] == "SUBSCRIPT":
      #print("--SUBSCRIPT--")
      #print(tree)
      leftType = "NONE"
      if isinstance(tree.left, StatementTree):
        if tree.left.operator[1] == "PARAMETERS":
          leftTemp = determineType(tree.left, varScope, arrayScope, funcScope, number)
          leftType = leftTemp[0]
          tree.left = leftTemp[5]
      elif isinstance(tree.left, list):
        if tree.left[1] == "IDENTIFIER":
          leftTemp = arrayScope.getArray(tree.left[0])
          tree.left[0] = leftTemp[3]
          leftType = leftTemp[1]
      rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
      rightType = rightTemp[0]
      tree.right = rightTemp[5]
      if rightType == "INT_CONST":
        rightType = "INT"
      elif rightType == "CHAR_CONST":
        rightType = "CHAR"
      elif rightType == "BOOLEAN_CONST":
       rightType = "BOOLEAN"
      if leftType == "ARRAY" and rightType in ["CHAR", "INT", "BOOLEAN"]:
        return "INT", varScope, arrayScope, funcScope, number, tree, None, None
      elif leftType == "STRING" and rightType in ["CHAR", "INT", "BOOLEAN"]:
        return "CHAR", varScope, arrayScope, funcScope, number, tree, None, None
      else:
        print(leftType, rightType)
        raise Exception("Invalid types around operator in: " + tree.cleanPrint())
        
    #PARAMETERS
    elif tree.operator[1] == "PARAMETERS":
      if not isinstance(tree.left, list) or not isinstance(tree.right, list):
        raise Exception("Invalid function call in: " + tree.cleanPrint())
      elif not tree.left[1] == "IDENTIFIER":
        raise Exception("Invalid function call in: " + tree.cleanPrint())
      else:
        identifier = tree.left[0]
        parameters = []
        for i in tree.right:
          temp = determineType(i, varScope, arrayScope, funcScope, number)
          i = temp[5]
          if temp[0] == "INT_CONST":
            temp[0] = "INT"
          elif temp[0] == "CHAR_CONST":
            temp[0] == "CHAR"
          elif temp[0] == "BOOLEAN_CONST":
            temp[0] == "BOOLEAN"
          parameters.append([temp[0], 0])
        tempFunc = funcScope.getFunction(identifier, parameters)
        #print(identifier, parameters)
        tree.left[0] = tempFunc[3]
        return tempFunc[1], varScope, arrayScope, funcScope, number, tree, None, None
        
    #ARRAY
    elif tree.operator[1] == "PARAMETERS":
      if not isinstance(tree.left, list) or not isinstance(tree.right, list):
        raise Exception("Invalid function call in: " + tree.cleanPrint())
      elif not tree.left != []:
        raise Exception("Invalid function call in: " + tree.cleanPrint())
      else:
        for i in tree.right:
          temp = determineType(i, varScope, arrayScope, funcScope, number)
          i = temp[5]
          if temp[0] == "INT_CONST":
            temp[0] = "INT"
          elif temp[0] == "CHAR_CONST":
            temp[0] == "CHAR"
          elif temp[0] == "BOOLEAN_CONST":
            temp[0] == "BOOLEAN"
          if temp[0] not in ["INT", "CHAR", "BOOLEAN"]:
            raise Exception("Invalid elements of array in: " + tree.cleanPrint())
        return "ARRAY", varScope, arrayScope, funcScope, number, tree, None, None
        
    #KEYWORD
    elif tree.operator[1] == "KEYWORD":
      #IF
      if tree.operator[0] == "if":
        if tree.left != []:
          raise Exception("Invalid if statement in: " + tree.cleanPrint())
        else:
          rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
          tree.right = rightTemp[5]
          if rightTemp[0] == "BOOLEAN":
            return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            print(rightTemp[0])
            raise Exception("Invalid condition type for if statement in: " + tree.cleanPrint())
      #ELIF
      elif tree.operator[0] == "elif":
        if tree.left != []:
          raise Exception("Invalid if statement in: " + tree.cleanPrint())
        else:
          rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
          tree.right = rightTemp[5]
          if rightTemp[0] == "BOOLEAN":
            return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            print(rightTemp[0])
            raise Exception("Invalid condition type for if statement in: " + tree.cleanPrint())
      #ELSE
      elif tree.operator[0] == "else":
        raise Exception("Invalid else statement in: " + tree.cleanPrint())
      #PAUSE
      elif tree.operator[0] == "pause":
        raise Exception("Invalid else statement in: " + tree.cleanPrint())
      #GRAPHICS
      elif tree.operator[0] == "graphics":
        raise Exception("Invalid else statement in: " + tree.cleanPrint())
      #WHILE
      elif tree.operator[0] == "while":
        if tree.left != []:
          raise Exception("Invalid if statement in: " + tree.cleanPrint())
        else:
          rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
          tree.right = rightTemp[5]
          if rightTemp[0] == "BOOLEAN":
            return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
          if rightTemp[0] == "BOOLEAN_CONST":
            return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            print(rightTemp[0])
            raise Exception("Invalid condition type for if statement in: " + tree.cleanPrint())
      #POP
      elif tree.operator[0] == "pop":
        if tree.left != []:
          raise Exception("Invalid pop in: " + tree.cleanPrint())
        else:
          rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
          rightType = rightTemp[0]
          tree.right = rightTemp[5]
          if rightType in ["INT", "CHAR", "BOOLEAN"]:
            return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            raise Exception("Invalid pop in: " + tree.cleanPrint())
      #PUSH
      elif tree.operator[0] == "push":
        if tree.left != []:
          raise Exception("Invalid push in: " + tree.cleanPrint())
        else:
          rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
          rightType = rightTemp[0]
          tree.right = rightTemp[5]
          if rightType in ["INT", "CHAR", "BOOLEAN", "INT_CONST", "CHAR_CONST", "BOOLEAN_CONST"]:
            return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            raise Exception("Invalid pop in: " + tree.cleanPrint())
      #FOR
      elif tree.operator[0] == "for":
        if tree.left != []:
          raise Exception("Invalid for statement in: " + tree.cleanPrint())
        elif not isinstance(tree.right, StatementTree):
          raise Exception("Invalid for statement in: " + tree.cleanPrint())
        elif tree.right.operator[0] == "in" and isinstance(tree.right.left, list):
          if tree.right.left[1] == "IDENTIFIER":
            if isinstance(tree.right.right, StatementTree):
              if tree.right.right.operator[0] == "to":
                leftTemp = determineType(tree.right.right.left, varScope, arrayScope, funcScope, number)
                rightTemp = determineType(tree.right.right.right, varScope, arrayScope, funcScope, number)
                leftType = leftTemp[0]
                rightType = rightTemp[0]
                tree.right.right.left = leftTemp[5]
                tree.right.right.right = rightTemp[5]
                if leftType == "INT_CONST":
                  leftType = "INT"
                elif leftType == "CHAR_CONST":
                  leftType = "CHAR"
                elif leftType == "BOOLEAN_CONST":
                  leftType = "BOOLEAN"
                if rightType == "INT_CONST":
                  rightType = "INT"
                elif rightType == "CHAR_CONST":
                  rightType = "CHAR"
                elif rightType == "BOOLEAN_CONST":
                 rightType = "BOOLEAN"
                if leftType in ["CHAR", "INT", "BOOLEAN"] and rightType in ["CHAR", "INT", "BOOLEAN"]:
                  nextScope = VariableScope(varScope)
                  tree.right.left[0] = nextScope.addVariable(tree.right.left[0], "INT", number)
                  number += 1
                  return "NONE", varScope, arrayScope, funcScope, number, tree, nextScope, ArrayScope(arrayScope)
                else:
                  print(leftType, rightType)
                  raise Exception("Invalid for statement in: " + tree.cleanPrint())
              elif tree.right.right.operator[1] == "PARAMETERS":
                rightTemp = determineType(tree.right.right, varScope, arrayScope, funcScope, number)
                rightType = rightTemp[0]
                tree.right.right = rightTemp[5]
                if rightType == "ARRAY":
                  nextScope = VariableScope(varScope)
                  tree.right.left[0] = nextScope.addVariable(tree.right.left[0], "INT", number)
                  number += 1
                  return "NONE", varScope, arrayScope, funcScope, number, tree, nextScope, ArrayScope(arrayScope)
                if rightType == "STRING":
                  nextScope = VariableScope(varScope)
                  tree.right.left[0] = nextScope.addVariable(tree.right.left[0], "CHAR", number)
                  number += 1
                  return "NONE", varScope, arrayScope, funcScope, number, tree, nextScope, ArrayScope(arrayScope)
                else:
                  raise Exception("Invalid for statement in: " + tree.cleanPrint())
              else:
                raise Exception("Invalid for statement in: " + tree.cleanPrint())
            elif isinstance(tree.right.right, list):
              if tree.right.right[1] == "IDENTIFIER":
                tempArray = arrayScope.getArray(tree.right.right[0])
                tree.right.right[0] = tempArray[3]
                if tempArray[1] == "ARRAY":
                  nextScope = VariableScope(varScope)
                  tree.right.left[0] = nextScope.addVariable(tree.right.left[0], "INT", number)
                  number += 1
                  return "NONE", varScope, arrayScope, funcScope, number, tree, nextScope, ArrayScope(arrayScope)
                if tempArray[1] == "STRING":
                  nextScope = VariableScope(varScope)
                  tree.right.left[0] = nextScope.addVariable(tree.right.left[0], "CHAR", number)
                  number += 1
                  return "NONE", varScope, arrayScope, funcScope, number, tree, nextScope, ArrayScope(arrayScope)
                else:
                  print(tempArray[1])
                  raise Exception("Invalid for statement in: " + tree.cleanPrint())
              else:
                raise Exception("Invalid for statement in: " + tree.cleanPrint())
            else:
              raise Exception("Invalid for statement in: " + tree.cleanPrint())
          else:
            raise Exception("Invalid for statement in: " + tree.cleanPrint())
        else:
          raise Exception("Invalid for statement in: " + tree.cleanPrint())  
      #DEF
      elif tree.operator[0] == "def":
        if not isinstance(tree.left, StatementTree) and not isinstance(tree.left, list):
          raise Exception("Invalid function declaration in: " + tree.cleanPrint())
        elif not isinstance(tree.right, StatementTree):
          raise Exception("Invalid function declaration in: " + tree.cleanPrint())
        elif not tree.right.operator[1] == "PARAMETERS" or not isinstance(tree.right.left, list) or not isinstance(tree.right.right, list):
          raise Exception("Invalid function declaration in: " + tree.cleanPrint())
        elif not tree.right.left[1] == "IDENTIFIER":
          raise Exception("Invalid function declaration in: " + tree.cleanPrint())
        else:
          parameters = []
          parameterNames = []
          identifier = tree.right.left[0]
          nextScope = VariableScope(varScope)
          nextArrayScope = ArrayScope(arrayScope)
          returnType = ""
          length = 1
          for i in tree.right.right:
            if not isinstance(i, StatementTree):
              raise Exception("Invalid function declaration in: " + tree.cleanPrint())
            elif i.operator[1] == "TYPE":
              if i.left != [] or not isinstance(i.right, list):
                raise Exception("Invalid function declaration in: " + tree.cleanPrint())
              elif i.right[1] != "IDENTIFIER":
                raise Exception("Invalid function declaration in: " + tree.cleanPrint())
              else:
                if i.operator[0] == "int":
                  i.right[0] = nextScope.addVariable(i.right[0], "INT", number)
                  parameterNames.append("INT" + str(number))
                  number += 1
                  parameters.append(["INT", 0])
                elif i.operator[0] == "char":
                  i.right[0] = nextScope.addVariable(i.right[0], "CHAR", number)
                  parameterNames.append("CHAR" + str(number))
                  number += 1
                  parameters.append(["CHAR", 0])
                elif i.operator[0] == "bool":
                  i.right[0] = nextScope.addVariable(i.right[0], "BOOLEAN", number)
                  parameterNames.append("BOOLEAN" + str(number))
                  number += 1
                  parameters.append(["BOOLEAN", 0])
                else:
                  raise Exception("Invalid function declaration in: " + tree.cleanPrint())
            elif i.operator[1] == "ARRAY_TYPE":
              if i.left != [] or not isinstance(i.right, StatementTree):
                raise Exception("Invalid function declaration in: " + tree.cleanPrint())
              elif not isinstance(i.right.left, list):
                raise Exception("Invalid function declaration in: " + tree.cleanPrint())
              elif len(i.right.left) != 2:
                print(i.right.left)
                raise Exception("Invalid function declaration in: " + tree.cleanPrint())
              elif i.right.left[1] != "IDENTIFIER":
                raise Exception("Invalid function declaration in: " + tree.cleanPrint())
              else:
                if i.operator[0] == "array":
                  rightTemp = determineType(i.right.right, varScope, arrayScope, funcScope, number)
                  if rightTemp[0] != "INT_CONST":
                    raise Exception("Invalid function declaration in: " + tree.cleanPrint())
                  length = convertToNumber(i.right.right[0])
                  i.right.left[0] = nextArrayScope.addArray(i.right.left[0], "ARRAY", length, number)
                  parameterNames.append("ARRAY" + str(number))
                  number += 1
                  parameters.append(["ARRAY", length])
                elif i.operator[0] == "string":
                  rightTemp = determineType(i.right.right, varScope, arrayScope, funcScope, number)
                  if rightTemp[0] != "INT_CONST":
                    raise Exception("Invalid function declaration in: " + tree.cleanPrint())
                  length = convertToNumber(i.right.right[0])
                  i.right.left[0] = nextArrayScope.addArray(i.right.left[0], "STRING", length, number)
                  parameterNames.append("STRING" + str(number))
                  number += 1
                  parameters.append(["STRING", length])
                else:
                  raise Exception("Invalid function declaration in: " + tree.cleanPrint())
            else:
              raise Exception("Invalid function declaration in: " + tree.cleanPrint())
          if isinstance(tree.left, StatementTree):
            if tree.left.operator[1] == "ARRAY_TYPE":
              if tree.left.operator[0] == "array":
                leftTemp = determineType(tree.left.right.right, varScope, arrayScope, funcScope, number)
                if leftTemp[0] != "INT_CONST":
                  raise Exception("Invalid function declaration in: " + tree.cleanPrint())
                length = convertToNumber(tree.left.right.right[0])
                returnType = "ARRAY"
              elif tree.left.operator[0] == "string":
                leftTemp = determineType(tree.left.right.right, varScope, arrayScope, funcScope, number)
                if leftTemp[0] != "INT_CONST":
                  raise Exception("Invalid function declaration in: " + tree.cleanPrint())
                length = convertToNumber(tree.left.right.right[0])
                returnType = "STRING"
          elif isinstance(tree.left, list):
            if len(tree.left) == 0:
              returnType = "NONE"
            elif tree.left[1] == "TYPE":
              if tree.left[0] == "int":
                returnType = "INT"
              elif tree.left[0] == "char":
                returnType = "CHAR"
              elif tree.left[0] == "bool":
                returnType = "BOOLEAN"
              else:
                raise Exception("Invalid function declaration in: " + tree.cleanPrint())
            else:
              raise Exception("Invalid function declaration in: " + tree.cleanPrint())
          else:
            raise Exception("Invalid function declaration in: " + tree.cleanPrint())
          tree.right.left[0] = funcScope.addFunction(identifier, returnType, parameters, number, parameterNames, length = length)
          number += 1
          return "NONE", varScope, arrayScope, funcScope, number, tree, nextScope, nextArrayScope
      #RETURN
      elif tree.operator[0] == "return":
        if not tree.left == []:
          raise Exception("Invalid return in: " + tree.cleanPrint())
        else:
          rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
          tree.right = rightTemp[5]
          return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
      
    #COMPARATOR
    elif tree.operator[1] == "COMPARATOR":
      leftTemp = determineType(tree.left, varScope, arrayScope, funcScope, number)
      rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
      leftType = leftTemp[0]
      rightType = rightTemp[0]
      tree.left = leftTemp[5]
      tree.right = rightTemp[5]
      if leftType == "INT_CONST":
        leftType = "INT"
      elif leftType == "CHAR_CONST":
        leftType = "CHAR"
      elif leftType == "BOOLEAN_CONST":
        leftType = "BOOLEAN"
      if rightType == "INT_CONST":
        rightType = "INT"
      elif rightType == "CHAR_CONST":
        rightType = "CHAR"
      elif rightType == "BOOLEAN_CONST":
       rightType = "BOOLEAN"
      if leftType in ["CHAR", "INT", "BOOLEAN"] and rightType in ["CHAR", "INT", "BOOLEAN"]:
        return "BOOLEAN", varScope, arrayScope, funcScope, number, tree, None, None
      else:
        raise Exception("Invalid types around operator in: " + tree.cleanPrint())
        
    #BOOLEAN_OPERATOR
    elif tree.operator[1] == "BOOLEAN_OPERATOR":
      leftTemp = determineType(tree.left, varScope, arrayScope, funcScope, number)
      rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
      leftType = leftTemp[0]
      rightType = rightTemp[0]
      tree.left = leftTemp[5]
      tree.right = rightTemp[5]
      if leftType == "INT_CONST":
        leftType = "INT"
      elif leftType == "CHAR_CONST":
        leftType = "CHAR"
      elif leftType == "BOOLEAN_CONST":
        leftType = "BOOLEAN"
      if rightType == "INT_CONST":
        rightType = "INT"
      elif rightType == "CHAR_CONST":
        rightType = "CHAR"
      elif rightType == "BOOLEAN_CONST":
       rightType = "BOOLEAN"
      elif leftType in ["CHAR", "INT", "BOOLEAN"] and rightType in ["CHAR", "INT", "BOOLEAN"]:
        return "BOOLEAN", varScope, arrayScope, funcScope, number, tree, None, None
      else:
        print(leftType, rightType)
        raise Exception("Invalid types around operator in: " + tree.cleanPrint())
    
    #OPERATOR
    elif tree.operator[1] == "OPERATOR":
      leftTemp = determineType(tree.left, varScope, arrayScope, funcScope, number)
      rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
      leftType = leftTemp[0]
      rightType = rightTemp[0]
      tree.left = leftTemp[5]
      tree.right = rightTemp[5]
      if leftType == "INT_CONST":
        leftType = "INT"
      elif leftType == "CHAR_CONST":
        leftType = "CHAR"
      elif leftType == "BOOLEAN_CONST":
        leftType = "BOOLEAN"
      if rightType == "INT_CONST":
        rightType = "INT"
      elif rightType == "CHAR_CONST":
        rightType = "CHAR"
      elif rightType == "BOOLEAN_CONST":
       rightType = "BOOLEAN"
      if leftType == "CHAR" and rightType == "CHAR":
        return "CHAR", varScope, arrayScope, funcScope, number, tree, None, None
      elif (leftType in ["CHAR", "INT", "BOOLEAN"] and rightType in ["CHAR", "INT", "BOOLEAN"]):
        return "INT", varScope, arrayScope, funcScope, number, tree, None, None
      else:
        print(leftType, rightType)
        raise Exception("Invalid types around operator in: " + tree.cleanPrint())
        
    #NEGATOR
    elif tree.operator[1] == "NEGATOR":
      if tree.left != []:
        raise Exception("Invalid negation in: " + tree.cleanPrint())
      else:
        rightTemp = determineType(tree.right, varScope, arrayScope, funcScope, number)
        rightType = rightTemp[0]
        tree.right = rightTemp[5]
        if rightType == "INT_CONST":
          rightType = "INT"
        elif rightType == "CHAR_CONST":
          rightType = "CHAR"
        elif rightType == "BOOLEAN_CONST":
         rightType = "BOOLEAN"
        if rightType == "INT":
          if tree.operator[0] == "not":
            return "BOOLEAN", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            return "INT", varScope, arrayScope, funcScope, number, tree, None, None
        elif rightType == "CHAR":
          if tree.operator[0] == "not":
            return "BOOLEAN", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            return "CHAR", varScope, arrayScope, funcScope, number, tree, None, None
        elif rightType == "BOOLEAN":
          if tree.operator[0] == "not":
            return "BOOLEAN", varScope, arrayScope, funcScope, number, tree, None, None
          else:
            return "INT", varScope, arrayScope, funcScope, number, tree, None, None
        else:
          print(leftType, rightType)
          raise Exception("Invalid types around operator in: " + tree.cleanPrint())
    
  elif isinstance(tree, list):
    if len(tree) != 0:
      #print("---tree---")
      #print(tree)
      if tree[1] == "IDENTIFIER":
        if varScope.variableFindable(tree[0]):
          var = varScope.getVariable(tree[0])
          tree[0] = var[2]
          return var[1], varScope, arrayScope, funcScope, number, tree, None, None
        elif arrayScope.arrayFindable(tree[0]):
          var = arrayScope.getArray(tree[0])
          tree[0] = var[3]
          return var[1], varScope, arrayScope, funcScope, number, tree, None, None
      elif tree[1] == "NUMBER":
        return "INT_CONST", varScope, arrayScope, funcScope, number, tree, None, None
      elif tree[1] == "CHAR":
        return "CHAR_CONST", varScope, arrayScope, funcScope, number, tree, None, None
      elif tree[1] == "BOOLEAN":
        return "BOOLEAN_CONST", varScope, arrayScope, funcScope, number, tree, None, None
      elif tree[1] == "STRING":
        return "STRING_CONST", varScope, arrayScope, funcScope, number, tree, None, None
      elif tree[0] == "ELSE":
        return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
  return "NONE", varScope, arrayScope, funcScope, number, tree, None, None
    
def removeDeclarationsCode(tree):
  if isinstance(tree,list):
    for i in range(len(tree)):
      if isinstance(tree[i], list):
        if len(tree[i]) == 2:
          if tree[i][1] in ["KEYWORD", "ASSIGNER", "MODIFIER", "TYPE", "ARRAY_TYPE", "COMPARATOR", "SUBSCRIPT", "OPERATOR", "BOOLEAN_OPERATOR", "NEGATOR", "NUMBER", "CHAR", "STRING", "IDENTIFIER", "PARAMETERS"]:
            if tree[i][1] in ["TYPE", "ARRAY_TYPE"]:
              tree[i] = []
            else:
              tree[i] = removeDeclarationsCode(tree[i])
          else:
            tree[i] = removeDeclarationsCode(tree[i])
        else:
          tree[i] = removeDeclarationsCode(tree[i])
      elif isinstance(tree[i], StatementTree):
          tree[i] = removeDeclarations(tree[i])
  return tree
    
def removeDeclarations(tree):
  #print(tree)
  if isinstance(tree, StatementTree):
    if tree.operator[1] == "TYPE":
      return removeDeclarations(tree.right)
    elif tree.operator[1] == "ARRAY_TYPE":
      return removeDeclarations(tree.right.left)
    elif tree.operator[1] == "PARAMETERS":
      parameters = []
      for i in tree.right:
        parameters.append(removeDeclarations(i))
      tree.right = parameters
      return(tree)
    elif tree.operator[1] == "ARRAY":
      elements = []
      for i in tree.right:
        elements.append(removeDeclarations(i))
      tree.right = elements
      return(tree)
    else:
      tree.left = removeDeclarations(tree.left)
      tree.right = removeDeclarations(tree.right)
      return tree
  elif isinstance(tree, list):
    if len(tree) == 2:
      if tree[1] in ["TYPE", "ARRAY_TYPE"]:
        return []
      elif tree[1] == "NUMBER":
        tree[0] = convertToNumber(tree[0])
        return tree
      elif tree[1] == "BOOLEAN":
        if tree[0] == "true":
          tree[0] = 1
        elif tree[0] == "false":
          tree[0] = 0
        return tree
      elif tree[1] == "CHAR":
        tree[0] = convertCharIntoDecimal(tree[0])
        return tree
      else:
        return tree
    else:
      return tree
    
def removeEmptyLines(tree):
  if isinstance(tree, list):
    for i in range(len(tree)-1, 0, -1):
      if isinstance(tree[i], list):
        if len(tree[i]) == 2:
          if tree[i][1] in ["KEYWORD", "ASSIGNER", "MODIFIER", "TYPE", "ARRAY_TYPE", "COMPARATOR", "SUBSCRIPT", "OPERATOR", "BOOLEAN_OPERATOR", "NEGATOR", "NUMBER", "CHAR", "STRING", "IDENTIFIER", "PARAMETERS"]:
            if tree[i][1] == "IDENTIFIER":
              tree.pop(i)
          else:
            tree[i] = removeEmptyLines(tree[i])
        elif tree[i] == []:
          tree.pop(i)
        else:
          tree[i] = removeEmptyLines(tree[i])
  return tree

def convertCodeIntoPartial(tree, previousLine, fullScope, number = 0, functionHeader = None):
  startPreviousLine = previousLine
  jumpNumber = number
  if isinstance(tree, list):
    i = 0
    endIfName = None
    previousConditionalName = None
    handlingIf = False
    functionBlock = []
    
    def handlingIfFunc():
      nonlocal handlingIf
      nonlocal previousLine
      nonlocal endIfName
      if handlingIf:
        if endIfName != None:
          previousLine.addName(endIfName)
          endIfName = None
        handlingIf = False
    
    while i < len(tree):
      if debug:
        #print("-----")
        #print(tree[i])
        pass
      if isinstance(tree[i], list):
        if len(tree[i]) == 2:
          
          #KEYWORD
          if tree[i][1] == "KEYWORD":
            
            #ELSE
            if tree[i][0] == "else":
              if endIfName == None:
                endIfName = "jENDIF" + str(jumpNumber)
                jumpNumber += 1
              
              if previousConditionalName != None:
                previousLine.getLastLine().removeName(previousConditionalName)
                previousLine.setLastLine(CodeLine("JMP", [endIfName], None))
                previousLine.getLastLine().getLastLine().addName(previousConditionalName)
                previousConditionalName = None
                
              i += 1
              temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
              previousLine = temp[1]
              jumpNumber = temp[2]
              previousLine.getLastLine().addName(endIfName)
              endIfName = None
              handlingIf = False
              
            #PAUSE
            elif tree[i][0] == "pause":
              handlingIfFunc()
              previousLine.setLastLine(CodeLine("PWS", [], None))
              previousLine = previousLine.getLastLine()
              
            #GRAPHICS
            elif tree[i][0] == "graphics":
              handlingIfFunc()
              previousLine.setLastLine(CodeLine("GRF", [], None))
              previousLine = previousLine.getLastLine()
              
      elif isinstance(tree[i], StatementTree):
        if debug:
          print("|" + tree[i].operator[0] + "|")
          pass
        
        #KEYWORD
        if tree[i].operator[1] == "KEYWORD":
          
          #IF
          if tree[i].operator[0] == "if":
            handlingIfFunc()
            
            temp = convertIntoPartial(previousLine, tree[i].right, fullScope, 0, jumpNumber)
            previousLine = temp[1]
            result = temp[2]
            tempNumber = temp[3]
            jumpNumber = temp[4]
            
            handlingIf = True
            if len(result) == 1:
              if result[0][1] == "CONST":
                if result[0][0] == 0:
                  i += 1
                else:
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number = jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
              elif result[0][1] == "DIR":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousLine.setLastLine(CodeLine("ANB INB", [0, result[0][0]], None))
                previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "IN":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousLine.setLastLine(CodeLine("LDI", [0, "TEMP0"], None))
                previousLine.setLastLine(CodeLine("ANB INB", [0, "TEMP0"], None))
                previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "ACC":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = None
                if result[0][2] == previousLine.getLastLine():
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                else:
                  tempOperator = "TEMP" + str(tempNumber)
                  tempNumber += 1
                  result[0][2].convertToACCDLoad(tempOperator)
                  previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "ACC2":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                tempOperator = "TEMP" + str(tempNumber)
                tempNumber += 1
                result[0][2].convertToACC2DLoad(tempOperator)
                previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "FLAG0":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = ConditionalLine("JPF 20", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "FLAG1":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = ConditionalLine("JPF 08", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "FLAG2":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = ConditionalLine("JPF 02", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "NFLAG2":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = ConditionalLine("JPF 03", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              else:
                raise Exception("Invalid type " + result[0][1] + " for condition in: " + tree[i].cleanPrint())
            else:
              raise Exception("Too many conditions for if statement in: " + tree[i].cleanPrint())
            
          #ELIF
          elif tree[i].operator[0] == "elif":
            if not handlingIf:
              raise Exception("Elif without if in: " + tree[i].cleanPrint())
            
            if endIfName == None:
              endIfName = "jENDIF" + str(jumpNumber)
              jumpNumber += 1
            
            if previousConditionalName != None:
              previousLine.getLastLine().removeName(previousConditionalName)
              previousLine.setLastLine(CodeLine("JMP", [endIfName], None))
              previousLine.getLastLine().addName(previousConditionalName)
              previousConditionalName = None
            
            temp = convertIntoPartial(previousLine, tree[i].right, fullScope, 0, jumpNumber)
            previousLine = temp[1]
            result = temp[2]
            tempNumber = temp[3]
            jumpNumber = temp[4]
            
            if len(result) == 1:
              if result[0][1] == "CONST":
                if result[0][0] == 0:
                  i += 1
                else:
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
              elif result[0][1] == "DIR":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousLine.setLastLine(CodeLine("ANB INB", [0, result[0][0]], None))
                previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "IN":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousLine.setLastLine(CodeLine("LDI", [0, "TEMP0"], None))
                previousLine.setLastLine(CodeLine("ANB INB", [0, "TEMP0"], None))
                previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "ACC":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = None
                if result[0][2] == previousLine.getLastLine():
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                else:
                  tempOperator = "TEMP" + str(tempNumber)
                  tempNumber += 1
                  result[0][2].convertToACCDLoad(tempOperator)
                  previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "ACC2":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                tempOperator = "TEMP" + str(tempNumber)
                tempNumber += 1
                result[0][2].convertToACC2DLoad(tempOperator)
                previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "FLAG0":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = ConditionalLine("JPF 20", [pastJumpName], None, None)
                previousLine.getLastLine().setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "FLAG1":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = ConditionalLine("JPF 08", [pastJumpName], None, None)
                previousLine.getLastLine().setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "FLAG2":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = ConditionalLine("JPF 02", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              elif result[0][1] == "NFLAG2":
                pastJumpName = "jPASTIF" + str(jumpNumber)
                jumpNumber += 1
                previousConditionalName = pastJumpName
                previousConditional = ConditionalLine("JPF 03", [pastJumpName], None, None)
                previousLine.setLastLine(previousConditional)
                i += 1
                temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                previousLine = temp[1]
                jumpNumber = temp[2]
                previousLine.getLastLine().addName(pastJumpName)
                previousConditional.setNextLineFalse(previousLine)
              else:
                raise Exception("Invalid type " + result[0][1] + " for condition in: " + tree[i].cleanPrint())
            else:
              raise Exception("Too many conditions for if statement in: " + tree[i].cleanPrint())
            
          #ELSE
          elif tree[i].operator[0] == "else":
            raise Exception("Invalid else statement")
            
          #FOR
          elif tree[i].operator[0] == "for":
            handlingIfFunc()
            if isinstance(tree[i].right.right, StatementTree):
              if tree[i].right.right.operator[0] == "to":
                counterIdentifier = tree[i].right.left
                
                tempLeft = convertIntoPartial(previousLine, StatementTree(counterIdentifier, tree[i].right.right.left, ["=", "ASSIGNER"]), fullScope, 0, jumpNumber)
                jumpNumber = tempLeft[4]
                previousLine = tempLeft[1]
                
                startLoopName = "jSTARTFOR" + str(jumpNumber)
                jumpNumber += 1
                previousLine.getLastLine().addName(startLoopName)
                  
                tempRight = convertIntoPartial(previousLine, StatementTree(tree[i].right.right.right, counterIdentifier, [">","COMPARATOR"]), fullScope, tempLeft[3], jumpNumber)
                previousLine = tempRight[1]
                result = tempRight[2]
                tempNumber = tempRight[3]
                jumpNumber = tempRight[4]
                
                if len(result) == 1:
                  if result[0][1] == "CONST":
                    if result[0][0] == 0:
                      i += 1
                    else:
                      i += 1
                      temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                      previousLine = temp[1]
                      jumpNumber = temp[2]
                      previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                      previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  elif result[0][1] == "DIR":
                    pastJumpName = "jPASTFOR" + str(jumpNumber)
                    jumpNumber += 1
                    previousConditionalName = pastJumpName
                    previousLine.setLastLine(CodeLine("ANB INB", [0, result[0][0]], None))
                    previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                    previousLine = previousLine.getLastLine()
                    previousLine.getLastLine().addName(pastJumpName)
                    previousConditional.setNextLineFalse(previousLine)
                  elif result[0][1] == "IN":
                    pastJumpName = "jPASTFOR" + str(jumpNumber)
                    jumpNumber += 1
                    previousConditionalName = pastJumpName
                    previousLine.setLastLine(CodeLine("LDI", [0, "TEMP0"], None))
                    previousLine.setLastLine(CodeLine("ANB INB", [0, "TEMP0"], None))
                    previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                    previousLine = previousLine.getLastLine()
                    previousLine.getLastLine().addName(pastJumpName)
                    previousConditional.setNextLineFalse(previousLine)
                  elif result[0][1] == "ACC":
                    pastJumpName = "jPASTFOR" + str(jumpNumber)
                    jumpNumber += 1
                    previousConditionalName = pastJumpName
                    previousConditional = None
                    if result[0][2] == previousLine.getLastLine():
                      previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                      previousLine.setLastLine(previousConditional)
                    else:
                      tempOperator = "TEMP" + str(tempNumber)
                      tempNumber += 1
                      result[0][2].convertToACCDLoad(tempOperator)
                      previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                      previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                      previousLine.setLastLine(previousConditional)
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                    previousLine = previousLine.getLastLine()
                    previousLine.getLastLine().addName(pastJumpName)
                    previousConditional.setNextLineFalse(previousLine)
                  elif result[0][1] == "ACC2":
                    pastJumpName = "jPASTFOR" + str(jumpNumber)
                    jumpNumber += 1
                    previousConditionalName = pastJumpName
                    tempOperator = "TEMP" + str(tempNumber)
                    tempNumber += 1
                    result[0][2].convertToACC2DLoad(tempOperator)
                    previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                    previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                    previousLine = previousLine.getLastLine()
                    previousLine.getLastLine().addName(pastJumpName)
                    previousConditional.setNextLineFalse(previousLine)
                  elif result[0][1] == "FLAG0":
                    pastJumpName = "jPASTFOR" + str(jumpNumber)
                    jumpNumber += 1
                    previousConditionalName = pastJumpName
                    previousConditional = ConditionalLine("JPF 20", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                    previousLine = previousLine.getLastLine()
                    previousLine.getLastLine().addName(pastJumpName)
                    previousConditional.setNextLineFalse(previousLine)
                  elif result[0][1] == "FLAG1":
                    pastJumpName = "jPASTFOR" + str(jumpNumber)
                    jumpNumber += 1
                    previousConditionalName = pastJumpName
                    previousConditional = ConditionalLine("JPF 08", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                    previousLine = previousLine.getLastLine()
                    previousLine.getLastLine().addName(pastJumpName)
                    previousConditional.setNextLineFalse(previousLine)
                  elif result[0][1] == "FLAG2":
                    pastJumpName = "jPASTFOR" + str(jumpNumber)
                    jumpNumber += 1
                    previousConditionalName = pastJumpName
                    previousConditional = ConditionalLine("JPF 02", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                    previousLine = previousLine.getLastLine()
                    previousLine.getLastLine().addName(pastJumpName)
                    previousConditional.setNextLineFalse(previousLine)
                  elif result[0][1] == "NFLAG2":
                    pastJumpName = "jPASTFOR" + str(jumpNumber)
                    jumpNumber += 1
                    previousConditionalName = pastJumpName
                    previousConditional = ConditionalLine("JPF 03", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                    previousLine = previousLine.getLastLine()
                    previousLine.getLastLine().addName(pastJumpName)
                    previousConditional.setNextLineFalse(previousLine)
                  else:
                    raise Exception("Unaccounted type " + result[0][1] + " in " + tree[i].cleanPrint())
                else:
                  raise Exception("Invalid condition for for in: " + tree[i].cleanPrint())
              
            else:
              
              counterIdentifier = "COUNTER" + str(jumpNumber)
              fullScope[counterIdentifier] = ["INT", 1, [], []]
              jumpNumber += 1
              elementIdentifier = tree[i].right.left
              
              tempLeft = convertIntoPartial(previousLine, tree[i].right.right, fullScope, 0, jumpNumber)
              jumpNumber = tempLeft[4]
              previousLine = tempLeft[1]
              arrayOperand = tempLeft[2]
              
              previousLine.setLastLine(CodeLine("LDV", [0, counterIdentifier], None))
              startLoopName = "jSTARTFOR" + str(jumpNumber)
              jumpNumber += 1
              previousLine.getLastLine().addName(startLoopName)
              
              temp = convertIntoPartial(previousLine, StatementTree(elementIdentifier, StatementTree([arrayOperand[0][0], "IDENTIFIER"], [counterIdentifier, "IDENTIFIER"], ["[]", "SUBSCRIPT"]), ["=", "ASSIGNER"]), fullScope, 0, jumpNumber, case=1)
              previousLine = temp[1]
              number = temp[3]
              jumpNumber = temp[4]
              
              temp = convertIntoPartial(previousLine, StatementTree([len(arrayOperand), "NUMBER"], [counterIdentifier, "IDENTIFIER"], [">", "COMPARATOR"]), fullScope, 0, jumpNumber)
              previousLine = temp[1]
              result = temp[2]
              number = temp[3]
              jumpNumber = temp[4]
              
              if len(result) == 1:
                if result[0][1] == "CONST":
                  if result[0][0] == 0:
                    i += 1
                  else:
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier, counterIdentifier], None))
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                elif result[0][1] == "DIR":
                  pastJumpName = "jPASTFOR" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousLine.setLastLine(CodeLine("ANB INB", [0, result[0][0]], None))
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier, counterIdentifier], None))
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "IN":
                  pastJumpName = "jPASTFOR" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousLine.setLastLine(CodeLine("LDI", [0, "TEMP0"], None))
                  previousLine.setLastLine(CodeLine("ANB INB", [0, "TEMP0"], None))
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier, counterIdentifier], None))
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "ACC":
                  pastJumpName = "jPASTFOR" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = None
                  if result[0][2] == previousLine.getLastLine():
                    previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                  else:
                    tempOperator = "TEMP" + str(tempNumber)
                    tempNumber += 1
                    result[0][2].convertToACCDLoad(tempOperator)
                    previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                    previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "ACC2":
                  pastJumpName = "jPASTFOR" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  tempOperator = "TEMP" + str(tempNumber)
                  tempNumber += 1
                  result[0][2].convertToACC2DLoad(tempOperator)
                  previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier[0], counterIdentifier[0]], None))
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "FLAG0":
                  pastJumpName = "jPASTFOR" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = ConditionalLine("JPF 20", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier, counterIdentifier], None))
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "FLAG1":
                  pastJumpName = "jPASTFOR" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = ConditionalLine("JPF 08", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier, counterIdentifier], None))
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "FLAG2":
                  pastJumpName = "jPASTFOR" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = ConditionalLine("JPF 02", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier, counterIdentifier], None))
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "NFLAG2":
                  pastJumpName = "jPASTFOR" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = ConditionalLine("JPF 03", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("ALB ICB", [0, counterIdentifier, counterIdentifier], None))
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                else:
                  raise Exception("Unaccounted type " + result[0][1] + " in " + tree[i].cleanPrint())
              else:
                raise Exception("Invalid condition for for in: " + tree[i].cleanPrint())
          
          #WHILE
          elif tree[i].operator[0] == "while":
            
            handlingIfFunc()
            startLoopName = "jSTARTWHILE" + str(jumpNumber)
            jumpNumber += 1
            previousLine.getLastLine().addName(startLoopName)
            
            tempLeft = convertIntoPartial(previousLine, tree[i].right, fullScope, 0, jumpNumber)
            jumpNumber = tempLeft[4]
            previousLine = tempLeft[1]
            result = tempLeft[2]
            if debug:
              print("Result:", result)
              pass
            
            if len(result) == 1:
              if len(result) == 1:
                if result[0][1] == "CONST":
                  if result[0][0] == 0:
                    i += 1
                  else:
                    i += 1
                    temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                    previousLine = temp[1]
                    jumpNumber = temp[2]
                    previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                elif result[0][1] == "DIR":
                  pastJumpName = "jPASTWHILE" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousLine.setLastLine(CodeLine("ANB INB", [0, result[0][0]], None))
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "IN":
                  pastJumpName = "jPASTTWHILE" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousLine.setLastLine(CodeLine("LDI", [0, "TEMP0"], None))
                  previousLine.setLastLine(CodeLine("ANB INB", [0, "TEMP0"], None))
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "ACC":
                  pastJumpName = "jPASTTWHILE" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = None
                  if result[0][2] == previousLine.getLastLine():
                    previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                  else:
                    tempOperator = "TEMP" + str(tempNumber)
                    tempNumber += 1
                    result[0][2].convertToACCDLoad(tempOperator)
                    previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                    previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                    previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "ACC2":
                  pastJumpName = "jPASTTWHILE" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  tempOperator = "TEMP" + str(tempNumber)
                  tempNumber += 1
                  result[0][2].convertToACC2DLoad(tempOperator)
                  previousLine.setLastLine(CodeLine("ANB INB", [0, tempOperator], None))
                  previousConditional = ConditionalLine("JPF EQL", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "FLAG0":
                  pastJumpName = "jPASTWHILE" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = ConditionalLine("JPF 20", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "FLAG1":
                  pastJumpName = "jPASTWHILE" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = ConditionalLine("JPF 08", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "FLAG2":
                  pastJumpName = "jPASTWHILE" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = ConditionalLine("JPF 02", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                elif result[0][1] == "NFLAG2":
                  pastJumpName = "jPASTWHILE" + str(jumpNumber)
                  jumpNumber += 1
                  previousConditionalName = pastJumpName
                  previousConditional = ConditionalLine("JPF 03", [pastJumpName], None, None)
                  previousLine.setLastLine(previousConditional)
                  i += 1
                  temp = convertCodeIntoPartial(tree[i], previousLine, fullScope, number=jumpNumber)
                  previousLine = temp[1]
                  jumpNumber = temp[2]
                  previousLine.setLastLine(CodeLine("JMP", [startLoopName], None))
                  previousLine = previousLine.getLastLine()
                  previousLine.getLastLine().addName(pastJumpName)
                  previousConditional.setNextLineFalse(previousLine)
                else:
                  raise Exception("Unaccounted type " + result[0][1] + " in " + tree[i].cleanPrint())
            
          #PUSH POP
          elif tree[i].operator[0] in ["pop", "push"]:
            handlingIfFunc()
            temp1, previousLine, temp2, number, jumpNumber = convertIntoPartial(previousLine.getLastLine(), tree[i], fullScope, 0, jumpNumber)
            
          #DEF
          elif tree[i].operator[0] == "def":
            if tree[i].right.operator[1] == "PARAMETERS":
              functionBlock.append([tree[i].right.left, tree[i+1]])
              i += 1
            else:
              raise Exception("Invalid function declaration in: " + tree[i].cleanPrint())
              
          elif tree[i].operator[0] == "return":
            handlingIfFunc()
            temp = convertIntoPartial(previousLine.getLastLine(), StatementTree([], tree[i].right, ["push", "KEYWORD"]), fullScope, 0, jumpNumber, case = 2)
            previousLine = temp[1]
            jumpNumber = temp[4]
        else:
          handlingIfFunc()
          temp = convertIntoPartial(previousLine.getLastLine(), tree[i], fullScope, 0, jumpNumber)
          previousLine = temp[1]
          jumpNumber = temp[4]
      i += 1
    
    handlingIfFunc()
    if functionHeader != None:
      previousLine.setLastLine(CodeLine("PPD", ["RETURNA"], None))
      previousLine.setLastLine(CodeLine("JPD", ["RETURNA"], None))
    for i in functionBlock:
      if debug:
        print(i[0][0])
      previousLine.getLastLine().addName(i[0][0])
      temp = convertCodeIntoPartial(i[1], previousLine, fullScope, number = jumpNumber, functionHeader = i[0][0])
      previousLine = temp[1]
      jumpNumber = temp[2]
      
  return startPreviousLine, previousLine.getLastLine(), jumpNumber

def convertFlagIntoPartial(previousLine, flagBit, number):
  if flagBit == "FLAG0":
    resultOperand = "TEMP" + str(number)
    number += 1
    previousLine.setLastLine(CodeLine("ALB AND", [1, "FLG", resultOperand], None))
    return previousLine, resultOperand, number
  elif flagBit == "FLAG1":
    resultOperand = "TEMP" + str(number)
    number += 1
    previousLine.setLastLine(CodeLine("ALB AND", [2, "FLG", resultOperand], None))
    previousLine.setLastLine(CodeLine("ALB SRB", [0, resultOperand, resultOperand], None))
    return previousLine, resultOperand, number
  elif flagBit == "FLAG2":
    resultOperand = "TEMP" + str(number)
    number += 1
    previousLine.setLastLine(CodeLine("ALB RSB", [2, "FLG", resultOperand], None))
    return previousLine, resultOperand, number
  elif flagBit == "NFLAG0":
    resultOperand = "TEMP" + str(number)
    number += 1
    previousLine.setLastLine(CodeLine("ALB 091", [1, "FLG", resultOperand], None))
    return previousLine, resultOperand, number
  elif flagBit == "NFLAG1":
    resultOperand = "TEMP" + str(number)
    number += 1
    previousLine.setLastLine(CodeLine("ALB 091", [2, "FLG", resultOperand], None))
    previousLine.setLastLine(CodeLine("ALB SRB", [0, resultOperand, resultOperand], None))
  elif flagBit == "NFLAG2":
    resultOperand = "TEMP" + str(number)
    number += 1
    previousLine.setLastLine(CodeLine("ALB NGB", [0, "FLG", resultOperand], None))
    previousLine.setLastLine(CodeLine("ALB RSB", [2, resultOperand, resultOperand], None))
    return previousLine, resultOperand, number

#returns previousLine, lastLine, [[resultLoc, resultType]], number, jumpNumber (resultType:, CONST = constant, DIR = direct address, IN = indirect address, POP = on Stack, FLAG0 = Flag bit 0, FLAG1 = Flag bit 1, FLAG2 = Flag Bit 2, NFLAG2 = NOT Flag Bit 2, ACC = accumukator, ACC2 = accumulator2)
def convertIntoPartial(previousLine, tree, fullScope, number, jumpNumber, case = 0):
  if debug:
    #print(tree)
    pass
  if isinstance(tree, StatementTree):
    
    #OPERATOR
    if tree.operator[1] == "OPERATOR":
      
      tempLeft = convertIntoPartial(previousLine, tree.left, fullScope, number, jumpNumber)
      leftOperand = tempLeft[2]
      number = tempLeft[3]
      jumpNumber = tempLeft[4]
      
      for i in range(len(leftOperand)):
        if leftOperand[i][1] == "POP":
          replaceOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
          leftOperand[i][0] = replaceOperand
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
          temp = convertFlagIntoPartial(previousLine, leftOperand[i][1], number)
          leftOperand[i][0] = temp[1]
          number = temp[2]
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] == "IN":
          resultOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("LDI", [leftOperand[i][0], resultOperand], None))
          leftOperand[i][0] = resultOperand
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] == "ACC":
          resultOperand = "TEMP" + str(number)
          number += 1
          leftOperand[i][2].convertToACCDLoad(resultOperand)
          leftOperand[i][0] = resultOperand
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] == "ACC2":
          resultOperand = "TEMP" + str(number)
          number += 1
          leftOperand[i][2].convertToACC2DLoad(resultOperand)
          leftOperand[i][0] = resultOperand
          leftOperand[i][1] = "DIR"
        
      tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber)
      rightOperand = tempRight[2]
      number = tempRight[3]
      jumpNumber = tempRight[4]
      
      for i in range(len(rightOperand)):
        if rightOperand[i][1] == "POP":
          replaceOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
          rightOperand[i][0] = replaceOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
          temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
          rightOperand[i][0] = temp[1]
          number = temp[2]
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "IN":
          resultOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("LDI", [rightOperand[i][0], resultOperand], None))
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "ACC":
          resultOperand = "TEMP" + str(number)
          number += 1
          rightOperand[i][2].convertToACCDLoad(resultOperand)
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "ACC2":
          resultOperand = "TEMP" + str(number)
          number += 1
          rightOperand[i][2].convertToACC2DLoad(resultOperand)
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
        
      result = []
      if len(leftOperand) == len(rightOperand):
        for i in range(len(leftOperand)):
          if leftOperand[i][1] == "CONST":
            if rightOperand[i][1] == "CONST":
              if tree.operator[0] == "+":
                result.append([leftOperand[i][0] + rightOperand[i][0], "CONST"])
              elif tree.operator[0] == "-":
                result.append([leftOperand[i][0] - rightOperand[i][0], "CONST"])
              elif tree.operator[0] == "*":
                result.append([leftOperand[i][0] * rightOperand[i][0], "CONST"])
              elif tree.operator[0] == "/":
                result.append([leftOperand[i][0] // rightOperand[i][0], "CONST"])
              elif tree.operator[0] == "%":
                result.append([leftOperand[i][0] % rightOperand[i][0], "CONST"])
              elif tree.operator[0] == ">>":
                result.append([leftOperand[i][0] >> rightOperand[i][0], "CONST"])
              elif tree.operator[0] == "<<":
                result.append([leftOperand[i][0] << rightOperand[i][0], "CONST"])
              elif tree.operator[0] == "&":
                result.append([leftOperand[i][0] & rightOperand[i][0], "CONST"])
              elif tree.operator[0] == "|":
                result.append([leftOperand[i][0] | rightOperand[i][0], "CONST"])
              elif tree.operator[0] == "^":
                result.append([leftOperand[i][0] ^ rightOperand[i][0], "CONST"])
              else:
                raise Exception("Missing case in: " + tree.cleanPrint())
            elif rightOperand[i][1] == "DIR":
              if tree.operator[0] != "%":
                assemblyOperator = "ANB"
                if tree.operator[0] == "+":
                  assemblyOperator += " ADD"
                elif tree.operator[0] == "-":
                  assemblyOperator += " SBA"
                elif tree.operator[0] == "*":
                  assemblyOperator += " MLT"
                elif tree.operator[0] == "/":
                  assemblyOperator += " DVA"
                elif tree.operator[0] == ">>":
                  assemblyOperator += " RSA"
                elif tree.operator[0] == "<<":
                  assemblyOperator += " LSA"
                elif tree.operator[0] == "&":
                  assemblyOperator += " AND"
                elif tree.operator[0] == "|":
                  assemblyOperator += " ORR"
                elif tree.operator[0] == "^":
                  assemblyOperator += " XOR"
                else:
                  raise Exception("Missing case in: " + tree.cleanPrint())
                previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[i][0], rightOperand[i][0]], None))
                result.append(["", "ACC", previousLine.getLastLine()])
              else:
                assemblyOperator = "ANB DVA"
                previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[i][0], rightOperand[i][0]], None))
                result.append(["", "ACC2", previousLine.getLastLine()])
            else:
              raise Exception("Invalid type " + rightOperand[i][1] + " in: " + tree.cleanPrint())
            pass
          elif leftOperand[i][1] == "DIR":
            if rightOperand[i][1] == "CONST":
              if tree.operator[0] != "%":
                assemblyOperator = "ANB"
                if tree.operator[0] == "+":
                  assemblyOperator += " ADD"
                elif tree.operator[0] == "-":
                  assemblyOperator += " SBB"
                elif tree.operator[0] == "*":
                  assemblyOperator += " MLT"
                elif tree.operator[0] == "/":
                  assemblyOperator += " DVB"
                elif tree.operator[0] == ">>":
                  assemblyOperator += " RSB"
                elif tree.operator[0] == "<<":
                  assemblyOperator += " LSB"
                elif tree.operator[0] == "&":
                  assemblyOperator += " AND"
                elif tree.operator[0] == "|":
                  assemblyOperator += " ORR"
                elif tree.operator[0] == "^":
                  assemblyOperator += " XOR"
                else:
                  raise Exception("Missing case in: " + tree.cleanPrint())
                previousLine.setLastLine(CodeLine(assemblyOperator, [rightOperand[i][0], leftOperand[i][0]], None))
                result.append(["", "ACC", previousLine.getLastLine()])
              else:
                assemblyOperator = "ANB DVB"
                previousLine.setLastLine(CodeLine(assemblyOperator, [rightOperand[i][0], leftOperand[i][0]], None))
                result.append(["", "ACC2", previousLine.getLastLine()])
            elif rightOperand[i][1] == "DIR":
              if tree.operator[0] != "%":
                assemblyOperator = "AND"
                if tree.operator[0] == "+":
                  assemblyOperator += " ADD"
                elif tree.operator[0] == "-":
                  assemblyOperator += " SBA"
                elif tree.operator[0] == "*":
                  assemblyOperator += " MLT"
                elif tree.operator[0] == "/":
                  assemblyOperator += " DVA"
                elif tree.operator[0] == "%":
                  assemblyOperator += " DVA"
                elif tree.operator[0] == ">>":
                  assemblyOperator += " RSA"
                elif tree.operator[0] == "<<":
                  assemblyOperator += " LSA"
                elif tree.operator[0] == "&":
                  assemblyOperator += " AND"
                elif tree.operator[0] == "|":
                  assemblyOperator += " ORR"
                elif tree.operator[0] == "^":
                  assemblyOperator += " XOR"
                else:
                  raise Exception("Missing case in: " + tree.cleanPrint())
                previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[i][0], rightOperand[i][0]], None))
                result.append(["", "ACC", previousLine.getLastLine()])
              else:
                assemblyOperator = "AND DVA"
                previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[i][0], rightOperand[i][0]], None))
                result.append(["", "ACC2", previousLine.getLastLine()])
            else:
              raise Exception("Invalid type " + rightOperand[i][1] + " in: " + tree.cleanPrint())
          else:
            raise Exception("Invalid type " + leftOperand[i][1] + " in: " + tree.cleanPrint())
      else:
        raise Exception("Mismatched operand lengths in: " + tree.cleanPrint())
        
      return previousLine, previousLine.getLastLine(), result, number, jumpNumber
    
    #BOOLEAN_OPERATOR
    elif tree.operator[1] == "BOOLEAN_OPERATOR":
      
      tempLeft = convertIntoPartial(previousLine, tree.left, fullScope, number, jumpNumber)
      leftOperand = tempLeft[2]
      number = tempLeft[3]
      jumpNumber = tempLeft[4]
      
      for i in range(len(leftOperand)):
        if leftOperand[i][1] == "POP":
          replaceOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
          leftOperand[i][0] = replaceOperand
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
          temp = convertFlagIntoPartial(previousLine, leftOperand[i][1], number)
          leftOperand[i][0] = temp[1]
          number = temp[2]
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] == "IN":
          resultOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("LDI", [leftOperand[i][0], resultOperand], None))
          leftOperand[i][0] = resultOperand
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] == "ACC":
          resultOperand = "TEMP" + str(number)
          number += 1
          leftOperand[i][2].convertToACCDLoad(resultOperand)
          leftOperand[i][0] = resultOperand
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] == "ACC2":
          resultOperand = "TEMP" + str(number)
          number += 1
          leftOperand[i][2].convertToACC2DLoad(resultOperand)
          leftOperand[i][0] = resultOperand
          leftOperand[i][1] = "DIR"
        
      tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber)
      rightOperand = tempRight[2]
      number = tempRight[3]
      jumpNumber = tempRight[4]
      
      for i in range(len(rightOperand)):
        if rightOperand[i][1] == "POP":
          replaceOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
          rightOperand[i][0] = replaceOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
          temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
          rightOperand[i][0] = temp[1]
          number = temp[2]
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "IN":
          resultOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("LDI", [rightOperand[i][0], resultOperand], None))
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "ACC":
          resultOperand = "TEMP" + str(number)
          number += 1
          rightOperand[i][2].convertToACCDLoad(resultOperand)
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "ACC2":
          resultOperand = "TEMP" + str(number)
          number += 1
          rightOperand[i][2].convertToACC2DLoad(resultOperand)
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
      
      result = []
      if len(leftOperand) == len(rightOperand):
        for i in range(len(leftOperand)):
          if leftOperand[i][1] == "CONST":
            if rightOperand[i][1] == "CONST":
              if tree.operator[0] == "and":
                result.append([(leftOperand[i][0] & rightOperand[i][0]) & 1, "CONST"])
              elif tree.operator[0] == "or":
                result.append([(leftOperand[i][0] | rightOperand[i][0]) & 1, "CONST"])
              elif tree.operator[0] == "xor":
                result.append([(leftOperand[i][0] ^ rightOperand[i][0]) & 1, "CONST"])
              elif tree.operator[0] == "nand":
                result.append([((leftOperand[i][0] & rightOperand[i][0]) ^ 0xffff) & 1, "CONST"])
              elif tree.operator[0] == "nor":
                result.append([((leftOperand[i][0] | rightOperand[i][0]) ^ 0xffff) & 1, "CONST"])
              elif tree.operator[0] == "xnor":
                result.append([((leftOperand[i][0] ^ rightOperand[i][0]) ^ 0xffff) & 1, "CONST"])
              else:
                raise Exception("Missing case in: " + tree.cleanPrint())
            elif rightOperand[i][1] == "DIR":
              assemblyOperator = "ALB"
              if tree.operator[0] == "and":
                assemblyOperator += " AND"
              elif tree.operator[0] == "or":
                assemblyOperator += " ORR"
              elif tree.operator[0] == "xor":
                assemblyOperator += " XOR"
              elif tree.operator[0] == "nand":
                assemblyOperator += " NND"
              elif tree.operator[0] == "nor":
                assemblyOperator += " NOR"
              elif tree.operator[0] == "xnor":
                assemblyOperator += " XNR"
              else:
                raise Exception("Missing case in: " + tree.cleanPrint())
              resultOperand = "TEMP" + str(number)
              number += 1
              previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[i][0], rightOperand[i][0], resultOperand], None))
              previousLine.setLastLine(CodeLine("ANB AND", [1, resultOperand], None))
              result.append(["", "ACC", previousLine.getLastLine()])
            else:
              raise Exception("Invalid type " + rightOperand[i][1] + " in: " + tree.cleanPrint())
            pass
          elif leftOperand[i][1] == "DIR":
            if rightOperand[i][1] == "CONST":
              assemblyOperator = "ALB"
              if tree.operator[0] == "and":
                assemblyOperator += " AND"
              elif tree.operator[0] == "or":
                assemblyOperator += " ORR"
              elif tree.operator[0] == "xor":
                assemblyOperator += " XOR"
              elif tree.operator[0] == "nand":
                assemblyOperator += " NND"
              elif tree.operator[0] == "nor":
                assemblyOperator += " NOR"
              elif tree.operator[0] == "xnor":
                assemblyOperator += " XNR"
              else:
                raise Exception("Missing case in: " + tree.cleanPrint())
              resultOperand = "TEMP" + str(number)
              number += 1
              previousLine.setLastLine(CodeLine(assemblyOperator, [rightOperand[i][0], leftOperand[i][0], resultOperand], None))
              previousLine.setLastLine(CodeLine("ANB AND", [1, resultOperand], None))
              result.append(["", "ACC", previousLine.getLastLine()])
            elif rightOperand[i][1] == "DIR":
              assemblyOperator = "ALD"
              if tree.operator[0] == "and":
                assemblyOperator += " AND"
              elif tree.operator[0] == "or":
                assemblyOperator += " ORR"
              elif tree.operator[0] == "xor":
                assemblyOperator += " XOR"
              elif tree.operator[0] == "nand":
                assemblyOperator += " NND"
              elif tree.operator[0] == "nor":
                assemblyOperator += " NOR"
              elif tree.operator[0] == "xnor":
                assemblyOperator += " XNR"
              else:
                raise Exception("Missing case in: " + tree.cleanPrint())
              resultOperand = "TEMP" + str(number)
              number += 1
              previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[i][0], rightOperand[i][0], resultOperand], None))
              previousLine.setLastLine(CodeLine("ANB AND", [1, resultOperand], None))
              result.append(["", "ACC", previousLine.getLastLine()])
            else:
              raise Exception("Invalid type " + rightOperand[i][1] + " in: " + tree.cleanPrint())
          else:
            raise Exception("Invalid type " + leftOperand[i][1] + " in: " + tree.cleanPrint())
      else:
        raise Exception("Mismatched operand lengths in: " + tree.cleanPrint())
        
      return previousLine, previousLine.getLastLine(), result, number, jumpNumber
    
    #NEGATOR
    elif tree.operator[1] == "NEGATOR":
      if tree.operator[0] == "not":
        
        tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber)
        rightOperand = tempRight[2]
        number = tempRight[3]
        jumpNumber = tempRight[4]
        
        result = []
        for i in range(len(rightOperand)):
          if rightOperand[i][1] == "POP":
            replaceOperand = "TEMP" + str(number)
            number += 1
            previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
            rightOperand[i][0] = replaceOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG1"]:
            temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
            rightOperand[i][0] = temp[1]
            number = temp[2]
          elif rightOperand[i][1] == "IN":
            resultOperand = "TEMP" + str(number)
            number += 1
            previousLine.setLastLine(CodeLine("LDI", [rightOperand[i][0], resultOperand], None))
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] == "ACC":
            resultOperand = "TEMP" + str(number)
            number += 1
            rightOperand[i][2].convertToACCDLoad(resultOperand)
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] == "ACC2":
            resultOperand = "TEMP" + str(number)
            number += 1
            rightOperand[i][2].convertToACC2DLoad(resultOperand)
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
            
          if rightOperand[i][1] == "CONST":
            result.append([(rightOperand[i][0] ^ 0xffff) & 1, "CONST"])
          elif rightOperand[i][1] == "DIR":
            resultOperand = "TEMP" + str(number)
            number += 1
            previousLine.setLastLine(CodeLine("ALB NTB", [0, rightOperand[i][0], resultOperand], None))
            previousLine.setLastLine(CodeLine("ANB AND", [1, resultOperand, resultOperand], None))
            result.append(["", "ACC", previousLine.getLastLine()])
          else:
            raise Exception("Invalid type " + rightOperand[i][1] + " in: " + tree.cleanPrint())
        
        return previousLine, previousLine.getLastLine(), result, number, jumpNumber
          
      else:
        
        tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber)
        rightOperand = tempRight[2]
        number = tempRight[3]
        jumpNumber = tempRight[4]
        
        result = []
        for i in range(len(rightOperand)):
          if rightOperand[i][1] == "POP":
            replaceOperand = "TEMP" + str(number)
            number += 1
            previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
            rightOperand[i][0] = replaceOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
            temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
            rightOperand[i][0] = temp[1]
            number = temp[2]
          elif rightOperand[i][1] == "IN":
            resultOperand = "TEMP" + str(number)
            number += 1
            previousLine.setLastLine(CodeLine("LDI", [rightOperand[i][0], resultOperand], None))
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] == "ACC":
            resultOperand = "TEMP" + str(number)
            number += 1
            rightOperand[i][2].convertToACCDLoad(resultOperand)
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] == "ACC2":
            resultOperand = "TEMP" + str(number)
            number += 1
            rightOperand[i][2].convertToACC2DLoad(resultOperand)
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
            
          if rightOperand[i][1] == "CONST":
            if tree.operator[0] == "!":
              result.append([(rightOperand[i][0] ^ 0xffff), "CONST"])
            elif tree.operator[0] == "-":
              result.append([-rightOperand[i][0], "CONST"])
            else:
              raise Exception("Invalid operator " + tree.operator[0] + " in: " + tree.cleanPrint())
          elif rightOperand[i][1] == "DIR":
            assemblyOperator = "ANB"
            if tree.operator[0] == "!":
              assemblyOperator += " NTB"
            elif tree.operator[0] == "-":
              assemblyOperator += " NGB"
            else:
              raise Exception("Invalid operator " + tree.operator[0] + " in: " + tree.cleanPrint())
            previousLine.setLastLine(CodeLine(assemblyOperator, [0, rightOperand[i][0]], None))
            result.append(["", "ACC", previousLine.getLastLine()])
          else:
            raise Exception("Invalid type " + rightOperand[i][1] + " in: " + tree.cleanPrint())
            
        
        return previousLine, previousLine.getLastLine(), result, number, jumpNumber
    
    #COMPARATOR
    elif tree.operator[1] == "COMPARATOR":
      
      tempLeft = convertIntoPartial(previousLine, tree.left, fullScope, number, jumpNumber)
      leftOperand = tempLeft[2]
      number = tempLeft[3]
      jumpNumber = tempLeft[4]
      
      for i in range(len(leftOperand)):
        if leftOperand[i][1] == "POP":
          replaceOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
          leftOperand[i][0] = replaceOperand
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
          temp = convertFlagIntoPartial(previousLine, leftOperand[i][1], number)
          leftOperand[i][0] = temp[1]
          number = temp[2]
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] == "IN":
          resultOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("LDI", [leftOperand[i][0], resultOperand], None))
          leftOperand[i][0] = resultOperand
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] == "ACC":
          resultOperand = "TEMP" + str(number)
          number += 1
          leftOperand[i][2].convertToACCDLoad(resultOperand)
          leftOperand[i][0] = resultOperand
          leftOperand[i][1] = "DIR"
        elif leftOperand[i][1] == "ACC2":
          resultOperand = "TEMP" + str(number)
          number += 1
          leftOperand[i][2].convertToACC2DLoad(resultOperand)
          leftOperand[i][0] = resultOperand
          leftOperand[i][1] = "DIR"
        
      tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber)
      rightOperand = tempRight[2]
      number = tempRight[3]
      jumpNumber = tempRight[4]
      
      for i in range(len(rightOperand)):
        if rightOperand[i][1] == "POP":
          replaceOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
          rightOperand[i][0] = replaceOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
          temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
          rightOperand[i][0] = temp[1]
          number = temp[2]
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "IN":
          resultOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("LDI", [rightOperand[i][0], resultOperand], None))
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "ACC":
          resultOperand = "TEMP" + str(number)
          number += 1
          rightOperand[i][2].convertToACCDLoad(resultOperand)
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "ACC2":
          resultOperand = "TEMP" + str(number)
          number += 1
          rightOperand[i][2].convertToACC2DLoad(resultOperand)
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
      
      result = []
      if len(leftOperand) == 1 and len(rightOperand) == 1:
        if leftOperand[0][1] == "CONST":
          if rightOperand[0][1] == "CONST":
            if tree.operator[0] == "==":
              result.append([int(leftOperand[0][0] == rightOperand[0][0]), "CONST"])
            elif tree.operator[0] == "<>":
              result.append([int(leftOperand[0][0] != rightOperand[0][0]), "CONST"])
            elif tree.operator[0] == "<":
              result.append([int(leftOperand[0][0] < rightOperand[0][0]), "CONST"])
            elif tree.operator[0] == ">":
              result.append([int(leftOperand[0][0] > rightOperand[0][0]), "CONST"])
            elif tree.operator[0] == "<=":
              result.append([int(leftOperand[0][0] <= rightOperand[0][0]), "CONST"])
            elif tree.operator[0] == ">=":
              result.append([int(leftOperand[0][0] >= rightOperand[0][0]), "CONST"])
            else:
              raise Exception("Missing case in: " + tree.cleanPrint())
          elif rightOperand[0][1] == "DIR":
            assemblyOperator = "ANB"
            flagBit = ""
            if tree.operator[0] == "==":
              assemblyOperator += " SBA"
              flagBit = "FLAG2"
            elif tree.operator[0] == "<>":
              assemblyOperator += " SBA"
              flagBit = "NFLAG2"
            elif tree.operator[0] == "<=":
              assemblyOperator += " SBB"
              flagBit = "FLAG1"
            elif tree.operator[0] == ">=":
              assemblyOperator += " SBA"
              flagBit = "FLAG1"
            elif tree.operator[0] == "<":
              assemblyOperator += " SBA"
              flagBit = "FLAG0"
            elif tree.operator[0] == ">":
              assemblyOperator += " SBB"
              flagBit = "FLAG0"
            else:
              raise Exception("Missing case in: " + tree.cleanPrint())
            previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[0][0], rightOperand[0][0]], None))
            result.append(["", flagBit])
          else:
            raise Exception("Invalid type " + rightOperand[0][1] + " in: " + tree.cleanPrint())
          pass
        elif leftOperand[0][1] == "DIR":
          if rightOperand[0][1] == "CONST":
            assemblyOperator = "ANB"
            flagBit = ""
            if tree.operator[0] == "==":
              assemblyOperator += " SBA"
              flagBit = "FLAG2"
            elif tree.operator[0] == "<>":
              assemblyOperator += " SBA"
              flagBit = "NFLAG2"
            elif tree.operator[0] == "<=":
              assemblyOperator += " SBA"
              flagBit = "FLAG1"
            elif tree.operator[0] == ">=":
              assemblyOperator += " SBB"
              flagBit = "FLAG1"
            elif tree.operator[0] == "<":
              assemblyOperator += " SBB"
              flagBit = "FLAG0"
            elif tree.operator[0] == ">":
              assemblyOperator += " SBA"
              flagBit = "FLAG0"
            else:
              raise Exception("Missing case in: " + tree.cleanPrint())
            previousLine.setLastLine(CodeLine(assemblyOperator, [rightOperand[0][0], leftOperand[0][0]], None))
            result.append(["", flagBit])
          elif rightOperand[0][1] == "DIR":
            assemblyOperator = "AND"
            flagBit = ""
            if tree.operator[0] == "==":
              assemblyOperator += " SBA"
              flagBit = "FLAG2"
            elif tree.operator[0] == "<>":
              assemblyOperator += " SBA"
              flagBit = "NFLAG2"
            elif tree.operator[0] == "<=":
              assemblyOperator += " SBB"
              flagBit = "FLAG1"
            elif tree.operator[0] == ">=":
              assemblyOperator += " SBA"
              flagBit = "FLAG1"
            elif tree.operator[0] == "<":
              assemblyOperator += " SBA"
              flagBit = "FLAG0"
            elif tree.operator[0] == ">":
              assemblyOperator += " SBB"
              flagBit = "FLAG0"
            else:
              raise Exception("Missing case in: " + tree.cleanPrint())
            previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[0][0], rightOperand[0][0]], None))
            result.append(["", flagBit])
          else:
            raise Exception("Invalid type " + rightOperand[0][1] + " in: " + tree.cleanPrint())
        else:
          raise Exception("Invalid type " + leftOperand[0][1] + " in: " + tree.cleanPrint())
        
      return previousLine, previousLine.getLastLine(), result, number, jumpNumber
    
    #KEYWORD
    elif tree.operator[1] == "KEYWORD":
      #PUSH
      if tree.operator[0] == "push":
        rightOperand = []
        
        tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber)
        rightOperand = tempRight[2]
        number = tempRight[3]
        jumpNumber = tempRight[4]
        
        result = []
        for i in range(len(rightOperand)):
          if rightOperand[i][1] == "POP":
            replaceOperand = "TEMP" + str(number)
            number += 1
            previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
            rightOperand[i][0] = replaceOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
            temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
            rightOperand[i][0] = temp[1]
            number = temp[2]
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] == "ACC":
            resultOperand = "TEMP" + str(number)
            number += 1
            rightOperand[i][2].convertToACCDLoad(resultOperand)
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] == "ACC2":
            resultOperand = "TEMP" + str(number)
            number += 1
            rightOperand[i][2].convertToACC2DLoad(resultOperand)
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
            
        if case == 2:
          previousLine.setLastLine(CodeLine("PPD", ["RETURNA"], None))
          
        for i in range(len(rightOperand)-1, -1, -1):
          if rightOperand[i][1] == "CONST":
            previousLine.setLastLine(CodeLine("PSV", [rightOperand[i][0]], None))
            result.append(["", "POP"])
          elif rightOperand[i][1] == "DIR":
            previousLine.setLastLine(CodeLine("PSD", [rightOperand[i][0]], None))
            result.append(["", "POP"])
          elif rightOperand[i][1] == "IN":
            previousLine.setLastLine(CodeLine("PSI", [rightOperand[i][0]], None))
            result.append(["", "POP"])
          else:
            raise Exception("Invalid type " + rightOperand[i][1] + " in: " + tree.cleanPrint())
            
        if case == 2:
          previousLine.setLastLine(CodeLine("JPD", ["RETURNA"], None))
        
        return previousLine, previousLine.getLastLine(), result, number, jumpNumber
      #POP
      elif tree.operator[0] == "pop":
        rightOperand = []
        
        tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber)
        rightOperand = tempRight[2]
        number = tempRight[3]
        jumpNumber = tempRight[4]
        
        result = []
        for i in range(len(leftOperand)-1, -1, -1):
          if rightOperand[i][1] == "DIR":
            previousLine.setLastLine(CodeLine("PPD", [rightOperand[i][0]], None))
            result.append([rightOperand[i][0], "DIR"])
          elif rightOperand[i][1] == "IN":
            previousLine.setLastLine(CodeLine("PPI", [rightOperand[i][0]], None))
            result.append([rightOperand[i][0], "IN"])
          else:
            raise Exception("Invalid type " + rightOperand[i][1] + " in: " + tree.cleanPrint())
        
        return previousLine, previousLine.getLastLine(), result, number, jumpNumber
    
    #SUBSCRIPT
    elif tree.operator[1] == "SUBSCRIPT":
      rightOperand = []
      
      tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber)
      rightOperand = tempRight[2]
      number = tempRight[3]
      jumpNumber = tempRight[4]
      
      for i in range(len(rightOperand)):
        if rightOperand[i][1] == "POP":
          replaceOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
          rightOperand[i][0] = replaceOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
          temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
          rightOperand[i][0] = temp[1]
          number = temp[2]
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "IN":
          resultOperand = "TEMP" + str(number)
          number += 1
          previousLine.setLastLine(CodeLine("LDI", [rightOperand[i][0], resultOperand], None))
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "ACC":
          resultOperand = "TEMP" + str(number)
          number += 1
          rightOperand[i][2].convertToACCDLoad(resultOperand)
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
        elif rightOperand[i][1] == "ACC2":
          resultOperand = "TEMP" + str(number)
          number += 1
          rightOperand[i][2].convertToACC2DLoad(resultOperand)
          rightOperand[i][0] = resultOperand
          rightOperand[i][1] = "DIR"
      
      leftOperand = []
      
      tempLeft = convertIntoPartial(previousLine, tree.left, fullScope, number, jumpNumber)
      leftOperand = tempLeft[2]
      number = tempLeft[3]
      jumpNumber = tempLeft[4]
      
      if len(rightOperand) == 1:
        leftOperandPop = False
        leftOperandAllPop = True
        for i in leftOperand:
          if i[1] == "POP":
            leftOperandPop = True
          else:
            leftOperandAllPop = False
        if leftOperandPop and leftOperandAllPop:
          if rightOperand[0][1] == "CONST":
            resultOperand = "TEMP" + str(number)
            number += 1
            for i in range(rightOperand[0][0]):
              previousLine.setLastLine(CodeLine("PPD", []))
            return previousLine, previousLine.getLastLine(), [[resultOperand, "DIR"]], number, jumpNumber
          elif rightOperand[0][1] == "DIR":
            if case == 1:
              return previousLine, previousLine.getLastLine(), [["", "POP"]], number, jumpNumber
            else:
              resultOperand = "TEMP" + str(number)
              number += 1
              raise Exception("Unfinished feature")
              previousLine.setLastLine(CodeLine("ALB ADD", [leftOperand[0][0], rightOperand[0][0], resultOperand], None))
              return previousLine, previousLine.getLastLine(), [[resultOperand, "DIR"]], number, jumpNumber
        elif not leftOperandPop and not leftOperandAllPop:
          if rightOperand[0][1] == "CONST":
            return previousLine, previousLine.getLastLine(), [[leftOperand[rightOperand[0][0]][0], "DIR"]], number, jumpNumber
          elif rightOperand[0][1] == "DIR":
            resultOperand = "TEMP" + str(number)
            number += 1
            previousLine.setLastLine(CodeLine("ALB ADD", [leftOperand[0][0], rightOperand[0][0], resultOperand], None))
            return previousLine, previousLine.getLastLine(), [[resultOperand, "IN"]], number, jumpNumber
        else:
          raise Exception("Problematic subscript in: " + tree.cleanPrint())
    
    #PARAMETERS
    elif tree.operator[1] == "PARAMETERS":
      funcInfo = fullScope[tree.left[0]]
      inputNames = funcInfo[3]
      if len(inputNames) != len(tree.right):
        raise Exception("Invalid parameter length at: " + tree.cleanPrint())
      for i in range(len(inputNames)):
        #print(StatementTree(inputNames[i], tree.right[i], ["=", "ASSIGNER"]))
        previousLine, temp, temp, number, jumpNumber = convertIntoPartial(previousLine, StatementTree([inputNames[i], "IDENTIFIER"], tree.right[i], ["=", "ASSIGNER"]), fullScope, number, jumpNumber)
      returnAddress = "jFUNCTIONRETURN" + str(jumpNumber)
      jumpNumber += 1
      previousLine.setLastLine(CodeLine("PSV", [returnAddress], None))
      previousLine.setLastLine(CodeLine("JMP", [tree.left[0]], None, name = returnAddress))
      
      if funcInfo[0] in ["INT", "CHAR", "BOOLEAN"]:
        return previousLine, previousLine.setLastLine, [["", "POP"]], number, jumpNumber
      
      elif funcInfo[0] in ["ARRAY", "STRING"]:
        result = []
        for i in range(funcInfo[1]):
          result.append(["", "POP"])
        return previousLine, previousLine.getLastLine(), result, number, jumpNumber
      
      elif funcInfo[0] == "":
        previousLine.setLastLine(CodeLine("PWS", [], None))
        return previousLine, previousLine.getLastLine(), [], number, jumpNumber
      
      else:
        raise Exception("Missing case in: " + tree.cleanPrint())
      
    elif tree.operator[1] == "ARRAY":
      result = []
      for i in tree.right:
        temp = convertIntoPartial(previousLine, i, fullScope, number, jumpNumber)
        if len(temp[2] != 1):
          raise Exception("Array in array in: ", tree)
        result.append(i[2][0])
        number = temp[3]
        jumpNumber = temp[4]
      return previousLine, previousLine.getLastLine(), result, number, jumpNumber
    
    #ASSIGNER
    elif tree.operator[1] == "ASSIGNER":
      leftOperand = []
      rightOperand = []
      
      tempLeft = convertIntoPartial(previousLine, tree.left, fullScope, number, jumpNumber, case=case)
      leftOperand = tempLeft[2]
      number = tempLeft[3]
      jumpNumber = tempLeft[4]
      
      tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber, case=case)
      rightOperand = tempRight[2]
      number = tempRight[3]
      jumpNumber = tempRight[4]
      
      if len(leftOperand) == len(rightOperand):
        for i in range(len(leftOperand)):
          if leftOperand[i][1] == "DIR":
            if rightOperand[i][1] == "POP":
              previousLine.setLastLine(CodeLine("PPD", [leftOperand[i][0]], None))
            elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
              temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
              number = temp[2]
              previousLine.setLastLine(CodeLine("LDD", [temp[1], leftOperand[i][0]], None))
            elif rightOperand[i][1] == "CONST":
              previousLine.setLastLine(CodeLine("LDV", [rightOperand[i][0], leftOperand[i][0]], None))
            elif rightOperand[i][1] == "DIR":
              previousLine.setLastLine(CodeLine("LDD", [rightOperand[i][0], leftOperand[i][0]], None))
            elif rightOperand[i][1] == "IN":
              previousLine.setLastLine(CodeLine("LDI", [rightOperand[i][0], leftOperand[i][0]], None))
            elif rightOperand[i][1] == "ACC":
              rightOperand[i][2].convertToACCDLoad(leftOperand[i][0])
            elif rightOperand[i][1] == "ACC2":
              rightOperand[i][2].convertToACC2DLoad(leftOperand[i][0])
            else:
              raise Exception("Invalid type " + rightOperand[i] + " around = in: " + tree.cleanPrint())
          elif leftOperand[i][1] == "IN":
            if rightOperand[i][1] == "POP":
              previousLine.setLastLine(CodeLine("PPI", [leftOperand[i][0]], None))
            elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
              temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
              number = temp[2]
              previousLine.setLastLine(CodeLine("LID", [temp[1], leftOperand[i][0]], None))
            elif rightOperand[i][1] == "CONST":
              previousLine.setLastLine(CodeLine("LIV", [rightOperand[i][0], leftOperand[i][0]], None))
            elif rightOperand[i][1] == "DIR":
              previousLine.setLastLine(CodeLine("LID", [rightOperand[i][0], leftOperand[i][0]], None))
            elif rightOperand[i][1] == "IN":
              previousLine.setLastLine(CodeLine("LII", [rightOperand[i][0], leftOperand[i][0]], None))
            elif rightOperand[i][1] == "ACC":
              rightOperand[i][2].convertToACCILoad(leftOperand[i][0])
            elif rightOperand[i][1] == "ACC2":
              rightOperand[i][2].convertToACC2ILoad(leftOperand[i][0])
            else:
              raise Exception("Invalid type " + rightOperand[i] + " around = in: " + tree.cleanPrint())
          else:
            raise Exception("Invalid type " + leftOperand[i] + " around = in: " + tree.cleanPrint())
      else:
        raise Exception("Mismatched lengths", len(leftOperand), "and", len(rightOperand), " in: " + tree.cleanPrint())
            
      return previousLine, previousLine.getLastLine(), [], number, jumpNumber
        
    #MODIFIER
    elif tree.operator[1] == "MODIFIER":
      if tree.operator[0] in ["++", "--"]:
        assemblyOperator = ""
        leftOperand = []
        
        tempLeft = convertIntoPartial(previousLine, tree.left, fullScope, number, jumpNumber)
        leftOperand = tempLeft[2]
        number = tempLeft[3]
        jumpNumber = tempLeft[4]
        
        if tree.operator[0] == "++":
          assemblyOperator = "ICB"
        elif tree.operator[0] == "--":
          assemblyOperator = "DCB"
          
        for i in range(len(leftOperand)):
          if leftOperand[i][1] == "DIR":
            previousLine.setLastLine(CodeLine("ALB " + assemblyOperator, [0, leftOperand[i][0], leftOperand[i][0]], None))
          elif leftOperand[i][1] == "IN":
            previousLine.setLastLine(CodeLine("ANB " + assemblyOperator, [0, leftOperand[i][0]], None))
            previousLine.setLastLine(CodeLine("LIA", [leftOperand[i][0]], None))
          
        return previousLine, previousLine.getLastLine(), [], number, jumpNumber
        
      else:
        leftOperand = []
        rightOperand = []
        
        tempLeft = convertIntoPartial(previousLine, tree.left, fullScope, number, jumpNumber)
        leftOperand = tempLeft[2]
        number = tempLeft[3]
        jumpNumber = tempLeft[4]
          
        tempRight = convertIntoPartial(previousLine, tree.right, fullScope, number, jumpNumber)
        rightOperand = tempRight[2]
        number = tempRight[3]
        jumpNumber = tempRight[4]
      
        for i in range(len(rightOperand)):
          if rightOperand[i][1] == "POP":
            replaceOperand = "TEMP" + str(number)
            number += 1
            previousLine.setLastLine(CodeLine("PPD", [replaceOperand], None))
            rightOperand[i][0] = replaceOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] in ["FLAG0", "FLAG1", "FLAG2", "NFLAG2"]:
            temp = convertFlagIntoPartial(previousLine, rightOperand[i][1], number)
            rightOperand[i][0] = temp[1]
            number = temp[2]
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] == "IN":
            resultOperand = "TEMP" + str(number)
            number += 1
            previousLine.setLastLine(CodeLine("LDI", [rightOperand[i][0], resultOperand], None))
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] == "ACC":
            resultOperand = "TEMP" + str(number)
            number += 1
            rightOperand[i][2].convertToACCDLoad(resultOperand)
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
          elif rightOperand[i][1] == "ACC2":
            resultOperand = "TEMP" + str(number)
            number += 1
            rightOperand[i][2].convertToACC2DLoad(resultOperand)
            rightOperand[i][0] = resultOperand
            rightOperand[i][1] = "DIR"
          
        if len(leftOperand) == len(rightOperand):
          for i in range(len(leftOperand)):
            if leftOperand[i][1] == "DIR":
              if rightOperand[i][1] == "CONST":
                if tree.operator[0] != "%=":
                  assemblyOperator = "ALB"
                  if tree.operator[0] == "+=":
                    assemblyOperator += " ADD"
                  elif tree.operator[0] == "-=":
                    assemblyOperator += " SBB"
                  elif tree.operator[0] == "*=":
                    assemblyOperator += " MLT"
                  elif tree.operator[0] == "/=":
                    assemblyOperator += " DVB"
                  elif tree.operator[0] == ">>=":
                    assemblyOperator += " RSB"
                  elif tree.operator[0] == "<<=":
                    assemblyOperator += " LSB"
                  elif tree.operator[0] == "&=":
                    assemblyOperator += " AND"
                  elif tree.operator[0] == "|=":
                    assemblyOperator += " ORR"
                  elif tree.operator[0] == "^=":
                    assemblyOperator += " XOR"
                  else:
                    raise Exception("Missing case in: " + tree.cleanPrint())
                  previousLine.setLastLine(CodeLine(assemblyOperator, [rightOperand[i][0], leftOperand[i][0], leftOperand[i][0]], None))
                else:
                  assemblyOperator = "ANB DVB"
                  previousLine.setLastLine(CodeLine(assemblyOperator, [rightOperand[i][0], leftOperand[i][0]], None))
                  previousLine.setLastLine(CodeLine("LDD", ["ACC2", leftOperand[i][0]], None))
              elif rightOperand[i][1] == "DIR":
                if tree.operator[0] != "%=":
                  assemblyOperator = "ALD"
                  if tree.operator[0] == "+=":
                    assemblyOperator += " ADD"
                  elif tree.operator[0] == "-=":
                    assemblyOperator += " SBA"
                  elif tree.operator[0] == "*=":
                    assemblyOperator += " MLT"
                  elif tree.operator[0] == "/=":
                    assemblyOperator += " DVA"
                  elif tree.operator[0] == "%=":
                    assemblyOperator += " DVA"
                  elif tree.operator[0] == ">>=":
                    assemblyOperator += " RSA"
                  elif tree.operator[0] == "<<=":
                    assemblyOperator += " LSA"
                  elif tree.operator[0] == "&=":
                    assemblyOperator += " AND"
                  elif tree.operator[0] == "|=":
                    assemblyOperator += " ORR"
                  elif tree.operator[0] == "^=":
                    assemblyOperator += " XOR"
                  else:
                    raise Exception("Missing case in: " + tree.cleanPrint())
                  previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[i][0], rightOperand[i][0], leftOperand[i][0]], None))
                else:
                  assemblyOperator = "AND DVA"
                  previousLine.setLastLine(CodeLine(assemblyOperator, [leftOperand[i][0], rightOperand[i][0]], None))
                  previousLine.setLastLine(CodeLine("LDD", ["ACC2", leftOperand[i][0]], None))
            elif leftOperand[i][1] == "IN":
              if rightOperand[i][1] == "CONST":
                if tree.operator[0] != "%=":
                  assemblyOperator = "ANB"
                  if tree.operator[0] == "+=":
                    assemblyOperator += " ADD"
                  elif tree.operator[0] == "-=":
                    assemblyOperator += " SBB"
                  elif tree.operator[0] == "*=":
                    assemblyOperator += " MLT"
                  elif tree.operator[0] == "/=":
                    assemblyOperator += " DVB"
                  elif tree.operator[0] == ">>=":
                    assemblyOperator += " RSB"
                  elif tree.operator[0] == "<<=":
                    assemblyOperator += " LSB"
                  elif tree.operator[0] == "&=":
                    assemblyOperator += " AND"
                  elif tree.operator[0] == "|=":
                    assemblyOperator += " ORR"
                  elif tree.operator[0] == "^=":
                    assemblyOperator += " XOR"
                  else:
                    raise Exception("Missing case in: " + tree.cleanPrint())
                  tempOperand = "TEMP" + str(number)
                  number += 1
                  previousLine.setLastLine(CodeLine("LDI", [leftOperand[i][0], tempOperand], None))
                  previousLine.setLastLine(CodeLine(assemblyOperator, [rightOperand[i][0], tempOperand], None))
                  previousLine.setLastLine(CodeLine("LIA", [leftOperand[i][0]], None))
                else:
                  tempOperand = "TEMP" + str(number)
                  number += 1
                  assemblyOperator = "ANB DVB"
                  previousLine.setLastLine(CodeLine("LDI", [leftOperand[i][0], tempOperand], None))
                  previousLine.setLastLine(CodeLine(assemblyOperator, [rightOperand[i][0], tempOperand], None))
                  previousLine.setLastLine(CodeLine("LID", ["ACC2", leftOperand[i][0]], None))
              elif rightOperand[i][1] == "DIR":
                if tree.operator[0] != "%=":
                  assemblyOperator = "AND"
                  if tree.operator[0] == "+=":
                    assemblyOperator += " ADD"
                  elif tree.operator[0] == "-=":
                    assemblyOperator += " SBA"
                  elif tree.operator[0] == "*=":
                    assemblyOperator += " MLT"
                  elif tree.operator[0] == "/=":
                    assemblyOperator += " DVA"
                  elif tree.operator[0] == "%=":
                    assemblyOperator += " DVA"
                  elif tree.operator[0] == ">>=":
                    assemblyOperator += " RSA"
                  elif tree.operator[0] == "<<=":
                    assemblyOperator += " LSA"
                  elif tree.operator[0] == "&=":
                    assemblyOperator += " AND"
                  elif tree.operator[0] == "|=":
                    assemblyOperator += " ORR"
                  elif tree.operator[0] == "^=":
                    assemblyOperator += " XOR"
                  else:
                    raise Exception("Missing case in: " + tree.cleanPrint())
                  tempOperand = "TEMP" + str(number)
                  number += 1
                  previousLine.setLastLine(CodeLine("LDI", [leftOperand[i][0], tempOperand], None))
                  previousLine.setLastLine(CodeLine(assemblyOperator, [tempOperand, rightOperand[i][0]], None))
                  previousLine.setLastLine(CodeLine("LIA", [leftOperand[i][0]], None))
                else:
                  tempOperand = "TEMP" + str(number)
                  number += 1
                  assemblyOperator = "AND DVA"
                  previousLine.setLastLine(CodeLine("LDI", [leftOperand[i][0], tempOperand], None))
                  previousLine.setLastLine(CodeLine(assemblyOperator, [tempOperand, rightOperand[i][0]], None))
                  previousLine.setLastLine(CodeLine("LID", ["ACC2", leftOperand[i][0]], None))
              else:
                raise Exception("Invalid type " + rightOperand[i][1] + " in: " + tree.cleanPrint())
            else:
              raise Exception("Invalid type " + leftOperand[i][1] + " in: " + tree.cleanPrint())
        else:
          raise Exception("Mismatched operand lengths in: " + tree.cleanPrint())
          
        return previousLine, previousLine.getLastLine(), [], number, jumpNumber
          
  elif isinstance(tree, list):
    if debug:
      #print("Tree is list")
      pass
    if len(tree) == 2:
      if tree[1] == "IDENTIFIER":
        
        if fullScope[tree[0]][0] in ["CHAR", "BOOLEAN", "INT"]:
          return previousLine, previousLine, [[tree[0], "DIR"]], number, jumpNumber
        elif fullScope[tree[0]][0] in ["ARRAY", "STRING"]:
          result = [[tree[0], "DIR"]]
          for i in range(1, fullScope[tree[0]][1]):
            result.append([tree[0] + "+" + str(i), "DIR"])
          return previousLine, previousLine, result, number, jumpNumber
      elif tree[1] in ["NUMBER", "CHAR", "BOOLEAN"]:
        if debug:
          #print("Tree in NUMBER, CHAR, BOOLEAN")
          pass
        return previousLine, previousLine, [[tree[0], "CONST"]], number, jumpNumber
      elif tree[1] == "STRING":
        result = []
        for i in tree[0][1:-1]:
          result.append([convertCharIntoDecimal("'" + i), "CONST"])
        return previousLine, previousLine, result, number, jumpNumber
      
  raise Exception("Missing case: ", tree)
  return previousLine, previousLine, ["NONE"], number, jumpNumber

def compiler():
      
  global debug
  
  lowerLetters = "abcdefghijklmnopqrstuvwxyz"
  upperLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  letters = lowerLetters + upperLetters + "_"
  digits = "0123456789"
  operators = "+-*/%|&^!"
  boolOperators = ["and", "or", "xor", "nand", "nor", "xnor", "not"]
  negators = "!-"       #negators act on one value
  #comments = "#"
  compareChars = "=><"
  #assigners = "="
  #modifiers = ["+=", "-=", "*=", "/=", "%=", "|=", "&=", "^=", "++", "--"]
  comparators = ["==", ">", "<", ">=", "<=", "<>"]
  spaces = " \n"
  #returns = ";"
  #oBrackets = "({["
  #cBrackets = ")}]"
  #brackets = oBrackets + cBrackets
  #charMarker = "'"
  #stringMarker = "\""

  source = open("Source.txt", "r")
  
  #Converting the source codes into tokens
  if debug:
    print("==============================================TOKENISATION==============================================")
  else:
    print("-=TOKENISATION=-")
  
  splitters = " \n"
  tokenSplitters = ",+-*/%|&^!=><;({[)}]\'\":"

  string = ""
  pretokens = []
  #lastChar = ""
  char = "\n"
  line = 1
  #prevLine = ""
  lineText = ""
  comment = False
  charVal = False
  stringVal = False
  #i=0
  while True:
    #lastChar = char
    char = source.read(1)
    if char == "":
      break
    elif char == "\n":
      line += 1
      #previousLine = lineText
      lineText = ""
    else:
      lineText += char
    if comment:
      if char in "\n;":
        comment = False
    elif stringVal:
      if char == "\"":
        stringVal = False
        string += char
        pretokens.append(string)
        string = ""
      else:
        string += char
    elif charVal:
      pretokens.append(string + char)
      charVal = False
      string = ""
    else:
      if char == "#":
        comment = True
        if string != "":
          pretokens.append(string)
          string = ""
      elif char == "\"":
        stringVal = True
        if string != "":
          pretokens.append(string)
        string = char
      elif char == "\'":
        charVal = True
        if string != "":
          pretokens.append(string)
        string = char
      elif char in splitters:
        if string != "":
          pretokens.append(string)
          string = ""
      elif char in tokenSplitters:
        if string != "":
          pretokens.append(string)
        pretokens.append(char)
        string = ""
      elif not char in spaces:
        string += char
  
  if string != "":
    pretokens.append(string)
  
  tokens = []
  i = 0
  while i < len(pretokens):
    if pretokens[i] == "=":
      if i - 1 >= 0:
        if pretokens[i-1] in operators or pretokens[i - 1] in [">>" or "<<"]:
          tokens[-1] += "="
        elif pretokens[i-1] in compareChars:
          tokens[-1] += "="
        else:
          tokens.append("=")
      else:
        tokens.append("=")
    elif pretokens[i] == ">":
      if i - 1 >= 0:
        if pretokens[i-1] == "<":
          tokens[-1] += ">"
        elif pretokens[i-1] == ">":
          tokens[-1] += ">"
        else:
          tokens.append(">")
      else:
        tokens.append(">")
    elif pretokens[i] == "<":
      if i - 1 >= 0:
        if pretokens[i-1] == "<":
          tokens[-1] += "<"
        else:
          tokens.append("<")
      else:
        tokens.append("<")
    elif pretokens[i] == "+":
      if i - 1 >= 0:
        if pretokens[i-1] == "+":
          tokens[-1] += "+"
        else:
          tokens.append("+")
      else:
        tokens.append("+")
    elif pretokens[i] == "-":
      if i - 1 >= 0:
        if pretokens[i-1] == "-":
          tokens[-1] += "-"
        else:
          tokens.append("-")
      else:
        tokens.append("-")
    else:
      tokens.append(pretokens[i])
    i += 1
    
  source.close()
    
  if debug:
    print(tokens)
    pass
  
  #Identifying what the tokens are
  if debug:
    print("==============================================IDENTIFYING TOKENS==============================================")
  else:
    print("-=IDENTIFYING TOKENS=-")
  #token type identification state machine
  tokenStateMap = {}
  
  #Start
  tokenState = {}
  for i in letters:
    tokenState[i] = "TEXT"
  for i in digits:
    tokenState[i] = "NUMBER"
  tokenState["0"] = "0"
  for i in operators + negators:
    tokenState[i] = "OPERATOR"
  tokenState["+"] = "+"
  tokenState["-"] = "-"
  tokenState[">"] = ">"
  tokenState["<"] = "<"
  tokenState["="] = "ASSIGNER"
  tokenState[";"] = "RETURN"
  tokenState[":"] = "SLICE"
  tokenState["{"] = "OPEN CURLY"
  tokenState["}"] = "CLOSE CURLY"
  tokenState["("] = "OPEN ROUND"
  tokenState[")"] = "CLOSE ROUND"
  tokenState["["] = "OPEN SQUARE"
  tokenState["]"] = "CLOSE SQUARE"
  tokenState["\'"] = "CHR"
  tokenState["\""] = "STR"
  tokenState[","] = "COMMA"
  tokenStateMap["S"] = tokenState
  
  #Text
  tokenState = {}
  for i in letters:
    tokenState[i] = "TEXT"
  for i in digits:
    tokenState[i] = "TEXT"
  tokenStateMap["TEXT"] = tokenState
  
  #Number
  tokenState = {}
  for i in digits:
    tokenState[i] = "NUMBER"
  tokenStateMap["NUMBER"] = tokenState
  
  tokenState = {}
  for i in digits:
    tokenState[i] = "NUMBER"
  tokenState["x"] = "HEX"
  tokenState["b"] = "BIN"
  tokenStateMap["0"] = tokenState
  
  tokenState = {}
  for i in digits + "abcdefABCDEF":
    tokenState[i] = "HEX"
  tokenStateMap["HEX"] = tokenState
  
  tokenState = {}
  for i in "01":
    tokenState[i] = "BIN"
  tokenStateMap["BIN"] = tokenState
  
  tokenState = {}
  tokenState["="] = "MODIFIER"
  tokenState["+"] = "MODIFIER"
  tokenStateMap["+"] = tokenState
  
  tokenState = {}
  tokenState["="] = "MODIFIER"
  tokenState["-"] = "MODIFIER"
  tokenStateMap["-"] = tokenState
  
  tokenState = {}
  tokenState[">"] = "OPERATOR"
  tokenState["="] = "COMPARATOR2"
  tokenStateMap[">"] = tokenState
  
  tokenState = {}
  tokenState["<"] = "OPERATOR"
  tokenState["="] = "COMPARATOR2"
  tokenState[">"] = "COMPARATOR2"
  tokenStateMap["<"] = tokenState
  
  #Operator
  tokenState = {}
  tokenState["="] = "MODIFIER"
  tokenStateMap["OPERATOR"] = tokenState
  
  #Assigners
  tokenState = {}
  tokenState["="] = "COMPARATOR2"
  tokenStateMap["ASSIGNER"] = tokenState
  
  #Comparators
  tokenState = {}
  tokenState["="] = "COMPARATOR2"
  tokenState[">"] = "COMPARATOR2"
  tokenStateMap["COMPARATOR"] = tokenState
  
  #Modifier
  tokenState = {}
  tokenStateMap["MODIFIER"] = tokenState
  
  #Characater
  tokenState = {}
  for i in supportedChars:
    tokenState[i] = "CHAR"
  tokenStateMap["CHR"] = tokenState
  
  #String
  tokenState = {}
  for i in supportedChars:
    tokenState[i] = "STR"
  tokenState["\""] = "STRING"
  tokenStateMap["STR"] = tokenState
  
  #StringEnd
  tokenState = {}
  tokenStateMap["STRING"] = tokenState
    
  tokenTypeIdentifier = StateMachine(tokenStateMap, "S")
  
  tokensTyped = []
  for i in tokens:
    for j in i:
      tokenTypeIdentifier.updateState(j)
    if tokenTypeIdentifier.state == "COMPARATOR2" or tokenTypeIdentifier.state == ">" or tokenTypeIdentifier.state == "<":
      tokensTyped.append([i, "COMPARATOR"])
    elif tokenTypeIdentifier.state == "HEX" or tokenTypeIdentifier.state == "BIN" or tokenTypeIdentifier.state == "0":
      tokensTyped.append([i, "NUMBER"])
    elif tokenTypeIdentifier.state == "+" or tokenTypeIdentifier.state == "-":
      tokensTyped.append([i, "OPERATOR"])
    elif tokenTypeIdentifier.state != "ERROR" and tokenTypeIdentifier.state != "STR" and tokenTypeIdentifier.state != "CHR":
      tokensTyped.append([i, tokenTypeIdentifier.state])
    else:
      print("ERROR: Unidentifiable token")
      print(i)
      return
    tokenTypeIdentifier.setState("S")
    
  if debug:
    print(tokensTyped)
    pass
  
  keywords = ["if", "elif", "else", "for", "in", "to", "while", "def", "pause", "graphics", "pop", "push", "pass", "jump", "return"]
  booleanConsts = ["true", "false"]
  varTypes = ["int", "char", "bool"]
  arrayTypes = ["array", "string"]
  
  for i in tokensTyped:
    if i[1] == "TEXT":
      if i[0] in keywords:
        i[1] = "KEYWORD"
      elif i[0] in varTypes:
        i[1] = "TYPE"
      elif i[0] in arrayTypes:
        i[1] = "ARRAY_TYPE"
      elif i[0] in booleanConsts:
        i[1] = "BOOLEAN"
      elif i[0] == "not":
        i[1] = "NEGATOR"
      elif i[0] in boolOperators:
        i[1] = "BOOLEAN_OPERATOR"
      else:
        #print(i[0])
        i[1] = "IDENTIFIER"
    elif i[1] == "COMPARATOR":
      if not i[0] in comparators:
        print("ERROR: Invalid comparator")
        print(i[0])
    
  if debug:
    print(tokensTyped)
    pass
  tokensByLine = sortIntoLines(tokensTyped)
    
  if debug:
    print("----------------------tokensByLine----------------------")
    print(tokensByLine)
    pass
  
  if debug:
    print("==============================================CONSTRUCTING OPERATOR TREE==============================================")
  else:
    print("-=CONSTRUCTING OPERATOR TREE=-")
  
  tokenTree = []
  for i in tokensByLine:
    #print(i)
    #print(constructTree(i))
    tokenTree.append(constructTree(i))
  
  if debug:
    print("----------------------TOKEN TREE----------------------")
    print(tokenTree)
    pass
  
  if debug:
    print("==============================================BUILDING SYMBOL TABLE AND TYPE CHECKING==============================================")
  else:
    print("-=BUILDING SYMBOL TABLE AND TYPE CHECKING=-")
  
  defaultSymbols = ["TTY", "OUTPUT", "CTRLR1P", "CTRLR1H", "CTRLR2P", "CTRLR2H", "KYBD", "RND", "MODE", "PRCT", "SELECT", 
                                 "STKPNTR", "ACC2", "FLG", "BinaryToBCD", "BCDToASCII", "SPR0COORD", "SPR0CLR", "SPR1COORD", 
                                 "SPR1CLR", "SPR2COORD", "SPR2CLR", "SPR3COORD", "SPR3CLR", "SPR4COORD", "SPR4CLR", "SPR5COORD", 
                                 "SPR5CLR", "SPR6COORD", "SPR6CLR", "SPR7COORD", "SPR7CLR", "SPR8COORD", "SPR8CLR", "SPR9COORD", 
                                 "SPR9CLR", "SPR10COORD", "SPR10CLR", "SPR11COORD", "SPR11CLR", "SPR12COORD", "SPR12CLR", "SPR13COORD", 
                                 "SPR13CLR", "SPR14COORD", "SPR14CLR", "SPR15COORD", "SPR15CLR", "SPR16COORD", "SPR16CLR", "SPR17COORD", 
                                 "SPR17CLR", "SPR18COORD", "SPR18CLR", "SPR19COORD", "SPR19CLR", "SPR20COORD", "SPR20CLR", "SPR21COORD", 
                                 "SPR21CLR", "SPR22COORD", "SPR22CLR", "SPR23COORD", "SPR23CLR", "SPR24COORD", "SPR24CLR", "SPR25COORD", 
                                 "SPR25CLR", "SPR26COORD", "SPR26CLR", "SPR27COORD", "SPR27CLR", "SPR28COORD", "SPR28CLR", "SPR29COORD", 
                                 "SPR29CLR", "SPR30COORD", "SPR30CLR", "SPR31COORD", "SPR31CLR"]
  
  defaultFunctions = FunctionScope(None)
  defaultVariables = VariableScope(None)
  defaultVariables.addSpecialVariable("TTY", "CHAR", "TTY")
  defaultVariables.addSpecialVariable("keyboard", "CHAR", "KYBD")
  defaultVariables.addSpecialVariable("controller1Pressed", "CHAR", "CTRLR1P")
  defaultVariables.addSpecialVariable("controller1Held", "CHAR", "CTRLR1H")
  defaultVariables.addSpecialVariable("controller2Pressed", "CHAR", "CTRLR2P")
  defaultVariables.addSpecialVariable("controller2Held", "CHAR", "CTRLR2P")
  defaultVariables.addSpecialVariable("mode", "INT", "MODE")
  defaultVariables.addSpecialVariable("protect", "INT", "PRCT")
  defaultVariables.addSpecialVariable("select", "INT", "SELECT")
  defaultVariables.addSpecialVariable("random", "INT", "RND")
  defaultVariables.addSpecialVariable("debugOut", "INT", "OUTPUT")
  defaultVariables.addSpecialVariable("accumulator2", "INT", "ACC2")
  defaultVariables.addSpecialVariable("stackPointer", "INT", "STKPNTR")
  defaultVariables.addSpecialVariable("flag", "INT", "FLG")
  for i in range(32):
    defaultVariables.addSpecialVariable("sprite" + str(i) + "colour", "INT", "SPR" + str(i) + "CLR")
    defaultVariables.addSpecialVariable("sprite" + str(i) + "coordinates", "INT", "SPR" + str(i) + "COORD")
  tree, variableTable, arrayTable, functionTable, number, totalScope = determineTypeOfCode(tokenTree, defaultVariables, ArrayScope(None), defaultFunctions, 0, [])
  
  dictionaryScope = {}
  for i in totalScope:
    dictionaryScope[i[0]] = i[1:5]
  
  if debug:
    #print("----------------------TOKEN TREE----------------------")
    #print(tree)
    print("----------------------SYMBOL TABLE----------------------")
    #print(totalScope)
    print(dictionaryScope)
    pass
  tree = removeDeclarationsCode(tree)
  tree = removeEmptyLines(tree)
  
  if debug:
    #print("----------------------TOKEN TREE----------------------")
    #print(tree)
    pass
  
  if debug:
    print("==============================================BUILDING CONTROL GRAPH==============================================")
  else:
    print("-=BUILDING CONTROL GRAPH=-")
  
  controlGraph = convertCodeIntoPartial(tree, CodeLine("", [], None), dictionaryScope)[0]
  
  if debug:
    #print("----------------------CONTROL GRAPH----------------------")
    #print(controlGraph.printAllCode())
    pass
  
  if debug:
    print("==============================================OPTIMISING==============================================")
  else:
    print("-=OPTIMISING=-")
  
  if debug:
    print("==============================================ASSIGNING SYMBOLS SPACE IN MEMORY==============================================")
  else:
    print("-=ASSIGNING SYMBOLS SPACE IN MEMORY=-")
  memoryDictionary = {}
  startOfWRAM = 4096
  memoryAddress = startOfWRAM
  for i in dictionaryScope.keys():
    if i[0] != "f" and not i in defaultSymbols:
      memoryDictionary[i] = memoryAddress
      memoryAddress += dictionaryScope[i][1]
      if debug:
        #print(i, dictionaryScope[i])
        #print(dictionaryScope[i][1], memoryAddress)
        pass
      
  if debug:
    print(memoryDictionary)
    pass
  
  if debug:
    print("==============================================CONVERTING TO ASSEMBLY==============================================")
  else:
    print("-=CONVERTING TO ASSEMBLY=-")
  currentLine = controlGraph
  
  while currentLine != None:
    for i in range(len(currentLine.operands)):
      try:
        if isinstance(currentLine.operands[i], str):
          if "+" in currentLine.operands[i]:
            #Convert array indices
            temp = currentLine.operands[i].split("+")
            currentLine.operands[i] = memoryDictionary[temp[0]] + int(temp[1])
            currentLine.operands[i] = formattedDecimalToHex(currentLine.operands[i])
          elif currentLine.operands[i] not in memoryDictionary.keys() and currentLine.operands[i][0] not in "jf" and not currentLine.operands[i] in defaultSymbols:
            memoryDictionary[currentLine.operands[i]] = memoryAddress
            memoryAddress += 1
        elif isinstance(i, int):
          currentLine.operands[i] = formattedDecimalToHex(currentLine.operands[i])
        pass
      except Exception as e:
        print(currentLine)
        raise e
    currentLine = currentLine.nextLineCode
    pass
  if debug:
    #print(controlGraph.printAllCode())
    print(memoryDictionary)
    pass
  
  assemblySymbolTable = ""
  for i in memoryDictionary.keys():
    assemblySymbolTable += "%" + i + " = " + formattedDecimalToHex(memoryDictionary[i]) + "\n"
    
  finalAssembly = assemblySymbolTable + controlGraph.printAllCode()
  if debug:
    #print("----------------------FINAL ASSEMBLY----------------------")
    #print(finalAssembly)
    pass
  
  if debug:
    print("==============================================WRITING TO FILE==============================================")  
  else:
    print("-=WRITING TO FILE=-")  
  
  assembly = open("Assembly.txt", "w")
  assembly.write(finalAssembly)
  assembly.close()
          
  symbolTable = open("SymbolTable.txt", "w")
  symbolTable.write(assemblySymbolTable + "\n")
  for i in dictionaryScope.keys():
    symbolTable.write(str(i))
    symbolTable.write(" ")
    symbolTable.write(str(dictionaryScope[i]))
    symbolTable.write("\n")
  symbolTable.close()
  
compiler()
assembler()