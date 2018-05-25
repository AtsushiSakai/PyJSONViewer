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
        """初期化

        args:
            master: 親ウィジェット
            path: どのパスを起点にツリーを作るか。デフォルトはカレント

        """
        super().__init__(master)
        self.root_path = os.path.abspath(path)
        self.nodes = {}
        self.create_widgets()

    def create_widgets(self):
        """ウィジェットの作成"""
        self.tree = ttk.Treeview(self)

        # configure scroll
        ysb = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)

        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        ysb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ディレクトリを開いた際と、ダブルクリック(ファイル選択)を関連付け
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        #  self.tree.bind('<Double-1>', self.choose_file)

        # ルートのパスを挿入
        #  self.insert_node('', self.root_path, self.root_path)

    def insert_node(self, parent, text):
        """Treeviewにノードを追加する

        args:
            parent: 親ノード
            text: 表示するパス名
            abspath: 絶対パス

        """
        # まずノードを追加する
        node = self.tree.insert(parent, 'end', text=text, open=False)

        self.nodes[node] = (False)
        # ディレクトリならば、空の子要素を追加し開けるようにしておく
        #  if os.path.isdir(abspath):
        #  self.tree.insert(node, 'end')
        #  self.nodes[node] = (False, abspath)
        #  else:
        #  self.nodes[node] = (True, abspath)

    def open_node(self, event):
        """ディレクトリを開いた際に呼び出される

        self.nodes[node][0]がFalseの場合はまだ開かれたことがないと判断し、
        そのディレクトリ内のパスを追加する
        一度開いたか、又はファイルの場合はself.nodes[node][0]はTrueになります

        """
        node = self.tree.focus()
        already_open, abspath = self.nodes[node]

        # まだ開かれたことのないディレクトリならば
        if not already_open:

            # 空白の要素が追加されているので、消去
            self.tree.delete(self.tree.get_children(node))

            # ディレクトリ内の全てのファイル・ディレクトリを取得し、Treeviewに追加
            for entry in os.scandir(abspath):
                self.insert_node(
                    node, entry.name, os.path.join(abspath, entry.path)
                )

            # 一度開いたディレクトリはTrueにする
            self.nodes[node] = (True, abspath)

    def choose_file(self, event):
        """ツリーをダブルクリックで呼ばれる"""
        node = self.tree.focus()
        # ツリーのノード自体をダブルクリックしているか?
        if node:
            already_open, abspath = self.nodes[node]
            if os.path.isfile(abspath):
                print(abspath)

    def update_dir(self, event=None):
        """ツリーの一覧を更新する"""
        self.create_widgets()

    def change_dir(self, event=None):
        """ツリーのルートディレクトリを変更する"""
        dir_name = filedialog.askdirectory()
        if dir_name:
            self.root_path = dir_name
            self.create_widgets()

    def select_json_file(self, event=None):
        print("Json file select")
        file_path = filedialog.askopenfilename(
            initialdir="~/", filetypes=[("JSON files", "*.json")])
        self.importjson(file_path)

    def importjson(self, file_path):
        #  print(file_path)
        f = open(file_path)
        data = json.load(f)
        f.close()
        #  print(json.dumps(data, sort_keys=True, indent=4))

        self.insert_nodes(data)

    def insert_nodes(self, data):

        parent = ""

        for d in data:
            self.insert_node(parent, d)
            print(d)


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
    root.bind('<F4>', app.change_dir)
    root.bind('<F5>', app.update_dir)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.config(menu=menubar)
    root.mainloop()


if __name__ == '__main__':
    main()
