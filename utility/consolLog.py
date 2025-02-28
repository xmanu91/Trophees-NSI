import datetime
import inspect

ORANGE = "\033[33m"
RED = "\033[31m"
END = "\033[0m"

debug = True

def getFileName(inspectStackFilename):
    templist = []
    for letter in reversed(inspectStackFilename):
        if letter != "\\" and letter != "/":
            templist.append(letter)
        else:
            break
    templist.reverse()
    return "".join(templist)

def info(*text: str | int | float | bool):
    if debug:
        message = " ".join(map(str, text)) 
        print(f"{str(datetime.datetime.now())[:19]} - INFO - {getFileName(inspect.stack()[1].filename)} - {message}")

def warn(*text: str | int | float | bool):
    if debug:
        message = " ".join(map(str, text))
        print(f"{ORANGE}{str(datetime.datetime.now())[:19]} - WARN - {getFileName(inspect.stack()[1].filename)} - {message}{END}")

def error(*text: str | int | float | bool):
    if debug:
        message = " ".join(map(str, text))
        print(f"{RED}{str(datetime.datetime.now())[:19]} - ERROR - {getFileName(inspect.stack()[1].filename)} - {message}{END}")
