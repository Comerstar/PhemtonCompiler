# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 13:37:01 2021

@author: rando
"""

from PIL import Image

hexConv = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

#Converts decimal values (as integers) to hexadecimal values (as strings). 
def decimal_to_hex(x):
  out = ""
  while x != 0:
    out = hexConv[x % 16] + out
    x = x//16
  return out

def convertColourIntoFemtoColour (colour):
  result = decimal_to_hex(((colour[0] // 8) << 11) + ((colour[1] // 8) << 6) + ((colour[2] // 8) << 1) + 1)
  result = "0" * (4 - len(result)) + result
  return result

def convertImageToDataTable ():
  f = Image.open("Source.png")
  width, height = f.size
  table = open("Table.txt", "w")
  for i in range(height):
    for j in range(width):
      table.write(convertColourIntoFemtoColour(f.getpixel((j, i))) + " ")
    table.write("\n")
  table.close()
  f.close()
  
convertImageToDataTable()