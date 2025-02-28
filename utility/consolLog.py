import datetime
import inspect

ORANGE = "\033[33m"
RED = "\033[31m"     
END = "\033[0m"   

def getFileName(inspectStackFilename):
    templist = []
    for letter in reversed(inspectStackFilename):
        if letter != "\\" and letter != "/":
            templist.append(letter)
        else:
            break
    templist.reverse()
    return "".join(templist)

def info(text: str):
    print(f"{str(datetime.datetime.now())[:19]} - INFO - {getFileName(inspect.stack()[1].filename)} - {text}")

def warn(text: str):
    print(f"{ORANGE}{str(datetime.datetime.now())[:19]} - WARN - {getFileName(inspect.stack()[1].filename)} - {text}{END}")

def error(text: str):
    print(f"{RED}{str(datetime.datetime.now())[:19]} - ERROR - {getFileName(inspect.stack()[1].filename)} - {text}{END}")
