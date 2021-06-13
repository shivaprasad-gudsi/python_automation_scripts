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
time.sleep(5)
output = net_connect.read_channel()
print(output)                             # Should hopefully see the server prompt
print(" "*80)
print("Printing the prompt found")
print("#"*80)
print(net_connect.find_prompt())
output = net_connect.send_command('terminal length 0')

print(" "*80)
print("show run snmp output below:")
print("#"*80)
output = net_connect.send_command('show run|inc snmp', delay_factor=2)
print(output)

print(" "*80)
print("show inventory output below:")
print("#"*80)
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