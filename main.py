#!/usr/bin/env python3

import subprocess
import time
import platform
from os import path
import os

os.chdir('..')
configpath = os.getcwd()

class ui:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    WARNING = '\033[93m'
    CLEAR ='\033c'
    
    banner = CLEAR + """
 ╔───────────────── Dependency Installer Engine v0.1──────────────────╗
 |  Dependency Installer Engine rpvides an automatic deployment and   |
 |   Instalation of independently developed 3rd party applications.   |
 ┖────────────────────────────────────────────────────────────────────┙ """+ ENDC
    menu = """
 [0] MENU:
 ==========
 [1] Change build path (defualt is: <cd ..>)
 [2] Open config file
 [3] Install
 [4] Help
 [5] Exit
  """
    help = """
  [i] please read README documentaion for a detailed instruction.   
    """
# Module for cheking internet

def internetCheck():
    print(" [i] checking internet connection..." ,end="       ")
    ping = subprocess.run(['ping www.google.com -c 2'],
                            text=True,
                            capture_output=True,
                            shell=True)
    print("output: " ,ping.stdout)
    print("return code ", ping.returncode)
    return_code = ping.check_returncode()

    if return_code == 0:
        return True
    else:
        return False


def engine():
    connection = internetCheck()
    if (not connection):
        print(f"{ui.WARNING} [Failed]\n [Warning] no internet connection{ui.ENDC}") 
        print(f"{ui.WARNING} [!] check internet connection and try again.{ui.ENDC}") 
        controller()
    else:
        print(f"{ui.OKBLUE} [Passed]\n {ui.ENDC}")
    dependency_conf = open("dependency.conf")
    commands = dependency_conf.readlines()
    for eachCommand in commands:
        print(eachCommand)
        

 
#controller module that listen to user willing what wants to do
def controller():
    print(ui.menu)
    global configpath
    try:
        selection = int(input(" [?] Select> ([0] for Menu): "))
    except:
        print(f"{ui.WARNING} [ERROR] Invalid type. try again. {ui.ENDC}") 
        controller()
    if selection == 1:
        print (f" [i] Current work directory for build is{ui.OKBLUE}:\n    " , configpath)
        print(f"{ui.ENDC}")
        prompt = input(" [?] would you like to modify? (y/n):")
        if (prompt == 'Y' or prompt == 'y'):
            print (" [?] Input new build path address:", end=" ")
            temp_configpath = input("(e.g: C:/mylib/source):")
            if len(temp_configpath) < 1:
                print(f"{ui.WARNING} [!] Input address is too short.{ui.ENDC}")
            else:
                print(" [i] New directory as buildpath is set to:")
                configpath = temp_configpath
                print("    ",configpath)
        elif(prompt == 'N' or prompt == 'n'):
            print(" [i] build dir not changed") 
        
    if selection == 2:
        config_check = path.exists("dependency.conf")
        if (config_check is False):
            print(f"{ui.WARNING} [Warning] Config file not find or wrong directory.{ui.ENDC}")
        elif platform.system() == 'Windows':    # Windows
            os.startfile("dependency.conf")
        else:                                  
            subprocess.call(('xdg-open', "dependency.conf"))  # opens file in linux
            print(" [i] waiting until file edit finishes...")
    if selection == 3:
        config_check = path.exists("dependency.conf")
        if (config_check is False): 
            print(f"{ui.WARNING} [Warning] Config file not find or wrong directory.{ui.ENDC}")
        elif selection == 3 and config_check:
            engine() #does the main job

    if selection == 4:
        print (ui.help)
    if selection == 5:
        exit()
    if selection == 0:
        print (ui.menu)
         

def main():
    print(ui.banner)  # first time title bar:
    while True:
        controller()  # keeps application running event loop simulation
        

main()