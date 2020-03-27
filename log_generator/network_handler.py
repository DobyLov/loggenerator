#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Network handler
# pip install pythonping # remplacé par ping3
# pip install ping3
from datetime import datetime
from pythonping import ping
import os, sys, shlex, subprocess
from log_generator.operating_system_handler import get_platform

# Ping host
def pingHost(ip:str):

    try:
        my_os = get_platform()

        if my_os == "windows":
            output = subprocess.Popen(["ping", "-n", "2" , ip], stdout=subprocess.PIPE).communicate()[0]
            #print(output.decode('iso8859-1'))
            if 'pas pu trouver' in str(output.decode('windows-1252',errors='ignore')):
                print("Ping Server : " + ip + " unreachable")
                exitProgram()
                
        elif my_os == "linux":
            output = subprocess.Popen(["ping", "-c", "1" , ip], stdout=subprocess.PIPE).communicate()[0]
            if output != 0:
                print("Ping Server : " + ip + " unreachable")
                exitProgram()
        
        else:
            print("unknow operating system")

    except subprocess.CalledProcessError:
        print("Ping Server : " + ip + " unreachable")
        exitProgram()
    
# Retourne la date et l heure
def get_dateNow():
    dateNow: str = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + " " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second)
    return dateNow

# sortir du programme
def exitProgram():
    import sys
    print("Exit script : " + get_dateNow() )
    sys.exit()
