
#The Assembler for the Femto-4 found on CircuitVerse.
#Refer to Developer Guide.txt if you want to understand what this is for. 


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
  AssemblyCodes1 = {"PWS": "0000", "GRF": "0001", "LDV": "1000", "LDD": "1001", "LDI": "1002", "LDP": "1004", "LDA": "1005", "LIV": "1008", "LID": "1009", "LII": "100a", "LIP": "100c", "LIA": "100d", "PSV": "4000", "PSD": "4001", "PPD": "4002", "PSI": "4003", "PPI": "4004", "JMP": "5000", "JPD": "5001"}
  #ALU opcodes
  AssemblyCodes2 = {"ANR": "20", "ANV": "24", "AND": "28", "ANB": "2c", "ALR": "30", "ALV": "34", "ALD": "38", "ALB": "3c"}
  ALUCodes = {"ADD": "0a8", "SBA": "198", "SBB": "168", "ICA": "188", "ICB": "128", "DCA": "0b8", "DCB": "0e8", "NGA": "148", "NGB": "118", "NTA": "040", "NTB": "010", "ORR": "0ad", "NOR": "051", "AND": "0a1", "NND": "05d", "XOR": "0a0", "XNR": "0ac", "SLA": "0ba", "SLB": "0ca", "INA": "080", "INB": "020", "HGH": "0c0", "LOW": "000", "SRA": "200", "SRB": "201", "MLT": "202", "DVA": "204", "DVB": "205", "LSA": "208", "LSB": "209", "RSA": "20c", "RSB": "20d", "XAD": "210", "XSA": "211", "XSB": "212", "CAD": "220", "CSA": "221", "CSB": "222", "CSL": "223", "CNG": "224", "CAT": "230", "CSR": "231"}
  #Flag jump opcodes
  AssemblyCodes3 = {"JPF": "504", "JDF": "508"}
  #Bit test jump opcodes
  AssemblyCodes4 = {"JPB": "50c", "JDB": "50e"}
  #Clock jump opcodes
  AssemblyCodes5 = {"JPC": "5100", "JDC": "5102"}
  #Expected number of data chunks for each opcode
  AssemblyNumber = {"PWS": 1, "GRF": 1, "LDV": 3, "LDD": 3, "LDI": 3, "LDP": 2, "LDA": 2, "LIV": 3, "LID": 3, "LII": 3, "LIP": 2,  "LIA": 2, "PSV": 2, "PSD": 2, "PSI": 2, "PPD": 2, "PPI": 2, "JMP": 2, "JPD": 2, "ANR": 3, "ANV": 4, "AND": 4,  "ANB": 4, "ALR": 4, "ALV": 5, "ALD": 5, "ALB": 5, "JPF": 3, "JDF": 3, "JPB": 3, "JDB": 3, "JPC": 3, "JDC": 3}

  #Flag jump opcodes. Not really that useful since a direct compare operation doesn't exist
  FlagJumpCodes = {"SGR": "0a", "EQL": "03", "ELS": "0c", "SLS": "0e", "NQL": "02", "CRY": "0c", "NCY": "08"}

  #List of preset variables, mostly of ASCII characters. 
  addresses = {"TTY": "3200", "OUTPUT": "3201", "CTRLR1P": "3000", "CTRLR1H": "3001", "CTRLR2P": "3002", "CTRLR2H": "3003",  "KYBD": "3004", "RND": "00ff", "MODE": "00ca", "PRCT": "00cb", "SELECT": "00cc", "STKPNTR": "00b0", "ACC2": "00c7",  "FLG": "00c8", "BinaryToBCD": "c000" , "BCDToASCII": "c01d", "SPR0COORD": "33c0", "SPR0CLR": "33c1", "SPR1COORD": "33c2", "SPR1CLR": "33c3", "SPR2COORD": "33c4", "SPR2CLR": "33c5",  "SPR3COORD": "33c6", "SPR3CLR": "33c7", "SPR4COORD": "33c8", "SPR4CLR": "33c9", "SPR5COORD": "33ca", "SPR5CLR": "33cb", "SPR6COORD": "33cc", "SPR6CLR": "33cd", "SPR7COORD": "33ce", "SPR7CLR": "33cf", "SPR8COORD": "33d0", "SPR8CLR": "33d1", "SPR9COORD": "33d2", "SPR9CLR": "33d3", "SPR10COORD": "33d4", "SPR10CLR": "33d5", "SPR11COORD": "33d6", "SPR11CLR": "33d7", "SPR12COORD": "33d8", "SPR12CLR": "33d9", "SPR13COORD": "33da", "SPR13CLR": "33db", "SPR14COORD": "33dc", "SPR14CLR": "33dd",  "SPR15COORD": "33de", "SPR15CLR": "33df", "SPR16COORD": "33e0", "SPR16CLR": "33e1", "SPR17COORD": "33e2", "SPR17CLR": "33e3", "SPR18COORD": "33e4", "SPR18CLR": "33e5", "SPR19COORD": "33e6", "SPR19CLR": "33e7", "SPR20COORD": "33e8", "SPR20CLR": "33e9",  "SPR21COORD": "33ea", "SPR21CLR": "33eb", "SPR22COORD": "33ec", "SPR22CLR": "33ed", "SPR23COORD": "33ee", "SPR23CLR": "33ef", "SPR24COORD": "33f0", "SPR24CLR": "33f1", "SPR25COORD": "33f2", "SPR25CLR": "33f3", "SPR26COORD": "33f4", "SPR26CLR": "33f5","SPR27COORD": "33f6", "SPR27CLR": "33f7", "SPR28COORD": "33f8", "SPR28CLR": "33f9", "SPR29COORD": "33fa", "SPR29CLR": "33fb", "SPR30COORD": "33fc", "SPR30CLR": "33fd", "SPR31COORD": "33fe", "SPR31CLR": "33ff",  "\'0": "0030", "\'1": "0031", "\'2": "0032", "\'3": "0033", "\'4": "0034", "\'5": "0035", "\'6": "0036", "\'7": "0037", "\'8": "0038", "\'9": "0039", "\'a": "0061", "\'b": "0062", "\'c": "0063", "\'d": "0064", "\'e": "0065", "\'f": "0066", "\'g": "0067", "\'h": "0068", "\'i": "0069", "\'j": "006a", "\'k": "006b", "\'l": "006c", "\'m": "006d", "\'n": "006e", "\'o": "006f", "\'p": "0070", "\'q": "0071", "\'r": "0072", "\'s": "0073", "\'t": "0074", "\'u": "0075", "\'v": "0076", "\'w": "0077", "\'x": "0078", "\'y": "0079", "\'z": "007a", "\'A": "0041", "\'B": "0042", "\'C": "0043", "\'D": "0044", "\'E": "0045", "\'F": "0046",  "\'G": "0047", "\'H": "0048", "\'I": "0049", "\'J": "004a", "\'K": "004b", "\'L": "004c", "\'M": "004d", "\'N": "004e", "\'O": "004f", "\'P": "0050", "\'Q": "0051", "\'R": "0052", "\'S": "0053", "\'T": "0054", "\'U": "0055", "\'V": "0056", "\'W": "0057", "\'X": "0058", "\'Y": "0059", "\'Z": "005a", "\'_": "0020", "\'exclamation": "0021", "\'\"": "0022", "\'hash": "0023", "\'$": "0024", "\'percent": "0025", "\'&": "0026", "\'\'": "0027", "\'(": "0028", "\')": "0029", "\'*": "002a", "\'+": "002b", "\',": "002c", "\'-": "002d", "\'.": "002e", "\'/": "002f", "\':": "003a", "\';": "003b", "\'<": "003c", "\'=": "003d", "\'>": "003e", "\'?": "003f", "\'@": "0040", "\'[": "005b", "\'\\": "005c", "\']": "005d", "\'^": "005e", "\'__": "005f", "\'{": "007b", "\'|": "007c", "\'}": "007d", "\'~": "007e"}

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
    instruction = (" " + line).split("#")[0].split("//")[0].split("%")[0].split("!")[0].split()

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
        
assembler()