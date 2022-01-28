from __future__ import unicode_literals, print_function
from netmiko import ConnectHandler
import time
import getpass
import logging

def installHP(hostname,username,password):
    net_connect = ConnectHandler(
        device_type='terminal_server',  # Notice 'terminal_server' here
        ip=hostname,
        username=username,
        password=password)
    #
    net_connect.write_channel("\r\n")
    time.sleep(5)
    output = net_connect.read_channel()
    print(output)  # Should hopefully see the server prompt
    print(" " * 80)
    print("Printing the prompt found")
    print("#" * 80)

    command = 'application install ise-apply-CSCwa47133_Ver_24_30_allpatches-SPA.tar.gz reponame'
    output = net_connect.send_command_timing(command, strip_prompt=False, strip_command=False, delay_factor=15)
    if "Save the current ADE-OS" in output:
        print(f"Starting to install HP on {hostname}...")
        output += net_connect.send_command("\n", delay_factor=15, expect_string=r"#")

    print("\nShow logging application hotpatch.log output below:")
    print("#" * 80)
    output = net_connect.send_command('show logging application hotpatch.log', delay_factor=2)
    print(output)

    net_connect.send_command('exit', auto_find_prompt=False)
    net_connect.disconnect()
    print("Session Closed.")


if __name__ == "__main__":
#This is main function
    logging.basicConfig(filename='test.log', level=logging.DEBUG)
    logger = logging.getLogger("netmiko")
    username1 = input('Enter the username: ')
    password1 = getpass.getpass('password: ')
    tmp = "none"
    devicelist = ["none","none","none","none","none"]

    # Loop for 5 devices, type "none" to skip
    # For example if only 1 device is there, give hostname1="abchost" and remaining as "none" to skip
    for i in range(5):
        print(f"Enter hostname{i+1}: ")
        devicelist[i] = input()

    for i in range(5):
     if devicelist[i] != tmp:
         installHP(devicelist[i],username1,password1)

#End of program
