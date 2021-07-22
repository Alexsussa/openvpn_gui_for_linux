#!/usr/bin/python3
# -*- coding: utf-8 -*-

from posixpath import expanduser
from tkinter.scrolledtext import ScrolledText
from tkinter.tix import Select
from tkinter.ttk import *
from tkinter import *
from threading import Thread
import gettext
import webbrowser
import os

APPNAME = 'openvpn'
LOCATION = os.path.abspath('locale')

gettext.bindtextdomain(APPNAME, LOCATION)
gettext.textdomain(APPNAME)
_ = gettext.gettext


class About(Thread):
    def __init__(self, master=None):
        Thread.__init__(self)

    def about(self, window):
        win_about = Toplevel()
        win_about.title(_('About OpenVPN Gui'))
        win_about.geometry('500x500')
        win_about.grab_set()
        win_about.focus_force()
        win_about.transient(window)

        self.logo_bg = PhotoImage(file='images/icon.png')
        self.lb_img = Label(win_about, image=self.logo_bg)
        self.lb_img.image = self.logo_bg
        self.lb_img.pack()

        self.github = Label(win_about, text=_('GitHub'), cursor='hand2')
        self.github.pack()

        self.license = Label(win_about, text=_('License'))
        self.license.pack()

        l_file = open('COPYING', 'r').read()
        self.license_info = ScrolledText(win_about, height=12, width=58, wrap=WORD, selectbackground='#00a2ed', selectforeground='white', state='disable')
        self.license_info.config(state='normal')
        self.license_info.insert(INSERT, l_file)
        self.license_info.config(state='disable')
        self.license_info.pack()

        self.copy = Label(win_about, text=_('©OpenVPN'), cursor='hand2')
        self.copy.pack(side=RIGHT, anchor=SE)

        self.dev = Label(win_about, text=_('Alex Pinheiro'), cursor='hand2')
        self.dev.pack(side=LEFT, anchor=SW)

        self.github.bind('<Enter>', lambda e: self.github.config(fg='blue'))
        self.github.bind('<Leave>', lambda e: self.github.config(fg='black'))
        self.github.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa'))
        
        self.copy.bind('<Button-1>', lambda e: webbrowser.open('https://openvpn.net'))
        self.copy.bind('<Enter>', lambda e: self.copy.config(fg='blue'))
        self.copy.bind('<Leave>', lambda e: self.copy.config(fg='black'))

        self.dev.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa'))
        self.dev.bind('<Enter>', lambda e: self.dev.config(fg='blue'))
        self.dev.bind('<Leave>', lambda e: self.dev.config(fg='black'))
