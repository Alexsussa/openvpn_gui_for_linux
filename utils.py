#!/usr/bin/python3
# -*- coding: utf-8 -*-

from threading import Thread
from tkinter import *


class Utilities(Thread):
    def __init__(self):
        Thread.__init__(self)

    def set_log_file(self):
        log_file = open('log', 'r').read()
        self.info_connection.config(state='normal')
        if self.info_connection.get(1.0, END) == '':
            self.info_connection.insert(INSERT, f'{log_file}')
        else:
            self.info_connection.delete(1.0, END)
            self.info_connection.insert(END, f'{log_file}')
            self.info_connection.see('end')
            self.info_connection.config(state='disable')

        #self.info_connection.after(1000, self.set_log_file)
