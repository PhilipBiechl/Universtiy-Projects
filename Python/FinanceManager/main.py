# Used packages import
import os
from tkinter import *
from tkinter import messagebox 
from tktooltip import ToolTip
from tkcalendar import Calendar
import customtkinter as cTk
from PIL import Image
from datetime import datetime, date, timedelta
import time
import sqlite3
from sqlite3 import Error
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import mplcyberpunk
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use("cyberpunk")

# Global variable -> directory of main.py on pc

current_dir_global = os.path.dirname(os.path.abspath(__file__))

# Functions to close and open windows on window-change

def page_pack_forget():
    window_main.pack_forget()
    window_inout.pack_forget()
    window_plot.pack_forget()
    window_settings.pack_forget()
    window_history.pack_forget()
    window_login.pack_forget()
    window_register.pack_forget()

def page_login():
    page_pack_forget()
    window.title('Finance App - Login')
    Login(window_login)
    window_login.pack()

def page_regis():
    page_pack_forget()
    window.title('Finance App - Register')
    Register(window_register)
    window_register.pack()

def page_main(user):
    page_pack_forget()
    window.title('Finance App')
    Main_Screen(window_main,user)
    window_main.pack()

def page_inout(user):
    page_pack_forget()
    InOut_Screen(window_inout,user)
    window_inout.pack()

def page_plot(user):
    page_pack_forget()
    Plot_Screen(window_plot,user)
    window_plot.pack()
    
def page_history(user):
    page_pack_forget()
    History_Screen(window_history,user)
    window_history.pack()
    
def page_settings(user, command):
    page_pack_forget()
    Settings_Screen(window_settings, user, command)
    window_settings.pack()

# Connect to used database or create if it does not exist

try:
    connection = sqlite3.connect("financeapp_local_data.db")
except Error as sqlerror:
    messagebox.showerror("Finance App - Sqlite", str(sqlerror))
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name TEXT, password TEXT, user_id_db TEXT, user_id_set TEXT, warn_zero INT, warn_sum INT)")

# classes definiton -> windows and included functions

# class structure:
#    __init__(self, [params])    |  slef.[func name](self, [params])              
#   ------------------------------------------------------------------------------------------------------------------
#    visual elements are         |  functions used when clicking a button/user-interactong or to process parameters.
#    defined here.               |  some functions also contain visual elements for implementation in init.
#                                |  
#    order:                      |  order:
#    o variables defined as:     |  o variables defined as: [if used in other parts of the class / only in this func]
#      self.__[var name]         |    self.__[var name]     /    [var name]
#                                |  
#    o tKinter elements as:      |  o tKinter elements as: 
#      self.__[elem name]        |    self.__[elem name]  
#                                |

######################################################################################################################################################################
##         CLASS  REGISTER
######################################################################################################################################################################

class Register:
    def __init__(self, window_r):
        self.__window_r = window_r
        self.__normal_bg = "#010712"
        
        # Background for the window
        self.__bg_image = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "Register_bg.png")), size=(1000 , 500))
        self.__bg_image_label = cTk.CTkLabel(self.__window_r, image=self.__bg_image, text="")
        self.__bg_image_label.grid(row=0, column=0)
        
        # WELCOME
        self.__heading = cTk.CTkLabel(master=self.__window_r, 
                                            font=('arial', 35, 'bold'),
                                            text="IT IS A PLEASURE TO MEET YOU",
                                            bg_color=self.__normal_bg)
        self.__heading.place(relx=0.33, rely=0.1, anchor=CENTER)
        
        # Register Username
        self.__uName_Label = cTk.CTkLabel(master=self.__window_r, 
                                            font=('arial', 17),
                                            text="Username",
                                            bg_color=self.__normal_bg)
        self.__uName_Label.place(relx=0.515, rely=0.23, anchor=CENTER)
        self.__uName_Entry = cTk.CTkEntry(master=self.__window_r, 
                                            placeholder_text="Choose a username - you can also edit it later",
                                            width=450,
                                            height=50,
                                            bg_color=self.__normal_bg,
                                            font=('arial', 20))
        self.__uName_Entry.place(relx=0.7, rely=0.32, anchor=CENTER)
        self.__uName_Canvas = cTk.CTkFrame(master=self.__window_r,
                                            corner_radius=0,
                                            fg_color="#494996",
                                            bg_color=self.__normal_bg,
                                            height=5,
                                            width=450)
        self.__uName_Canvas.place(relx=0.7, rely=0.365, anchor=CENTER)
        
        # Register Password
        self.__uPW_Label = cTk.CTkLabel(master=self.__window_r, 
                                            font=('arial', 17),
                                            text="Password",
                                            bg_color=self.__normal_bg)
        self.__uPW_Label.place(relx=0.515, rely=0.43, anchor=CENTER)
        self.__uPW_Entry = cTk.CTkEntry(master=self.__window_r, 
                                            placeholder_text="Choose a password",
                                            width=450,
                                            height=50,
                                            show="*",
                                            bg_color=self.__normal_bg,
                                            font=('arial', 20))
        self.__uPW_Entry.place(relx=0.7, rely=0.52, anchor=CENTER)
        self.__uPW_Canvas = cTk.CTkFrame(master=self.__window_r,
                                            corner_radius=0,
                                            fg_color="#494996",
                                            bg_color=self.__normal_bg,
                                            height=5,
                                            width=450)
        self.__uPW_Canvas.place(relx=0.7, rely=0.565, anchor=CENTER)
        
        # Register Button
        self.__Register_Button = cTk.CTkButton(master=self.__window_r,
                                            text="Register",
                                            font=('arial', 20),
                                            fg_color="#00A417",
                                            bg_color=self.__normal_bg,
                                            hover_color="#009017",
                                            corner_radius=10,
                                            width=450,
                                            height=50,
                                            command=self.register_user
                                            )
        self.__Register_Button.place(relx=0.7, rely=0.715, anchor=CENTER)
        
        # PASSWORD visable
        self.__pwview_image = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "eye-3-xxl.png")), size=(44 , 44))
        self.__uPW_Button = cTk.CTkButton(master=self.__window_r,
                                            image=self.__pwview_image,
                                            text="",
                                            fg_color='#494996',
                                            bg_color=self.__normal_bg,
                                            corner_radius=0,
                                            width=45,
                                            command=self.hide)
        self.__uPW_Button.place(relx=0.9, rely=0.52, anchor=CENTER)
        
        # LOGIN already registered
        self.__register_Label = cTk.CTkLabel(master=self.__window_r, 
                                            font=('arial', 20),
                                            text="Do you already have an account?",
                                            bg_color=self.__normal_bg,)
        self.__register_Label.place(relx=0.195, rely=0.25, anchor=CENTER)
        
        self.__register_Button = cTk.CTkButton(master=self.__window_r,
                                            text="LOGIN",
                                            font=('arial', 20),
                                            fg_color="#494996",
                                            bg_color=self.__normal_bg,
                                            hover_color="#3D3D9A",
                                            corner_radius=5,
                                            width=280,
                                            height=35,
                                            command=page_login)
        self.__register_Button.place(relx=0.19, rely=0.33, anchor=CENTER)
    
    def register_user(self): # A new table "user_[user number]_data" / "...sets" is created -> entry in general table "user"
        
        helptxt = "SELECT EXISTS (SELECT 1 FROM user WHERE name = '" + str(self.__uName_Entry.get()) + "')"
        cursor.execute(helptxt)
        
        if self.__uName_Entry.get() == "" or self.__uPW_Entry.get() == "":
            messagebox.showerror("Finance App", "Username and password must not be blank!") 
            return
        
        elif cursor.fetchone()[0]:
            messagebox.showerror("Finance App", "Username already taken!") 
            return
        
        elif len(self.__uName_Entry.get()) >= 25:
            messagebox.showerror("Finance App", "Username maximum lenght is 25 characters!") 
            return
        
        else:
            cursor.execute("select * from user")
            numbervar = len(cursor.fetchall())
            if numbervar != 0:
                cursor.execute("select id from user where id=(select max(id) from user)")
                numbervar = (cursor.fetchall()[0][0] + 1)
            
            var = (str(numbervar),self.__uName_Entry.get(),self.__uPW_Entry.get(),str("user_" + str(numbervar) + "_data"),str("user_" + str(numbervar) + "_sets"), 0, 0)
            cursor.execute("INSERT INTO user VALUES (?,?,?,?,?,?,?)", var)
            
            connection.commit()
            
            user_id_db = "CREATE TABLE IF NOT EXISTS user_" + str(numbervar) + "_data (id INTEGER PRIMARY KEY, date INTEGER, sum INTEGER, sum_total INTEGER, io INTEGER, kat TEXT, wh TEXT)"
            user_id_set = "CREATE TABLE IF NOT EXISTS user_" + str(numbervar) + "_sets (id INTEGER PRIMARY KEY, cat TEXT)"
            
            cursor.execute(user_id_db)
            connection.commit()
            
            cursor.execute(user_id_set)
            connection.commit()
            
            page_pack_forget()
            window.title('Finance App')
            Main_Screen(window_main, str(numbervar))
            window_main.pack()
            return
    
    def hide(self): # function for password show/hide button
        if self.__uPW_Entry.cget("show") == '':
            self.__uPW_Entry.configure(show='*')
        else:
            self.__uPW_Entry.configure(show='')
        return

######################################################################################################################################################################
##         CLASS  LOGIN
######################################################################################################################################################################

class Login:
    def __init__(self, window):
        self.__window = window
        self.__normal_bg = "#010712"
        
        # Background for the window
        self.__bg_image = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "login_bg.png")), size=(1000 , 500))
        self.__bg_image_label = cTk.CTkLabel(self.__window, image=self.__bg_image, text="")
        self.__bg_image_label.grid(row=0, column=0)
        
        #WELCOME
        self.__heading = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 35, 'bold'),
                                            text="WELCOME",
                                            bg_color=self.__normal_bg)
        self.__heading.place(relx=0.1, rely=0.1, anchor=CENTER)
        
        #LOGIN Username
        self.__uName_Label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text="Username",
                                            bg_color=self.__normal_bg)
        self.__uName_Label.place(relx=0.515, rely=0.23, anchor=CENTER)
        self.__uName_Entry = cTk.CTkEntry(master=self.__window, 
                                            width=450,
                                            height=50,
                                            bg_color=self.__normal_bg,
                                            font=('arial', 20))
        self.__uName_Entry.place(relx=0.7, rely=0.32, anchor=CENTER)
        self.__uName_Canvas = cTk.CTkFrame(master=self.__window,
                                            corner_radius=0,
                                            fg_color="#494996",
                                            bg_color=self.__normal_bg,
                                            height=5,
                                            width=450)
        self.__uName_Canvas.place(relx=0.7, rely=0.365, anchor=CENTER)
        
        #LOGIN Password
        self.__uPW_Label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text="Password",
                                            bg_color=self.__normal_bg)
        self.__uPW_Label.place(relx=0.515, rely=0.43, anchor=CENTER)
        self.__uPW_Entry = cTk.CTkEntry(master=self.__window, 
                                            width=450,
                                            height=50,
                                            show="*",
                                            bg_color=self.__normal_bg,
                                            font=('arial', 20))
        self.__uPW_Entry.place(relx=0.7, rely=0.52, anchor=CENTER)
        self.__uPW_Canvas = cTk.CTkFrame(master=self.__window,
                                            corner_radius=0,
                                            fg_color="#494996",
                                            bg_color=self.__normal_bg,
                                            height=5,
                                            width=450)
        self.__uPW_Canvas.place(relx=0.7, 
                                rely=0.565, 
                                anchor=CENTER)
        
        # LOGIN Button
        self.__login_Button = cTk.CTkButton(master=self.__window,
                                            text="Login",
                                            font=('arial', 20),
                                            fg_color="#494996",
                                            bg_color=self.__normal_bg,
                                            hover_color="#3D3D9A",
                                            corner_radius=10,
                                            width=450,
                                            height=50,
                                            command=self.page_load
                                            )
        self.__login_Button.place(relx=0.7, 
                                rely=0.715, 
                                anchor=CENTER)
        
        # PASSWORD visable
        self.__pwview_image = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "eye-3-xxl.png")), size=(44 , 44))
        self.__uPW_Button = cTk.CTkButton(master=self.__window,
                                            image=self.__pwview_image,
                                            text="",
                                            fg_color='#494996',
                                            bg_color=self.__normal_bg,
                                            corner_radius=0,
                                            width=45,
                                            command=self.hide)
        self.__uPW_Button.place(relx=0.9, 
                                            rely=0.52, 
                                            anchor=CENTER)
        
        # New Account
        self.__register_Label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 20),
                                            text="Not Registered yet?",
                                            bg_color=self.__normal_bg)
        self.__register_Label.place(relx=0.145, 
                            rely=0.25, 
                            anchor=CENTER)
        
        self.__register_Button = cTk.CTkButton(master=self.__window,
                                            text="Register now!",
                                            font=('arial', 20),
                                            fg_color="#00A417",
                                            bg_color=self.__normal_bg,
                                            hover_color="#009017",
                                            corner_radius=5,
                                            width=175,
                                            height=35,
                                            command=page_regis)
        self.__register_Button.place(relx=0.145, 
                                rely=0.33, 
                                anchor=CENTER)
    
    def page_load(self): # load page with user-data if user & password pair exists
        helptxt = "SELECT EXISTS (SELECT 1 FROM user WHERE name = '" + str(self.__uName_Entry.get()) + "' AND password = '" + str(self.__uPW_Entry.get()) + "')"
        cursor.execute(helptxt)
        
        if cursor.fetchone()[0]:
            page_pack_forget()
            window.title('Finance App')
            
            helptxt = "SELECT id FROM user WHERE name='" + str(self.__uName_Entry.get()) + "'"
            cursor.execute(helptxt)
            Main_Screen(window_main, str(cursor.fetchall()[0][0]))
            window_main.pack()
        else:
            messagebox.showerror("Finance App", "Invalid username or password") 
    
    def hide(self): # function for password show/hide button
        if self.__uPW_Entry.cget("show") == '':
            self.__uPW_Entry.configure(show='*')
        else:
            self.__uPW_Entry.configure(show='')
        return

