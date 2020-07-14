import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True) # Reset Colour after every line

colorama.init() #Initialize

def col_info(msg):
    print(Fore.MAGENTA + msg)

def col_connect(method,path):
    print(Fore.GREEN + method+" ",end="")
    print(Fore.CYAN + path)

def col_warning(msg):
    print(Fore.YELLOW + msg)

def col_error(msg):
    print(Fore.RED + msg)