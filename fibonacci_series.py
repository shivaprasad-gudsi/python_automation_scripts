###################################################
### This is Simple program Fibonacci Series   #####
### but using my logic tried to make it short #####
###################################################

import os
import io

'''
fibonacci series
index 0 1 2 3 4 5  6  7   8
value 1 1 2 3 5 8 13  21 34
'''

print("Welcome to fibonacci series output printer")
index = int(input('\nEnter the index value of fibonacci to print:'))

a = 0
b = 1

if (index<=1):
    print("Value is", b)

for num in range(index):
    c=a+b
    a=b
    b=c    

if (index > 1):
    print("Value is", c)
    
# End of the program