######################################################################################################################################################################
##         CLASS  MAIN_SCREEN
######################################################################################################################################################################

class Main_Screen:
    def __init__(self, window, user):
        self.__window = window
        self.__user = user
        self.__normal_bg = "#010712"
        
        # Background for the window
        self.__bg_image = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "login_bg.png")), size=(1000 , 500))
        self.__bg_image_label = cTk.CTkLabel(self.__window, image=self.__bg_image, text="")
        self.__bg_image_label.grid(row=0, column=0)
        
        # Frames TOP
        self.__top_frame = cTk.CTkFrame(master=self.__window, width=1000, height=175, fg_color="#494996", corner_radius=0)
        self.__top_frame.place(relx=0.5, rely=0, anchor=cTk.CENTER)
        
        # SETTINGS BUTTON
        self.__imgh = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "settings-17-xxl.png")), size=(35, 35))
        self.__button_h = cTk.CTkButton(master=self.__window,
                                            image=self.__imgh,
                                            text="",
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_settings(self.__user, Settings_Screen.set_01))
        self.__button_h.place(relx=0.925, rely=0.1, anchor=cTk.CENTER)
        
        # PLOT BUTTON
        self.__imgp = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "combo-xxl.png")), size=(35, 35))
        self.__button_p = cTk.CTkButton(master=self.__window,
                                            image=self.__imgp,
                                            text=" Analyse",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_plot(self.__user))
        self.__button_p.place(relx=0.740, rely=0.1, anchor=cTk.CENTER)
        
        # HISTORY BUTTON
        self.__imghis = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "database-xxl.png")), size=(35, 35))
        self.__button_his = cTk.CTkButton(master=self.__window,
                                            image=self.__imghis,
                                            text=" History",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=221,
                                            height=60,
                                            command=lambda: page_history(self.__user))
        self.__button_his.place(relx=0.5, rely=0.1, anchor=cTk.CENTER)
        
        # NEW INPUT BUTTON
        self.__imgnew = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "expensive-xxl.png")), size=(50 , 50))
        self.__button_new = cTk.CTkButton(master=self.__window,
                                            image=self.__imgnew,
                                            text=" Income/Expense",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_inout(self.__user))
        self.__button_new.place(relx=0.2, rely=0.1, anchor=cTk.CENTER)
        
        # Greeting TEXT
        helptxt = "SELECT name FROM user WHERE id =" + self.__user + ";"
        cursor.execute(helptxt)
        self.__name = cursor.fetchall()[0][0]
        helptxt = "SELECT sum_total FROM user_" + self.__user + "_data where id=(select max(id) from user_" + self.__user + "_data)"
        cursor.execute(helptxt)
        try:
            self.__balance = cursor.fetchall()[0][0]
            grtxt = "Good day " + str(self.__name) + ", it is a pleasure seeing you\nYour avaiable money is " + f'{self.__balance:.2f}' + " €!"
        except (IndexError, ValueError):
            self.__balance = 0
            grtxt = "Good day " + str(self.__name) + ", it is a pleasure seeing you\nYour account has no amount of money safed at the moment"
        
        
        self.__greeting = cTk.CTkLabel(master=self.__window, text=grtxt, font=("arial", 15), text_color="white", width=350, height=60, fg_color="#3e3e80", bg_color=self.__normal_bg, corner_radius=20)
        self.__greeting.place(relx=0.98, rely=0.25, anchor=cTk.E)
        
        # Frames SLIDER
        self.__bottom_frame = cTk.CTkFrame(master=self.__window, width=100, height=30, fg_color="#494996", corner_radius=20, bg_color=self.__normal_bg)
        self.__bottom_frame.place(relx=0.5, rely=0.95, anchor=cTk.CENTER)
        
        self.__b1_frame = cTk.CTkButton(master=self.__bottom_frame, width=10, height=10, fg_color="white", corner_radius=20, command=self.slide_1, text="")
        self.__b1_frame.place(relx=0.25, rely=0.5, anchor=cTk.CENTER)
        
        self.__b2_frame = cTk.CTkButton(master=self.__bottom_frame, width=10, height=10, fg_color="gray", corner_radius=20, command=self.slide_2, text="")
        self.__b2_frame.place(relx=0.5, rely=0.5, anchor=cTk.CENTER)
        
        self.__b3_frame = cTk.CTkButton(master=self.__bottom_frame, width=10, height=10, fg_color="gray", corner_radius=20, command=self.slide_3, text="")
        self.__b3_frame.place(relx=0.75, rely=0.5, anchor=cTk.CENTER)
        
        # Mid - Frame
        self.__mid = cTk.CTkLabel(master=self.__window, text="Made with python, sqlite and CustomTkinter\napprox. hours coded ... around 35", font=("arial", 35), text_color="white", width=500, height=70, fg_color=self.__normal_bg, bg_color=self.__normal_bg, corner_radius=20)
        self.__mid.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    def slide_1(self): # number 1 of 3 main-screen "infos" showed
        self.__b1_frame.configure(fg_color="white")
        self.__b2_frame.configure(fg_color="gray")
        self.__b3_frame.configure(fg_color="gray")
        self.__mid.configure(text="Made with python, sqlite and CustomTkinter\napprox. hours coded ... around 35")
        return
    
    def slide_2(self): # number 2 of 3 main-screen "infos" showed
        self.__b1_frame.configure(fg_color="gray")
        self.__b2_frame.configure(fg_color="white")
        self.__b3_frame.configure(fg_color="gray")
        self.__mid.configure(text="HIER KÖNNTE IHRE WERBUNG STEHEN :)")
        return
    
    def slide_3(self): # number 3 of 3 main-screen "infos" showed
        self.__b1_frame.configure(fg_color="gray")
        self.__b2_frame.configure(fg_color="gray")
        self.__b3_frame.configure(fg_color="white")
        self.__mid.configure(text="Did you know that it is even possible\nto set a monthly limit to your expenses?\n(Settings > Warnings > Activate Warning)")
        return

######################################################################################################################################################################
##         CLASS  SCROLL SIDE_FRAME
######################################################################################################################################################################
#
#   a special class where all the elements in the various frames are defined
#   these elements are listed as items of a big scrollable frame that filles the main-frame of the class
#
#   elements are:
#       - button, dropdown, slider, calendar, entry for left-sided SIDEFRAMES (parameters to chose paramters of main window-data)
#       - rows (incl. row_lite for simpler list) for central-placed SCROLLFRAMES (intention is to show a table or list)
#

