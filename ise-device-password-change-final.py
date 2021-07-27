#########################################################################
### This program eliminates manual process of changing password     ####
### on expired network device, this program can change the password ####
### automatically (user need to enter username/password once) and   ####
### password will be changed to new password.                       #### 
########################################################################

from __future__ import unicode_literals, print_function
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import sys
import time
import getpass
import re
import logging

def changedevicepass(hostname,username,password):
    net_connect = ConnectHandler(
        device_type='terminal_server',  # Notice 'terminal_server' here
        ip=hostname,
        username=username,
        password=password)
    #
    time.sleep(4)
    output = net_connect.read_channel()  # Should hopefully see the server prompt
    #
    match = re.search(r'WARNING: Your password has expired.', output)
    if match:
        newpass = input('Enter new password: ')
        for i, v in enumerate(password):
            net_connect.write_channel(v)
        net_connect.write_channel("\n")
        time.sleep(3)
        output = net_connect.read_channel()
        #output = net_connect.send_command("\n")
        print(output)
        if "New password" in output:
            for i, v in enumerate(newpass):
                net_connect.write_channel(v)
            net_connect.write_channel("\n")
            time.sleep(3)
            output = net_connect.read_channel()
            print(output)
            if "Retype new password" in output:
                for i, v in enumerate(newpass):
                    net_connect.write_channel(v)
                net_connect.write_channel("\n")
                time.sleep(3)
                output = net_connect.read_channel()
                if "passwd: all authentication tokens updated successfully" in output:
                    print("*" * 70 + "\n" + "Successfully changed password" + "\n" + "*" * 70)
                    print(output)
    else:
        print("*"*70+"\n"+"SSH Timed Out or not enabled"+"\n"+"*"*70)

if __name__ == "__main__":
#This is main function
    logging.basicConfig(filename='test.log', level=logging.DEBUG) #we can remove DEBUG when we are not troubleshooting since i used it to troubleshoot
    logger = logging.getLogger("netmiko")
    hostname = input("Enter the hostname: ")
    username = input("Enter the username: ")
    password = getpass.getpass("password: ")

    try:
        changedevicepass(hostname,username,password)
    except (NetmikoAuthenticationException):
        print("*"*70+"\n"+"Authentication Failure"+"\n"+"*"*70)
    except (EOFError, SSHException, NetMikoTimeoutException):
        print("*"*70+"\n"+"SSH Timed Out or not enabled"+"\n"+"*"*70)
    except (OSError):
        print("*" * 70 + "\n" + "OSError: Socket is closed" + "\n" + "*" * 70)
    except Exception as err:
        exception_type = type(err).__name__
        print("*"*70+"\n"+"Exception or Error occured::"+exception_type+"\n"+"*"*70)

#End of program