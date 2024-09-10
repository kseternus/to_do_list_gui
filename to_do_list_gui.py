import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tinydb import TinyDB, Query

# Initialize the TinyDB
db = TinyDB('todo_list.json')


def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])


# Function to load all tasks from TinyDB
def load_tasks():
    tasks = db.all()
    for task in tasks:
        if task['completed']:
            strike_task = strike(task['task'])
            task_listbox.insert(tk.END, f'{strike_task} ✓')    # Strike through the task text
            task_listbox.itemconfig(tk.END, {'foreground': '#000000'})
        else:
            task_listbox.insert(tk.END, task['task'])


# Function to add a new task
def add_task():
    task = entry_task.get()
    if task:
        db.insert({'task': task, 'completed': False})
        task_listbox.insert(tk.END, task)
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning('Input Error', 'Please enter a task.')


# Function to mark a task as completed
def complete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)

        # Check if the task is already completed (contains the checkmark)
        if '✓' in task_text:
            # Task is completed, revert to uncompleted
            task_text = task_text.replace(' ✓', '')    # Remove the checkmark
            remove_unstrie_task = task_text.replace('\u0336', '')    # Remove the strikethrough

            # Update the task in the database as uncompleted
            db.update({'completed': False}, Query().task == remove_unstrie_task)

            # Update the visual listbox with uncompleted task
            task_listbox.delete(selected_task_index)
            task_listbox.insert(selected_task_index, remove_unstrie_task)
            task_listbox.itemconfig(selected_task_index, {'foreground': '#000000'})
        else:
            # Task is uncompleted, mark as completed
            task_text = task_text.replace(' ✓', '')    # Ensure no checkmarks in the task
            db.update({'completed': True}, Query().task == task_text)

            # Update the visual listbox with strikethrough text
            task_listbox.delete(selected_task_index)
            strike_task = strike(task_text)    # Strike through the task text
            task_listbox.insert(selected_task_index, f'{strike_task} ✓')
            task_listbox.itemconfig(selected_task_index, {'foreground': '#000000'})
    else:
        messagebox.showwarning('Selection Error', 'Please select a task to mark as completed.')


# Function to delete the selected task
def delete_selected_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_text = task_listbox.get(selected_task_index)
        # Strip out any existing check marks if present
        task_text = task_text.replace(' ✓', '')

        # Remove the task from the database
        db.remove(Query().task == task_text)

        # Remove the task from the listbox
        task_listbox.delete(selected_task_index)
    else:
        messagebox.showwarning('Selection Error', 'Please select a task to delete.')


# Function to delete all tasks
def delete_all_tasks():
    if messagebox.askyesno('Delete All', 'Are you sure you want to delete all tasks?'):
        task_listbox.delete(0, tk.END)
        db.truncate()


# GUI Setup
root = tk.Tk()
root.title('To-Do List')
root.geometry('510x630')
root.resizable(False, False)    # Locking ability to resize window
root.configure(background='#f2e8cf')    # Main window background color

# Define custom fonts
app_font = font.Font(family='Helvetica', size=12)   # Font for general use

# Frame for Listbox and Scrollbar
frame = tk.Frame(root)
frame.pack(pady=(15, 10))

# Listbox with larger font
task_listbox = tk.Listbox(frame, activestyle='dotbox', height=20, width=50, bd=0, background='#e6ccb2',
                          foreground='#000000', font=app_font)
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Scrollbar for Listbox
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

task_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_listbox.yview)

# Entry box with larger font
entry_task = tk.Entry(root, width=50, background='#b08968', foreground='#000000', font=app_font)
entry_task.pack(pady=10)

# Buttons with larger font
add_task_button = tk.Button(root, text='Add Task', command=add_task, background='#ddb892', foreground='#000000',
                            font=app_font)
add_task_button.pack(pady=5)

complete_task_button = tk.Button(root, text='Complete Task', command=complete_task, background='#ddb892',
                                 foreground='#000000', font=app_font)
complete_task_button.pack(pady=5)

delete_selected_button = tk.Button(root, text='Delete Selected Task', command=delete_selected_task,
                                   background='#ddb892', foreground='#000000', font=app_font)
delete_selected_button.pack(pady=5)

delete_all_button = tk.Button(root, text='Delete All Tasks', command=delete_all_tasks, background='#ddb892',
                              foreground='#000000', font=app_font)
delete_all_button.pack(pady=5)

# Load tasks when the app starts
load_tasks()

# Run the app
root.mainloop()