class ScrollSIDE_Frame(cTk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.__user = command # command wird als nicht verwendete Variable von CTkScrollableFrame genutzt, um den user-parameter zu übergeben
        self.__button_list = []
        self.__row_list = []
    
    def add_button(self, item, command, button_image):
        button = cTk.CTkButton(self, text=item, width=230, height=50, font=("Arial", 20), anchor=W, command=command, image=button_image)
        button.grid(row=len(self.__button_list), column=0, columnspan=2, pady=(10, 10), padx=(10,10))
        self.__button_list.append(button)
        return self
    
    def add_button_settings(self, item, user, command, button_image):
        button = cTk.CTkButton(self, text=item, width=230, height=50, font=("Arial", 20), anchor=W, command=lambda: page_settings(user, command), image=button_image)
        button.grid(row=len(self.__button_list), column=0, columnspan=2, pady=(10, 10), padx=(10,10))
        self.__button_list.append(button)
        return self
    
    def add_dropdown(self, command, init_val, val_list):
        self.__box_var = cTk.StringVar(value=init_val)
        buttonbox = cTk.CTkComboBox(self,
                                            width=230, 
                                            height=50, 
                                            font=("Arial", 20),
                                            state="readonly",
                                            command=command,
                                            values=val_list,
                                            variable=self.__box_var,
                                            fg_color="#494996",
                                            button_color="#3e3e80",
                                            border_color="#3e3e80")
        buttonbox.grid(row=len(self.__button_list), column=0, columnspan=2, pady=(10, 10), padx=(10,10))
        
        self.__button_list.append(buttonbox)
        return self
    
    def add_entry(self, variable, placeholder, command):
        entry = cTk.CTkEntry(self, width=160, height=50, corner_radius=0, bg_color="#464696", font=('arial', 15), textvariable=variable)
        entry.grid(row=len(self.__button_list), column=0, pady=(10, 10), padx=(0,0))
        
        img_conf = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "expensive-xxl.png")), size=(40,40))
        conf_entry = cTk.CTkButton(self, text="", width=50, height=50, anchor=W, command=lambda: read_value(entry, variable, command), image=img_conf)
        conf_entry.grid(row=len(self.__button_list), column=1, pady=(10, 10), padx=(0,0))
        ToolTip(conf_entry, msg=placeholder, delay=0, font=("Arial", 25),
        parent_kwargs={"bg": "#494996", "padx": 5, "pady": 5},
        fg="white", bg="#3e3e80", padx=10, pady=10)
        
        self.__button_list.append(entry)
        return
    
    def add_slider(self, command, min, max, text):
        frame = cTk.CTkFrame(master=self, width=10, height=50, fg_color="#464696", corner_radius=10)
        frame.grid(row=len(self.__button_list), column=0, pady=(10,10), padx=(10,10), sticky="ew")
        
        entry = cTk.CTkSlider(frame, width=230, corner_radius=0, button_color="white", command=command, from_=min, to=max, button_length=1)
        entry.grid(row=0, column=0, pady=(10, 10), padx=(0,0))
        
        grid_txt = " " + str(text) + str(entry.get()) + ""
        grid_pos = cTk.CTkLabel(frame, text=grid_txt, font=("Arial", 15), text_color="gray", anchor="e")
        grid_pos.grid(row=1, column=0, padx=(15,5), sticky="ew")
        return
    
    def add_row(self, id, num, io, date, sum, sum_total, cat, repeat):
        row_bg = "#424242"
        
        frameline = cTk.CTkFrame(master=self, width=850, height=50, fg_color=row_bg, corner_radius=0)
        frameline.grid(row=num, column=0, pady=(10,10), padx=(5,5), sticky="ew")
        
        grid_pos0 = cTk.CTkLabel(frameline, text=str(num), font=("Arial", 15), text_color="gray", bg_color=row_bg, height=40, width=20, anchor="e")
        grid_pos0.grid(row=0, column=0, padx=(0,5), sticky="ew")
        
        if io == 0:
            img_io = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "positive-dynamic-xxl.png")), size=(12 , 12))
        else:
            img_io = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "negative-dynamic-xxl.png")), size=(12 , 12))
        grid_pos1 = cTk.CTkLabel(frameline, text="", bg_color=row_bg, height=40, width=20, anchor="e", image=img_io)
        grid_pos1.grid(row=0, column=1, padx=(5,5), sticky="ew")
        
        grid_pos2 = cTk.CTkLabel(frameline, text=str(date), font=("Arial", 15), text_color="gray", bg_color=row_bg, height=40, width=100, anchor="e")
        grid_pos2.grid(row=0, column=2, padx=(5,5), sticky="ew")
        
        if io == 0:
            sum_txt = "" + f'{sum:.2f}' + " "
        else:
            sum_txt = "- " + f'{sum:.2f}' + " "
        img_euro = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "euro-3-xxl.png")), size=(12 , 12))
        grid_pos3 = cTk.CTkLabel(frameline, text=str(sum_txt), font=("Arial", 15), text_color="white", bg_color=row_bg, height=40, width=150, image=img_euro, compound=RIGHT, anchor="e")
        grid_pos3.grid(row=0, column=3, padx=(5,5), sticky="ew")
        
        if cat != "":
            cattxt = "  Category: " + cat
        else:
            cattxt = "  Category: ----"
        grid_pos4 = cTk.CTkLabel(frameline, text=str(cattxt), font=("Arial", 15), text_color="white", bg_color=row_bg, height=40, width=200, anchor="w")
        grid_pos4.grid(row=0, column=4, padx=(5,5), sticky="ew")
        
        grid_pos5 = cTk.CTkLabel(frameline, text=str(repeat), font=("Arial", 15), text_color="gray", bg_color=row_bg, height=40, width=100, anchor="w")
        grid_pos5.grid(row=0, column=5, padx=(5,5), sticky="ew")
        
        img_del = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "delete-xxl.png")), size=(25 , 25))
        button_pos6 = cTk.CTkButton(frameline, text="", width=40, height=40, anchor=W, command=lambda: delete_row(self.__user, id, sum), image=img_del, bg_color=row_bg)
        button_pos6.grid(row=0, column=6, sticky="ew")
        
        sum_total_txt = "Balance: " + f'{sum_total:.2f}' + "€ "
        grid_pos7 = cTk.CTkLabel(frameline, text=str(sum_total_txt), font=("Arial", 15), text_color="gray", bg_color=row_bg, height=20, width=150, anchor="w")
        grid_pos7.grid(row=1, column=4, padx=(5,5), sticky="ew")
        
        self.__row_list.append(frameline)
        return self 
    
    def label(self, item):
        self.add_button(item, None, None)
        for button in self.__button_list:
            try:
                if item == button.cget("text"):
                    button.configure(fg_color='#262626', command=None, font=("Arial", 20, "bold"), text_color='gray', image=None, hover_color='#262626')
            except (ValueError, AttributeError):
                continue # wenn eine combobox in button_list abgearbeitet wird, gibt es kein attribut "text" - ValueError soll einfach ignoriert werden und for fortgeführt werden
        
        return self
    
    def remove_item(self, item):
        for button in self.__button_list:
            if item == button.cget("text"):
                button.destroy()
                self.__button_list.remove(button)
            return self
    
    def add_row_lite(self, id, num, name):
        row_bg = "#424242"
        
        frameline = cTk.CTkFrame(master=self, width=850, height=50, fg_color=row_bg, corner_radius=0)
        frameline.grid(row=num, column=0, pady=(5,5), padx=(5,5), sticky="ew")
        
        grid_pos0 = cTk.CTkLabel(frameline, text=str(num), font=("Arial", 15), text_color="gray", bg_color=row_bg, height=40, width=30, anchor="e")
        grid_pos0.grid(row=0, column=0, padx=(0,5), sticky="ew")
        
        grid_pos1 = cTk.CTkLabel(frameline, text="", font=("Arial", 15), text_color="gray", bg_color=row_bg, height=40, width=150, anchor="e")
        grid_pos1.grid(row=0, column=0, padx=(0,5), sticky="ew")
        
        grid_pos2 = cTk.CTkLabel(frameline, text=str(name), font=("Arial", 15), text_color="white", bg_color=row_bg, height=40, width=500, anchor="w")
        grid_pos2.grid(row=0, column=1, padx=(5,5), sticky="ew")
        
        img_del = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "delete-xxl.png")), size=(25 , 25))
        button_pos6 = cTk.CTkButton(frameline, text="", width=40, height=40, anchor=W, command=lambda: delete_lite_row(self.__user, id, name), image=img_del, bg_color=row_bg)
        button_pos6.grid(row=0, column=2, sticky="ew")
        
        self.__row_list.append(frameline)
        return self 
    
    def add_calandar(self, variable, text, command):
        frame = cTk.CTkFrame(master=self, width=10, height=50, fg_color="#464696", corner_radius=10)
        frame.grid(row=len(self.__button_list), column=0, columnspan=2, pady=(10,10), padx=(10,10), sticky="ew")
        
        calendarview = Calendar(master=frame, 
                                            selectmode="day",
                                            year=datetime.today().year, 
                                            month=datetime.today().month, 
                                            day=datetime.today().day, 
                                            date_pattern="yyyy-mm-dd",
                                            background="#3e3e80",
                                            headersbackground="gray",
                                            weekendbackground="white")
        calendarview.grid(row=0, column=0, sticky="ew")
        
        dateinput_button = cTk.CTkButton(master=frame, 
                                            text=text, 
                                            command=lambda: read_value(calendarview, variable, command), 
                                            width=230, 
                                            height=50, 
                                            corner_radius=0, 
                                            font=("Arial", 20))
        dateinput_button.grid(row=1, column=0, sticky="ew")
        
        self.__button_list.append(calendarview)
        return
    
    def get_checked_items(self):
        return [button.cget("text") for button in self.__button_list if button.get() == 1]

# Function read_value for reading and processing text from input (has to edit some special parameters,
# therefore cannot be defined inside corresponding class "SCROLL SIDE-FRAME")
def read_value(item, output, command):
    try:
        output.set(item.get())
    except AttributeError:
        output.set(item.get_date())
    finally:
        command()
    return

# Function delete_row_lite for deleting simple rows from table of categories (has to edit some special parameters,
# therefore cannot be defined inside corresponding class "SCROLL SIDE-FRAME")
def delete_lite_row(user, item, name):
    helptxt = "Do you really want to delete \"" + str(name) + "\" as category?"
    msg_box = messagebox.askquestion("Finance App", helptxt)
    if msg_box == 'yes':
        helptxt = "DELETE from user_" + str(user) + "_sets where id = " + str(item) + ""
        cursor.execute(helptxt)
        connection.commit()
        
        cursor.execute("select id,cat from user_" + str(user) + "_sets")
        rows = (cursor.fetchall())
        for row in rows:
            helptxt = "UPDATE user_" + str(user) + "_sets SET cat='" + str(row[1]) + "' where id='" + str(row[0]) + "'"
            cursor.execute(helptxt)
            connection.commit()
        
        page_settings(user, Settings_Screen.set_01)
    return

# Function delete_row for deleting rows from table of incomes/expenses (has to edit some special parameters,
# therefore cannot be defined inside corresponding class "SCROLL SIDE-FRAME")
def delete_row(user, item, sum):
    helptxt = "Do you really want to delete " + str(sum) + "€ from your history?"
    msg_box = messagebox.askquestion("Finance App", helptxt)
    if msg_box == 'yes':
        helptxt = "DELETE from user_" + str(user) + "_data where id = " + str(item) + ""
        cursor.execute(helptxt)
        connection.commit()
        
        new_totals = 0
        i = 0
        cursor.execute("select sum,io,id from user_" + str(user) + "_data order by date asc")
        rows = (cursor.fetchall())
        for row in rows:
            if row[1] == 0:
                new_totals += row[0]
            elif row[1] == 1:
                new_totals -= row[0]
            else:
                helptxt = "Error occured while calculating balance from data!\nIncome/Expense says: " + str(row[1]) + " (0: Income, 1: Expense)"
                messagebox.showerror("Finance App - Sqlite", helptxt)
                return
            helptxt = "UPDATE user_" + str(user) + "_data SET sum_total='" + str(new_totals) + "' where id='" + str(row[2]) + "'"
            cursor.execute(helptxt)
            connection.commit()
        
        page_history(user)
    return

######################################################################################################################################################################
##         CLASS  IN OUT_SCREEN
######################################################################################################################################################################

