__author__ = "Pierre-Louis Deschamps https://github.com/pldeschamps"
__license__ = "CC BY-SA https://creativecommons.org"

import sqlite3


class TasksDB:
    def __init__(self):
        self._db = sqlite3.connect("./tasks.db")
        self._cursor = self._db.cursor()
        self._cursor.execute("CREATE TABLE IF NOT EXISTS tasks("
                             "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,"
                             "name TEXT,"
                             "dueDate TEXT,"
                             "urgent INTEGER,"
                             "important INTEGER,"
                             "done INTEGER,"
                             "category TEXT)")
        self._db.commit()

    def close(self):
        self._cursor.close()

    def append(self, newTask):
        self._cursor.execute("INSERT INTO tasks(name, dueDate, urgent, important, done, category) VALUES(?, ?, ?, ?, ?, ?)",
                             (newTask._name, newTask._dueDate, newTask._urgent, newTask._important,newTask._done, newTask._category))
        newTask._id = self._cursor.lastrowid
        self._db.commit()

    def selectAll(self):
        self._cursor.execute("SELECT * FROM tasks")
        return self._cursor

    def delete(self, taskID):
        self._cursor.execute("DELETE FROM tasks WHERE id=?", (taskID,))
        self._db.commit()

    def update(self, task):
        self._cursor.execute("UPDATE tasks SET name=?, dueDate=?, urgent=?, important=?, done=?, category=? WHERE id=?",
                             (task._name, task._dueDate, task._urgent, task._important, task._done, task._category, task._id))
        self._db.commit()
