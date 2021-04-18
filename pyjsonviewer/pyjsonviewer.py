"""

A JSON viewer using pure python

author: Atsushi Sakai (@Atsushi_twi)

"""

import argparse
import json
import os
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from tkinter import filedialog, Tk
from tkinter import font
from tkinter import messagebox
from urllib.parse import urlparse


def get_version(project_dir):
    try:
        version = open(project_dir + "/VERSION", "r").readline()
    except FileNotFoundError:
        version = "unknown"
    return version


# === Config ===
MAX_N_SHOW_ITEM = 300
MAX_HISTORY = 10
FILETYPES = [("JSON files", "*.json"), ("All Files", "*.*")]
HISTORY_FILE_PATH = os.path.join(os.path.expanduser('~'),
                                 ".pyjsonviewer_history")
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION = get_version(PROJECT_DIR)


class JSONTreeFrame(ttk.Frame):
    class Listbox(tk.Listbox):
        """
            auto width list box container
        """

        def auto_width(self, max_width):
            f = font.Font(font=self.cget("font"))
            pixels = 0
            for item in self.get(0, "end"):
                pixels = max(pixels, f.measure(item))
            # bump listbox size until all entries fit
            pixels = pixels + 10
            width = int(self.cget("width"))
            for w in range(0, max_width + 1, 5):
                if self.winfo_reqwidth() >= pixels:
                    break
                self.config(width=width + w)

    def __init__(self, master, json_path=None, initial_dir="~/"):
        super().__init__(master)
        self.master = master
        self.tree = ttk.Treeview(self)
        self.create_widgets()
        self.sub_win = None
        self.initial_dir = initial_dir
        self.search_box = None
        self.bottom_frame = None
        self.search_box = None
        self.search_label = None

        if json_path:
            self.set_table_data_from_json(json_path)

    def create_widgets(self):
        self.tree.bind('<Double-1>', self.click_item)

        ysb = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)

        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        ysb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def init_search_box(self):
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.search_label = tk.Label(self.bottom_frame, text="Search:")
        self.search_label.pack(side=tk.LEFT)

        self.search_box = tk.Entry(self.bottom_frame)
        self.search_box.pack(fill='x')
        self.search_box.bind('<Key>', self.find_word)

    def insert_node(self, parent, key, value):
        node = self.tree.insert(parent, 'end', text=key, open=False)

        if value is None:
            return

        if type(value) is not dict:
            if type(value) is list:
                value = value[0:MAX_N_SHOW_ITEM]
                value = "[" + ",".join(map(str, value)) + "]"
            self.tree.insert(node, 'end', text=value, open=False)
        else:
            for (key, value) in value.items():
                self.insert_node(node, key, value)

    def click_item(self, event=None):
        """
        Callback function when an item is clicked

        :param event: event arg (not used)
        """
        item_id = self.tree.selection()
        item_text = self.tree.item(item_id, 'text')

        if self.is_url(item_text):
            webbrowser.open(item_text)

    def select_json_file(self, event=None):
        """
        :param event: event arg (not used)
        """
        file_path = filedialog.askopenfilename(
            initialdir=self.initial_dir,
            filetypes=FILETYPES)
        self.set_table_data_from_json(file_path)

    def expand_all(self, event=None):
        """
        :param event: event arg (not used)
        """
        for item in self.get_all_children(self.tree):
            self.tree.item(item, open=True)

    def collapse_all(self, event=None):
        """
        :param event: event arg (not used)
        """
        for item in self.get_all_children(self.tree):
            self.tree.item(item, open=False)

    def find_window(self, event=None):
        """
        :param event: event arg (not used)
        """
        self.search_box = tk.Entry(self.master)
        self.search_box.pack()
        self.search_box.bind('<Key>', self.find_word)

    def find_word(self, event=None):
        """
        :param event: event arg (not used)
        """
        search_text = self.search_box.get()
        self.find(search_text)

    def find(self, search_text):
        if not search_text:
            return
        self.collapse_all(None)
        for item_id in self.get_all_children(self.tree):
            item_text = self.tree.item(item_id, 'text')
            if search_text.lower() in item_text.lower():
                self.tree.see(item_id)

    def get_all_children(self, tree, item=""):
        children = tree.get_children(item)
        for child in children:
            children += self.get_all_children(tree, child)
        return children

    def select_listbox_item(self, event):
        """
        :param event: event arg (not used)
        """
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.set_table_data_from_json(value)
        self.sub_win.destroy()  # close window

    def select_json_file_from_history(self, event=None):
        """
        :param event: event arg (not used)
        """
        self.sub_win = tk.Toplevel()
        lb = self.Listbox(self.sub_win)
        with open(HISTORY_FILE_PATH) as f:
            lines = self.get_unique_list(reversed(f.readlines()))
            for ln, line in enumerate(lines):
                lb.insert(ln, line.replace("\n", ""))
        lb.bind('<Double-1>', self.select_listbox_item)
        maximum_width = 250
        lb.auto_width(maximum_width)
        lb.pack()

    def save_json_history(self, file_path):
        lines = []
        try:
            with open(HISTORY_FILE_PATH, "r") as f:
                lines = self.get_unique_list(f.readlines())
        except FileNotFoundError:
            print("created:" + HISTORY_FILE_PATH)

        lines.append(file_path)

        with open(HISTORY_FILE_PATH, "w") as f:
            lines = lines[max(0, len(lines) - MAX_HISTORY):]
            for line in lines:
                f.write(line.replace("\n", "") + "\n")

    def set_table_data_from_json(self, file_path):
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

    def open_github_page(self):
        self.open_url("https://github.com/AtsushiSakai/PyJSONViewer")

    def open_release_note(self):
        self.open_url(
            "https://github.com/AtsushiSakai/PyJSONViewer/blob/master"
            "/pyjsonviewer/CHANGELOG.md")

    def open_url(self, url):
        if self.is_url(url):
            webbrowser.open(url)
        else:
            print("Error: this is not url:", url)

    @staticmethod
    def is_url(text):
        """check input text is url or not

        :param text: input text
        :return: url or not
        """
        parsed = urlparse(text)
        return all([parsed.scheme, parsed.netloc, parsed.path])

    @staticmethod
    def get_unique_list(seq):
        seen = []
        return [x for x in seq if x not in seen and not seen.append(x)]

    @staticmethod
    def load_json_data(file_path):
        with open(file_path, encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def show_info_window():
        msg = """
        PyJSONViewer
        by Atsushi Sakai(@Atsushi_twi)
        Ver.""" + VERSION + """\n
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

    root: Tk = tk.Tk()
    root.title('PyJSONViewer')
    root.geometry("500x500")
    root.tk.call('wm', 'iconphoto', root._w,
                 tk.PhotoImage(file=PROJECT_DIR + '/icon.png'))
    menubar = tk.Menu(root)

    if args.open:
        args.file = filedialog.askopenfilename(
            initialdir=args.dir,
            filetypes=FILETYPES)

    app = JSONTreeFrame(root, json_path=args.file, initial_dir=args.dir)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open", accelerator='Ctrl+O',
                          command=app.select_json_file)
    file_menu.add_command(label="Open from History", accelerator='Ctrl+H',
                          command=app.select_json_file_from_history)
    menubar.add_cascade(label="File", menu=file_menu)

    tool_menu = tk.Menu(menubar, tearoff=0)
    tool_menu.add_command(label="Expand all",
                          accelerator='Ctrl+E', command=app.expand_all)
    tool_menu.add_command(label="Collapse all",
                          accelerator='Ctrl+L', command=app.collapse_all)
    menubar.add_cascade(label="Tools", menu=tool_menu)

    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=app.show_info_window)
    help_menu.add_command(label="Show GitHub page",
                          command=app.open_github_page)
    help_menu.add_command(label="Show release note",
                          command=app.open_release_note)
    menubar.add_cascade(label="Help", menu=help_menu)

    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    app.init_search_box()

    root.config(menu=menubar)
    root.bind_all("<Control-o>", lambda e: app.select_json_file(event=e))
    root.bind_all("<Control-h>",
                  lambda e: app.select_json_file_from_history(event=e))
    root.bind_all("<Control-e>", lambda e: app.expand_all(event=e))
    root.bind_all("<Control-l>", lambda e: app.collapse_all(event=e))

    root.mainloop()


if __name__ == '__main__':
    main()