class InOut_Screen:
    def __init__(self, window, user):
        self.__window = window
        self.__user = user
        self.__normal_bg = "#010712"
        self.__calendar_var = cTk.StringVar(value="")
        
        # Background for the window
        self.__bg_image = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "login_bg.png")), size=(1000 , 500))
        self.__bg_image_label = cTk.CTkLabel(self.__window, image=self.__bg_image, text="")
        self.__bg_image_label.grid(row=0, column=0)
        
        # Frames SIDE
        self.__scrollable_checkbox_frame = ScrollSIDE_Frame(master=self.__window, width=250, height=405, command=None)
        self.__scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        self.__scrollable_checkbox_frame.place(relx=0.135, rely=0.585, anchor=cTk.CENTER)
        self.__scrollable_checkbox_frame.add_button("  Income", self.income_scr, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "euro-3-xxl.png")), size=(20 , 20)))
        self.__scrollable_checkbox_frame.add_button("  Expense", self.expense_scr, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "euro-3-xxl.png")), size=(20 , 20)))
        self.__scrollable_checkbox_frame.label("Billing date")
        self.__scrollable_checkbox_frame.add_calandar(self.__calendar_var, "Select Date", self.calendar_var)
        
        # Frames TOP
        self.__top_frame = cTk.CTkFrame(master=self.__window, width=1000, height=175, fg_color="#494996", corner_radius=0)
        self.__top_frame.place(relx=0.5, rely=0, anchor=cTk.CENTER)
        
        # Mittelframe - Arbeitsort                                  ############################################
        self.__mode_inout = 0
        self.__validation = self.__window.register(self.only_numbers)
        
        self.__heading = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 25, 'bold'),
                                            bg_color=self.__normal_bg,
                                            compound=LEFT)
        self.__heading.place(relx=0.32525, rely=0.30, anchor=W)
        self.income_scr()
        
        # Input Sum
        self.__amount_in = cTk.CTkEntry(master=self.__window, 
                                            placeholder_text="Enter the amount here",
                                            width=450,
                                            height=50,
                                            border_color="white",
                                            bg_color=self.__normal_bg,
                                            validate="key", 
                                            validatecommand=(self.__validation, '%S'),
                                            font=('arial', 20))
        self.__amount_in.place(relx=0.55, rely=0.42, anchor=CENTER)
        self.__amount_in_label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 12, 'bold'),
                                            text="Only numbers and '.'-comma allowed as input",
                                            bg_color=self.__normal_bg)
        self.__amount_in_label.place(relx=0.46, rely=0.5, anchor=CENTER)
        
        # Load Categories
        try:
            cursor.execute("select cat from user_" + self.__user + "_sets")
            self.__cats = cursor.fetchall()
        except sqlite3.OperationalError:
            self.__cats = ()
        
        self.__categories = ["no category"]
        for row in self.__cats:
            self.__categories.append(str(row[0]))
        
        # Category
        self.__cat_in_label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text="INTO CATEGORY:",
                                            bg_color=self.__normal_bg)
        self.__cat_in_label.place(relx=0.4, rely=0.58, anchor=CENTER)
        
        self.__cat_in_var = cTk.StringVar(value=self.__categories[0])
        self.__cat_in = cTk.CTkOptionMenu(self.__window,
                                            width=450, 
                                            height=50, 
                                            font=("Arial", 20),
                                            command=None,
                                            values=self.__categories,
                                            variable=self.__cat_in_var,
                                            bg_color=self.__normal_bg,
                                            fg_color="#494996",
                                            button_color="#3e3e80")
        self.__cat_in.place(relx=0.55, rely=0.67, anchor=CENTER)
        
        # Wiederholung
        self.__cat_in_label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text="ROUTINE:",
                                            bg_color=self.__normal_bg)
        self.__cat_in_label.place(relx=0.368, rely=0.78, anchor=CENTER)
        
        self.__optionmenu_var = cTk.StringVar(value="only once")
        self.__optionmenu = cTk.CTkOptionMenu(self.__window,
                                            values=["only once", "every day", "every week", "every month", "every year"],
                                            command=None,
                                            variable=self.__optionmenu_var,
                                            width=450,
                                            height=50,
                                            bg_color=self.__normal_bg,
                                            font=('arial', 20),
                                            fg_color="#494996",
                                            button_color="#3e3e80")
        self.__optionmenu.place(relx=0.55, rely=0.87, anchor=CENTER)
        
        self.__date = date.today()
        self.__imgaccin = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "arrow-53-xxl.png")), size=(50 , 50))
        self.__button_newin = cTk.CTkButton(master=self.__window,
                                            image=self.__imgaccin,
                                            text=" Enter",
                                            font=("Arial",30),
                                            fg_color='#00A417',
                                            bg_color=self.__normal_bg,
                                            text_color="white",
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=self.input_button)        
        self.__button_newin.place(relx=0.89, rely=0.87, anchor=cTk.CENTER)
        
        # INFO regarding AVIABILITY AND PROGNOSES
        # Perspective from date
        self.__date_text = "TODAY"
        self.__date_info = "Seen from date:"
        self.__date_info = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 9),
                                            text=self.__date_info,
                                            bg_color=self.__normal_bg,
                                            text_color="gray")
        self.__date_info.place(relx=0.7825, rely=0.285, anchor=NW)
        self.__date_txt = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 12, "bold"),
                                            text=self.__date_text,
                                            bg_color=self.__normal_bg,
                                            text_color='#00A417')
        self.__date_txt.place(relx=0.7825, rely=0.32, anchor=NW)
        
        # Currently avaiable amount
        cursor.execute("select sum_total from user_" + self.__user + "_data where id=(select max(id) from user_" + self.__user + "_data where date=(select max(date) from user_" + self.__user + "_data where date<='" + str(self.__date) + "'))")
        try:
            self.__balance_var = cursor.fetchall()[0][0]
        except IndexError:
            self.__balance_var = 0
        
        self.__balace_text = "" + f'{self.__balance_var:.2f}' + " €"
        self.__balance_info = "Your currently avaiable amount is:"
        self.__balance_info = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 12),
                                            text=self.__balance_info,
                                            bg_color=self.__normal_bg)
        self.__balance_info.place(relx=0.7825, rely=0.365, anchor=NW)
        self.__balance_txt = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text=self.__balace_text,
                                            bg_color=self.__normal_bg)
        self.__balance_txt.place(relx=0.7825, rely=0.47, anchor=SW)
        
        cursor.execute("select sum_total from user_" + self.__user + "_data where (date=(select max(date) from user_" + self.__user + "_data) and date >'" + str(self.__date) + "')")
        try:
            self.__future_bal = cursor.fetchall()[0][0] - self.__balance_var
        except IndexError:
            self.__future_bal = 0
        
        if self.__future_bal > 0:
            self.__future_color = "#40b000"
        elif self.__future_bal < 0:
            self.__future_color = "#9c0000"
        else:
            self.__future_color = "white"
        
        self.__future_txt = "" + f'{self.__future_bal:.2f}' + " €"
        self.__future_info = "Calculated future additional amount:"
        self.__future_info = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 12),
                                            text=self.__future_info,
                                            bg_color=self.__normal_bg)
        self.__future_info.place(relx=0.7825, rely=0.465, anchor=NW)
        self.__future_txt_label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text=self.__future_txt,
                                            text_color=self.__future_color,
                                            bg_color=self.__normal_bg)
        self.__future_txt_label.place(relx=0.7825, rely=0.57, anchor=SW)
        # ENDE MITTELFRAME                                                  ########################################
        
        # SETTINGS BUTTON
        self.__imgh = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "settings-17-xxl.png")), size=(35, 35))
        self.__button_h = cTk.CTkButton(master=self.__window,
                                            image=self.__imgh,
                                            text="",
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_settings(self.__user, Settings_Screen.set_01))
        self.__button_h.place(relx=0.925, rely=0.1, anchor=cTk.CENTER)
        
        # PLOT BUTTON
        self.__imgp = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "combo-xxl.png")), size=(35, 35))
        self.__button_p = cTk.CTkButton(master=self.__window,
                                            image=self.__imgp,
                                            text=" Analyse",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=233,
                                            height=60,
                                            command=lambda: page_plot(self.__user))
        self.__button_p.place(relx=0.740, rely=0.1, anchor=cTk.CENTER)
        
        # HISTORY BUTTON
        self.__imghis = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "database-xxl.png")), size=(35, 35))
        self.__button_his = cTk.CTkButton(master=self.__window,
                                            image=self.__imghis,
                                            text=" History",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=221,
                                            height=60,
                                            command=lambda: page_history(self.__user))
        self.__button_his.place(relx=0.5, rely=0.1, anchor=cTk.CENTER)
        
        # HOME BUTTON
        self.__imgnew = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "house-xxl.png")), size=(35, 35))
        self.__button_new = cTk.CTkButton(master=self.__window,
                                            image=self.__imgnew,
                                            text="   Home-Screen   ",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_main(self.__user))
        self.__button_new.place(relx=0.2, rely=0.1, anchor=cTk.CENTER)
    
    def only_numbers(self, char): # Checks if input (char) is a number or a '.'
        if char.isdigit() or char == '.':
            return True
        else:
            return False
    
    def calendar_var(self): # when a date is selected in calendar, the avaiable amount of money now and in future is changed to that dates true value
        self.__date = self.__calendar_var.get()
        cursor.execute("select sum_total from user_" + self.__user + "_data where id=(select max(id) from user_" + self.__user + "_data where date=(select max(date) from user_" + self.__user + "_data where date<='" + str(self.__date) + "'))")
        try:
            self.__balance_var = cursor.fetchall()[0][0]
        except IndexError:
            self.__balance_var = 0
        
        bal_txt = "" + f'{self.__balance_var:.2f}' + " €"
        self.__balance_txt.configure(text=bal_txt)
        
        cursor.execute("select sum_total from user_" + self.__user + "_data where (date=(select max(date) from user_" + self.__user + "_data))")
        try:
            self.__future_bal = cursor.fetchall()[0][0] - self.__balance_var
        except IndexError:
            self.__future_bal = 0 - self.__balance_var
        
        if self.__future_bal > 0:
            self.__future_color = "#40b000"
        elif self.__future_bal < 0:
            self.__future_color = "#9c0000"
        else:
            self.__future_color = "white"
        
        fut_txt = "" + f'{self.__future_bal:.2f}' + " €"
        self.__future_txt_label.configure(text=fut_txt)
        
        if datetime.strptime(self.__calendar_var.get(), '%Y-%m-%d').date() == date.today():
            self.__date_txt.configure(text="TODAY")
        else:
            self.__date_txt.configure(text=self.__calendar_var.get())
        return
    
    def income_scr(self): # button to change mode to income
        self.__img_inc = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "positive-dynamic-xxl.png")), size=(30 , 30))
        self.__heading.configure(text="  New income", image=self.__img_inc)
        self.__mode_inout = 0
        return
    
    def expense_scr(self): # button to change mode to expense
        self.__img_exp = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "negative-dynamic-xxl.png")), size=(30 , 30))
        self.__heading.configure(text="  New expense", image=self.__img_exp)
        self.__mode_inout = 1
        return
    
    def input_button(self): # button writing data to database if input is accepted and action is confirmed through pop-up
        if self.__amount_in.get() == '':
            messagebox.showerror("Finance App", "No amount entered!") 
            return
        
        try:
            self.__income = float(self.__amount_in.get())
        except ValueError:
            messagebox.showerror("Finance App", "Amount is not a number!") 
            return
        
        if self.__income > 100000000000.0:
            messagebox.showerror("Finance App", "Maximum input allowed is 100 billon €!") 
            return
        
        modetxt = "" if self.__mode_inout == 0 else "-"
        asktxt = "Do you want to enter the amount of " + modetxt
        
        if self.__cat_in.get() == "no category" and self.__optionmenu_var.get() == "only once":
            info = asktxt + self.__amount_in.get() + "€?"
            msg_box = messagebox.askquestion("Finance App", info)
        elif self.__cat_in.get() == "no category":
            info = asktxt + self.__amount_in.get() + "€?\n Repeat is set " + self.__optionmenu_var.get() + "."
            msg_box = messagebox.askquestion("Finance App", info)
        elif self.__optionmenu_var.get() == "only once":
            info = asktxt + self.__amount_in.get() + "€ to the category \"" + self.__cat_in.get() + "\"?"
            msg_box = messagebox.askquestion("Finance App", info)
        else:
            info = asktxt + self.__amount_in.get() + "€ to the category \"" + self.__cat_in.get() + "\"?\nRepeat is set " + self.__optionmenu_var.get() + "."
            msg_box = messagebox.askquestion("Finance App", info)
        
        if msg_box == 'yes':
            cursor.execute("select * from user_" + self.__user + "_data")
            num = len(cursor.fetchall())
            if num != 0:
                cursor.execute("select id from user_" + self.__user + "_data where id=(select max(id) from user_" + self.__user + "_data)")
                num = (cursor.fetchall()[0][0] + 1)
            
            if self.__mode_inout == 0:
                self.__totals = self.__income
            elif self.__mode_inout == 1:
                self.__totals = 0 - self.__income
            else:
                helptxt = "Error occured while calculating balance from data!\nIncome/Expense says: " + str(self.__mode_inout) + " (0: Income, 1: Expense)"
                messagebox.showerror("Finance App - Sqlite", helptxt)
                return
            
            cursor.execute("select warn_sum from user where id='" + self.__user + "'")
            h1 = 0 - int(cursor.fetchall()[0][0])
            cursor.execute("select warn_zero from user where id='" + self.__user + "'")
            h2 = int(cursor.fetchall()[0][0])
            cursor.execute("select sum_total from user_" + self.__user + "_data where date='" + str(date.today() - timedelta(days=30)) + "'")
            try:
                balance_month = int(cursor.fetchall()[0][0]) - self.__totals
            except IndexError:
                balance_month = 0 + self.__totals
            
            if h2 != 0 and self.__totals < 0 and self.__mode_inout == 1:
                helptxt = "Your total balance is below your declared minimum!\nThe transaction cannot be processed"
                messagebox.showwarning("Finance App", helptxt)
                return
            
            if h2 != 0 and (h1 > balance_month and h1 != 0) and self.__mode_inout == 1:
                helptxt = "Your expenses are beyond your declared maximum!\nThe transaction cannot be processed"
                messagebox.showwarning("Finance App", helptxt)
                return
            
            var = (num, self.__date, self.__amount_in.get(), self.__totals, self.__mode_inout, self.__cat_in.get(), self.__optionmenu_var.get())
            helptxt = "INSERT INTO user_" + self.__user + "_data VALUES (?,?,?,?,?,?,?)"
            cursor.execute(helptxt, var)
            
            connection.commit()
            
            new_totals = 0
            i = 0
            cursor.execute("select sum,io,id from user_" + str(self.__user) + "_data order by date asc")
            rows = (cursor.fetchall())
            for row in rows:
                if row[1] == 0:
                    new_totals += row[0]
                elif row[1] == 1:
                    new_totals -= row[0]
                else:
                    helptxt = "Error occured while calculating balance from data!\nIncome/Expense says: " + str(row[1]) + " (0: Income, 1: Expense)"
                    messagebox.showerror("Finance App - Sqlite", helptxt)
                    return
                helptxt = "UPDATE user_" + str(self.__user) + "_data SET sum_total='" + str(new_totals) + "' where id='" + str(row[2]) + "'"
                cursor.execute(helptxt)
                connection.commit()
            
            page_inout(self.__user)
        return

######################################################################################################################################################################
##         CLASS  PLOT_SCREEN
######################################################################################################################################################################

