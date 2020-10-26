#===========================
# Imports
#===========================

import tkinter as tk
from tkinter import ttk, colorchooser as cc, Menu, Spinbox as sb, scrolledtext as st, messagebox as mb, filedialog as fd


#===========================
# Main App
#===========================

class NewForm(tk.Toplevel):
    # ==========================================
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_config()
        self.init_UI()

    # ==========================================
    def init_config(self):
        self.resizable(False, False)
        self.attributes('-toolwindow', True)

    # ==========================================
    def init_UI(self):
        self.id = tk.StringVar()
        self.firstname = tk.StringVar()
        self.middlename = tk.StringVar()
        self.lastname = tk.StringVar()
        self.age = tk.StringVar()

        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        fieldset = ttk.LabelFrame(self.frame, text='Create Student Account')
        fieldset.pack(fill=tk.BOTH, expand=True, anchor=tk.N, padx=5, pady=5)

        titles = [
            ('First Name', self.firstname),
            ('Middle Name', self.middlename),
            ('Last Name', self.lastname),
            ('Age', self.age)
            ]

        for title, datatype in titles:
            frame = ttk.Frame(fieldset)
            frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

            label = ttk.Label(frame, text=title)
            label.pack(side=tk.TOP, anchor=tk.E, fill=tk.X)

            entry = tk.Entry(frame, textvariable=datatype, width=50)
            entry.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, ipady=2)

        button = ttk.Button(self.frame, text='Submit', command=self.save)
        button.pack(side=tk.RIGHT, padx=5, pady=(0, 5))

    # INSTANCE METHODS -------------------------
    def save(self):
        print(self.parent.crud.save({
            'id' : self.id.get(),
            'first_name' : self.firstname.get(),
            'middle_name' : self.middlename.get(),
            'last_name' : self.lastname.get(),
            'age' : self.age.get()
            }))
        self.parent.refresh()
        self.destroy()

class EditForm(tk.Toplevel):
    # ==========================================
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_config()
        self.init_UI()

    # ==========================================
    def init_config(self):
        self.resizable(False, False)
        self.attributes('-toolwindow', True)

    # ==========================================
    def init_UI(self):
        self.id = tk.StringVar()
        self.firstname = tk.StringVar()
        self.middlename = tk.StringVar()
        self.lastname = tk.StringVar()
        self.age = tk.StringVar()

        student = self.parent.crud.find_by_id(self.parent.id.get())

        self.id.set(student['id'])
        self.firstname.set(student['first_name'])
        self.middlename.set(student['middle_name'])
        self.lastname.set(student['last_name'])
        self.age.set(student['age'])

        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        fieldset = ttk.LabelFrame(self.frame, text='Edit Student Account')
        fieldset.pack(fill=tk.BOTH, expand=True, anchor=tk.N, padx=5, pady=5)

        titles = [
            ('First Name', self.firstname),
            ('Middle Name', self.middlename),
            ('Last Name', self.lastname),
            ('Age', self.age)
            ]

        for title, datatype in titles:
            frame = ttk.Frame(fieldset)
            frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

            label = ttk.Label(frame, text=title)
            label.pack(side=tk.TOP, anchor=tk.E, fill=tk.X)

            entry = tk.Entry(frame, textvariable=datatype, width=50)
            entry.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, ipady=2)

        button = ttk.Button(self.frame, text='Save', command=self.save)
        button.pack(side=tk.RIGHT, padx=5, pady=(0, 5))

    # INSTANCE METHODS -------------------------
    def save(self):
        print(self.parent.crud.save({
            'id' : self.id.get(),
            'first_name' : self.firstname.get(),
            'middle_name' : self.middlename.get(),
            'last_name' : self.lastname.get(),
            'age' : self.age.get()
            }))
        self.parent.refresh()
        self.parent.id.set('')
        self.destroy()


#===========================
# Start GUI
#===========================

def main():
    app = Form()
    app.mainloop()

if __name__ == '__main__':
    main()