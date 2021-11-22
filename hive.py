import os

# >/dev/null 2>&1
def check():
    if os.system("miner status > /dev/null 2>&1") == 0:
        return True
    else:
        return False

def toggle():
    if check() == True:
        os.system("miner stop > /dev/null 2>&1")
    else:
        os.system("miner start > /dev/null 2>&1")