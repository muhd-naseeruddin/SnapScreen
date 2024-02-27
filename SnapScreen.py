import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog, messagebox
import datetime
import time
import os
import ScreenShot
import threading
from PIL import ImageTk, Image
import webbrowser
import tkinter.font as tkFont

class SnapScreenApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SnapScreen")
        self.master.iconbitmap('Images\\screenshot_icon.ico')

        self.master.geometry("765x440")

        self.gray = "#a6a6a6"
        self.beige = "#836c58"

        self.name_placeholder = "Enter name here..."
        self.phone_placeholder = "Enter phone number here..."

        # Create a main notebook
        self.main_tab = tb.Notebook(self.master, bootstyle='default')
        self.main_tab.grid(row=0, column=0, padx=10, pady=10)

        # Create frames for each tab
        self.primary_tab = tb.Frame(self.main_tab)
        self.help_tab = tb.Frame(self.main_tab)

        # Widgets for primary tab
        # Name widget
        self.name_label = tb.Label(self.primary_tab, text="Name:", bootstyle='default', anchor="w")
        self.name_label.grid(row=0, column=0, padx=10, pady=20, sticky="w")
        self.name_entry = tb.Entry(self.primary_tab, width=40, foreground=self.gray)
        self.name_entry.placeholder = self.name_placeholder
        self.name_entry.insert(0, self.name_placeholder)
        self.name_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.name_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.name_entry.grid(row=0, column=1, padx=0)

        # Phone widget
        self.phone_label = tb.Label(self.primary_tab, text="Phone number:", bootstyle="default", anchor="w")
        self.phone_label.grid(row=1, column=0, padx=10, pady=0, sticky="w")
        self.phone_entry = tb.Entry(self.primary_tab, width=40, foreground=self.gray)
        self.phone_entry.placeholder = self.phone_placeholder
        self.phone_entry.insert(0, self.phone_placeholder)
        self.phone_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.phone_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.phone_entry.grid(row=1, column=1, padx=0)

        # Browse folder path widget
        self.folder_label = tb.Label(self.primary_tab, text="Folder Path:", bootstyle="default", anchor="w")
        self.folder_label.grid(row=2, column=0, padx=10, pady=20, sticky="w")
        self.initial_folder_path = os.path.expanduser("~\\Desktop")
        self.folder_var = tb.StringVar()
        self.folder_var.set(self.initial_folder_path)
        self.folder_entry = tb.Entry(self.primary_tab, width=40, textvariable=self.folder_var)
        self.folder_entry.grid(row=2, column=1)

        self.browse_button = tb.Button(self.primary_tab, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=2, column=2, padx=10)

        # Create label frame for checkbox
        self.label_frame = tb.LabelFrame(self.primary_tab, text="Websites", bootstyle="default")
        self.label_frame.grid(row=0, column=4, rowspan=3, padx=20)

        self.function_checkboxes = {}

        self.function = {
            "automate_website_sprm": "SPRM",
            "automate_website_rmp": "RMP",
            "automate_website_kehakiman": "EFS Kehakiman",
            "automate_website_ccid": "CCID"
        }

        for i, (func_name, func_desc) in enumerate(self.function.items()):
            self.function_checkboxes[func_name] = tb.BooleanVar(value=True)
            checkbox = tb.Checkbutton(self.label_frame, text=func_desc, variable=self.function_checkboxes[func_name])
            checkbox.grid(row=i + 3, column=0, sticky="w", padx=10, pady=5)

        # Create label frame for status
        self.status_frame = tb.LabelFrame(self.primary_tab, text="Status", bootstyle="default")
        self.status_frame.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="w")

        self.scrollbar = tb.Scrollbar(self.status_frame, orient="vertical", bootstyle="default")
        self.scrollbar.pack(side="right", fill="y")

        self.status_text = tb.Text(self.status_frame, height=4, state="disabled", width=84,
                                   yscrollcommand=self.scrollbar.set, wrap="none")
        self.status_text.pack(padx=10, pady=10)

        self.scrollbar.configure(command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=self.scrollbar.set)

        self.execute_button = tb.Button(self.primary_tab,
                                        text="Execute",
                                        bootstyle="default",
                                        command=self.execute_selenium)
        self.execute_button.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

        self.master.bind('<Return>', self.execute_selenium)

        # Widget for help tab
        self.help_frame = ScrolledFrame(self.help_tab, autohide=False)
        self.help_frame.pack(padx=10, pady=10, fill=BOTH, expand="yes")

        self.contact_label = tb.Label(self.help_frame, text='Basic Guide', anchor=CENTER)
        self.contact_label.grid(row=0, column=0, padx=0, pady=10)

        self.tutorial_image = Image.open("Images\\tutorial.png")
        self.tutorial_image = self.tutorial_image.resize((700, 389), Image.Resampling.LANCZOS)
        self.tutorial_image = ImageTk.PhotoImage(self.tutorial_image)
        self.image_label = tb.Label(self.help_frame, image=self.tutorial_image, anchor=CENTER)
        self.image_label.grid(row=1, column=0)

        self.tutorial_number_one = tb.Label(self.help_frame, text="1. [Name] is refering to candidate name. This field is required.")
        self.tutorial_number_one.grid(row=2, column=0, padx=10, pady=(5,0), sticky="w")
        self.tutorial_number_two = tb.Label(self.help_frame, text="2. [Phone] is refering to candidate's phone number. This field is optional unless CCID is checked.")
        self.tutorial_number_two.grid(row=3, column=0, padx=10, pady=0, sticky="w")
        self.tutorial_number_three = tb.Label(self.help_frame, text="3. [Folder Path] is refering to save location path for your screenshot.")
        self.tutorial_number_three.grid(row=4, column=0, padx=10, pady=0, sticky="w")
        self.tutorial_number_four = tb.Label(self.help_frame, text="4. [Website], in this section, you can choose which website you want to perform SnapScreen.")
        self.tutorial_number_four.grid(row=5, column=0, padx=10, pady=0, sticky="w")
        self.tutorial_number_five = tb.Label(self.help_frame, text="5. [Status] shows the status message of SnapScreen progress.")
        self.tutorial_number_five.grid(row=6, column=0, padx=10, pady=0, sticky="w")
        self.tutorial_number_six = tb.Label(self.help_frame, text="6. [Execute button] will execute the SnapScreen.")
        self.tutorial_number_six.grid(row=7, column=0, padx=10, pady=0, sticky="w")
        self.tutorial_number_seven = tb.Label(self.help_frame, text="Status Message Types:")
        self.tutorial_number_seven.grid(row=8, column=0, padx=10, pady=(15, 0), sticky="w")
        self.tutorial_number_eight = tb.Label(self.help_frame, text="1. [SUCCESS] Automation has completed - The screenshot is completed")
        self.tutorial_number_eight.grid(row=9, column=0, padx=10, pady=0, sticky="w")
        self.tutorial_number_eight = tb.Label(self.help_frame, text="2. [ERROR] Error during process: - There is an error during execution")
        self.tutorial_number_eight.grid(row=10, column=0, padx=10, pady=0, sticky="w")
        self.tutorial_number_eight = tb.Label(self.help_frame, text="3. [WARNING] <Warning message> - Refer to the warning message")
        self.tutorial_number_eight.grid(row=11, column=0, padx=10, pady=0, sticky="w")

        

        email_address = "muhd.naseeruddin@gmail.com"
        self.email_label = tb.Label(self.help_frame, text='For questions or issues, please contact:', anchor=CENTER)
        self.email_add = tb.Label(self.help_frame, text=f"{email_address}", cursor="hand2", anchor=CENTER, bootstyle = 'info')
        f = tkFont.Font(self.email_add, self.email_add.cget("font"))
        f.configure(underline=True, size=10)
        self.email_add.configure(font=f)
        self.email_label.grid(row=12, column=0, padx=0, pady=(10,0), sticky='we')
        self.email_add.grid(row=13, column=0, sticky="we")
        self.email_add.bind("<Button-1>", lambda event: webbrowser.open(f"mailto:{email_address}"))
        

        # Add frames to notebook
        self.main_tab.add(self.primary_tab, text="Main")
        self.main_tab.add(self.help_tab, text="Help")

        # Close window
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

        # Create right-click menu
        self.entry_menu = tb.Menu(master, tearoff=0)
        self.entry_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        self.entry_menu.add_command(label="Copy", accelerator="Ctrl+C",  command=self.copy_text)
        self.entry_menu.add_command(label="Paste",  accelerator="Ctrl+V", command=self.paste_text)
        self.entry_menu.add_separator()
        self.entry_menu.add_command(label="Select all",  accelerator="Ctrl+A", command=self.select_all)

        # Create a right-click menu for copying the email address
        self.email_menu = tk.Menu(self.email_label, tearoff=0)
        self.email_menu.add_command(label="Copy Email Address", command=lambda: self.copy_email_address(email_address))
        self.email_label.bind("<Button-3>", self.show_email_menu)

        # Bind right-click menu to entry widgets
        self.name_entry.bind("<Button-3>", self.show_entry_menu)
        self.phone_entry.bind("<Button-3>", self.show_entry_menu)
        self.folder_entry.bind("<Button-3>", self.show_entry_menu)
        self.email_add.bind("<Button-3>", self.show_email_menu)

       

    def show_email_menu(self, event):
        self.email_menu.post(event.x_root, event.y_root)

    def copy_email_address(self, email_address):
        self.master.clipboard_clear()
        self.master.clipboard_append(email_address)
        self.master.update()  # Required on macOS

    def show_entry_menu(self, event):
        self.entry_menu.post(event.x_root, event.y_root)

    def cut_text(self):
        self.master.focus_get().event_generate("<<Cut>>")

    def copy_text(self):
        self.master.focus_get().event_generate("<<Copy>>")

    def paste_text(self):
        self.master.focus_get().event_generate("<<Paste>>")
        
    def select_all(self):
        focused_widget = self.master.focus_get()
        focused_widget.selection_range(0, tk.END)

    
    def browse_folder(self):
        folder_path = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder_path:
            self.folder_var.set(folder_path)

    def on_entry_focus_in(self, event):
        entry = event.widget
        placeholder = entry.placeholder
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(foreground=self.beige)

    def on_entry_focus_out(self, event):
        entry = event.widget
        placeholder = entry.placeholder
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(foreground=self.gray)

    def execute_selenium(self, event=None):
        threads = []
        start_event = threading.Event()

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        folder = self.folder_entry.get().strip()

        self.status_text.configure(state="normal")
        self.status_text.delete(1.0, tk.END)
        self.status_text.configure(state="disable")

        if not name or name == self.name_placeholder:
            self.status_message("warning", "[WARNING] Please enter candidate name...")
            return

        if not folder:
            self.status_message("warning", "[WARNING] Please enter folder path...")
            return

        selected_functions = [func_name for func_name, var in self.function_checkboxes.items() if var.get()]

        if (not phone or phone == self.phone_placeholder) and "automate_website_ccid" in selected_functions:
            self.status_message("warning", "[WARNING] Please enter phone number as you have checked CCID...")
            return

        ScreenShot.create_folder_if_not_exists(name, self.folder_var.get())
        

        try:
            self.status_message("info", f"Automation started for {name}")

            for selected_func in selected_functions:
                thread = threading.Thread(target=self.run_selenium, args=(selected_func, name, folder, phone))
                threads.append(thread)
                thread.start()
                self.status_message("info", f"{selected_func} is running...")

            start_event.set()

            monitoring_thread = threading.Thread(target=self.monitor_threads_periodically, args=(threads,))
            monitoring_thread.start()

        except Exception as e:
            self.status_message("warning", f"[ERROR] Error during process: {e}")
        finally:
            if not selected_functions:  # Check if no checkboxes are checked
                self.status_message("warning", "[WARNING] No websites selected for automation.")
            # else:
            #     for thread in threads:
            #         self.status_message("info", f"{thread}")
            

    def monitor_threads(self, threads):
        for thread in threads:
            thread.join()
            # threads.remove(thread)
        # All threads have finished
        self.status_message("success", "[SUCCESS] Automation has completed.")

    def monitor_threads_periodically(self, threads):
        while any(thread.is_alive() for thread in threads):
            time.sleep(1)  # Wait for 1 second before checking again
        time.sleep(1)
        self.status_message("success", "[SUCCESS] Automation has completed.")
        messagebox.showinfo("[SUCCESS]", "Automation has completed")


    def run_selenium(self, selected_func, name, folder_path, phone=None, start_event = None):
        if start_event:
            start_event.wait()
        if selected_func == "automate_website_sprm":
            ScreenShot.automate_website_sprm(name, folder_path)
        elif selected_func == "automate_website_kehakiman":
            ScreenShot.automate_website_kehakiman(name, folder_path)
        elif selected_func == "automate_website_rmp":
            ScreenShot.automate_website_rmp(name, folder_path)
        elif selected_func == "automate_website_ccid":
            ScreenShot.automate_website_ccid(phone, name, folder_path)
        self.status_message("info", f"{selected_func} is finished.")


    def status_message(self, type, message):
        time_stamp = datetime.datetime.now()
        if type == "warning":
            self.status_text.configure(foreground="red")
        else:
            self.status_text.configure(foreground=self.beige)
        self.status_text.configure(state="normal")
        self.status_text.insert(tk.END, f"[{time_stamp}]: {message}\n")
        self.status_text.configure(state="disabled")
        self.status_text.yview_pickplace("end")

    def close_window(self):
        self.master.destroy()

def main():
    root = tb.Window(themename="beigetheme")
    app = SnapScreenApp(root)
    root.resizable(False,False)
    root.mainloop()

if __name__ == "__main__":
    main()