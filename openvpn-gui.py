#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter.ttk import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
from tkinter.dnd import dnd_start
from threading import Thread
from common import About as a
import os
import datetime
import gettext
import webbrowser

APPNAME = 'openvpn'
LOCATION = os.path.abspath('locale')

gettext.bindtextdomain(APPNAME, LOCATION)
gettext.textdomain(APPNAME)
_ = gettext.gettext


class OpenVpn(Thread):
    def __init__(self, master=None):
        Thread.__init__(self)

        # Creates a menu
        self.supmenu = Menu(window, tearoff=0, bd=0, bg='#d8d8d8', activeborderwidth=0, postcommand=self.menu_color)
        self.filemenu = Menu(tearoff=0, bd=0, activebackground='#00a2ed', activeforeground='white')

        # File Menu
        self.filemenu.add_command(label=_('Open File'), accelerator='Ctrl+O', command=self.openfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=_('Quit'), accelerator='Ctrl+Q', command=window.quit)

        # Help Menu
        self.helpmenu = Menu(tearoff=0, bd=0, activebackground='#00a2ed', activeforeground='white')
        self.helpmenu.add_command(label=_('Check for updates'), accelerator='Ctrl+A')
        self.helpmenu.add_command(label=_('GitHub'), accelerator='Ctrl+G')
        self.helpmenu.add_command(label='Documentation', accelerator='Ctrl+D')
        self.helpmenu.add_command(label=_('License'), accelerator='Ctrl+U')
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label=_('About'), accelerator='Ctrl+H', command=lambda: a.about(self, window))

        # Sets Up Menu
        self.supmenu.add_cascade(label=_('File'), menu=self.filemenu)
        self.supmenu.add_cascade(label=_('Help'), menu=self.helpmenu)
        window.config(menu=self.supmenu)

        # Frames Creation
        c1 = Frame(master)
        c1.pack()

        c2 = Frame(master)
        c2.pack()

        c3 = Frame(master)
        c3.pack()

        c4 = Frame(master)
        c4.pack()
        
        # Widgets Creation
        self.img = Image.open('images/openvpn.png').resize((250, 80), 1)
        self.bg_image = ImageTk.PhotoImage(self.img)
        
        self.logo = Label(c1, image=self.bg_image)
        self.logo.pack(pady=10)

        self.lb_clock = Label(window)
        self.lb_clock.pack(side=RIGHT, anchor=SE, padx=5)

        self.lb_date = Label(window)
        self.lb_date.pack(side=LEFT, anchor=S, padx=5)

        self.ip_lb = Label(window, text=_('My IP'), fg='blue', cursor='hand2')
        self.ip_lb.pack(side=BOTTOM)

        # Just a simple style
        self.style = Style()
        self.style.configure('TCombobox', selectbackground='#00a2ed', selectforeground='white')
        self.style.configure('TScrollbar', background='lightgray', troughcolor='#F5F5F5')
        self.style.map('TScrollbar', background=[('pressed', '#00a2ed'), ('active', 'white')])

        # Main Widgets
        self.file_combo = Combobox(c2, width=48, style='TCombobox')
        self.file_combo.pack(side=LEFT, padx=5)

        window.option_add('*TCombobox*Listbox*Background', 'white')
        window.option_add('*TCombobox*Listbox*selectBackground', '#00a2ed')
        window.option_add('*TCombobox*Listbox*selectForeground', 'white')

        self.btn_connect = Button(c2, text=_('Connect'), activebackground='#00a2ed', activeforeground='white', command=lambda: Thread(target=self.connect).start())
        self.btn_connect.pack(side=LEFT)

        self.info_connection = ScrolledText(c3, selectbackground='#00a2ed', selectforeground='white', wrap=WORD)
        self.info_connection.pack(fill=BOTH, expand=True, pady=5, padx=5)

        self.clock_update()
        self.combo_files()

        # Set binds (Keyboard Shortcuts)
        self.supmenu.bind('<Button-1>', lambda e: self.menu_color())
        self.supmenu.bind('<Leave>', lambda e: self.menu_uncolor())
        self.ip_lb.bind('<Button-1>', lambda e: Thread(target=webbrowser.open('https://meuip.com.br')).start())
        self.file_combo.bind('<<ComboboxSelected>>', lambda e: self.user_and_pass())
        window.bind('<Control-o>', lambda e: self.openfile())
        window.bind('<Control-O>', lambda e: self.openfile())
        window.bind('<Control-q>', lambda e: window.quit())
        window.bind('<Control-Q>', lambda e: window.quit())
        """window.bind('<Control-a>', lambda e: )
        window.bind('<Control-A>', lambda e: )
        window.bind('<Control-g>', lambda e: )
        window.bind('<Control-G>', lambda e: )
        window.bind('<Control-d>', lambda e: )
        window.bind('<Control-D>', lambda e: )
        window.bind('<Control-u>', lambda e: )
        window.bind('<Control-U>', lambda e: )"""
        window.bind('<Control-h>', lambda e: a.about(self, window))
        window.bind('<Control-H>', lambda e: a.about(self, window))
        window.bind('<Control-l>', lambda e: self.clear_fields())
        window.bind('<Control-L>', lambda e: self.clear_fields())

    def connect(self):
        files = os.path.abspath('files')
        ovpn = self.file_combo.get()
        ovpn_e = str(ovpn).replace('.ovpn', '.temp')
        user_pass = os.path.join(f'data/{ovpn_e}')
        log_w = open('log', 'w')
        log_w.write('')
        log_w.close()
        
        if ovpn == '':
            showerror(title=_('Status'), message=_('Select one file to connect.'))
        else:
            self.set_log_file()
            title = _('OpenVpn Gui - Ctrl+C to stop connection')
            os.system(f'xterm -T "{title}" -e sudo openvpn --config {files}/{ovpn} --auth-user-pass {user_pass} --log log ; rm {user_pass}')

    def user_and_pass(self):
        popup = Toplevel()
        popup.grab_set()
        popup.focus_force()
        popup.transient(window)
        popup.geometry('250x130')
        self.user_lb = Label(popup, text=_('User'))
        self.user_lb.pack()
        self.user_txt = Entry(popup, selectbackground='#00a2ed', selectforeground='white')
        self.user_txt.pack()

        self.pass_lb = Label(popup, text=_('Pass'))
        self.pass_lb.pack()
        self.pass_txt = Entry(popup, show='•', selectbackground='#00a2ed', selectforeground='white')
        self.pass_txt.pack()

        self.ok = Button(popup, text=_('OK'), activebackground='#00a2ed', activeforeground='white', command=lambda: [Thread(target=self.save_user_pass).start(), Thread(target=popup.destroy).start(), Thread(target=popup.update).start()])
        self.ok.pack(pady=5)

        self.user_txt.insert(INSERT, 'tcpvpn.com-Alexsussa')
        self.pass_txt.insert(INSERT, 'alex1234')
        
    def save_user_pass(self):
        user = self.user_txt.get()
        passw = self.pass_txt.get()
        ovpn = str(self.file_combo.get()).replace('.ovpn', '.temp')

        if not os.path.exists(f'data/{ovpn}'):
            en_pass = open(f'data/{ovpn}', 'w')
            en_pass.write(f'{user}\n')
            en_pass.write(f'{passw}')
            en_pass.close()
        else:
            os.system(f'cd data ; rm *.temp')
            en_pass = open(f'data/{ovpn}', 'w')
            en_pass.write(f'{user}\n')
            en_pass.write(f'{passw}')
            en_pass.close()

    def openfile(self):
        file = askopenfilename(initialdir='~/', filetypes=[('OpenVpn File', '*.ovpn')])
        files = os.path.abspath('files')
        if self.file_combo.get() == '':
            self.file_combo.insert(INSERT, os.path.basename(file))
            if self.file_combo.get() != '':
                self.user_and_pass()
        else:
            self.file_combo.delete(0, END)
            self.file_combo.insert(INSERT, os.path.basename(file))
            self.user_and_pass()

        os.system(f'cp {file} {files}')

    def combo_files(self):
        ovpn_files = []
        files = os.path.abspath('files')
        for f in os.listdir(files):
            if f not in ovpn_files and f.endswith('.ovpn'):
                ovpn_files.append(f)

        self.file_combo.config(values=ovpn_files)
        self.file_combo.after(500, self.combo_files)

    def clock_update(self):
        date_now = datetime.datetime.today().strftime('%d-%m-%Y')
        time_now = datetime.datetime.today().strftime('%H:%M:%S')
        self.lb_clock.config(text=time_now)
        self.lb_date.config(text=date_now)
        self.lb_clock.after(1000, self.clock_update)
        #self.lb_date.after(1000, self.clock_update)

    def menu_color(self):
        self.supmenu.config(activebackground='#00a2ed')

    def menu_uncolor(self):
        self.supmenu.config(activebackground='#cccccc')

    def clear_fields(self):
        self.file_combo.delete(0, END)
        self.info_connection.delete(1.0, END)

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

        self.info_connection.after(1000, self.set_log_file)


window = Tk()
OpenVpn(window)
window.tk.call('source', 'config/themes/azure/azure.tcl')
window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='images/icon.png'))
try:
    window.tk.call('tk_getOpenFile', '-foobarbaz')
except TclError:
    pass
window.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
window.title('OpenVpn Gui')
window.geometry('500x600')
window.resizable(0, 0)
window.update()
window.mainloop()
if window.quit or window.destroy:
    os.system('cd data ; rm *.temp')
