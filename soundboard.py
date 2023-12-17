
# --------------------------- All Libs And Imports --------------------------- #

import os
import signal
import subprocess

from time import sleep

import gi.repository
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3

from tkinter import *
from tkinter import ttk as tk


# ------------------------------- Create Tk Gui ------------------------------ #
root = None
app = None
menu = None

# --------------------------------- Constants -------------------------------- #
APPINDICATOR_ID = "server_util"
iconname = "icon3.png"
iconpath =  os.path.join(os.path.dirname(os.path.abspath(__file__)), iconname)

filePath = "conf.txt"

file = open(filePath).readlines()
serverName = file[0].split()[1]
    

vpnActive = False

# ============================================================================ #
#                                 Main Function                                #
# ============================================================================ #
def main():
    
    global app, Gtk, vpnActive, appQuit
    
    # Setup
    os.setpgrp()
    
    if get_vpn_status():
        vpnActive = True
    
    init_top_bar()
    
    # update top bar / gui events
    while True:
        
        if (app):
            try:
                app.update_idletasks()
                app.update()
                
                app.update_internal()
                
            except:
                pass
            
        Gtk.main_iteration_do(False)
        
        sleep(1/10)
  

# ============================================================================ #
#                           Application Window Class                           #
# ============================================================================ #
class Application(tk.Frame): 
    # init da shit             
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=master)
        self.grid(padx=10, pady=10)             
        self.createWidgets()

        
    # update things like text etc based on vpn status
    def update_internal(self):
        
        global vpnActive
        
        chunks = get_cmd_output("sudo wg show", ["interface", "key", "handshake", "transfer", "received"])
        vpnActive = (len(chunks) >= 4 and chunks[0] == serverName)
            
        # if has connection to VPN
        if vpnActive:
            try:
                self.vpnButton.config(text="Deactivate VPN")
                self.sshButton.config(text="Connect SSH")
                # change text
                self.text_status.config(text="Connected: True")
                self.text_name.config(text="Name: " + chunks[0])
                self.text_pubkey.config(text="Public Key: " + chunks[1])
                self.text_handshake.config(text="Handshake: " + chunks[2] + " seconds ago")
                self.text_total_downup.config(text="Total Down/Up-load: " + chunks[3] + "B / " + chunks[4] + "B")
                self.text_average_downup.config(text="Average Down/Up-load: TBD")
            except:
                pass
            
        # if no current connection to VPN
        else:
            self.vpnButton.config(text="Activate VPN")
            self.sshButton.config(text="no")
            #change text
            self.text_status.config(text="Connected: False")
            self.text_name.config(text="")
            self.text_pubkey.config(text="")
            self.text_handshake.config(text="")
            self.text_total_downup.config(text="")
            self.text_average_downup.config(text="")
            
            

	# Create Elements inside App Window
    def createWidgets(self):
        
        
        # Activate/deactivate VPN
        self.vpnButton = tk.Button(self, text='Activate VPN', command=self.activateVPN)
        self.vpnButton.grid(row=0, column=0)
        
        # start new ssh terminal
        self.sshButton = tk.Button(self, text='SSH', command=self.activateSSH)
        self.sshButton.grid(row=1, column=0)
        
        # Quit Button
        self.quitButton = tk.Button(self, text='Quit', command=self.quit_app)            
        self.quitButton.grid(row=4, column=0) 
        
        # Quit Button
        self.sudokuButton = tk.Button(self, text='Close & SIGKILL', command=self.sudoku)            
        self.sudokuButton.grid(row=5, column=0) 
        
        # text
        self.text_status = tk.Label(self, text="")
        self.text_status.grid(sticky="W", row=0, column=1, padx=10, pady=10)
        self.text_name = tk.Label(self, text="")
        self.text_name.grid(sticky="W", row=1, column=1, padx=10, pady=10)
        self.text_pubkey = tk.Label(self, text="")
        self.text_pubkey.grid(sticky="W", row=2, column=1, padx=10, pady=10)
        self.text_handshake = tk.Label(self, text="Handshake: ")
        self.text_handshake.grid(sticky="W", row=3, column=1, padx=10, pady=10)
        self.text_total_downup = tk.Label(self, text="")
        self.text_total_downup.grid(sticky="W", row=4, column=1, padx=10, pady=10)
        self.text_average_downup = tk.Label(self, text="")
        self.text_average_downup.grid(sticky="W", row=5, column=1, padx=10, pady=10)
        
        #space
        self.extra_space = tk.Label(self, text=" ")
        self.extra_space.grid(row=0, column=2, padx=100, pady=10)


    
    # quit app while leaving top bar running. actually done in main loop but this sets the variable for it to do so
    def quit_app(self):
        global root
        root.destroy()
        
        
          
    # close vpn and SIGKILL self
    def sudoku(self):    

        print("\n Et tu Brutus...")            
        if vpnActive:
            print("\n Closing the Portal...")
            self.activateVPN()
            
        os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)
        
    
    # Activate/Deactivate VPN based on current wg show status
    def activateVPN(self):
        if vpnActive:
            print("\n Deactivating VPN...")
            string = get_cmd_output("sudo wg-quick down " + serverName, [])
            
        else:
            print("\n Activating VPN...")
            string = get_cmd_output("sudo wg-quick up " + serverName, [])
            
            
    
    # Start neww ssh terminal to server
    def activateSSH(self):
        if vpnActive: 
            os.system("terminator --new-tab -e 'python3 ssh.py'")
    
			
            
    
    
        
        
 
# ============================================================================ #
#                               Utility Functions                              #
# ============================================================================ #
        
# --------------- Init App Window From Class, Called By Top Bar -------------- #
def init_app(str):
    
    global app, root
    
    if app != None:
        return
    
    print("\n Creating app window...")
    
    root = Tk()
    root.wm_title("Server Util")
    app = Application(root)
    
  
 
# ------------------------------ GUI Definitions ----------------------------- #
def init_top_bar():
    
    global menu, indicator, app
    print("\n Creating top bar...")
    
    menu = Gtk.Menu()
    
    option_open = Gtk.MenuItem.new_with_label('Open Server Utility')
    option_open.connect('activate', init_app)
    menu.append(option_open)

    option_quit = Gtk.MenuItem.new_with_label('Quit')
    option_quit.connect('activate', quit)
    menu.append(option_quit)
    
    menu.show_all()
    
    indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID, iconpath, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu)
 
 
 
# ------------------------- Execute Command In Shell ------------------------- #
def get_cmd_output(string, arr):
    string = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    chunks = string.split()
    result = []
    for a in arr:
        for i, c in enumerate(chunks):
            try:
                j = c.index(a)
            except:
                continue
            
            result.append(chunks[i+1])
            break
            
    return result
            
 
 
 
# --------------------------- Read Wireguard Status -------------------------- #
def get_vpn_status():
    a = ["interface"]
    arr = get_cmd_output("sudo wg show", a)
    if (len(arr) > 0 and arr[0] == serverName):
        return True
    else:
        return False
        
main()
