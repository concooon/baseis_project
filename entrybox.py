import re
import tkinter as tk
from tkinter import ttk

class EnntryBox:
    def __init__(self, parent, row, col, width, settings, callback=None):
        self.callback = callback
        self.validation = settings[2]
        self.data = "" # initialize data

        # 2a. Create housing frame
        self.frame = ttk.LabelFrame(parent, text=f"  {settings[0]}  ", width=width, name=f"f{settings[0]}")
        self.frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # 2b. Create description label
        self.label = ttk.Label(self.frame, text=settings[1], foreground="gray", state="disabled", width=width)
        self.label.pack(padx=5, pady=5, fill="x")       

        # 2c. Create error label
        self.error_label = ttk.Label(self.frame, text="", foreground="red", state="disabled", width=width, font=("Helvetica", 8))
        self.error_label.pack(padx=5, pady=5, fill="x")

        # 2d. Create entry field
        if settings[3] == "entry":
            self.entry = ttk.Entry(self.frame, width=width)
        
        elif settings[3] == "combobox":
            values = settings[-1] if isinstance(settings[-1], tuple) else []
            self.entry = ttk.Combobox(self.frame, values=values, state="readonly", width=width)

        # 2e. Add entry field and bind focus out event
        self.entry.pack(padx=5, pady=5, fill="x")
        self.entry.bind("<FocusOut>", self.lost_focus) # on focus out, validate data

    def lost_focus(self, event):
        if self.validation == None or re.match(self.validation, self.entry.get()): #todo: not None validation
            # if data are valid, notify user
                        
            self.error_label.config(foreground="green")
            self.error_label.config(text="✔")
            self.data = self.entry.get() #update data
        elif self.entry.get() == "":
            # if data are empty, do nothing

            self.error_label.config(text="")
            self.data = "" #update data
        else:
            # if data are invalid, notify user (error label)

            self.error_label.config(foreground="red")
            self.error_label.config(text="⚠ Μη έγκυρη τιμή")
            self.data = False #update data

        # update buttons of parent
        self.callback(event)

    def reset(self):
        # Resets entry field, data and error label
        self.entry.delete(0, "end")
        self.error_label.config(text="")
        self.data = ""