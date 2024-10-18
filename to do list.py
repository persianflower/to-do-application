import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Define the file where tasks will be stored
TASKS_FILE = 'tasks.txt'

# Load tasks from a file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)
    else:
        tasks = []
    return tasks

# Save tasks to a file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

# Create the main application class
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        self.tasks = load_tasks()

        # Frame for task input
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.title_label = tk.Label(self.frame, text="Task Title:")
        self.title_label.grid(row=0, column=0)
        self.title_entry = tk.Entry(self.frame, width=30)
        self.title_entry.grid(row=0, column=1)

        self.desc_label = tk.Label(self.frame, text="Task Description:")
        self.desc_label.grid(row=1, column=0)
        self.desc_entry = tk.Entry(self.frame, width=30)
        self.desc_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.tasks_listbox = tk.Listbox(self.root, width=50, height=10)
        self.tasks_listbox.pack(pady=10)

        self.edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.complete_button = tk.Button(self.root, text="Mark Completed", command=self.mark_completed)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.populate_tasks()

    def populate_tasks(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, f"{task['title']} - {task['description']} {'[Completed]' if task['completed'] else ''}")

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        if title and description:
            self.tasks.append({"title": title, "description": description, "completed": False})
            save_tasks(self.tasks)
            self.populate_tasks()
            messagebox.showinfo("Success", "Task added successfully!")
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter both title and description.")

    def edit_task(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            task = self.tasks[selected_index]
            new_title = simpledialog.askstring("Edit Task", "New title:", initialvalue=task['title'])
            new_description = simpledialog.askstring("Edit Task", "New description:", initialvalue=task['description'])
            if new_title is not None and new_description is not None:
                self.tasks[selected_index]['title'] = new_title
                self.tasks[selected_index]['description'] = new_description
                save_tasks(self.tasks)
                self.populate_tasks()
                messagebox.showinfo("Success", "Task updated successfully!")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit.")

    def mark_completed(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            self.tasks[selected_index]['completed'] = True
            save_tasks(self.tasks)
            self.populate_tasks()
            messagebox.showinfo("Success", "Task marked as completed!")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as completed.")

    def delete_task(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            del self.tasks[selected_index]
            save_tasks(self.tasks)
            self.populate_tasks()
            messagebox.showinfo("Success", "Task deleted successfully!")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    todo_app = TodoApp(root)
    root.mainloop()
