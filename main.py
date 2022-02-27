import wx
import wx.adv
import yaml
from lib import clipboard

TRAY_TOOLTIP = 'System Tray Demo'
ID_MENU_ABOUT = 1025
TRANSLATE_EVENTS_START = 2000


__version__ = '0.0.1'


def ShowAbout(event):
	dialog = wx.MessageDialog(None, "Создал Pavlov Artemiy", caption="О программе", style=wx.OK|wx.CENTRE, pos=wx.DefaultPosition)
	dialog.ShowModal()
	

def onExit(event):
	wx.Exit()


def Translete(event):
	text = clipboard.get_clipboard_data()
	text_array = list(text)
	dictionary = encoding_translate_config[event.GetId() - TRANSLATE_EVENTS_START]["dictionary"]
	
	print(text_array)
	
	for i in range(len(text_array)):
		if text_array[i] in dictionary:
			text_array[i] = dictionary[text_array[i]]
			
	text = "".join(text_array)
	
	clipboard.set_clipboard_data(text)
	
	
	
	print(text)



class MyTaskBarIcon(wx.adv.TaskBarIcon):
	def __init__(self):
		 super().__init__()
		 
	def CreatePopupMenu(self):
		menu = wx.Menu()
		
		for i in range(len(encoding_translate_config)):
			menu.Append(TRANSLATE_EVENTS_START + i, encoding_translate_config[i]["title"], "")
			self.Bind(wx.EVT_MENU, Translete, id=TRANSLATE_EVENTS_START + i)
			
		menu.Append(wx.ID_SEPARATOR, '', "")
		menu.Append(ID_MENU_ABOUT, 'О программе', "")
		menu.Append(wx.ID_EXIT, 'Выход', "")
		self.Bind(wx.EVT_MENU, onExit, id=wx.ID_EXIT)
		self.Bind(wx.EVT_MENU, ShowAbout, id=ID_MENU_ABOUT)		
		
		return menu


app = wx.App(False)

crutch = wx.Frame(None, -1, "")

#TODO change dir to this script dir

sys_tray =  MyTaskBarIcon()
icon = wx.Icon(wx.Bitmap("./assets/icon.png")) 
sys_tray.SetIcon(icon, TRAY_TOOLTIP)
#sys_tray.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, showInfoMenu)


print(clipboard.get_clipboard_data())


try:
	with open("./assets/sw_templates.yml", "r", encoding="utf8") as fh:
		encoding_translate_config = yaml.safe_load(fh)
		#TODO if codepage in encoding_translate_config[i]
except FileNotFoundError:
	None
except Exception as e:
	print(str(e))
	dialog = wx.MessageDialog(None, "Неудалось запустить программу. Код ошибки: " + str(e), caption="Error", style=wx.OK|wx.CENTRE|wx.ICON_ERROR, pos=wx.DefaultPosition)
	dialog.ShowModal()
	


app.MainLoop()