class Plot_Screen:
    def __init__(self, window, user):
        self.__window = window
        self.__user = user
        self.__calendar_var1 = cTk.StringVar(value="")
        self.__calendar_var2 = cTk.StringVar(value="")
        
        # Background for the window
        self.__bg_image = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "login_bg.png")), size=(1000 , 500))
        self.__bg_image_label = cTk.CTkLabel(self.__window, image=self.__bg_image, text="")
        self.__bg_image_label.grid(row=0, column=0)
        
        # Frames SIDE
        self.__scrollable_filter_frame = ScrollSIDE_Frame(master=self.__window, width=250, height=405, command=None)
        self.__scrollable_filter_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        self.__scrollable_filter_frame.place(relx=0.135, rely=0.585, anchor=cTk.CENTER)
        
        # Load Categories
        try:
            cursor.execute("select cat from user_" + self.__user + "_sets")
            self.__cats = cursor.fetchall()
        except sqlite3.OperationalError:
            self.__cats = ()
        
        self.__categories = []
        for row in self.__cats:
            self.__categories.append(str(row[0]))
        
        if len(self.__categories) < 1:
            self.__categories.append("Category")
        
        # Configure sideframe
        self.__scrollable_filter_frame.label("Filter input")
        self.__scrollable_filter_frame.add_button("  Balance", self.no_filter, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "activity-feed-xxl.png")), size=(20 , 20)))
        self.__scrollable_filter_frame.add_button("  All individual sums", self.no_filter_sum, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "activity-feed-xxl.png")), size=(20 , 20)))
        self.__scrollable_filter_frame.add_button("  Indivdual incomes", self.income_filter_sum, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "positive-dynamic-xxl.png")), size=(20 , 20)))
        self.__scrollable_filter_frame.add_button("  Income balance", self.income_filter, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "positive-dynamic-xxl.png")), size=(20 , 20)))
        self.__scrollable_filter_frame.add_button("  Indivdual expenses", self.expense_filter_sum, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "negative-dynamic-xxl.png")), size=(20 , 20)))
        self.__scrollable_filter_frame.add_button("  Expense balance", self.expense_filter, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "negative-dynamic-xxl.png")), size=(20 , 20)))
        self.__scrollable_filter_frame.label("Repeat")
        self.__scrollable_filter_frame.add_dropdown(self.repeat_filter, "only once", ["only once", "every day", "every week", "every month", "every year"])
        self.__scrollable_filter_frame.label("Category")
        self.__scrollable_filter_frame.add_dropdown(self.category_filter_sum, self.__categories[0], self.__categories)
        self.__scrollable_filter_frame.label("Category balance")
        self.__scrollable_filter_frame.add_dropdown(self.category_filter, self.__categories[0], self.__categories)
        self.__scrollable_filter_frame.label("Date")
        self.__scrollable_filter_frame.add_calandar(self.__calendar_var1, "Select target date", self.date_filter)
        self.__scrollable_filter_frame.add_calandar(self.__calendar_var2, "Select range to that date", self.date_filter)
        
        # Frames TOP 
        self.__top_frame = cTk.CTkFrame(master=self.__window, width=1000, height=175, fg_color="#494996", corner_radius=0)
        self.__top_frame.place(relx=0.5, rely=0, anchor=cTk.CENTER)
        
        # Mainframe - PLOT
        self.no_filter()
        
        # SETTINGS BUTTON
        self.__imgh = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "settings-17-xxl.png")), size=(35, 35))
        self.__button_h = cTk.CTkButton(master=self.__window,
                                            image=self.__imgh,
                                            text="",
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_settings(self.__user, Settings_Screen.set_01))
        self.__button_h.place(relx=0.925, rely=0.1, anchor=cTk.CENTER)
        
        # HISTORY BUTTON
        self.__imghis = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "database-xxl.png")), size=(35, 35))
        self.__button_his = cTk.CTkButton(master=self.__window,
                                            image=self.__imghis,
                                            text=" History",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=221,
                                            height=60,
                                            command=lambda: page_history(self.__user))
        self.__button_his.place(relx=0.5, rely=0.1, anchor=cTk.CENTER)
        
        # INOUT BUTTON
        self.__imgp = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "expensive-xxl.png")), size=(50 , 50))
        self.__button_p = cTk.CTkButton(master=self.__window,
                                            image=self.__imgp,
                                            text="  In/Exp ",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=233,
                                            height=60,
                                            command=lambda: page_inout(self.__user))
        self.__button_p.place(relx=0.740, rely=0.1, anchor=cTk.CENTER)
        
        # HOME BUTTON
        self.__imgnew = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "house-xxl.png")), size=(35, 35))
        self.__button_new = cTk.CTkButton(master=self.__window,
                                            image=self.__imgnew,
                                            text="   Home-Screen   ",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_main(self.__user))
        self.__button_new.place(relx=0.2, rely=0.1, anchor=cTk.CENTER)
    
    def plot(self, xx, yy): # draws final plot from processed data on main frame
        xx = pd.to_datetime(xx)
        DF = pd.DataFrame()
        DF['value'] = yy
        DF = DF.set_index(xx)
        
        fig = Figure(figsize=(15, 8), dpi=105)
        fig.add_subplot(111).plot(DF, "", DF, "ro")
        
        canvas = FigureCanvasTkAgg(fig, master=self.__window)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.664, rely=0.5945, anchor=cTk.CENTER)
        return
    
    def filter_cats(self, xx, yy, plotdata, startzero): # processing data from database for further plot-function (ordering datapoints)
        i = 0
        for row in plotdata:
            try:
                if row[1] == xx[i-1]:
                    try:
                        if row[2] == 0:
                            yy[i-1] += row[0]
                        elif row[2] == 1:
                            yy[i-1] -= row[0]
                        else:
                            messagebox.showerror("Finance App","An Error occured while calculating data for plot!")
                    except IndexError:
                        yy[i-1] += row[0]
                else:
                    yy.append(row[0] + yy[i-1])
                    xx.append((row[1]))
                    i += 1
            
            except IndexError:
                if startzero == 1:
                    cursor.execute("select date from user_" + self.__user + "_data where date=(select min(date) from user_" + self.__user + "_data)")
                    date_zero = datetime.strptime(cursor.fetchall()[0][0], '%Y-%m-%d').date() - timedelta(days=1)
                    yy.append(0)
                    xx.append(date_zero)
                else:
                    yy.append(row[0])
                    xx.append((row[1]))
                i += 1
        
        self.plot(xx, yy)
        return
    
    def filter_cats_sum(self, xx, yy, plotdata): # processing data from database for further plot-function (summing up single datapoints)
        i = 0
        
        for row in plotdata:
            try:
                if row[1] == xx[i-1]:
                    try:
                        if row[0] > yy[i-1]:
                            yy[i-1] = row[0]
                        elif row[0] <= yy[i-1]:
                            None
                        else:
                            messagebox.showerror("Finance App","An Error occured while calculating data for plot!")
                    except IndexError:
                        yy[i-1] = yy[i-1] + row[0]
                else:
                    yy.append(row[0])
                    xx.append((row[1]))
                    i += 1
            
            except IndexError:
                yy.append(row[0])
                xx.append((row[1]))
                i += 1
        
        self.plot(xx, yy)
        return
    
    def no_filter(self): # load data from database for processing through filter-sum (just balances from db)
        xx = []
        yy = []
        
        cursor.execute("select sum_total,date,io from user_" + self.__user + "_data order by date asc")
        plotdata = cursor.fetchall()
        
        self.filter_cats_sum(xx, yy, plotdata)
        return
    
    def no_filter_sum(self): # load data from database for plot (just balances from db)
        xx = []
        yy = []
        
        cursor.execute("select sum,date,io from user_" + self.__user + "_data order by date asc")
        plotdata = cursor.fetchall()
        
        i = 0
        for row in plotdata:
            try:
                if row[1] == xx[i-1]:
                    try:
                        if row[2] == 0:
                            yy[i-1] += row[0]
                        elif row[2] == 1:
                            yy[i-1] -= row[0]
                        else:
                            messagebox.showerror("Finance App","An Error occured while calculating data for plot!")
                    except IndexError:
                        yy[i-1] += row[0]
                else:
                    if row[2] == 0:
                        yy.append(row[0])
                        xx.append((row[1]))
                    elif row[2] == 1:
                        yy.append(-row[0])
                        xx.append((row[1]))
                    else:
                        messagebox.showerror("Finance App","An Error occured while calculating data for plot!")
                    
                    i += 1
            
            except IndexError:
                yy.append(row[0])
                xx.append((row[1]))
                i += 1
        
        self.plot(xx, yy)
        return
    
    def income_filter(self): # load data from database for processing through filter (just incomes from db)
        xx = []
        yy = []
        
        cursor.execute("select sum,date from user_" + self.__user + "_data where io='0' order by date asc")
        plotdata = cursor.fetchall()
        
        self.filter_cats(xx, yy, plotdata, 1)
        return
    
    def income_filter_sum(self): # load data from database for processing through filter-sum (just incomes from db)
        xx = []
        yy = []
        
        cursor.execute("select sum,date from user_" + self.__user + "_data where io='0' order by date asc")
        plotdata = cursor.fetchall()
        
        self.filter_cats_sum(xx, yy, plotdata)
        return
    
    def expense_filter(self): # load data from database for processing through filter (just expenses from db)
        xx = []
        yy = []
        
        cursor.execute("select sum,date from user_" + self.__user + "_data where io='1' order by date asc")
        plotdata = cursor.fetchall()
        
        self.filter_cats(xx, yy, plotdata, 1)
        return
    
    def expense_filter_sum(self): # load data from database for processing through filter-sum (just expenses from db)
        xx = []
        yy = []
        
        cursor.execute("select sum,date from user_" + self.__user + "_data where io='1' order by date asc")
        plotdata = cursor.fetchall()
        
        self.filter_cats_sum(xx, yy, plotdata)
        return
    
    def category_filter(self, category): # load data from database for processing through filter (balances by category from db)
        xx = []
        yy = []
        
        cursor.execute("select sum,date,io from user_" + self.__user + "_data where kat='" + str(category) + "'")
        plotdata = cursor.fetchall()
        
        self.filter_cats(xx, yy, plotdata, 0)
        return
    
    def category_filter_sum(self, category): # load data from database for processing through filter-sum (balances by category from db)
        xx = []
        yy = []
        
        cursor.execute("select sum,date,io from user_" + self.__user + "_data where kat='" + str(category) + "'")
        plotdata = cursor.fetchall()
        
        self.filter_cats_sum(xx, yy, plotdata)
        return
    
    def repeat_filter(self, repeat): # load data from database for processing through filter-sum (balances by repeat-value from db)
        xx = []
        yy = []
        
        cursor.execute("select sum,date,io from user_" + self.__user + "_data where wh='" + str(repeat) + "' order by date asc")
        plotdata = cursor.fetchall()
        
        self.filter_cats_sum(xx, yy, plotdata)
        return
    
    def date_filter(self): # load data from database for processing through filter-sum (balances by date from db)
        date = self.__calendar_var1.get()
        enddate = self.__calendar_var2.get()
        
        try:
            if date != "" and enddate == "":
                xx = []
                yy = []
                cursor.execute("select sum_total,date,io from user_" + self.__user + "_data where date='" + str(date) + "' order by date asc")
                plotdata = cursor.fetchall()
            
            elif date != "" and enddate != "" and date < enddate:
                xx = []
                yy = []
                cursor.execute("select sum_total,date,io from user_" + self.__user + "_data where (date>='" + str(date) + "' and date<='" + str(enddate) + "') order by date asc")
                plotdata = cursor.fetchall()
            
            elif date != "" and enddate != "" and date >= enddate:
                xx = []
                yy = []
                cursor.execute("select sum_total,date,io from user_" + self.__user + "_data where (date>='" + str(date) + "' and date<='" + str(enddate) + "') order by date asc")
                plotdata = cursor.fetchall()
            
            else:
                messagebox.showerror("Finance App", "Not possible to load selected dates.\nAre you sure you selected a date?")
                return
        
        except (ValueError, AttributeError):
            messagebox.showerror("Finance App", "Date value may not be ok: " + str(date) + str(enddate))
            return
        
        self.filter_cats_sum(xx, yy, plotdata)
        return

######################################################################################################################################################################
##         CLASS  HISTORY_SCREEN
######################################################################################################################################################################

