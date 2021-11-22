import os

# >/dev/null 2>&1
def check():
    if os.system("/hive/bin/miner status > /dev/null 2>&1") == 0:
        return True
    else:
        return False

def toggle():
    if check() == True:
        os.system("/hive/bin/miner > /dev/null 2>&1")
    else:
        os.system("/hive/bin/miner > /dev/null 2>&1")