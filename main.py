#!/usr/bin/python3
import time
import argparse
import render
import os
import shutil
import threading
import uploadserver

# Time to search for files and render path
time.sleep(20)
render_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "render")
upload_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "upload")
sec = 10
# Adding arguments for the type of server wanted
parser = argparse.ArgumentParser()
parser.add_argument("-H", "--hive", action='store_true', help="help")
parser.add_argument("-G", "--drive", action='store_true', help="help")
parser.add_argument("-F", "--fileServer", action='store_true', help="help")
args = parser.parse_args()

# Importing files based on server selected

if args.drive:
    import drive
if args.fileServer:
    import uploadserver


# Searches drive for folder and renders it
def drive_timer():
    while True:
        compare = drive.get_folders()
        time.sleep(sec)
        new = drive.get_folders()
        for file in new:
            if file not in compare:
                drive.download(os.path.join(render_path, file['name']), file['id'])
                if args.hive:
                    render.render_hive(file['name'])
                else:
                    render.render(file['name'])


# Adds webserver support to render files remotely
def file_server():
    while True:
        compare = os.listdir(upload_dir)
        print(compare)
        time.sleep(sec)
        new = os.listdir(upload_dir)
        for file in new:
            if file not in compare:
                shutil.unpack_archive(os.path.join(upload_dir, file), render_path)
                if args.hive:
                    render.render_hive(os.path.splitext(file)[0])
                else:
                    render.render(os.path.splitext(file)[0])


# Figures out what to do based on arguments given
if args.drive:
    if args.fileServer:
        p1 = threading.Thread(target=uploadserver.main)
        p2 = threading.Thread(target=file_server)
        p3 = threading.Thread(target=drive_timer)
        p2.start()
        p1.start()
    else:
        drive_timer()
else:
    if args.fileServer:
        p1 = threading.Thread(target=uploadserver.main)
        p2 = threading.Thread(target=file_server)
        p2.start()
        p1.start()