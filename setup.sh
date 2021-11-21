#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
if  [[ $1 = "-h" || $2 = "-h" || $3 = "-h" ]]; then
    printf "Use this file with root permissions\n"
    printf "Option '-g' or '-f' required\n"
    printf "'-g': Use this if you want google drive support\n"
    printf "'-f': Use this if you want a built-in webserver for file upload located at http://0.0.0.0:8000/upload\n"
    printf "'-H': Use this if you have HiveOS as an operating system\n"
    printf "'-h': Use this to get this help message\n"
    exit
fi

if  [[ $1 = "-H" || $2 = "-H" || $3 = "-H" ]]; then
    if [[ $1 = "-f" || $1 = "-g" ]]; then
        if [[ $1 = "-f" ]]; then
            if [[ $2 = "-g" ]]; then
                python3.7 drive.py
                printf "@reboot root $DIR/main.py '-GFH'" > /etc/cron.d/blender-server
            else
                printf "@reboot root $DIR/main.py '-FH'" > /etc/cron.d/blender-server
            fi
        fi
        if [[ $1 = "-g" ]]; then
            if [[ $2 = "-f" ]]; then
                python3.7 drive.py
                printf "@reboot root $DIR/main.py '-GFH'" > /etc/cron.d/blender-server
            else
                python3.7 drive.py
                printf "@reboot root $DIR/main.py '-GH'" > /etc/cron.d/blender-server
            fi
        fi
    fi    

elif [[ $1 = "-f" || $1 = "-g" ]]; then
    if [[ $1 = "-f" ]]; then
        if [[ $2 = "-g" ]]; then
            python3.7 drive.py
            printf "@reboot root $DIR/main.py '-GF'" > /etc/cron.d/blender-server
        else
            printf "@reboot root $DIR/main.py '-F'" > /etc/cron.d/blender-server
        fi
    fi
    if [[ $1 = "-g" ]]; then
        if [[ $2 = "-f" ]]; then
            python3.7 drive.py
            printf "@reboot root $DIR/main.py '-GF'" > /etc/cron.d/blender-server
        else
            python3.7 drive.py
            printf "@reboot root $DIR/main.py '-G'" > /etc/cron.d/blender-server
        fi
    fi

else
    printf "Requires either -f or -g to work\nUse -h for help\n"
    exit
fi

printf "All Done!\n"
exit