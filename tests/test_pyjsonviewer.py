#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for Pyjsonviewer."""

import sys
import traceback
sys.path.insert(0, "../pyjsonviewer")
import tkinter as tk
from pyjsonviewer import JSONTreeFrame


def test_dictionary_file():
    """
    should read dictionary file okay
    """
    # given
    root: Tk = tk.Tk()
    app = JSONTreeFrame(root, json_path="../dat/dictionary.json")

    # when
    children = app.get_all_children(app.tree)
    # print([app.tree.item(item_id, 'text') for item_id in children])

    # then
    assert len(children) == 53


def test_list_file():
    """
    should read list file okay
    """
    # given
    root: Tk = tk.Tk()
    app = JSONTreeFrame(root, json_path="../dat/list.json")

    # when
    children = app.get_all_children(app.tree)
    # print([app.tree.item(item_id, 'text') for item_id in children])

    # then
    assert len(children) == 18


def test_nested_file():
    """
    should read list file okay
    """
    # given
    root: Tk = tk.Tk()
    app = JSONTreeFrame(root, json_path="../dat/nested.json")

    # when
    children = app.get_all_children(app.tree)
    print([app.tree.item(item_id, 'text') for item_id in children])

    # then
    assert len(children) == 72


def test_search():
    """
       search should not break in case of numeric fields
    """
    # given
    root: Tk = tk.Tk()
    app = JSONTreeFrame(root, json_path="../dat/list.json")


    try:
        x = app.find("fuzzy")
    except AttributeError as err:
        # AttributeError: 'int' object has no attribute 'lower'
        assert False
    assert True

