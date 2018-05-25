"""

A JSON viewer using pure python

author: Atsushi Sakai (@Atsushi_twi)

"""

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import json


class JSONTreeFrame(ttk.Frame):

    def __init__(self, master, path=os.curdir):
        super().__init__(master)
        self.create_widgets()

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
            node = self.tree.insert(node, 'end', text=value, open=False)
        else:
            for (key, value) in value.items():
                self.insert_node(node, key, value)

    def select_json_file(self, event=None):
        file_path = filedialog.askopenfilename(
            initialdir="~/", filetypes=[("JSON files", "*.json")])
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


def main():
    print(__file__ + " start!!")

    root = tk.Tk()
    root.title('PyJSONViewer')
    root.geometry("500x500")
    menubar = tk.Menu(root)
    app = JSONTreeFrame(root)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=app.select_json_file)
    menubar.add_cascade(label="File", menu=filemenu)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.config(menu=menubar)
    root.mainloop()


if __name__ == '__main__':
    main()
