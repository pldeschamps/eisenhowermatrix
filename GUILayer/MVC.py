__author__ = "Pierre-Louis Deschamps https://github.com/pldeschamps"
__license__ = "CC BY-SA https://creativecommons.org"

import tkinter as tk
from tkinter import font as font

from GUILayer import Texts, DialogBox
from LogicLayer import Tasks
from tkcalendar import DateEntry
# import datetime

class Model:
    def __init__(self):
        self._tasks = Tasks.Tasks()
        pass


class View:
    def __init__(self, tkroot, model):
        self._tkroot = tkroot
        self._model = model
        tkroot.title(Texts.applicationTitle)
        tkroot.geometry("1000x1000")   # (210x2 + 2x10) x (297x2 + 2x10)

        # Menu
        self.mainMenu = tk.Menu(tkroot, tearoff=False)

        # MenuFile
        self.menuFile = tk.Menu(self.mainMenu, tearoff=False)
        self.menuFile.add_command(label=Texts.quit, command=tkroot.quit)
        self.mainMenu.add_cascade(label=Texts.file, menu=self.menuFile)

        # MenuTasks
        self.menuTasks = tk.Menu(self.mainMenu, tearoff=False)
        self.menuTasks.add_command(label=Texts.newTask, command=self.newTask)
        self.mainMenu.add_cascade(label=Texts.tasks, menu=self.menuTasks)
        tkroot.config(menu=self.mainMenu)

        # MenuView
        self._maskDone = tk.IntVar()
        self.menuView = tk.Menu(self.mainMenu, tearoff=False)
        self.menuView.add_checkbutton(label=Texts.maskDone, command=self.maskDone, variable=self._maskDone)
        self.menuView.add_command(label=Texts.deleteDone, command=self.deleteDone)
        self.mainMenu.add_cascade(label=Texts.view, menu=self.menuView)
        tkroot.config(menu=self.mainMenu)

        # Labels Urgent and Important
        self.labelUrgent =    tk.Label(tkroot, text=Texts.urgency[1]).grid(row=0, column=1)
        self.labelNonUrgent = tk.Label(tkroot, text=Texts.urgency[0]).grid(row=0, column=2)
        self.labelImportant =    tk.Label(tkroot, text=Texts.importance[1], wraplength=1).grid(row=1, column=0)
        self.labelNonImportant = tk.Label(tkroot, text=Texts.importance[0], wraplength=1).grid(row=2, column=0)
        tk.Grid.rowconfigure(tkroot, 1, weight=1)
        tk.Grid.rowconfigure(tkroot, 2, weight=1)
        tk.Grid.columnconfigure(tkroot, 1, weight=1)
        tk.Grid.columnconfigure(tkroot, 2, weight=1)

        # Frames Urgent and Important
        self.frames = [[], []]

        for urgency in [0, 1]:
            for importance in [0, 1]:
                self.frames[urgency].append(tk.Frame(tkroot, bg=Tasks.classificationColor[urgency][importance],
                                                     borderwidth=3, relief=tk.SUNKEN, padx=2, pady=2))
                self.frames[urgency][importance].grid(column=2-urgency, row=2-importance,
                                                        sticky=tk.N + tk.S + tk.E + tk.W)

        # Define which event handlers when the user clics on a frame
        def frameClic(event):
            self.newTask(0, 0)
        def frameUClic(event):
            self.newTask(1, 0)
        def frameIClic(event):
            self.newTask(0, 1)
        def frameUIClic(event):
            self.newTask(1, 1)
        self.frames[0][0].bind('<Button-1>', frameClic)
        self.frames[1][0].bind('<Button-1>', frameUClic)
        self.frames[0][1].bind('<Button-1>', frameIClic)
        self.frames[1][1].bind('<Button-1>', frameUIClic)

        # Tasks frames
        self.framesTask = []

        for task in self._model._tasks:
            self.displayTask(task)



    def newTask(self, urgency=0, importance=0): # I could not bind the menu with fonctions in the class Controller...
        nt = DialogBoxNewTask(self._tkroot, Texts.newTask, self._model._tasks, urgency, importance)
        if nt.result:
            self._model._tasks.add(nt.result)
            self.displayTask(nt.result)

    def displayTask(self, task):
        master = self.frames[task._urgent][task._important]
        frameTask = FrameTask(self, master, task, self._model._tasks)
        # frameTask.config(bg=Tasks.classificationColor[task._urgent][task._important])
        frameTask.pack(in_=master, side=tk.TOP, anchor='w', fill=tk.X, padx=1, pady=1)
        self.framesTask.append(frameTask)

    def maskDone(self):
        if self._maskDone.get():
            newFramesTask = []
            for frame in self.framesTask:
                if frame.task._done:
                    # It is a bad idea to remove items from a list in an iteration:
                    # self.framesTask.remove(frame)
                    frame.destroy()
                else:
                    newFramesTask.append(frame)
            self.framesTask = newFramesTask
        else:
            for task in self._model._tasks:
                if task._done:
                    self.displayTask(task)

    def deleteDone(self):
        for frame in self.framesTask:
            if frame.task._done:
                frame.destroy()
        for task in self._model._tasks:
            if task._done:
                task.delete()

