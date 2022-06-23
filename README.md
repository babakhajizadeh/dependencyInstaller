![made-with-python](https://img.shields.io/badge/python-v3.7-blue)
# Dependency Installer

__Dependency Installer is a powered by Python tool that eases building of independently developed applications.__  
It can be usefull to organize your build commands within a config file (dependency.conf) and run __accross platforms__
made possible by taking advantage of Python's _Subprocess Module_ which handles system shell commands accross variety of platforms
including _Linux X11_ and _Microsoft Windows._
__Still under development__  
 
### Build  
```sh
chmod +x main.py
```
### Usage:
```sh

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
            Dependency Installer to your source folder simply
            change config file path
         


```

#### acknowledgement
Development of this tool supervised by Mentor __Amirreza Ashouri. [AMP999](https://github.com/AMP999)__ 