class History_Screen:
    def __init__(self, window, user):
        self.__window = window
        self.__user = user  
        self.__calendar_var1 = cTk.StringVar(value="")
        self.__calendar_var2 = cTk.StringVar(value="")
        self.__amount_var1 = cTk.StringVar(value="")
        self.__amount_var2 = cTk.StringVar(value="")
        
        # Background for the window
        self.__bg_image = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "login_bg.png")), size=(1000 , 500))
        self.__bg_image_label = cTk.CTkLabel(self.__window, image=self.__bg_image, text="")
        self.__bg_image_label.grid(row=0, column=0)
        
        # Frames SIDE 
        self.__scrollable_filter_frame = ScrollSIDE_Frame(master=self.__window, width=250, height=405, command=None)
        self.__scrollable_filter_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        self.__scrollable_filter_frame.place(relx=0.135, rely=0.585, anchor=cTk.CENTER)
        
        # Load Categories
        try:
            cursor.execute("select cat from user_" + self.__user + "_sets")
            self.__cats = cursor.fetchall()
        except sqlite3.OperationalError:
            self.__cats = ()
        
        self.__categories = []
        for row in self.__cats:
            self.__categories.append(str(row[0]))
        
        if len(self.__categories) < 1:
            self.__categories.append("Category")
        
        # Configure sideframe
        self.__scrollable_filter_frame.label("Filter input")
        self.__scrollable_filter_frame.add_button("  All", self.no_filter, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "activity-feed-xxl.png")), size=(20 , 20)))
        self.__scrollable_filter_frame.add_button("  Income", self.income_filter, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "positive-dynamic-xxl.png")), size=(20 , 20)))
        self.__scrollable_filter_frame.add_button("  Expense", self.expense_filter, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "negative-dynamic-xxl.png")), size=(20 , 20)))
        self.__scrollable_filter_frame.label("Repeat")
        self.__scrollable_filter_frame.add_dropdown(self.repeat_filter, "only once", ["only once", "every day", "every week", "every month", "every year"])
        self.__scrollable_filter_frame.label("Category")
        self.__scrollable_filter_frame.add_dropdown(self.category_filter, self.__categories[0], self.__categories)
        self.__scrollable_filter_frame.label("Date")
        self.__scrollable_filter_frame.add_calandar(self.__calendar_var1, "Select target date", self.date_filter)
        self.__scrollable_filter_frame.add_calandar(self.__calendar_var2, "Select range to that date", self.date_filter)
        self.__scrollable_filter_frame.label("Amount   Min/Max")
        self.__scrollable_filter_frame.add_entry(self.__amount_var1, "Search exact amount\n(note: only unsigned numbers)", self.sum_filter)
        self.__scrollable_filter_frame.add_entry(self.__amount_var2, "Search for amount in range\n(note: only unsigned numbers)", self.sumrange_filter)
        
        # Frames TOP 
        self.__top_frame = cTk.CTkFrame(master=self.__window, width=1000, height=175, fg_color="#494996", corner_radius=0)
        self.__top_frame.place(relx=0.5, rely=0, anchor=cTk.CENTER)
        
        # Mainframe - HISTORY
        self.no_filter()
        
        # SETTINGS BUTTON
        self.__imgh = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "settings-17-xxl.png")), size=(35, 35))
        self.__button_h = cTk.CTkButton(master=self.__window,
                                            image=self.__imgh,
                                            text="",
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_settings(self.__user, Settings_Screen.set_01))
        self.__button_h.place(relx=0.925, rely=0.1, anchor=cTk.CENTER)
        
        # PLOT BUTTON
        self.__imgp = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "combo-xxl.png")), size=(35, 35))
        self.__button_p = cTk.CTkButton(master=self.__window,
                                            image=self.__imgp,
                                            text=" Analyse",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=223,
                                            height=60,
                                            command=lambda: page_plot(self.__user))
        self.__button_p.place(relx=0.740, rely=0.1, anchor=cTk.CENTER)
        
        # INOUT BUTTON
        self.__imghis = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "expensive-xxl.png")), size=(50 , 50))
        self.__button_his = cTk.CTkButton(master=self.__window,
                                            image=self.__imghis,
                                            text=" In/Exp",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=221,
                                            height=60,
                                            command=lambda: page_inout(self.__user))
        self.__button_his.place(relx=0.5, rely=0.1, anchor=cTk.CENTER)
        
        # HOME BUTTON
        self.__imgnew = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "house-xxl.png")), size=(35, 35))
        self.__button_new = cTk.CTkButton(master=self.__window,
                                            image=self.__imgnew,
                                            text="   Home-Screen   ",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_main(self.__user))
        self.__button_new.place(relx=0.2, rely=0.1, anchor=cTk.CENTER)
    
    def balance_info(self): # shows total balance in window (final position is not defined yet)
        cursor.execute("select * from user_" + self.__user + "_data")
        self.__balance_info = len(cursor.fetchall())
        if self.__balance_info != 0:
            cursor.execute("select sum_total from user_" + self.__user + "_data where id=(select max(id) from user_" + self.__user + "_data)")
            self.__balance_info = (cursor.fetchall()[0][0] + 1)
        
        self.__info_txt = "End balance: " + str(f'{self.__balance_info:.2f}') +  "€"
        self.__info_but = cTk.CTkButton(master=self.__window,
                                            text=self.__info_txt,
                                            font=('arial', 20),
                                            fg_color="#00A417",
                                            bg_color="#313166",
                                            hover_color="#009017",
                                            corner_radius=10,
                                            width=150,
                                            height=50,
                                            command=None)
        self.__info_but.place(relx=0.95, rely=0.9, anchor=cTk.E)
    
    def load_table(self, records): # loads table from SCROLL SIDE_FRAME as rows from "records"
        try:
            self.__scrollable_table_frame.destroy()
        except AttributeError:
            None
        
        finally:
            self.__scrollable_table_frame = ScrollSIDE_Frame(master=self.__window, width=713, height=413, command=self.__user, fg_color='#313166', corner_radius=0)
            self.__scrollable_table_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
            self.__scrollable_table_frame.place(relx=0.635, rely=0.5875, anchor=cTk.CENTER)
            
            self.__i = 1
            for row in records:
                self.__scrollable_table_frame.add_row(num=self.__i,
                                            id=row[0],
                                            io=row[4], #in oder out
                                            date=row[1], 
                                            sum=row[2], 
                                            sum_total=row[3],
                                            cat=row[5], 
                                            repeat=row[6])
                self.__i += 1
            return
    
    def no_filter(self): # load data from database for transfer to table (everything from db / order by date)
        cursor.execute("select * from user_" + self.__user + "_data order by date asc")
        records = cursor.fetchall()
        self.load_table(records)
        return
    
    def income_filter(self): # load data from database for transfer to table (just incomes from db / order by date)
        cursor.execute("select * from user_" + self.__user + "_data where io ='0' order by date asc")
        records = cursor.fetchall()
        self.load_table(records)
        return
    
    def expense_filter(self): # load data from database for transfer to table (just expenses from db / order by date)
        cursor.execute("select * from user_" + self.__user + "_data where io='1' order by date asc")
        records = cursor.fetchall()
        self.load_table(records)
        return
    
    def category_filter(self, category): # load data from database for transfer to table (everything of a category from db / order by date)
        helptxt = "select * from user_" + self.__user + "_data where kat='" + str(category) + "' order by date asc"
        cursor.execute(helptxt)
        records = cursor.fetchall()
        self.load_table(records)
        return
    
    def repeat_filter(self, repeat): # load data from database for transfer to table (everything of a repeat from db / order by date)
        cursor.execute("select * from user_" + self.__user + "_data where wh='" + str(repeat) + "' order by date asc")
        records = cursor.fetchall()
        self.load_table(records)
        return
    
    def sum_filter(self): # load data from database for transfer to table (everything with a sum from db / order by date)
        try: 
            sum = float(self.__amount_var1.get())
            cursor.execute("select * from user_" + self.__user + "_data where sum='" + str(sum) + "' order by date asc")
            records = cursor.fetchall()
            self.load_table(records)
        except ValueError:
            messagebox.showerror("Finance App", "Not possible to load selected amount.\nAre you sure you entered a number?")
        return
    
    def sumrange_filter(self): # load data from database for transfer to table (everything in a sum range from db / order by date)
        try: 
            sum = float(self.__amount_var1.get())
        except ValueError:
            sum = None
        
        try:
            endsum = float(self.__amount_var2.get())
        except ValueError:
            endsum = None
        
        if sum == None and endsum != None:
            cursor.execute("select * from user_" + self.__user + "_data where sum<='" + str(endsum) + "' order by date asc")
        elif endsum == None and sum != None:
            cursor.execute("select * from user_" + self.__user + "_data where sum>='" + str(sum) + "' order by date asc")
        elif endsum == None and sum == None:
            messagebox.showerror("Finance App", "Not possible to load selected amount.\nAre you sure you entered a number?")
            return
        elif sum < endsum:
            cursor.execute("select * from user_" + self.__user + "_data where (sum>='" + str(sum) + "' and sum<='" + str(endsum) + "') order by date asc")
        elif sum >= endsum:
            cursor.execute("select * from user_" + self.__user + "_data where (sum>='" + str(sum) + "' and sum<='" + str(endsum) + "') order by date asc")
        else:
            messagebox.showerror("Finance App", "Not possible to load selected amount.\nAre you sure you entered a number?")
            return
        
        records = cursor.fetchall()
        self.load_table(records)
        return
    
    def date_filter(self): # load data from database for transfer to table (everything at a date or date range from db / order by date)
        date = self.__calendar_var1.get()
        enddate = self.__calendar_var2.get()
        
        try:
            if date != "" and enddate == "":
                cursor.execute("select * from user_" + self.__user + "_data where date='" + str(date) + "' order by date asc")
            elif date != "" and enddate != "" and date < enddate:
                cursor.execute("select * from user_" + self.__user + "_data where (date>='" + str(date) + "' and date<='" + str(enddate) + "') order by date asc")
            elif date != "" and enddate != "" and date >= enddate:
                cursor.execute("select * from user_" + self.__user + "_data where (date>='" + str(date) + "' and date<='" + str(enddate) + "') order by date asc")
            else:
                messagebox.showerror("Finance App", "Not possible to load selected dates.\nAre you sure you selected a date?")
                return
            
            records = cursor.fetchall()
            self.load_table(records)
        
        except (ValueError, AttributeError):
            messagebox.showerror("Finance App", "Date value may not be ok: " + str(date) + str(enddate))
        return

######################################################################################################################################################################
##         CLASS  SETTINGS_SCREEN
######################################################################################################################################################################

