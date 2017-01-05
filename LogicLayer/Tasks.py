__author__ = "Pierre-Louis Deschamps https://github.com/pldeschamps"
__license__ = "CC BY-SA https://creativecommons.org"

from DataLayer import Data


classificationColor = (("#80C0FF", "#C0FF80"), ("#FFFF80", "#FF4040"))


class Task:
    def __init__(self,  tasks, db_id, name, due_date, urgent, important, done=0, category=None):
        self._tasks = tasks
        self._id = db_id
        self._name = name
        self._dueDate = due_date

        self._urgent = urgent
        self._important = important
        self._done = done
        self._category = category

    def change_urgency(self):
        if self._urgent:
            self._urgent = 0
        else:
            self._urgent = 1
        self.updateInDB()

    def change_importance(self):
        if self._important:
            self._important = 0
        else:
            self._important = 1
        self.updateInDB()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def urgent(self):
        return self._urgent

    @urgent.setter
    def urgent(self, value):
        self._urgent = value

    def delete(self):
        db = Data.TasksDB()
        db.delete(self._id)
        db.close()
        self._tasks.remove(self)

    def updateInDB(self):
        db = Data.TasksDB()
        db.update(self)
        db.close()

class Tasks(list):
    def __init__(self):
        db = Data.TasksDB()
        allTasksDB = db.selectAll()
        for taskDB in allTasksDB:
            task = Task(self, taskDB[0],taskDB[1],taskDB[2],taskDB[3],taskDB[4],taskDB[5])
            list.append(self, task)
        db.close()

    def add(self, newTask):
        db = Data.TasksDB()
        db.append(newTask)
        db.close()
        list.append(self, newTask)

if __name__ == "__main__":
    my_task = Task("CISSP", "1/12/2016", "reconversion", False, True)
    my_task.change_urgency()
    print(my_task.urgent)


