<img src="https://github.com/AtsushiSakai/PyJSONViewer/raw/master/img/icon.png" align="right" width="200"/>

# PyJSONViewer
A JSON file data viewer using pure python

[![Downloads](https://pepy.tech/badge/pyjsonviewer)](https://pepy.tech/project/pyjsonviewer)
[![Downloads](https://pepy.tech/badge/pyjsonviewer/month)](https://pepy.tech/project/pyjsonviewer)
[![Downloads](https://pepy.tech/badge/pyjsonviewer/week)](https://pepy.tech/project/pyjsonviewer)

# Gallery

- Mac OS

![img1](https://github.com/AtsushiSakai/PyJSONViewer/raw/master/img/mac.png)

- Windows10

![img1](https://github.com/AtsushiSakai/PyJSONViewer/raw/master/img/windows.png)

- Ubuntu

![img1](https://github.com/AtsushiSakai/PyJSONViewer/raw/master/img/ubuntu.png)


# What is this?

This is a JSON file data viewer based on python.

It only uses built-in libraries of python (tkinter, json).

Features:

1. Minimum dependency. 

2. Multi-platform (Mac, Windows, Linux).

3. Easy to use.


# Requirements

- Python 3.6.x or higher

# Download

>$ pip install PyJSONViewer

or download as zip.

- [PyJSONViewer · PyPI](https://pypi.org/project/PyJSONViewer/)

# How to use

## Select JSON file with CUI.

1. Run pyjsonviewer with -f option and the path to a JSON file:

> $ pyjsonviewer -f path\_to\_json\_file/sample.json

2. JSON data tree will be shown.

## Select JSON file with GUI.

1. Run pyjsonviewer

> $ pyjsonviewer

2. File-\>Open and then select json file.

3. JSON data tree will be shown.

You can set initial directory:

> $ pyjsonviewer -d path\_to\_json\_file\_dir

## Select JSON file from history.

1. Run pyjsonviewer.py

2. File-\>"Open from history" and then double click a json file path from the list.

![img1](https://github.com/AtsushiSakai/PyJSONViewer/raw/master/img/history.png)

3. JSON data tree will be shown.

## Select JSON file with drag and drop.

1. Run pyjsonviewer.py with the option -o

> $ python pyjsonviewer.py -o path\_to\_json\_file\_dir

2. File browser is shown.

3. You can drag and drop a JSON file to the file browser.

## Menu bar function

- Expand all items: Tools -> Expand all

- Collapse all items: Tools -> Collapse all

- Show version: Help -> About

- Show github page: Help -> GitHub page

- Show release note: Help -> Release note

## Vimrc setting

If you are a vim user, you can set this command in your vimrc.

	"JSON format
	function! JsonFormat()
		%!python -m json.tool
	endfunction
	command! JsonFormat :call JsonFormat()

	"JSON viewer
	function! JsonViewer()
		"%!python -m pyjsonviewer -f % > /dev/null
  		let filename = expand('%')
		let s:job = job_start(
		\   ["/bin/sh", "-c", "python -m pyjsonviewer -f".filename],{})
	endfunction
	command! JsonViewer :call JsonViewer()

When you are editing a json file with vim,

you can open it using PyJSONViewer with

>: JSONViewer()

You can also format json file with

>: JSONFormat()

# Open a link with a browser

If a URL is included in a json file,

you can open it with a browser with double click the URL.

# License 

MIT

# Author

- [Atsushi Sakai](https://github.com/AtsushiSakai/) ([@Atsushi_twi](https://twitter.com/Atsushi_twi))

