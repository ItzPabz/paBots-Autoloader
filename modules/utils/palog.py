
import colorama as clr
import datetime
import sys

DEBUG_MODE = True
sys.dont_write_bytecode = True

def timestamp():
    now = datetime.datetime.now()
    return now.strftime('%H:%M:%S')

def debug(message, level='DEBUG'):
    if DEBUG_MODE:
        time = timestamp()
        print(f'[{time} {level}] {message}')

def info(message, level='INFO'):
    time = timestamp()
    print(f'{clr.Fore.LIGHTBLUE_EX}[{time} {level}] {message}{clr.Style.RESET_ALL}')

def warning(message, level='WARNING'):
    time = timestamp()
    print(f'{clr.Fore.YELLOW}[{time} {level}] {message}{clr.Style.RESET_ALL}')

def error(message, level='ERROR'):
    time = timestamp()
    print(f'{clr.Fore.RED}[{time} {level}] {message}{clr.Style.RESET_ALL}')

def critical(message, level='CRITICAL'):
    time = timestamp()
    print(f'{clr.Back.RED}{clr.Fore.YELLOW}[{time} {level}] {message}{clr.Style.RESET_ALL}')
    sys.exit(1)
