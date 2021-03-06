#####################################################
#### Program for login to ise device and collect ####
#### the show commands. Will work on saving the  ####
#### results to a local file in future           ####
#####################################################

from __future__ import unicode_literals, print_function
import time
from netmiko import ConnectHandler, redispatch
import getpass

hostname = input('Enter the hostname: ')
username = input('Enter the username: ')
password = getpass.getpass('password: ')

net_connect = ConnectHandler(
    device_type='terminal_server',        # Notice 'terminal_server' here
    ip=hostname, 
    username=username, 
    password=password)

# Manually handle interaction in the Server
# 
net_connect.write_channel("\r\n")
time.sleep(3)
output = net_connect.read_channel()
print(output)                             # Should hopefully see the server prompt

print("*" * 80 + "\n" + "Printing the prompt found" + "\n" + "*" * 80)
print(net_connect.find_prompt())
output = net_connect.send_command('terminal length 0')

print("*" * 80 + "\n" + "show run snmp output below:" + "\n" + "*" * 80)
output = net_connect.send_command('show run|inc snmp', delay_factor=2)
print(output)

print("*" * 80 + "\n" + "show inventory output below:" + "\n" + "*" * 80)
output = net_connect.send_command('show inventory|inc PID', delay_factor=2)
print(output)
print(" "*80)

print(" "*80)
print("show DNS output below:")
print("#"*80)
output = net_connect.send_command('show run|inc name-server', delay_factor=2)
print(output)
print(" "*80)
net_connect.send_command('exit', auto_find_prompt=False)
net_connect.disconnect()
print("Session Closed.")

# End of the program