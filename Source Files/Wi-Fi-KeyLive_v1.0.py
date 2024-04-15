import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import json
import webbrowser

class WiFiKeyLive:
    def __init__(self, Window):
        self.Window = Window
        self.Window.title("Wi-Fi Key (Live)")
        
        self.Menu()

    def Menu(self):
        # Create Menu 
        self.Menu = tk.Menu(self.Window)
        self.Window.config(menu=self.Menu)

        # Create Menu 'File'
        self.File = tk.Menu(self.Menu, tearoff=0)
        self.Menu.add_cascade(label="File", menu=self.File)
        self.File.add_command(label="Export", command=self.Export)
        self.File.add_separator()
        self.File.add_command(label="Exit", command=self.Window.quit)

        # Create Menu 'Help'
        self.Help = tk.Menu(self.Menu, tearoff=0)
        self.Menu.add_cascade(label="Help", menu=self.Help)
        self.Help.add_command(label="Check for Updates", command=self.Check_for_Updates)
        self.Help.add_separator()
        self.Help.add_command(label="About", command=self.About)

        # Create Frame for Button
        self.Frame_For_Button = ttk.Frame(self.Window)
        self.Frame_For_Button.pack(padx=10, pady=10)

        # Create Button 'Show SSID & Key' on Frame
        self.Button_GoLive = ttk.Button(self.Frame_For_Button, text="Go Live!", command=self.Parse_Key)
        self.Button_GoLive.pack(side="left")

        # Create Frame for Table
        self.Frame_For_Table = ttk.Frame(self.Window)
        self.Frame_For_Table.pack(padx=10, pady=10)

        # Create Table 'SSID & Key' on Frame
        self.Table = ttk.Treeview(self.Frame_For_Table, columns=('SSID', 'Key'), show='headings')
        self.Table.heading('SSID', text='SSID')
        self.Table.heading('Key', text='Key')
        self.Table.pack(side="left", fill="both", expand=True)

        # Add Vertical Scrollbar to the Table
        self.Vertical_Scrollbar = ttk.Scrollbar(self.Frame_For_Table, orient="vertical", command=self.Table.yview)
        self.Vertical_Scrollbar.pack(side="right", fill="y")
        self.Table.config(yscrollcommand=self.Vertical_Scrollbar.set)

    def Export(self):
        Data = []
        for Child in self.Table.get_children():
            Values = self.Table.item(Child, 'values')
            Data.append({'SSID': Values[0], 'Key': Values[1]})
        
        File_PATH = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if File_PATH:
            with open(File_PATH, "w") as File_Export:
                json.dump(Data, File_Export, indent=4)
                messagebox.showinfo("Exported", "Data exported successfully!")

    def Check_for_Updates(self):
        webbrowser.open("https://www.github.com/Satyeshvara/Wi-Fi-KeyLive")

    def About(self):
        messagebox.showinfo("About", "Wi-Fi Key (Live) (v1.0)\nDeveloped by Satish Kumar Singh")

    def Get_SSID(self):
        try:
            Result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, check=True)
            return Result.stdout
        except subprocess.CalledProcessError as e:
            print("Error:", e.stderr)
            return None

    def Get_Key(self, SSID):
        try:
            Result = subprocess.run(['netsh', 'wlan', 'show', 'profile', SSID, 'key=clear'], capture_output=True, text=True, check=True)
            return Result.stdout
        except subprocess.CalledProcessError as e:
            print("Error:", e.stderr)
            return None

    def Parse_SSID(self, SSIDs):
        SSID_List = []
        for line in SSIDs.split("\n"):
            if "All User Profile" in line:
                SSID_List.append(line.split(":")[1].strip())
        return SSID_List

    def Parse_Key(self):
        WiFi_SSID = self.Get_SSID()
        if WiFi_SSID:
            SSIDs = self.Parse_SSID(WiFi_SSID)
            
            # Clear Previous Table Content
            for row in self.Table.get_children():
                self.Table.delete(row)

            for SSID in SSIDs:
                WiFi_Key = self.Get_Key(SSID)
                if WiFi_Key:
                    Lines = WiFi_Key.split('\n')
                    Data_SSID = SSID
                    Data_Key = None
                    for Line in Lines:
                        if "Key Content" in Line:
                            Data_Key = Line.split(":")[1].strip()
                    self.Table.insert('', 'end', values=(Data_SSID, Data_Key))

def main():
    root = tk.Tk()
    Application = WiFiKeyLive(root)
    root.mainloop()

if __name__ == "__main__":
    main()