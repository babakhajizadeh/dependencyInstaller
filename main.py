#!/usr/bin/env python3

import ctypes
from mimetypes import init
import subprocess
import sys
import platform
from os import path
import os
import socket

os.chdir('..')
configpath = os.getcwd()
buildall = False




#stage class is blueprint to stage object which is consist of stage body List (commands) and a key 
class Stage:
    def __init__(self, key, commands):   # commands known as stagebody list and key is the stage key
        self.key = key                   # key is the stage key
        self.value = commands            # value is stagebody which is a list data strcture
class ui:
    BOLD = '\033[1m'
    RED = '\033[91m'
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
    failureprompt ="""
     what are you willing to do:
     [1] Continue to execute next stage.
     [2] Break the operation. 
     [3] Exit.  
    """
    buildallprompt = """
  [?] Build all stages?
      [1] Continue/build and prompt each time a stage done.
      [2] execute all stages untill finish or raise of an Error.
    """
    help = """
  [i] Instruction:
      config file name must be: dependency.conf (case sensetive).
      config file must contain encapsulated build commands in 'Stages' whithin 
      the format shown below: (case sensitive).
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



#this method handles user input (selection of options from the menu)
def select():                             
    try:
        selection = int(input("\n [?] Select> ([0] for Menu): "))
    except:
        print(f"{ui.WARNING} [!] Invalid type. try again. {ui.ENDC}") 
        select() 
    else:
        return selection
        
#this method checks for internet connection using system ping program
def internetCheck():
    print(" [i] checking internet connection...",end="        ")
    try:
        # connect to the host -- tells us if the host is actually
        # reachable 
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False


# this method executes commands whithn an stage
def stageExe(stage_instance):
    stage_status = True                              # if it executed successfully will report true, 
    commands = stage_instance.value                  # any error will change it false
    for command in commands:
        print(f"{ui.RED} [Execute]{ui.ENDC} stage:", stage_instance.key , f"command:{ui.BOLD}", command, f"{ui.ENDC}")
        
        commandexe = subprocess.Popen(str(command),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True)

        while True:
            output = commandexe.stdout.readline()
            if output == '' or commandexe.poll() is not None:
                break
            if output:
                output = (str(output))[1:]
                print(f" [OS] stdout report:{ui.HEADER}" ,output, f" {ui.ENDC}")
        return_code = commandexe.poll()
        if (return_code == 0):
            print(f"{ui.OKBLUE} [OS] command succeed, return code 0.{ui.ENDC}")
        else:
            print(f"{ui.WARNING} [OS] Command Failed, return code:{ui.ENDC}", return_code)
            stage_status=False
    return stage_status

                

    
    
# commands stager
def engine():
    global buildall
    stage_key = 0
    stagebody = []
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
        
    #above control conditions verifies availablity of config file
    lines = dependency_conf.readlines()  
    expect_STAGE_END_identifier = False
    expect_STAGE_START_identofier = False
    for line in lines :
        line = line.rstrip()
        if line == "" or line[0] == "#":                                           # skips empty lines
            continue
        if line.find('STAGE_START') == 0 and not expect_STAGE_END_identifier:      # detects start of new satge from config file by reading
            expect_STAGE_END_identifier = True 
            expect_STAGE_START_identofier = False
            stage_key_position = line.find("STAGE_START:")                         # specifc "STAGE_START identifier in config file"
            buffer_mode = True
            stage_key = (line[stage_key_position+12:]).strip()                     # reads the stage key
            #print("[debug] stage_key", stage_key)
            continue
        elif line.find('STAGE_START') == 0 and expect_STAGE_END_identifier:
            print(f"{ui.RED} [Fatal] Expected STAGE_END identifier, but missing.\n{ui.ENDC}")
            exit() 
            
        if line.find("STAGE_END") == 0 and not expect_STAGE_START_identofier:      # detecs end of stage by "STAGE_END" identifier and stops buffering commands
            expect_STAGE_END_identifier = False
            expect_STAGE_START_identofier = True
            buffer_mode = False 
        elif line.find('STAGE_END') == 0 and expect_STAGE_START_identofier:
            print(f"{ui.RED} [Fatal] Expected STAGE_START identifier, but missing.\n{ui.ENDC}")      
            exit() 
        if (buffer_mode ):                                       # reads commands from buffer whithin the stage body 
                stagebody.append(line)                           # into a list data structure named as "stagebody"
                #print("[Debug] buffer:", stage_key,stagebody)
        if(not buffer_mode and len(stagebody)>0):
            stagesList.append(Stage(stage_key,stagebody))        # creates a stage list consisting of stage class object(body,key)
            stagebody = []                                       # each stage class object is made of several commands knwon as stage "body" 
            continue                                             # and a refrence key, each body has a unique key
   
  
    for stage_instance in stagesList:                            # reads every single stage class objects from the stage list
        stage_status = stageExe(stage_instance)                                 # and sends it to stageexe() which takes responsiblity is executing a stage 
        if stage_status:
            print(f"{ui.OKBLUE} [i] stage:", stage_instance.key, 
                  f"executed with no Errors.{ui.ENDC}")
            if not buildall:
                print(ui.buildallprompt)
                selection = select()
                if selection == 1:
                    buildall =  False
                elif selection == 2:
                    buildall = True
                else:
                    while buildall == 0:
                        print(ui.buildallprompt)
                        select()
                
        else:
            print(f"{ui.WARNING} [i] Stage Nom.: ", stage_instance.key, 
                  f" ,execution resulted in atleast one Error.{ui.ENDC}",sep="")
            print(ui.failureprompt)
            selection =select()
            if selection == 0:
                print(ui.failureprompt)
                select()
            elif selection == 1:
                continue
            elif selection == 2:
                print (ui.menu)
                controller();
            elif selection == 3:
                exit()  
            else:
                print(f"{ui.WARNING} [!] Invalid type. try again. {ui.ENDC}")
                select()
    if stage_status:
        print(f"{ui.OKBLUE} [i] Job Finished. All stages done successfully. {ui.ENDC}")
        dependency_conf.close()
    else:
        print(f"{ui.WARNING} [!] Job Finished. Encountered atleast one error. {ui.ENDC}")
        dependency_conf.close()
     
 
#controller module that listen to user willing what wants to do
def controller():
    global configpath
    global buildall
    selection = select()
    if selection == 1:
        print (f" [i] Current work directory for build is{ui.OKBLUE}:\n    " , configpath)
        print(f"{ui.ENDC}")
        prompt = input(" [?] would you like to modify? (y/n):")
        if (prompt == 'Y' or prompt == 'y'):
            print (" [?] Input new build path address:", end=" ")
            temp_configpath = input("(POSIX: ~/ is not supported)(e.g: C:/mylib/source):")
            if len(temp_configpath) < 1:
                print(f"{ui.WARNING} [!] Input address is too short.{ui.ENDC}")
            else:
                print(" [i] New directory as buildpath is set to:")
                configpath = temp_configpath
                print("    ",configpath)
                try:
                    os.chdir(configpath)
                except:
                    print(f"{ui.WARNING} [!] No such file or directory: ",configpath , f"{ui.ENDC}")
                    configpath = os.getcwd()
        elif(prompt == 'N' or prompt == 'n'):
            print(" [i] Build directory has not changed.") 
        else: 
            print (f"{ui.WARNING} [!] Input invalid.{ui.ENDC}")
    if selection == 2:
        config_check = path.exists("dependency.conf")            # returns True if config file found
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
            print(ui.buildallprompt)
            selection = select()
            if selection == 1:
                buildall =  False
            elif selection == 2:
                buildall = True
            else:
                while buildall == 0:
                    print(ui.buildallprompt)
                    select()
                    
            engine() #does the main job
            

    if selection == 4:
        print (ui.help)
    if selection == 5:
        exit()
    if selection == 0:
        print (ui.menu)
         

def main():
    currentPlatform = platform.system()
    if currentPlatform == "Windows":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        
    print (ui.CLEAR) #cleans screen
    print (ui.banner)
    print (ui.menu)
    while True:
        controller()  # keeps application running, sort of event loop simulation
        

main()