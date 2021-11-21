import os
import sys

# >/dev/null 2>&1
def check():
    if os.system("miner status") == 0:
        return True
    else:
        return False

def toggle():
    if check() == True:
        os.system("miner stop")
    else:
        os.system("miner start")