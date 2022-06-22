#!/usr/bin/env python3
import subprocess
import json
import time
import platform
from os import path
import os

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
 |   Instalation of independently developed 3rd party application.    |
 ┖────────────────────────────────────────────────────────────────────┙ """+ ENDC
    menu = """
  [0] MENU:
 ─────────────────────────────
  [1] Open config file
  [2] Install
  [3] Help
  [4] Exit
  """
    help = """
  [i] please check README documentaion for a detailed instruction.   
    """
# Module for cheking internet

def internetCheck():
    print(" [i] checking internet connection..." ,end="       ")
    ping = subprocess.run(['ping www.github.com -c 2'],
                            capture_output=True,
                            shell=True)
    print("output: " ,ping.stdout)
    print("return code ", ping.returncode)
    return_code = ping.poll()

    if return_code == 0:
        return True
    else:
        return False


def engine():
    connection = internet()
    if (not connection):
        print(f"{ui.WARNING} [Failed]\n [Warning] no internet connection{ui.ENDC}") 
    else:
        print(f"{ui.OKBLUE} [Passed]\n {ui.ENDC}")

 
#controller module that listen to user willing what wants to do
def controller():
    print(ui.menu)
    global selection
    selection = int(input(" [?] Select> ([0] for Menu): "))
    os.chdir('..')
    configpath = os.getcwd()
    if selection == 1:
        config_check = path.exists("dependency.conf")
        if (config_check is False):
            print(f"{ui.WARNING} [Warning] Config file not find or wrong directory.{ui.ENDC}")
            controller()
        elif platform.system() == 'Windows':    # Windows
            os.startfile("dependency.conf")
        else:                                  
            subprocess.call(('xdg-open', "dependency.conf"))  # opens file in linux
            print(" [i] waiting until file edit finishes...")
    if selection == 2:
        config_check = path.exists("dependency_config.conf")
        if (config_check is False): 
            print(f"{ui.WARNING} [Warning] Config file not find or wrong directory.{ui.ENDC}")
            controller()
        elif selection == 2 and config_check:
            engine() #does the main job

    if selection == 3:
        print (ui.help)
    if selection == 4:
        exit()
    if selection == 0:
        print (ui.menu)
         
            



def internet():
    print(" [i] checking connection please wait...")
    ping = subprocess.Popen(['ping https://www.github.com -c 2'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            shell=True)
    poll = ping.poll()
    while (poll is None):
        print ("pre-sleep line")
        time.sleep(0.1)
        
    if poll == 0:
        return True
        print (f"{ui.OKBLUE} [i] Internet connection verified.{ui.ENDC}")
    else:
        return False
        print(f"{ui.WARNING} [ERROR] Network error, Check your internet connection:  {ui.ENDC}")
        control()


def main():
    print(ui.banner)  # first time title bar:
    controller()  # keeps application running



main()