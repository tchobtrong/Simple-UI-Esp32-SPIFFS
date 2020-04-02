# Copyright 2020 simplixio GmbH or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
# Author: Chobtrong, Thitipun Email: tchobtrong@googlemail.com

from tkinter import *
from tkinter import filedialog
import os
import sys
import glob
import serial
from shutil import copyfile


# Find serial ports
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print(result)
    set_COM(result[0])
    return result

# Generate spiffs immage at flash at the defined address
def flash():

    print("===== START =====")
    # create temp config file
    print("Copying file to target folfer ...")
    copyfile(txt.get(), './data/config.ini')
    print("Successfully copied file to target folfer.")

    # create spiffs image
    print("Generating spiffs image ...")
    spiffsconfig = ' -c ./data -p 256 -b 4096 -s 1507328 config.spiffs.bin'
    os.system('mkspiffs.exe ' + spiffsconfig)
    print("Successfully generated the spiffs image.")

    # Upload image
    print("Uploading spiffs image ...")
    config = '--chip esp32 --port '+ txtcom.get()+ ' --baud 115200 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x00290000 config.spiffs.bin'
    os.system('esptool.exe ' + config)

    # Clear temp files
    print("Deleting temp files in target folder ...")
    os.remove("./data/config.ini")
    os.remove("config.spiffs.bin")
    print("Successfully cleared temp files in target folfer.")
    print("===== END =====")

# open file dialog to select file
def browse():
    window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select binary file",filetypes = (("Config files","*.ini"),("all files","*.*")))
    print ("Selected file : " + window.filename)
    set_text(window.filename)
    return

# Set text in path
def set_text(text):
    txt.delete(0,END)
    txt.insert(0,text)
    return

# Set text in COM
def set_COM(text):
    txtcom.delete(0,END)
    txtcom.insert(0,text)
    return

def initconsole():
    print("(((((((((((((((((((((((((((((((((((((((((((((((((((");
    print("(((((((((((((((/*((((((((((((((((((((((((((((((((((");
    print("((((((((((((        (((((((((((((((((((((((((((((((");
    print("((((((((((((         ((((((((((((((((((((((((((((((");
    print("(((((((((((((      ((((((((((((((((((((((((((((((((");
    print("((((((((((((((((((((((((((((*. .(((((((((((((((((((");
    print("((((((((((((((     (((((            /((((((((((((((");
    print("((((((((((((((     ((((     ((((     ((((((((((((((");
    print("((((((((((((((     ((((     (((((     (((((((((((((");
    print("((((((((((((((     (((/     (((((     (((((((((((((");
    print("((((((((((((((     (((/     (((((     (((((((((((((");
    print("((((((((((((((     ((((     (((((     (((((((((((((");
    print("((((((((((((((     ((((     ((((,    *(((((((((((((");
    print("((((((((((((((     (((((             ((((((((((((((");
    print("((((((((((((((,,,,,(((((((/       (((((((((((((((((");
    print("(((((((((((((((((((((((((((((((((((((((((((((((((((");
    print("((((((((((((/                         (((((((((((((");
    print("((((((((((((/                         (((((((((((((");
    print("(((((((((((((((((((((((((((((((((((((((((((((((((((");
    print("***************************************************");
    print("******  simplixio ESP32 SPIFFS Tool v.0.4.0    ****");
    print("***************************************************");

    # Give info
    print("")
    print("")
    print("###### Please see console for checking flash process ####")
    print("")

if __name__ == '__main__':

    # init console
    initconsole()

    # init windows
    window = Tk()
    window.iconbitmap('./logo.ico')
    window.title("simplixio ESP32 SPIFFS Tool v.0.4.0")
    window.geometry('450x100')

    # Path
    lbl = Label(window, text="Config :")
    lbl.grid(column=0, row=0)
    txt = Entry(window,width=50)
    txt.grid(column=1, row=0)

    # Browse button
    brw = Button(window, text="Browse",command=browse,width=10)
    brw.grid(column=2, row=0)

    # Com
    lblcom = Label(window, text="COM :")
    lblcom.grid(column=0, row=2)
    txtcom = Entry(window,width=50)
    txtcom.grid(column=1, row=2)

    # Refresh button
    chk = Button(window, text="R",command=serial_ports,width=10)
    chk.grid(column=2, row=2)

    # Upload button
    btn = Button(window, text="Upload",command=flash,width=30)
    btn.grid(column=1, row=3)

    # View windows
    window.mainloop()
