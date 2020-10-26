#===========================
# Imports
#===========================

import tkinter as tk
from tkinter import ttk, colorchooser as cc, Menu, Spinbox as sb, scrolledtext as st, messagebox as mb, filedialog as fd

import csv

from includes.Database import Database
from includes.CRUD import CRUD
from components.Form import NewForm, EditForm


#===========================
# Main App
#===========================

class App(tk.Tk):
    """Main Application."""

    # ==========================================
    def __init__(self):
        super().__init__()
        # self.init_db()
        self.init_db_connection()
        self.init_config()
        self.init_UI()
        self.init_events()

    # ==========================================
    def init_db(self):
        db = Database('student_db')
        db.server = 'localhost'
        db.username = 'root'
        db.password = 'root'
        print(db.create_database())

        db.table_name = 'students'
        print(db.create_table_fields({
            'id' : 'INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY',
            'first_name' : 'VARCHAR(255)',
            'middle_name' : 'VARCHAR(255)',
            'last_name' : 'VARCHAR(255)',
            'age' : 'INT(3)'
            }))

    # ==========================================
    def init_db_connection(self):
        self.crud = CRUD(
            server='localhost',
            username='root',
            password='root',
            database_name='student_db',
            table_name='students',
            table_id='id'
            )

    # ==========================================
    def init_config(self):
        self.resizable(True, True)
        self.title('Student Information System Version 1.0')
        self.iconbitmap('notepad.ico')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

    # ==========================================
    def init_events(self):
        self.tree.bind('<ButtonRelease-1>', self.show_popupmenu1)
        self.tree.bind('<Button-3>', self.show_popupmenu2)
        self.bind('<Key>', self.show_auto_suggest)
        self.entry.bind('<FocusOut>', self.remove_listbox)

    # ==========================================
    def init_UI(self):
        self.id = tk.StringVar()

        self.frame = ttk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = ttk.Frame(self.frame)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        button = ttk.Button(toolbar, text=f'Export to CSV', command=self.export)
        button.pack(side=tk.LEFT)

        fieldset = ttk.LabelFrame(self.frame, text='Search')
        fieldset.pack(side=tk.TOP, fill=tk.X, anchor=tk.N, padx=5, pady=5)

        self.search = tk.StringVar()
        self.entry = ttk.Entry(fieldset, width=50, textvariable=self.search)
        self.entry.pack(side=tk.LEFT, ipady=5, fill=tk.X, expand=True)

        button = ttk.Button(fieldset, text=f'Go', command=self.result)
        button.pack(side=tk.LEFT)

        button = ttk.Button(fieldset, text=f'Clear', command=self.clear)
        button.pack(side=tk.LEFT)

        self.listbox = tk.Listbox(self)
        self.listbox.place(in_=self.entry, relx=0, rely=1, anchor=tk.NW)
        self.listbox.place_forget()

        # ------------------------------------------
        fieldset = ttk.LabelFrame(self.frame, text='Students Information')
        fieldset.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N, expand=True, padx=5, pady=5)

        fields = ('ID', 'First Name', 'Middle Name', 'last Name', 'Age')
        columns = [index for index, field in enumerate(fields)]

        self.tree = ttk.Treeview(fieldset, show='headings', columns=columns, selectmode='browse')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for index, field in enumerate(fields):
            self.tree.column(index, minwidth=25, width=120, anchor=tk.E)
            self.tree.heading(index, text=field)

        self.style.configure('Treeview', background='#fff', foreground='#000', fieldbackground='#fff', rowheight=35)
        self.style.map('Treeview', background=[('selected', '#83d160')])

        self.tree.tag_configure('odd', background='#eaf8e6')
        self.tree.tag_configure('even', background='#fff')

        scrollbar = ttk.Scrollbar(fieldset, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        self.refresh()

        # ------------------------------------------
        self.popupmenu1 = Menu(self.tree, tearoff=0)
        self.popupmenu1.add_command(label='Update Account', command=self.save)
        self.popupmenu1.add_command(label='Delete Account', command=self.delete)

        self.popupmenu2 = Menu(self.tree, tearoff=0)
        self.popupmenu2.add_command(label='Create Account', command=self.create)

    # INSTANCE METHODS -------------------------
    def create(self):
        self.form = NewForm(self)
        self.form.grab_set()

    def save(self):
        selected_row = self.tree.item(self.tree.focus())
        self.id.set(selected_row['values'][0])

        self.form = EditForm(self)
        self.form.grab_set()

    def delete(self):
        selected_row = self.tree.item(self.tree.focus())
        self.id.set(selected_row['values'][0])

        prompt = mb.askyesno('Are you sure?', 'Do you really want to delete this record? This process cannot be undone.')
        if prompt:
            print(self.crud.delete(self.id.get()))
            self.refresh()
            self.id.set('')
        else:
            return

    def clear(self):
        self.search.set('')
        self.listbox.place_forget()
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for index, record in enumerate(self.crud.find_all_by_order('id', 'DESC')):
            if (index % 2) == 0:
                self.tree.insert(parent='', index=tk.END, iid=index, text='', tags=('even',), values=(record['id'], record['first_name'], record['middle_name'], record['last_name'], record['age']))
            else:
                self.tree.insert(parent='', index=tk.END, iid=index, text='', tags=('odd',), values=(record['id'], record['first_name'], record['middle_name'], record['last_name'], record['age']))

    def result(self):
        self.tree.delete(*self.tree.get_children())
        for index, record in enumerate(self.crud.search_by_order('last_name', 'id', self.search.get(), 'DESC')):
            if (index % 2) == 0:
                self.tree.insert(parent='', index=tk.END, iid=index, text='', tags=('even',), values=(record['id'], record['first_name'], record['middle_name'], record['last_name'], record['age']))
            else:
                self.tree.insert(parent='', index=tk.END, iid=index, text='', tags=('odd',), values=(record['id'], record['first_name'], record['middle_name'], record['last_name'], record['age']))

    def export(self):
        with open('students.csv', 'w', newline='') as file:
            w = csv.writer(file, dialect='excel')

            for line in self.tree.get_children():
                w.writerow(self.tree.item(line)['values'])

    # EVENTS -----------------------------------
    def show_popupmenu1(self, event):
        self.popupmenu1.post(event.x_root, event.y_root)

    def show_popupmenu2(self, event):
        if len(self.tree.selection()) > 0:
            self.tree.selection_remove(self.tree.selection()[0])

        self.popupmenu2.post(event.x_root, event.y_root)

    def remove_listbox(self, event):
        self.listbox.place_forget()

    def show_auto_suggest(self, event):
        self.listbox.delete(0, tk.END)

        if self.search.get() == '':
            self.listbox.place_forget()
        else:
            for line in self.crud.search_v1('last_name', self.search.get()):
                self.listbox.insert(tk.END, f"{line['last_name'].title()}, {line['first_name'].title()} {line['middle_name'][0].title()}.")

                self.listbox.place(in_=self.entry, relx=0, rely=1, anchor=tk.NW)


#===========================
# Start GUI
#===========================

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()