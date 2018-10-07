"""

A JSON viewer using pure python

author: Atsushi Sakai (@Atsushi_twi)

"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import json
import os
import argparse
from tkinter import messagebox

MAX_N_ITEM = 300

HISTORY_FILE_PATH = os.path.expanduser('~') + "/.pyjsonviewer_history"


class JSONTreeFrame(ttk.Frame):

    def __init__(self, master, jsonpath=None, initialdir="~/"):
        super().__init__(master)
        self.create_widgets()
        self.initialdir = initialdir

        if jsonpath:
            self.importjson(jsonpath)

    def create_widgets(self):
        self.tree = ttk.Treeview(self)

        ysb = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)

        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        ysb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def insert_node(self, parent, key, value):
        node = self.tree.insert(parent, 'end', text=key, open=False)

        if value is None:
            return

        if type(value) is not dict:
            if type(value) is list:
                value = value[0:MAX_N_ITEM]
            node = self.tree.insert(node, 'end', text=value, open=False)
        else:
            for (key, value) in value.items():
                self.insert_node(node, key, value)

    def select_json_file(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.initialdir, filetypes=[("JSON files", "*.json")])
        self.importjson(file_path)

    def get_unique_list(self, seq):
        seen = []
        return [x for x in seq if x not in seen and not seen.append(x)]

    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
        self.importjson(value)
        self.sub_win.destroy()  # close window

    def select_json_file_from_history(self):
        self.sub_win = tk.Toplevel()
        lb = tk.Listbox(self.sub_win, width=100)
        with open(HISTORY_FILE_PATH) as f:
            lines = self.get_unique_list(reversed(f.readlines()))
            for ln, line in enumerate(lines):
                lb.insert(ln, line.replace("\n", ""))
        lb.bind('<Double-1>', self.onselect)
        lb.pack()

    def save_json_history(self, file_path):
        with open(HISTORY_FILE_PATH, "a") as f:
            f.write(file_path + '\n')

    def load_json_data(self, file_path):
        with open(file_path) as f:
            return json.load(f)

    def importjson(self, file_path):

        data = self.load_json_data(file_path)
        self.save_json_history(file_path)
        self.delete_all_nodes()
        self.insert_nodes(data)

    def delete_all_nodes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def insert_nodes(self, data):
        parent = ""

        for (key, value) in data.items():
            self.insert_node(parent, key, value)

    def showinfo(self):
        msg = """
        PyJSONViewer
        by Atsushi Sakai(@Atsushi_twi)
        Ver.1.0
        GitHub:https://github.com/AtsushiSakai/PyJSONViewer
        """
        messagebox.showinfo("About", msg)


def main():
    print(__file__ + " start!!")

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='JSON file path')
    parser.add_argument('-d', '--dir', type=str,
                        help='JSON file directory')
    parser.add_argument('-o', '--open', action='store_true',
                        default=False, help='Open with finder')
    args = parser.parse_args()

    root = tk.Tk()
    root.title('PyJSONViewer')
    root.geometry("500x500")
    menubar = tk.Menu(root)

    if args.open:
        args.file = filedialog.askopenfilename(
            initialdir=args.dir,
            filetypes=[("JSON files", "*.json")])

    app = JSONTreeFrame(root, jsonpath=args.file, initialdir=args.dir)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=app.select_json_file)
    filemenu.add_command(label="Open from History",
                         command=app.select_json_file_from_history)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=app.showinfo)
    menubar.add_cascade(label="Help", menu=helpmenu)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.config(menu=menubar)
    root.mainloop()


if __name__ == '__main__':
    main()
