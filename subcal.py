#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import ipaddress
from enum import Enum
import os
import re
import sys
import yaml

class Color():
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CLEAR = '\033[0m'

class LoggingSeverity():
    ERROR = Color.RED + '[Error] ' + Color.CLEAR
    INFO = Color.GREEN + '[Info] ' + Color.CLEAR

class Message():
    FILE_NOT_FOUND = "File is not found"
    FORMAT_ERROR_PREFIX = "The format of the Prefix is incorrect"
    COLUMN_ERROR_PREFIX = "Unavailable columns exist"
    COLUMNOPTION_ERROR_PREFIX = "Unavailable columns option exist"

class OutputColumn():
    column = [
        "hostAddr",
        "hostPrefix", 
        "networkAddr", 
        "networkPrefix", 
        "broadcastAddr", 
        "broadcastPrefix", 
        "prefixLen", 
        "subnetmask", 
        "wildcardmask", 
        "addressNum", 
        "hostNum", 
        "public", 
        "custom"
    ]

class ColumnOption():
    common = [
        "name"
    ]
    custom = [
        "name",
        "fromTheLast",
        "fromThefirst"
    ]

def parse_args():
    parser = argparse.ArgumentParser(prog="Subnet Calculator", description="This Script is Subnet Calculate. A useful tool for network engineers.")
    parser.add_argument('-i', '--input_file', help='Use file to calculate multiple values.')
    parser.add_argument('-o', '--output_file', help='File to output calculation results')
    parser.add_argument('-s', '--settings', help='Select the settings file you wish to use')
    args = parser.parse_args()
    return args

def analyze_args():
    pass

def is_file(a):
    return os.path.isfile(a)

def load_inputfile(inputFile):
    with open(inputFile) as f:
        targetPrefixList = f.read().split('\n')
    errorFlag = False
    for i, v in enumerate(targetPrefixList):
        v = v.replace(',', '/').rstrip().lstrip()
        targetPrefixList[i] = v
        if check_format_prefix(v):
            pass
        else:
            print(LoggingSeverity.ERROR + Message.FORMAT_ERROR_PREFIX + " line:" + str(i) + " " + v)
            errorFlag = True
    if errorFlag:
        exit()
    return targetPrefixList

def check_format_prefix(value):
    prefixRegex = "((25[0-5]|1[0-9]{2}|2[0-4][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|1[0-9]{2}|2[0-4][0-9]|[1-9]?[0-9])/(3[12]|[1-2]?[0-9])"
    if re.fullmatch(prefixRegex, value) or value == "":
        return True
    else:
        return False

def load_settings(inputFile):
    with open(inputFile) as f:
        settings = yaml.safe_load(f)
    errorFlag = False
    for v in settings['output']['column'].keys():
        if check_column(v):
            for i,j in settings['output']['column'][v].items():
                if check_column_option(v,i):
                    pass
                else:
                    print(LoggingSeverity.ERROR + Message.COLUMNOPTION_ERROR_PREFIX + " (" + str(v) + "." + str(i) + ")")
                    errorFlag = True
        else:
            print(LoggingSeverity.ERROR + Message.COLUMN_ERROR_PREFIX + " (" + v + ")")
            errorFlag = True
    if errorFlag:
        exit()
    return settings['output']['column']


def check_column(column):
    return column in OutputColumn.column

def check_column_option(column,option):
    if column == "custom":
        return option in ColumnOption.custom
    else:
        return option in ColumnOption.common

def main():
    # input
    args = parse_args()
    targetValue = []
    if (args.input_file): # input or stdin
        if not is_file(args.input_file):
            print(LoggingSeverity.ERROR + Message.FILE_NOT_FOUND)
            exit()
        targetValue = load_inputfile(args.input_file)
    else:
        analyze_args()

    settingsFile = args.settings
    if (settingsFile):
        if not is_file(settingsFile):
            print(LoggingSeverity.ERROR + Message.FILE_NOT_FOUND)
            exit()
    else:
        if not is_file("./settings.yaml"):
            print(LoggingSeverity.ERROR + Message.FILE_NOT_FOUND + " (./settings.yaml)")
            exit()
        settingsFile = "./settings.yaml"
    
    outputColumnList = load_settings(settingsFile)
    print(outputColumnList)
    # process

    # output

if __name__ == "__main__":
    main()