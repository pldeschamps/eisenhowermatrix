__author__ = "Pierre-Louis Deschamps https://github.com/pldeschamps"
__license__ = "CC BY-SA https://creativecommons.org"

import tkinter as tk

from GUILayer import Texts


class DialogBox(tk.Toplevel):
    def __init__(self, container, title=None, offx=250, offy=250):
        tk.Toplevel.__init__(self, container)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.transient(container)
        if title:
            self.title(title)
        else:
            self.title(Texts.applicationTitle)

        self.container = container
        self.result = None

        frame = tk.Frame(self)
        self.initial_focus = self.packing(frame)
        frame.pack(padx=10, pady=10)

        focusDefault = self.buttons()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = focusDefault

        self.initial_focus.focus_set()

        self.wait_window(self)

    def packing(self, master):
        pass #to be overloaded

    def buttons(self):
        frame = tk.Frame(self)
        buttonOK = tk.Button(frame, text=Texts.ok, command=self.ok, default=tk.ACTIVE, width=10)
        buttonOK.pack(side=tk.LEFT, padx=5, pady=5)
        buttonCancel = tk.Button(frame, text=Texts.cancel, command=self.cancel, width=10)
        buttonCancel.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        frame.pack()
        return buttonOK #Pourquoi ??

    def ok(self, event=None):
        self.initial_focus.focus_set()
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.container.focus_set()
        self.destroy()

    def apply(self):
        pass #to be overloaded