class FrameTask(tk.Frame):
    def __init__(self, view, master, task, tasks):
        tk.Frame.__init__(self, view._tkroot, borderwidth=1, relief=tk.SOLID)
        self.view = view
        self.task = task
        self.tasks = tasks
        color = Tasks.classificationColor[task._urgent][task._important]
        self.config(bg=color, borderwidth=1, relief=tk.SOLID)
        # self.done = tk.IntVar()
        # self.doneCheckButton = tk.Checkbutton(self, text=task._name, bg=color, variable=self.done, command=)
        # self.doneCheckButton.pack(side=tk.LEFT, padx=1, pady=1)
        self.checkButtonTask = CheckButtonTask(self, task, self.cget('bg'))
        self.labelDueDate = tk.Label(self, text=task._dueDate, bg=self.cget('bg'))
        self.labelDueDate.pack(side=tk.RIGHT, padx=1, pady=1)
        def button3(event):
            PopUpMenu(self.view, self, event, self.task._id, self.tasks)
            #return self.popupmenu(event)
        self.bind('<Button-3>', button3)
        self.checkButtonTask.bind('<Button-3>', button3)
        self.labelDueDate.bind('<Button-3>', button3)

    #def popupmenu(self, event):
    #    popUpMenu = PopUpMenu(self.view, self, event, self.task._id, self.tasks)

    def taskDone(self, task):
        if task._done:
            task._done = 0
            # print("done!")
        else:
            task._done = 1
        task.updateInDB()



class PopUpMenu(tk.Menu):
    def __init__(self, view, frameTask, event, task_id, tasks):
        tk.Menu.__init__(self, frameTask, tearoff=0, borderwidth=1, relief=tk.SOLID)
        self.view = view
        self._frameTask = frameTask
        self._task_id = task_id
        self._tasks = tasks
        self.add_command(label=Texts.deleteTask, command=self.deleteTask)
        self.add_command(label=Texts.editTask, command=self.editTask)
        self.urgency_var = tk.IntVar()
        for task in self._tasks:
            if task._id == self._task_id:
                self.urgency_var.set(task._urgent)
        self.add_checkbutton(label=Texts.urgency[1], variable=self.urgency_var, command=self.toggleUrgency)
        self.importance_var = tk.IntVar()
        for task in self._tasks:
            if task._id == self._task_id:
                self.importance_var.set(task._important)
        self.add_checkbutton(label=Texts.importance[1], variable=self.importance_var, command=self.toggleImportance)
        # self.add_command(label=Texts.changeUrgency, command=self.changeUrgency)
        # self.add_command(label=Texts.changeImportance, command=self.changeImportance)
        self.post(event.x_root, event.y_root)

    def deleteTask(self):
        for task in self._tasks:
            if task._id==self._task_id:
                task.delete()
        self._frameTask.destroy()

    def editTask(self):
        for task in self._tasks:
            if task._id == self._task_id:
                et = DialogBoxEditTask(self.view._tkroot, Texts.editTask, task)
                if et.result:
                    self.updateFrameTask(task)
                    task.updateInDB()
                    self._frameTask.destroy() 
                    self.view.displayTask(task)
    def toggleUrgency(self):
        for task in self._tasks:
            if task._id == self._task_id:
                task._urgent = self.urgency_var.get()
                task.updateInDB()
                self.updateFrameTask(task)
    def toggleImportance(self):
        for task in self._tasks:
            if task._id == self._task_id:
                task._important = self.importance_var.get()
                task.updateInDB()
                self.updateFrameTask(task)

    def changeUrgency(self):
        for task in self._tasks:
            if task._id == self._task_id:
                task.change_urgency()
                self.updateFrameTask(task)

    def updateFrameTask(self, task):
        self._frameTask.pack(in_=self.view.frames[task._urgent][task._important], side=tk.TOP, anchor='w', fill=tk.X,
                             padx=1, pady=1)
        color = Tasks.classificationColor[task._urgent][task._important]
        self._frameTask.config(bg=color)
        self._frameTask.checkButtonTask.config(bg=color)
        self._frameTask.labelDueDate.config(bg=color)

    def changeImportance(self):
        for task in self._tasks:
            if task._id == self._task_id:
                task.change_importance()
                self.updateFrameTask(task)

