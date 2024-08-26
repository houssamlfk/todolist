from tkinter import *
from tkinter import ttk
import sqlite3

# Setting up of Database that will store the tasks
connector = sqlite3.connect("tasks.db")
cursor = connector.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Tasks (task TEXT)")
connector.commit()
connector.close()

# universal count of tasks and label list
count = 0
task_dict = {}

# functions block


def destroy_func():
    l = []
    for x in task_dict.keys():
        if (task_dict[x][2].get() == True):
            l.append(x)
            txt = task_dict[x][1].cget("text")
            conn = sqlite3.connect("tasks.db")
            crsr = conn.cursor()
            crsr.execute(f"DELETE FROM Tasks WHERE task='{txt}'")
            conn.commit()
            conn.close()

            task_dict[x][0].destroy()
            task_dict[x][1].destroy()
            break
    del task_dict[l[0]]


def add_func():
    # variables
    global count
    global entry_text
    global task_dict
    if entry_text.get() != "":
        count += 1
        # creation of label and storage in database
        conn = sqlite3.connect("tasks.db")
        crsr = conn.cursor()
        crsr.execute(f"INSERT INTO Tasks VALUES ('{entry_text.get()}')")
        conn.commit()
        conn.close()

        # adding task to the window and storing it in dictionary
        state = BooleanVar()
        label = Label(master=m, text=entry_text.get())
        label.grid(column=1, row=count)
        check = Checkbutton(master=m, command=destroy_func, variable=state)
        check.grid(row=count, column=0)
        task_dict[f"task{count}"] = (check, label, state)
        entry_text.set(value="")


def clear_func():
    global task_dict
    global count
    global entry_text
    conn = sqlite3.connect("tasks.db")
    crsr = conn.cursor()
    for x in task_dict.keys():
        if task_dict[x][1].winfo_exists():
            txt = task_dict[f"{x}"][1].cget("text")
            crsr.execute(f"DELETE FROM Tasks WHERE task='{txt}'")
            conn.commit()
            task_dict[f"{x}"][0].destroy()
            task_dict[f"{x}"][1].destroy()
        else:
            print(f"{task_dict[x][1]} doesn't exist")
    conn.close()
    count = 0
    task_dict = {}
    entry_text.set(value="")


# Execution of the window and initialization of widgets
m = Tk()
m.geometry("250x300")

var1 = IntVar()
entry_text = StringVar(master=m)


conn = sqlite3.connect("tasks.db")
crsr = conn.cursor()
crsr.execute("SELECT * FROM Tasks")
conn.commit()
task_list = crsr.fetchall()
conn.close()
for x in task_list:
    count += 1
    add_state = BooleanVar()
    add_label = Label(master=m, text=x[0])
    add_check = Checkbutton(master=m, variable=add_state, command=destroy_func)
    add_check.grid(column=0, row=count)
    add_label.grid(column=1, row=count)
    task_dict[f"task{count}"] = (add_check, add_label, add_state)
    print(f"{x[0]} has been added succesfully!")

# Visualizing GUI components
add_text = Entry(master=m, textvariable=entry_text, width=26)
add_text.grid(row=0, column=1)

clear_button = Button(master=m, text="Clear", command=clear_func, width=6)
clear_button.grid(row=0, column=2)

add_button = Button(master=m, text='+', width=4, command=add_func)
add_button.grid(row=0, column=0)

# Functionning stage

m.mainloop()