class Settings_Screen:
    def __init__(self, window, user, command):
        self.__window = window
        self.__user = user
        self.__normal_bg = "#010712"
        
        # Background for the window
        self.__bg_image = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "login_bg.png")), size=(1000 , 500))
        self.__bg_image_label = cTk.CTkLabel(self.__window, image=self.__bg_image, text="")
        self.__bg_image_label.grid(row=0, column=0)
        
        # Frames SIDE
        self.__scrollable_checkbox_frame = ScrollSIDE_Frame(master=self.__window, width=250, height=405, command=None)
        self.__scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        self.__scrollable_checkbox_frame.place(relx=0.135, rely=0.585, anchor=cTk.CENTER)
        
        # Frames TOP 
        self.__top_frame = cTk.CTkFrame(master=self.__window, width=1000, height=175, fg_color="#494996", corner_radius=0)
        self.__top_frame.place(relx=0.5, rely=0, anchor=cTk.CENTER)
        
        # SETTINGS
        self.__scrollable_checkbox_frame.label("General") # hier einbauen, dass bei klick window neu geladen wird und dann der zugehörige teil in den set_##
        self.__scrollable_checkbox_frame.add_button_settings(" Help", self.__user, Settings_Screen.set_01, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "help-xxl.png")), size=(20 , 20)))
        self.__scrollable_checkbox_frame.add_button_settings(" Categories", self.__user, Settings_Screen.set_02, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "activity-feed-xxl.png")), size=(20 , 20)))
        self.__scrollable_checkbox_frame.add_button_settings(" Warnings", self.__user, Settings_Screen.set_03, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "warning-5-xxl.png")), size=(20 , 20)))
        self.__scrollable_checkbox_frame.add_button_settings(" Credits", self.__user, Settings_Screen.set_04, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "organization-xxl.png")), size=(20 , 20)))
        self.__scrollable_checkbox_frame.label(" Account")
        self.__scrollable_checkbox_frame.add_button_settings(" My Data", self.__user, Settings_Screen.set_05, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "user-xxl.png")), size=(20 , 20)))
        self.__scrollable_checkbox_frame.add_button_settings(" Change Data", self.__user, Settings_Screen.set_06, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "align-bottom-xxl.png")), size=(20 , 20)))
        self.__scrollable_checkbox_frame.add_button_settings(" Logout", self.__user, Settings_Screen.set_07, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "close-window-xxl.png")), size=(20 , 20)))
        self.__scrollable_checkbox_frame.label(" Developer Options")
        self.__scrollable_checkbox_frame.add_button_settings(" Delete Database", self.__user, Settings_Screen.set_08, cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "database-xxl.png")), size=(20 , 20)))
        
        # Mainframe
        command(self)
        
        # INFO LINE
        self.__imgh = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "building-xxl.png")), size=(50 , 50))
        self.__button_h = cTk.CTkLabel(master=self.__window,
                                            image=self.__imgh,
                                            text="         Finance App by Philip Biechl\nFH Vorarlberg - Python",
                                            font=("Arial", 25),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            corner_radius=30,
                                            compound=LEFT,
                                            width=550)
        self.__button_h.place(relx=0.7, rely=0.1, anchor=cTk.CENTER)
        
        
        # HOME BUTTON
        self.__imgnew = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "house-xxl.png")), size=(35, 35))
        self.__button_new = cTk.CTkButton(master=self.__window,
                                            image=self.__imgnew,
                                            text="   Home-Screen   ",
                                            font=("Arial",30),
                                            fg_color='#3e3e80',
                                            bg_color='#494996',
                                            text_color="white",
                                            corner_radius=30,
                                            width=50,
                                            height=60,
                                            command=lambda: page_main(self.__user))
        self.__button_new.place(relx=0.2, rely=0.1, anchor=cTk.CENTER)
    
    def set_01(self, notable=None): # HELP text
        self.__help_label = cTk.CTkLabel(self.__window, text="Help", font=("Arial", 35), bg_color=self.__normal_bg)
        self.__help_label.place(relx=0.3, rely=0.25, anchor=cTk.W)
        self.__help_label = cTk.CTkLabel(self.__window, text="This is how a help-text may look like.\nHowever, you will not find any help here\nWish you a nice day ;)", font=("Arial", 20), bg_color=self.__normal_bg)
        self.__help_label.place(relx=0.3, rely=0.45, anchor=cTk.W)
        return
    
    def set_02(self): # Category management
        self.__cat_label = cTk.CTkLabel(self.__window, text="Categories", font=("Arial", 35), bg_color=self.__normal_bg)
        self.__cat_label.place(relx=0.3, rely=0.25, anchor=cTk.W)
        
        try:
            self.__scrollable_table_frame.destroy()
        except AttributeError:
            None
        
        finally:
            self.__scrollable_table_frame = ScrollSIDE_Frame(master=self.__window, width=713, height=225, command=self.__user, fg_color='#313166', corner_radius=0)
            self.__scrollable_table_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
            self.__scrollable_table_frame.place(relx=0.635, rely=0.55, anchor=cTk.CENTER)
            
            try:
                cursor.execute("select id,cat from user_" + self.__user + "_sets")
                self.__records = cursor.fetchall()
            except sqlite3.OperationalError:
                self.__records = ()
            
            self.__j = 1
            for row in self.__records:
                self.__scrollable_table_frame.add_row_lite(num=self.__j,
                                                        id=row[0],
                                                        name=row[1])
                self.__j += 1
        
        self.__text_cat = cTk.CTkEntry(master=self.__window,
                                            font=('arial', 15),
                                            bg_color=self.__normal_bg,
                                            corner_radius=10,
                                            width=500,
                                            height=50)
        self.__text_cat.place(relx=0.3, rely=0.9, anchor=cTk.W)
        self.__img_add = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "plus-8-xxl.png")), size=(20 , 20))
        self.__add_cat = cTk.CTkButton(master=self.__window,
                                            text="  Add",
                                            image=self.__img_add,
                                            font=('arial', 20),
                                            fg_color="#00A417",
                                            bg_color=self.__normal_bg,
                                            hover_color="#009017",
                                            corner_radius=10,
                                            width=150,
                                            height=50,
                                            command=self.add_cat)
        self.__add_cat.place(relx=0.98, rely=0.9, anchor=cTk.E)
        self.__add_stdcat = cTk.CTkButton(master=self.__window,
                                            text="Add standard categories",
                                            font=('arial', 20),
                                            fg_color="#00A417",
                                            bg_color=self.__normal_bg,
                                            hover_color="#009017",
                                            corner_radius=10,
                                            width=150,
                                            height=50,
                                            command=self.add_stdcats)
        self.__add_stdcat.place(relx=0.98, rely=0.25, anchor=cTk.E)
        return
    
    def set_03(self): # Warnings
        self.__in_str = cTk.StringVar(value="")
        
        cursor.execute("select warn_zero from user where id='" + self.__user + "'")
        warn_zero = int(cursor.fetchone()[0])
        
        if warn_zero == 0:
            self.__activate_warning_zero = cTk.CTkButton(master=self.__window,
                                            text=" Activate Warning when Budget is below 0",
                                            font=('arial', 25),
                                            fg_color="gray",
                                            bg_color=self.__normal_bg,
                                            corner_radius=10,
                                            width=625,
                                            height=50,
                                            command=self.in_warning_zero)
            self.__activate_warning_zero.place(relx=0.325, rely=0.25, anchor=cTk.W)
        else:
            self.__activate_warning_zero = cTk.CTkButton(master=self.__window,
                                            text=" Deactivate Warning when Budget is below 0",
                                            font=('arial', 25),
                                            fg_color="#00A417",
                                            bg_color=self.__normal_bg,
                                            corner_radius=10,
                                            width=625,
                                            height=50,
                                            command=self.out_warning_zero)
            self.__activate_warning_zero.place(relx=0.325, rely=0.25, anchor=cTk.W)
        
        cursor.execute("select warn_sum from user where id='" + self.__user + "'")
        warn_sum = int(cursor.fetchone()[0])
        if warn_sum == 0:
            self.__activate_warning_sum = cTk.CTkButton(master=self.__window,
                                            text=" Activate Warning (Amount spent per month)",
                                            font=('arial', 25),
                                            fg_color="gray",
                                            bg_color=self.__normal_bg,
                                            corner_radius=10,
                                            width=625,
                                            height=50,
                                            command=self.in_warning_sum)
            self.__activate_warning_sum.place(relx=0.325, rely=0.375, anchor=cTk.W)
        else:
            self.__in_str = cTk.StringVar(value=str(warn_sum))
            self.__activate_warning_sum = cTk.CTkButton(master=self.__window,
                                            text=" Deactivate Warning (Amount spent per month)",
                                            font=('arial', 25),
                                            fg_color="#00A417",
                                            bg_color=self.__normal_bg,
                                            corner_radius=10,
                                            width=625,
                                            height=50,
                                            command=self.out_warning_sum)
            self.__activate_warning_sum.place(relx=0.325, rely=0.375, anchor=cTk.W)
        
        self.__validation = self.__window.register(self.only_numbers)
        
        # Input Sum
        self.__amount_in = cTk.CTkEntry(master=self.__window, 
                                            placeholder_text="Enter the maximum amount here",
                                            width=450,
                                            height=50,
                                            border_color="white",
                                            bg_color=self.__normal_bg,
                                            validate="key", 
                                            validatecommand=(self.__validation, '%S'),
                                            textvariable=self.__in_str,
                                            font=('arial', 20))
        self.__amount_in.place(relx=0.55, 
                                rely=0.5, 
                                anchor=CENTER)
        self.__amount_in_label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 12, 'bold'),
                                            text="Only numbers and '.'-comma allowed as input",
                                            bg_color=self.__normal_bg)
        self.__amount_in_label.place(relx=0.46, 
                                rely=0.58, 
                                anchor=CENTER)
        return
    
    def only_numbers(self, char): # Checks if input (char) is a number or a '.'
        if char.isdigit() or char == '.':
            return True
        else:
            return False
    
    def in_warning_zero(self):
        helptxt = "UPDATE user SET warn_zero='1' where id='" + str(self.__user) + "'"
        cursor.execute(helptxt)
        connection.commit()
        page_settings(self.__user, Settings_Screen.set_03)
        return
    
    def out_warning_zero(self):
        helptxt = "UPDATE user SET warn_zero='0' where id='" + str(self.__user) + "'"
        cursor.execute(helptxt)
        connection.commit()
        page_settings(self.__user, Settings_Screen.set_03)
        return
    
    def in_warning_sum(self):
        if str(self.__in_str.get()) != '' and int(self.__in_str.get()) != 0:
            helptxt = "UPDATE user SET warn_sum='" + str(self.__in_str.get()) + "' where id='" + str(self.__user) + "'"
            cursor.execute(helptxt)
            connection.commit()
            page_settings(self.__user, Settings_Screen.set_03)
        else:
            messagebox.showwarning("Finance App", "Minimum value cannot be blank or zero!")
        return
    
    def out_warning_sum(self):
        helptxt = "UPDATE user SET warn_sum='0' where id='" + str(self.__user) + "'"
        cursor.execute(helptxt)
        connection.commit()
        page_settings(self.__user, Settings_Screen.set_03)
        return
    
    def set_04(self): # Credits
        self.__label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text="For my project I had great resources to use, \nwithout which I would have never been able to make this.\n\nProf. Geigers Python Course resources\n\nIcons DB for these incredible free images\n\n Some great Python resources:\ncustom tkinter by Tom Schimansky\n...",
                                            bg_color=self.__normal_bg)
        self.__label.place(relx=0.445, rely=0.65, anchor=W)
        return
    
    def set_05(self): # INFO regarding users profile
        self.__user_info = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 25),
                                            text="Welcome",
                                            bg_color=self.__normal_bg)
        self.__user_info.place(relx=0.35, rely=0.25, anchor=NW)
        
        cursor.execute("select name from user where id='" + self.__user + "'")
        self.__user_name = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 35, "bold"),
                                            text=str(cursor.fetchone()[0]),
                                            bg_color=self.__normal_bg,
                                            text_color='#00A417')
        self.__user_name.place(relx=0.35, rely=0.31, anchor=NW)
        
        # User picture
        self.__userpic = cTk.CTkImage(light_image=Image.open(os.path.join(current_dir_global, "resources", "user-xxl.png")), size=(50 , 50))
        self.__picframe = cTk.CTkButton(master=self.__window, 
                                            width=100, 
                                            height=100, 
                                            text="", 
                                            fg_color="#494996", 
                                            hover_color="#494996",
                                            corner_radius=10, 
                                            image=self.__userpic, 
                                            bg_color=self.__normal_bg)
        self.__picframe.place(relx=0.85, rely=0.25, anchor=NW)
        
        self.__date = date.today()
        cursor.execute("select sum_total from user_" + self.__user + "_data where id=(select max(id) from user_" + self.__user + "_data where date=(select max(date) from user_" + self.__user + "_data where date<='" + str(self.__date) + "'))")
        try:
            self.__balace_text = "" + f'{cursor.fetchone()[0]:.2f}' + " €"
        except TypeError:
            self.__balace_text = "0 €"
        self.__balance_info = "Your currently avaiable amount is:"
        self.__balance_info = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 20),
                                            text=self.__balance_info,
                                            bg_color=self.__normal_bg)
        self.__balance_info.place(relx=0.35, rely=0.425, anchor=NW)
        self.__balance_txt = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 25),
                                            text=self.__balace_text,
                                            bg_color=self.__normal_bg)
        self.__balance_txt.place(relx=0.35, rely=0.55, anchor=SW)
        
        cursor.execute("select * from user_" + self.__user + "_data")
        numbervar = len(cursor.fetchall())
        self.__number_txt = "You have already made " + str(numbervar) + " transactions"
        self.__number_label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text=self.__number_txt,
                                            text_color="#00A417",
                                            bg_color=self.__normal_bg)
        self.__number_label.place(relx=0.35, rely=0.65, anchor=SW)
        
        if numbervar < 10:
            self.__cheertxt = "There is much more possible!"
        elif numbervar < 35:
            self.__cheertxt = "That is very good!"
        else:
            self.__cheertxt = "Wow, that number of transactions is astonishing!"
        self.__cheer_txt_label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text=self.__cheertxt,
                                            bg_color=self.__normal_bg)
        self.__cheer_txt_label.place(relx=0.35, rely=0.7, anchor=SW)
        
        try:
            cursor.execute("select min(date) from user_" + self.__user + "_data")
            self.__mindate = datetime.strptime(cursor.fetchall()[0][0], '%Y-%m-%d').date()
            cursor.execute("select max(date) from user_" + self.__user + "_data")
            self.__maxdate = datetime.strptime(cursor.fetchall()[0][0], '%Y-%m-%d').date()
            
            datetxt = "Since " + str(int((str(self.__maxdate - self.__mindate).split(" "))[0]) + 1) + " days"
        except TypeError:
            datetxt = "Not a single day"
        except ValueError:
            datetxt = "Since 1 day"
        
        self.__dates = cTk.CTkButton(master=self.__window, 
                                            width=185, 
                                            height=70, 
                                            text=datetxt, 
                                            fg_color="#494996", 
                                            hover_color="#494996",
                                            corner_radius=10,
                                            bg_color=self.__normal_bg)
        self.__dates.place(relx=0.35, rely=0.75, anchor=NW)
        
        try:
            cursor.execute("select sum from user_" + self.__user + "_data where io='0'")
            self.__inputval = 0
            for row in cursor.fetchall():
                self.__inputval += row[0]
            
            if self.__inputval > 1000000:
                self.__inputval = "over a Million "
            
            invaltxt = "Already " + str(self.__inputval) + "€ earned"
        except (TypeError, ValueError):
            invaltxt = "Not a single € earned"
        
        if (self.__inputval == 0):
            invaltxt = "Not a single € earned"
        
        self.__dates = cTk.CTkButton(master=self.__window, 
                                            width=185, 
                                            height=70, 
                                            text=invaltxt, 
                                            fg_color="#494996", 
                                            hover_color="#494996",
                                            corner_radius=10,
                                            bg_color=self.__normal_bg)
        self.__dates.place(relx=0.5575, rely=0.75, anchor=NW)
        
        try:
            cursor.execute("select sum from user_" + self.__user + "_data where io='1'")
            self.__outputval = 0
            for row in cursor.fetchall():
                self.__outputval += row[0]
            
            if self.__outputval > 1000000:
                self.__outputval = "over a Million "
            
            outvaltxt = "Yet " + str(self.__outputval) + "€ spent"
        except (TypeError, ValueError):
            outvaltxt = "Not a single € spent"
        
        if (self.__outputval == 0):
            outvaltxt = "Not a single € spent"
        
        self.__dates = cTk.CTkButton(master=self.__window, 
                                            width=185, 
                                            height=70, 
                                            text=outvaltxt, 
                                            fg_color="#494996", 
                                            hover_color="#494996",
                                            corner_radius=10,
                                            bg_color=self.__normal_bg)
        self.__dates.place(relx=0.765, rely=0.75, anchor=NW)
        return
    
    def set_06(self): # Change Data
        cursor.execute("select name from user where id='" + self.__user + "'")
        self.__user_txt = "Username: " + str(cursor.fetchone()[0])
        self.__user_name = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 20),
                                            text=self.__user_txt,
                                            bg_color=self.__normal_bg)
        self.__user_name.place(relx=0.35, rely=0.28, anchor=NW)
        
        # Enter new Username
        self.__nuser_Entry = cTk.CTkEntry(master=self.__window, 
                                            placeholder_text="Enter new Username",
                                            width=450,
                                            height=50,
                                            bg_color=self.__normal_bg,
                                            font=('arial', 20))
        self.__nuser_Entry.place(relx=0.35, rely=0.345, anchor=NW)
        self.__nuser_Canvas = cTk.CTkFrame(master=self.__window,
                                            corner_radius=0,
                                            fg_color="#494996",
                                            bg_color=self.__normal_bg,
                                            height=5,
                                            width=450)
        self.__nuser_Canvas.place(relx=0.35, rely=0.435, anchor=NW)
        
        # New Username Button
        self.__Register_Button = cTk.CTkButton(master=self.__window,
                                            text="Change Username",
                                            font=('arial', 20),
                                            fg_color="#00A417",
                                            bg_color=self.__normal_bg,
                                            hover_color="#009017",
                                            corner_radius=10,
                                            width=450,
                                            height=50,
                                            command=lambda: self.change_data("user"))
        self.__Register_Button.place(relx=0.35, rely=0.455, anchor=NW)
        
        # Enter new Password
        self.__uoPW_Label = cTk.CTkLabel(master=self.__window, 
                                            font=('arial', 17),
                                            text="Change your password here",
                                            bg_color=self.__normal_bg)
        self.__uoPW_Label.place(relx=0.35, rely=0.575, anchor=NW)
        self.__uoPW_Entry = cTk.CTkEntry(master=self.__window, 
                                            placeholder_text="Enter old password",
                                            width=450,
                                            height=50,
                                            show="*",
                                            bg_color=self.__normal_bg,
                                            font=('arial', 20))
        self.__uoPW_Entry.place(relx=0.35, rely=0.635, anchor=NW)
        self.__uoPW_Canvas = cTk.CTkFrame(master=self.__window,
                                            corner_radius=0,
                                            fg_color="#494996",
                                            bg_color=self.__normal_bg,
                                            height=5,
                                            width=450)
        self.__uoPW_Canvas.place(relx=0.35, rely=0.725, anchor=NW)
        
        self.__unPW_Entry = cTk.CTkEntry(master=self.__window, 
                                            placeholder_text="Enter new password",
                                            width=450,
                                            height=50,
                                            show="*",
                                            bg_color=self.__normal_bg,
                                            font=('arial', 20))
        self.__unPW_Entry.place(relx=0.35, rely=0.745, anchor=NW)
        self.__unPW_Canvas = cTk.CTkFrame(master=self.__window,
                                            corner_radius=0,
                                            fg_color="#494996",
                                            bg_color=self.__normal_bg,
                                            height=5,
                                            width=450)
        self.__unPW_Canvas.place(relx=0.35, rely=0.835, anchor=NW)
        
        # New Password Button
        self.__Register_Button = cTk.CTkButton(master=self.__window,
                                            text="Change Password",
                                            font=('arial', 20),
                                            fg_color="#00A417",
                                            bg_color=self.__normal_bg,
                                            hover_color="#009017",
                                            corner_radius=10,
                                            width=450,
                                            height=50,
                                            command=lambda: self.change_data("pw"))
        self.__Register_Button.place(relx=0.35, rely=0.855, anchor=NW)
        return
    
    def change_data(self, mode): # changes username or password if possible
        if mode == "pw":
            msg_nPW = messagebox.askquestion("Finance App", "Do you want to change your password?")
            if msg_nPW == 'yes':
                try:
                    helptxt = "SELECT EXISTS (SELECT 1 FROM user WHERE id = '" + str(self.__user) + "' AND password = '" + str(self.__uoPW_Entry.get()) + "')"
                    cursor.execute(helptxt)
                    if not cursor.fetchone():
                        print(str(cursor.fetchone()))
                        messagebox.showerror("Finance App", "Current password not correct!") 
                        return
                except ValueError:
                    print("help")
                    messagebox.showerror("Finance App", "Current password not correct!") 
                    return
                
                if self.__uoPW_Entry.get() == "" or self.__unPW_Entry.get() == "":
                    messagebox.showerror("Finance App", "Old and new password field must not be blank!") 
                    return
                
                else:
                    helptxt = "UPDATE user SET password='" + str(self.__unPW_Entry.get()) + "' where id='" + str(self.__user) + "'"
                    cursor.execute(helptxt)
                    connection.commit()
        
        else:
            msg_nuser = messagebox.askquestion("Finance App", "Do you want to change your username?")
            if msg_nuser == 'yes':
                if self.__nuser_Entry.get() == "":
                    messagebox.showerror("Finance App", "New username field must not be blank!") 
                    return
                
                else:
                    helptxt = "UPDATE user SET name='" + str(self.__nuser_Entry.get()) + "' where id='" + str(self.__user) + "'"
                    cursor.execute(helptxt)
                    connection.commit()
        
        page_settings(self.__user, Settings_Screen.set_06)
        return
    
    
    def set_07(self): # Logout function
        msg_logout = messagebox.askquestion("Finance App", "Do you want to logout and return to the login screen?")
        if msg_logout == 'yes':
            page_login()
        return
    
    def set_08(self): # Function to delete whole database on computer
        msg_delete = messagebox.askquestion("Finance App", "DO YOU WANT TO DELETE WHOLE DATA FROM DATABASE?\nWarning: This process is irreversible!")
        if msg_delete == 'yes':
            delete_all_tables(connection)
        return
    
    def add_cat(self): # Function to add an entered category to the list of categories if value is accepted
        helptxt = "SELECT EXISTS (SELECT 1 FROM user_" + self.__user + "_sets WHERE cat='" + str(self.__text_cat.get()) + "')"
        cursor.execute(helptxt)
        
        if self.__text_cat.get() == "":
            messagebox.showerror("Finance App", "Category must not be blank!") 
            return
        
        elif cursor.fetchone()[0]:
            messagebox.showerror("Finance App", "Category already exists!") 
            return
        
        elif len(self.__text_cat.get()) >= 16:
            messagebox.showerror("Finance App", "Category maximum lenght is 16 characters!") 
            return
        
        else:
            cursor.execute("select * from user_" + self.__user + "_sets")
            idvar = len(cursor.fetchall())
            if idvar != 0:
                cursor.execute("select id from user_" + self.__user + "_sets where id=(select max(id) from user_" + self.__user + "_sets)")
                idvar = (cursor.fetchall()[0][0] + 1)
                
            var = (idvar, str(self.__text_cat.get()))
            helptxt = "INSERT INTO user_" + self.__user + "_sets VALUES (?,?)"
            cursor.execute(helptxt, var)
            
            connection.commit()
            
            page_settings(self.__user, Settings_Screen.set_02)
        return
    
    def add_stdcats(self): # Function to add some pre-defined standard-categories to list of categories
        std_cat_list = ("Food", "Drinks", "Job", "Car", "House", "Restaurants", "Beer")
        for category in std_cat_list:
            
            helptxt = "SELECT EXISTS (SELECT 1 FROM user_" + self.__user + "_sets WHERE cat='" + str(category) + "')"
            cursor.execute(helptxt)
            if cursor.fetchone()[0]:
                messagebox.showerror("Finance App", "Standard categories already exist!") 
                return
            
            cursor.execute("select * from user_" + self.__user + "_sets")
            idvar = len(cursor.fetchall())
            if idvar != 0:
                cursor.execute("select id from user_" + self.__user + "_sets where id=(select max(id) from user_" + self.__user + "_sets)")
                idvar = (cursor.fetchall()[0][0] + 1)
                
            var = (idvar, category)
            helptxt = "INSERT INTO user_" + self.__user + "_sets VALUES (?,?)"
            cursor.execute(helptxt, var)
            
            connection.commit()
            
            page_settings(self.__user, Settings_Screen.set_02)
        return

