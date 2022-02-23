__version__ = '0.0.1'

import pyperclip


def get_clipboard_data():
	return pyperclip.paste()
	
def set_clipboard_data(data):
	return pyperclip.copy(data)
	
