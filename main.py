#!/usr/bin/env python3

from mimetypes import init
import subprocess
import time
import platform
from os import path
import os
import json

os.chdir('..')
configpath = os.getcwd()



class Stage:
    def __init__(self, key, commands):
        self.key = key
        self.value = commands
        

class ui:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    WARNING = '\033[93m'
    CLEAR ='\033c'
    
    banner = """
 ╔───────────────── Dependency Installer Engine v0.1──────────────────╗
 |  Dependency Installer Engine provides an automatic deployment and  |
 |   Instalation of independently developed 3rd party applications.   |
 ┖────────────────────────────────────────────────────────────────────┙ """+ ENDC
    menu = """
 [0] MENU:
 ==========
 [1] Change config file path (defualt is: <cd ..>) 
 [2] Open config file
 [3] Install
 [4] Help
 [5] Exit
  """
    help = """
  [i] Instruction:
      config file name must be: dependency.conf (case sensetive).
      config file must contain encapsulated build commands in Stages in 
      format shown below: (case sensitive).
      Note: each stage starts with STAGE_START and ends to STAGE_END.
      
      ╔───────────dependency.conf───────────────╗
      |STAGE_START:<config key>                 |
      |comand                                   |
      |comand                                   |
      |...                                      |
      |STAGE_END                                |
      |                                         |
      |STAGE_START:<config key>                 |
      |comand                                   |
      |comand                                   |
      |...                                      |
      |STAGE_END                                |
      |.                                        |
      |.                                        |
      |.                                        |
      ┖─────────────────────────────────────────┙
      
      Note: in case you are not willing want to clone the 
            Dependency Installe to your source folder simply
            change config file path
         
    """
# Module for cheking internet

def select():
    try:
        selection = int(input("\n [?] Select> ([0] for Menu): "))
    except:
        print(f"{ui.WARNING} [ERROR] Invalid type. try again. {ui.ENDC}") 
        select() 
    else:
        return selection
        

def internetCheck():
    print(" [i] checking internet connection...",end="        ")
    ping = subprocess.Popen(['ping 8.8.8.8 -c 2'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            shell=True)
    try:
        ping.wait(timeout=3)
    except:
        return False
    return_code = ping.poll()

    if return_code == 0:
        return True
    else:
        return False


# commands stager
def engine():
    stage_key = 0
    reading_statge = False
    eachstage = []
    stagesList = []
    connection = internetCheck()
    if (not connection):
        print(f"{ui.WARNING} [Failed]\n [Warning] no internet connection{ui.ENDC}") 
        print(f"{ui.WARNING} [!] check internet connection and try again.{ui.ENDC}") 
        controller()
    else:
        print(f"{ui.OKBLUE} [Passed] {ui.ENDC}")
    try:
        print(" [i] Reading config file...",end="                 ")
        dependency_conf = open("dependency.conf","r")
    except:
        print(f"{ui.WARNING} [Failed] {ui.ENDC}")
        print(f"{ui.WARNING} [!] Can not read config file might be locked or corrupted. {ui.ENDC}")
        controller()
    else:
        print(f"{ui.OKBLUE} [Passed] {ui.ENDC}")
    lines = dependency_conf.readlines()  
    for line in lines:
        line = line.rstrip()
        if line.find('STAGE_START') == 0:                        #detects a new satge
            stage_key_position = line.find("STAGE_START:")
            buffer_mode = True
            stage_key = (line[stage_key_position+12:]).strip()
            #print("[debug] stage_key", stage_key)
            continue
        if line.find("STAGE_END") == 0:
            buffer_mode = False        
        if (buffer_mode):                                         #read from stage
                eachstage.append(line) 
                #print("[Debug] buffer:", stage_key,eachstage)
        if(not buffer_mode and len(eachstage)>0):
            stagesList.append(Stage(stage_key,eachstage))
            eachstage = []
            continue
  

    for s in  stagesList:
        print("[debug] stage_key:",s.key ,"value:", s.value)

        
        
   
        

 
#controller module that listen to user willing what wants to do
def controller():
    selection = select()
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
        print(" [i] cheking if config file exist...",end="        ")
        config_check = path.exists("dependency.conf")
        if (config_check is False): 
            print(f"{ui.WARNING} [Failed] {ui.ENDC}")
            print(f"{ui.WARNING} [Warning] Config file not find or wrong directory.{ui.ENDC}")
        elif selection == 3 and config_check:
            print(f"{ui.OKBLUE} [Passed] {ui.ENDC}")
            engine() #does the main job

    if selection == 4:
        print (ui.help)
    if selection == 5:
        exit()
    if selection == 0:
        print (ui.menu)
         

def main():
    print (ui.CLEAR) #cleans screen
    print (ui.banner)
    print (ui.menu)
    while True:
        controller()  # keeps application running event loop simulation
        

main()