# END OF CLASS DEFINITIONS

# Function definition to delete whole database

TABLE_PARAMETER = "{TABLE_PARAMETER}"
DROP_TABLE_SQL = f"DROP TABLE {TABLE_PARAMETER};"
GET_TABLES_SQL = "SELECT name FROM sqlite_schema WHERE type='table';"

def delete_all_tables(con):
    tables = get_tables(con)
    delete_tables(con, tables)


def get_tables(con):
    cur = con.cursor()
    cur.execute(GET_TABLES_SQL)
    tables = cur.fetchall()
    cur.close()
    return tables


def delete_tables(con, tables):
    cur = con.cursor()
    for table, in tables:
        helptxt = DROP_TABLE_SQL.replace(TABLE_PARAMETER, table)
        cur.execute(helptxt)
    cur.close()

# END OF ALL FUNCTION DEFINITIONS

# Load Custom tKinter Screen with global parameters

window = cTk.CTk()
cTk.set_appearance_mode("dark")
cTk.set_default_color_theme("dark-blue")

# every window has a global frame defined here
window_login = cTk.CTkFrame(master=window)
window_register = cTk.CTkFrame(master=window)
window_main = cTk.CTkFrame(master=window)
window_inout = cTk.CTkFrame(master=window)
window_history = cTk.CTkFrame(master=window)
window_plot = cTk.CTkFrame(master=window)
window_settings = cTk.CTkFrame(master=window)

# window properties
window.geometry('1000x500')
window.resizable(0,0)
window.configure(bg="white")

# first window load and start of tKinter mainloop
window.title('Finance App - Login')
Login(window_login)
window_login.pack()
window.mainloop()
