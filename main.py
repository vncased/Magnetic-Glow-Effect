import os
import platform

system_name = platform.uname().system 

if system_name == "Linux":
    os.system('python3 src/tll.py')
elif system_name == "Windows":
    os.system("python3 src/tll.py")