class CheckButtonTask(tk.Checkbutton):
    def __init__(self, frameTask, task, color):
        self.frameTask = frameTask
        self.done = tk.IntVar()
        self.task = task
        defaultFont = font.nametofont('TkDefaultFont')
        self.fontOverstrike = font.Font(family=defaultFont.cget('family'), size=defaultFont.cget('size'),
                                       overstrike=True, )
        self.fontOverstrikeFalse = font.Font(family=defaultFont.cget('family'), size=defaultFont.cget('size'),
                                            overstrike=False)
        if task._done:
            fontTask = self.fontOverstrike
        else:
            fontTask = self.fontOverstrikeFalse
        tk.Checkbutton.__init__(self, frameTask, text=task._name, variable=self.done, bg=color, command=self.clic,
                                font=fontTask)
        if task._done:
            self.select()
        self.pack(side=tk.LEFT, padx=1, pady=1)

    def clic(self):
        if self.done.get():
            self.config(font=self.fontOverstrike)
        else:
            self.config(font=self.fontOverstrikeFalse)
        self.frameTask.taskDone(self.task)

class DialogBoxNewTask(DialogBox.DialogBox):
    def __init__(self, root, title,  tasks, urgency=0, importance=0):
        self._tasks = tasks
        self._urgency = urgency
        self._importance = importance
        DialogBox.DialogBox.__init__(self, root, title, offx=0, offy=0)

    def packing(self, master):
        frameTask = tk.Frame(master)
        tk.Label(frameTask, text="Task :").pack(side=tk.LEFT)
        self.taskTask = tk.Entry(frameTask)
        self.taskTask.pack(side=tk.LEFT)
        tk.Label(frameTask, text="Due Date :").pack(side=tk.LEFT)
        self.taskDueDate = DateEntry(frameTask, date_pattern='dd/mm/yyyy')
        self.taskDueDate.pack(side=tk.LEFT)
        frameTask.pack(side=tk.TOP)
        frameUrgencyImportance = tk.Frame(master)
        self.urgent = tk.IntVar()
        self.urgentCheckButton = tk.Checkbutton(frameUrgencyImportance, text=Texts.urgency[1],
                                                variable=self.urgent)
        self.urgentCheckButton.pack(side=tk.LEFT)
        if self._urgency:
            self.urgentCheckButton.select()
        self.important = tk.IntVar()
        self.importanceCheckButton = tk.Checkbutton(frameUrgencyImportance, text=Texts.importance[1],
                                                    variable=self.important)
        self.importanceCheckButton.pack(side=tk.LEFT)
        if self._importance:
            self.importanceCheckButton.select()
        frameUrgencyImportance.pack(side=tk.TOP)
        return self.taskTask                             # Pourquoi ??

    def apply(self):
        self.result = Tasks.Task(0, self._tasks, self.taskTask.get(), self.taskDueDate.get(), self.urgent.get(), self.important.get())

class DialogBoxEditTask(DialogBox.DialogBox):
    def __init__(self, root, title, task):
        self._task = task
        DialogBox.DialogBox.__init__(self, root, title, offx=0, offy=0)

    def packing(self, master):
        frameTask = tk.Frame(master)
        tk.Label(frameTask, text="Task :").pack(side=tk.LEFT)
        self.taskTask = tk.Entry(frameTask)
        self.taskTask.insert(0, self._task._name)
        self.taskTask.pack(side=tk.LEFT)
        tk.Label(frameTask, text="Due Date :").pack(side=tk.LEFT)
        self.taskDueDate = DateEntry(frameTask, date_pattern='dd/mm/yyyy')
        if self._task._dueDate:
            self.taskDueDate.set_date(self._task._dueDate)
        # else:
        #     current_date = datetime.datetime.now().strftime('%d/%m/%Y')
        #     self.taskDueDate.set_date(current_date)
        self.taskDueDate.pack(side=tk.LEFT)
        frameTask.pack(side=tk.TOP)
        frameUrgencyImportance = tk.Frame(master)
        self.urgent = tk.IntVar(value=self._task._urgent)
        self.urgentCheckButton = tk.Checkbutton(frameUrgencyImportance, text=Texts.urgency[1],
                                                variable=self.urgent)
        self.urgentCheckButton.pack(side=tk.LEFT)
        self.important = tk.IntVar(value=self._task._important)
        self.importanceCheckButton = tk.Checkbutton(frameUrgencyImportance, text=Texts.importance[1],
                                                    variable=self.important)
        self.importanceCheckButton.pack(side=tk.LEFT)
        frameUrgencyImportance.pack(side=tk.TOP)
        return self.taskTask

    def apply(self):
        self._task._name = self.taskTask.get()
        self._task._dueDate = self.taskDueDate.get()
        self._task._urgent = self.urgent.get()
        self._task._important = self.important.get()
        self.result = self._task

class Controller:
    def __init__(self):
        self.tkroot = tk.Tk()
        self.model = Model()
        self.view = View(self.tkroot, self.model)

    def run(self):
        self.tkroot.mainloop()


