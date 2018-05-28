"""

A JSON viewer using pure python

author: Atsushi Sakai (@Atsushi_twi)

"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import json
import argparse
from tkinter import messagebox

MAX_N_ITEM = 20

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

    def importjson(self, file_path):
        f = open(file_path)
        data = json.load(f)
        f.close()

        self.delte_all_nodes()
        self.insert_nodes(data)

    def delte_all_nodes(self):
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
    parser.add_argument('-d', '--dir', type=str, help='JSON file directory')
    args = parser.parse_args()

    root = tk.Tk()
    root.title('PyJSONViewer')
    root.geometry("500x500")
    menubar = tk.Menu(root)
    app = JSONTreeFrame(root, jsonpath=args.file, initialdir=args.dir)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=app.select_json_file)
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
