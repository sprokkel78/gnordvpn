import subprocess
import socket
import sys
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
from threading import Thread
from time import sleep

# VERSION = 1.1.14
ver = "1.1.14"


# TODO


# GLOBALS
pause = 0
TPL = 0
MES = 0
sens = 0
selected_file = ""

# CHECK IF THE NORDVPN COMMANDLINE TOOL IS INSTALLED
file = "/usr/bin/nordvpn"
if os.path.exists(file):
	print("Found the nordvpn binary. (CONTINUE)")
else:
	print("Can't find the nordvpn binary. It should be in /usr/bin/ (EXIT)")
	sys.exit(0)


# CHECK IF YOU'RE LOGGED INTO NORDVPN
print("Checking if you are logged in to nordvpn. Please wait.")
status = subprocess.Popen("/usr/bin/nordvpn login", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
							universal_newlines=True)
rcstat = status.wait()
statout, staterr = status.communicate()
statout = statout.strip('\n')

if "already" in statout:
	print("You are logged in to nordvpn. (CONTINUE)")
else:
	print(statout)
	print("You are not logged in to nordvpn. Please log in to nordvpn first.(EXIT)")
	sys.exit(0)


# GUI SIGNAL HANDLER FUNCTIONS

def Stop_Application(obj):
	Gtk.main_quit()
	sys.exit(0)


def Key_Event(obj, event):
	if event.keyval == Gdk.KEY_q and event.state & Gdk.ModifierType.CONTROL_MASK:
		Gtk.main_quit()
		sys.exit(0)

	if event.keyval == Gdk.KEY_m and event.state & Gdk.ModifierType.CONTROL_MASK:
		win.iconify()

		
def Button_Connect_Clicked(obj):
	item = combobox1.get_model()[combobox1.get_active()]
	if item[0] != "Select Country  ":
		status = subprocess.Popen("/usr/bin/nordvpn c " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	else:
		status = subprocess.Popen("/usr/bin/nordvpn c", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()


def Button_Disconnect_Clicked(obj):
	status = subprocess.Popen("/usr/bin/nordvpn d", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	rcstat = status.wait()


def Technology_Changed(obj):
	item = combobox2.get_model()[combobox2.get_active()]
	# print("technology changed" + " to " + item[0])
	if item[0] != "Technology    ":
		status = subprocess.Popen("/usr/bin/nordvpn set technology " + item[0], shell=True,
			stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	combobox2.set_active(0)


def Protocol_Changed(obj):
	item = combobox3.get_model()[combobox3.get_active()]
	# print("protocol changed" + " to " + item[0])
	if item[0] != "Protocol      ":
		status = subprocess.Popen("/usr/bin/nordvpn set protocol " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	combobox3.set_active(0)


def Routing_Changed(obj):
	item = combobox51.get_model()[combobox51.get_active()]
	if item[0] != "Routing       ":
		routing = subprocess.Popen("/usr/bin/nordvpn set routing " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = routing.wait()
	combobox51.set_active(0)


def Killswitch_Changed(obj):
	item = combobox4.get_model()[combobox4.get_active()]
	#print("killswitch changed" + " to " + item[0])
	if item[0] != "Kill Switch   ":
		status = subprocess.Popen("/usr/bin/nordvpn set killswitch " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	combobox4.set_active(0)


def Connect_Changed(obj):
	item = combobox3a.get_model()[combobox3a.get_active()]
	if item[0] != "Auto-Connect  ":
		status = subprocess.Popen("/usr/bin/nordvpn set autoconnect " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	combobox3a.set_active(0)


def Notify_Changed(obj):
	item = combobox4a.get_model()[combobox4a.get_active()]
	if item[0] != "Notification  ":
		status = subprocess.Popen("/usr/bin/nordvpn set notify " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	combobox4a.set_active(0)



def Analytics_Changed(obj):
	item = combobox6a.get_model()[combobox6a.get_active()]
	if item[0] != "Analytics      ":
		status = subprocess.Popen("/usr/bin/nordvpn set analytics " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	combobox6a.set_active(0)


def IPV6_Changed(obj):
	item = combobox6b.get_model()[combobox6b.get_active()]
	if item[0] != "IPV6           ":
		status = subprocess.Popen("/usr/bin/nordvpn set ipv6 " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	combobox6b.set_active(0)


def Lan_Discovery_Changed(obj):
	item = combobox6c.get_model()[combobox6c.get_active()]
	if item[0] != "Lan Discovery  ":
		status = subprocess.Popen("/usr/bin/nordvpn set lan-discovery " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	combobox6c.set_active(0)


def TPL_Changed(obj):
	if button_tpl.get_active() == 0:
		label_tpl_status.set_text("Disabled")
		status = subprocess.Popen("/usr/bin/nordvpn set threatprotectionlite disable", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	if button_tpl.get_active() == 1:
		label_tpl_status.set_text("Enabled")
		status = subprocess.Popen("/usr/bin/nordvpn set threatprotectionlite enable ", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()


def Update_TextView(st):
	global pause

	if pause == 0:
		tbuffer.set_text("\n  " + st)


def Get_Nordvpn_Status():
	i = 1
	while i != 0:
		txt = ""
		y = 0
		status = subprocess.Popen("/usr/bin/nordvpn status", shell=True, stdout=subprocess.PIPE,
								stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		statout, staterr = status.communicate()
		statout = statout.strip('\n')
		lstatus = statout.split('\n')
		for st in lstatus:
			if st != "\r" and st != "-" and st != "/" and st != "\\" and st != "|" and st != "\n":
				if st != "":
					txt = txt + "\n  " + st

		status = subprocess.Popen("/usr/bin/nordvpn settings", shell=True, stdout=subprocess.PIPE,
								stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		statout, staterr = status.communicate()
		statout = statout.strip('\n')
		lsettings = statout.split('\n')

		while y < len(lsettings):
			if "Routing" in lsettings[y]:
				txt = txt + "\n  ------\n  " + lsettings[y] + "\n"
			y = y + 1
		y = 0

		while y < len(lsettings):
			if "Kill" in lsettings[y]:
				txt = txt + "  " + lsettings[y] + "\n"
			y = y + 1
		y = 0

		while y < len(lsettings):
			if "Auto" in lsettings[y]:
				txt = txt + "  " + lsettings[y] + "\n"
			y = y + 1
		y = 0

		while y < len(lsettings):
			if "Notify" in lsettings[y]:
				txt = txt + "  " + lsettings[y] + "\n"
			y = y + 1
		y = 0

		while y < len(lsettings):
			if "Analytics" in lsettings[y]:
				txt = txt + "  " + lsettings[y] + "\n"
			y = y + 1
		y = 0

		while y < len(lsettings):
			if "IPv6" in lsettings[y]:
				txt = txt + "  " + lsettings[y] + "\n"
			y = y + 1
		y = 0

		while y < len(lsettings):
			if "LAN" in lsettings[y]:
				txt = txt + "  " + lsettings[y] + "\n"
			y = y + 1
		y = 0

		global TPL

		while y < len(lsettings):
			if "Lite" in lsettings[y]:
				if "enabled" in lsettings[y]:
					TPL = 1
				else:
					TPL = 0
			y = y + 1
		y = 0

		global MES

		while y < len(lsettings):
			if "Meshnet" in lsettings[y]:
				if "enabled" in lsettings[y]:
					MES = 1

			y = y + 1
		y = 0

		txt = txt.strip()
		GLib.idle_add(Update_TextView, txt)

		if TPL == 0:
			button_tpl.set_active(0)
			label_tpl_status.set_text("Disabled")
		else:
			button_tpl.set_active(1)
			label_tpl_status.set_text("Enabled")

		global sens

		if MES == 0:
			button_mes.set_active(0)
			label_mes_status.set_text("Disabled")
			button_mes.set_sensitive(1)
			label_mes_status.set_sensitive(1)
			button_fsi.set_sensitive(0)
			label_fs.set_sensitive(0)
			label_fss.set_sensitive(0)
			label_fsi.set_sensitive(0)
			entry_fsi.set_sensitive(0)
			label_send_file.set_sensitive(0)
			entry_send_file.set_sensitive(0)
			button_send_file.set_sensitive(0)
			label_host.set_sensitive(0)
			entry_host.set_sensitive(0)
			button_send_host.set_sensitive(0)

			if sens == 0:
				button_fs_list.set_sensitive(0)
				button_device.set_sensitive(0)

		else:
			MES = 1
			button_mes.set_active(1)
			label_mes_status.set_text("Enabled")
			button_mes.set_sensitive(1)
			label_mes_status.set_sensitive(1)
			button_fsi.set_sensitive(1)
			label_fs.set_sensitive(1)
			label_fss.set_sensitive(1)
			label_fsi.set_sensitive(1)
			entry_fsi.set_sensitive(1)
			label_send_file.set_sensitive(1)
			entry_send_file.set_sensitive(1)
			button_send_file.set_sensitive(1)
			label_host.set_sensitive(1)
			entry_host.set_sensitive(1)
			button_send_host.set_sensitive(1)

			if sens == 1:
				button_device.set_sensitive(1)
				button_fs_list.set_sensitive(1)

		sleep(4)


def MES_Changed(obj):
	global MES
	global pause

	if button_mes.get_active() == 0:
		label_mes_status.set_text("Disabled")
		button_device.set_sensitive(0)
		button_fs_list.set_sensitive(0)
		button_fsi.set_sensitive(0)
		label_fs.set_sensitive(0)
		label_fss.set_sensitive(0)
		label_fsi.set_sensitive(0)
		entry_fsi.set_sensitive(0)
		label_send_file.set_sensitive(0)
		entry_send_file.set_sensitive(0)
		button_send_file.set_sensitive(0)
		label_host.set_sensitive(0)
		entry_host.set_sensitive(0)
		button_send_host.set_sensitive(0)

		status = subprocess.Popen("/usr/bin/nordvpn set meshnet off", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		MES = 0
		if pause == 1:
			pause = 0
			button_device.set_label("Show Devices")
			button_fs_list.set_label("   Show List   ")
			
	if button_mes.get_active() == 1:
		status = subprocess.Popen("/usr/bin/nordvpn set meshnet on", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		out,err = status.communicate()
		split_out = out.split("\\n")
		y = 0
		x = 0
		while y < len(split_out):
			if "enabled" in split_out[y]:
				x = 1
			y = y + 1

			if x == 1:
				MES = 1
				label_mes_status.set_text("Enabled")
				button_mes.set_active(1)
				button_device.set_sensitive(1)
				button_fs_list.set_sensitive(1)
				button_fsi.set_sensitive(1)
				label_fs.set_sensitive(1)
				label_fss.set_sensitive(1)
				label_fsi.set_sensitive(1)
				entry_fsi.set_sensitive(1)
				label_send_file.set_sensitive(1)
				entry_send_file.set_sensitive(1)
				button_send_file.set_sensitive(1)
				label_host.set_sensitive(1)
				entry_host.set_sensitive(1)
				button_send_host.set_sensitive(1)

			else:
				MES = 0
				label_mes_status.set_text("Disabled")
				button_mes.set_active(0)
				button_fs_list.set_sensitive(0)
				button_fsi.set_sensitive(0)
				label_fs.set_sensitive(0)
				label_fss.set_sensitive(0)
				label_fsi.set_sensitive(0)
				entry_fsi.set_sensitive(0)
				label_send_file.set_sensitive(0)
				entry_send_file.set_sensitive(0)
				button_send_file.set_sensitive(0)
				label_host.set_sensitive(0)
				entry_host.set_sensitive(0)
				button_send_host.set_sensitive(0)


def Get_Peer_List():
	sleep(1)
	global MES
	internet = 0

	try:
		host = socket.gethostbyname("www.nordvpn.com")
		if host != "":
			internet = 1
			# print ("Internet")
		else:
			# print ("No Internet")
			internet = 0
	except Exception:
		# print("No Internet")
		internet = 0

	if MES == 1 and internet == 1:

		txtp = "\n"
		status = subprocess.Popen("/usr/bin/nordvpn meshnet peer list", shell=True, stdout=subprocess.PIPE,
					stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		statout, staterr = status.communicate()
		statout = statout.strip('\n')
		lstatus = statout.split('\n')
		for st in lstatus:
			if st != "\r" and st != "-" and st != "/" and st != "\\" and st != "|" and st != "\\n":
				if st != "":
					if "Local Peers" in st:
						txtp = txtp + "\n\n  " + st
					else:
						if "Hostname" in st:
							txtp = txtp + "\n\n  " + st
						else:
							if "External Peers" in st:
								txtp = txtp + "\n\n  " + st
							else:
								txtp = txtp + "\n  " + st
	else:
		txtp = "Can't update peer list. No Connection."

	return(txtp.strip())


def Device_Clicked(obj):
	global MES
	global pause
	global sens

	if MES == 1:
		if pause == 0:
			button_device.set_label("Hide Devices")
			txtp = Get_Peer_List()
			txte = "\n  " + txtp
			tbuffer.set_text(txte)
			button_fs_list.set_sensitive(0)
			sens = 0
		else:
			sleep(3)
			button_device.set_label("Show Devices")
			button_fs_list.set_sensitive(1)
			sens = 1
	if pause == 1:
		pause = 0
	else:
		pause = 1


def Get_File_List():
	sleep(1)
	global MES
	internet = 0

	try:
		host = socket.gethostbyname("www.nordvpn.com")
		if host != "":
			internet = 1
			# print ("Internet")
		else:
			# print ("No Internet")
			internet = 0
	except Exception:
		# print("No Internet")
		internet = 0

	if MES == 1 and internet == 1:

		txtp = "\n"
		status = subprocess.Popen("/usr/bin/nordvpn fileshare list | grep waiting", shell=True, stdout=subprocess.PIPE,
					stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		statout, staterr = status.communicate()
		statout = statout.strip('\n')
		lstatus = statout.split('\n')
		for st in lstatus:
			if st != "\r" and st != "-" and st != "/" and st != "\\" and st != "|" and st != "\\n":
				if st != "":
					txtp = txtp + "\n  " + st

		if txtp == "\n":
			txtp = "No incoming files."
	else:
		txtp = "Can't update file list. No Connection."

	return(txtp.strip())



def FS_Show_List(obj):
	# print("clicked FS LIST")
	global MES
	global pause
	global sens

	if MES == 1:
		if pause == 0:
			button_fs_list.set_label("   Hide List   ")
			txtp = Get_File_List()
			txte = "\n  " + txtp
			tbuffer.set_text(txte)
			button_device.set_sensitive(0)
			sens = 0
		else:
			sleep(3)
			button_fs_list.set_label("   Show List   ")
			button_device.set_sensitive(1)
			sens = 1
	if pause == 1:
		pause = 0
	else:
		pause = 1


def Get_Incoming_Files():
	global MES
	internet = 0
	i = 0
	while i == 0:
		try:
			host = socket.gethostbyname("www.nordvpn.com")
			if host != "":
				internet = 1
				# print ("Internet")
			else:
				# print ("No Internet")
				internet = 0
		except Exception:
			# print("No Internet")
			internet = 0

		if MES == 1 and internet == 1:

			txtp = "\n"
			status = subprocess.Popen("/usr/bin/nordvpn fileshare list | grep waiting | wc -l", shell=True, stdout=subprocess.PIPE,
						stderr=subprocess.PIPE, universal_newlines=True)
			rcstat = status.wait()
			statout, staterr = status.communicate()
			statout = statout.strip('\n')
			lstatus = statout.split('\n')
			for st in lstatus:
				if st != "\r" and st != "-" and st != "/" and st != "\\" and st != "|" and st != "\\n":
					if st != "":
						txtp = txtp + "\n  " + st
		else:
			txtp = "0"

		#print(txtp.strip())
		GLib.idle_add(Update_File_Label, txtp.strip())

		sleep(9)

def Update_File_Label(txtp):
	label_fss.set_text("Incoming (" + txtp + ")")


def Accept_File(obj):
	# print("clicked")
	file_id = entry_fsi.get_text()
	# print(file_id)
	if ";" not in file_id and " " not in file_id and file_id != "":
		try:
			host = socket.gethostbyname("www.nordvpn.com")
			if host != "":
				internet = 1
				# print ("Internet")
			else:
				# print ("No Internet")
				internet = 0
		except Exception:
			# print("No Internet")
			internet = 0

		if internet == 1:
			status = subprocess.Popen("gnome-terminal -- sh -c '/usr/bin/nordvpn fileshare accept " + file_id + "; sleep 5'", shell=True,
									  stdout=subprocess.PIPE,
									  stderr=subprocess.PIPE, universal_newlines=True)
			rcstat = status.wait()

		else:
			dialog = Gtk.MessageDialog(
				parent=None,
				flags=0,
				message_type=Gtk.MessageType.INFO,
				buttons=Gtk.ButtonsType.OK,
				text="gNordVPN\n\nCan't get files. No Connection."
			)
			dialog.run()
			dialog.destroy()

		entry_fsi.set_text("")


def Button_Settings_Clicked(obj):
	box4.show()
	box51.show()
	box6a.show()
	box6b.show()

	box6c.hide()
	box6d.hide()
	box6e.hide()
	box6f.hide()
	box6g.hide()

def Button_Mshnet_Clicked(obj):
	box4.hide()
	box51.hide()
	box6a.hide()
	box6b.hide()

	box6c.show()
	box6d.show()
	box6e.show()
	box6f.show()
	box6g.show()


def Choose_File(obj):
	dialog = Gtk.FileChooserDialog(
		title="Open File",
		parent=None,
		action=Gtk.FileChooserAction.OPEN,
	)

	dialog.add_buttons(
		Gtk.STOCK_CANCEL,
		Gtk.ResponseType.CANCEL,
		Gtk.STOCK_OPEN,
		Gtk.ResponseType.OK
	)
	dialog.show()
	global selected_file

	response = dialog.run()
	if response == Gtk.ResponseType.OK:
		selected_file = dialog.get_filename()
		file_split = selected_file.split("/")
		y = len(file_split)
		x = y - 1
		entry_send_file.set_text(file_split[x])
		# print("Selected file:", selected_file)
	elif response == Gtk.ResponseType.CANCEL:
		# print("Dialog closed")
		selected_file = "";

	dialog.destroy()


def Send_Host(obj):
	global selected_file
	file_id = selected_file
	hostname = entry_host.get_text()
	# print(file_id)
	if ";" not in file_id and file_id != "" and hostname != "" and ";" not in hostname:
		try:
			host = socket.gethostbyname("www.nordvpn.com")
			if host != "":
				internet = 1
				# print ("Internet")
			else:
				# print ("No Internet")
				internet = 0
		except Exception:
			# print("No Internet")
			internet = 0

		if internet == 1 and hostname != "" and ";" not in hostname:
			status = subprocess.Popen("gnome-terminal -- bash -c '/usr/bin/nordvpn fileshare send " + hostname + " " + selected_file + " ; sleep 5'", shell=True,
									  stdout=subprocess.PIPE,
									  stderr=subprocess.PIPE, universal_newlines=True)
			rcstat = status.wait()

		else:
			dialog = Gtk.MessageDialog(
				parent=None,
				flags=0,
				message_type=Gtk.MessageType.INFO,
				buttons=Gtk.ButtonsType.OK,
				text="gNordVPN\n\nCan't send files. No Connection."
			)
			dialog.run()
			dialog.destroy()

		entry_send_file.set_text("")
		selected_file = ""


# MAIN CODE

# CREATE THE MAIN WINDOW
win = Gtk.Window()
win.set_title("gNordVPN " + ver)
win.set_default_size(550, 500)
file = "./gnordvpn.svg"
if os.path.exists(file):
	win.set_default_icon_from_file("./gnordvpn.svg")
# win.set_resizable(False)
win.connect("destroy", Stop_Application)
win.connect("key-press-event", Key_Event)

css_provider = Gtk.CssProvider()
css_provider.load_from_path('./gnordvpn.css')

screen = win.get_screen()
context = win.get_style_context()
context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# CREATE SOME SEPARATORS
sep1 = Gtk.Separator()
sep1.show()
sep2 = Gtk.Separator()
sep2.show()
sep3 = Gtk.Separator()
sep3.show()
sep4 = Gtk.Separator()
sep4.show()
sep5 = Gtk.Separator()
sep5.show()
sep6 = Gtk.Separator()
sep6.show()

# CREATE THE GUI CONTAINER
box1 = Gtk.VBox(spacing=6)
box1.show()
win.add(box1)
boxs = Gtk.Box(spacing=6)
boxs.show()
boxs.pack_start(sep1, True, True, 0)
box1.pack_start(boxs, False, False, 0)
box2 = Gtk.Box(spacing=6)
box2.show()
box1.pack_start(box2, False, False, 0)
boxss = Gtk.Box(spacing=6)
boxss.show()
boxss.pack_start(sep2, True, True, 0)
box1.pack_start(boxss, False, False, 0)
box3 = Gtk.Box(spacing=6)
box3.show()
box1.pack_start(box3, True, True, 0)
box3a = Gtk.Box(spacing=6)
box3a.show()
box1.pack_start(box3a, False, False, 0)
box6ab = Gtk.Box(spacing=6)
box6ab.show()
box6ab.pack_start(sep6, True, True, 0)
box1.pack_start(box6ab, False, False, 0)

# SETTINGS
box4 = Gtk.Box(spacing=6)
box4.show()
box1.pack_start(box4, False, False, 0)
box51 = Gtk.Box(spacing=6)
box51.show()
box1.pack_start(box51, False, False, 0)
box6a = Gtk.Box(spacing=6)
box6a.show()
box1.pack_start(box6a, False, False, 0)
box6b = Gtk.Box(spacing=6)
box6b.show()
box1.pack_start(box6b, False, False, 0)

# MESHNET
box6c = Gtk.Box(spacing=6)
box1.pack_start(box6c, False, False, 0)
box6d = Gtk.Box(spacing=6)
box1.pack_start(box6d, False, False, 0)
box6e = Gtk.Box(spacing=6)
box1.pack_start(box6e, False, False, 0)
box6f = Gtk.Box(spacing=6)
box1.pack_start(box6f, False, False, 0)
box6g = Gtk.Box(spacing=6)
box1.pack_start(box6g, False, False, 0)
box6b4 = Gtk.Box(spacing=6)
box6b4.pack_start(sep5, True, True, 0)
box1.pack_start(box6b4, False, False, 0)
boxsss = Gtk.Box(spacing=6)
boxsss.pack_start(sep3, True, True, 0)
box1.pack_start(boxsss, False, False, 0)

# STATUSBAR EOP
box7 = Gtk.Box(spacing=6)
box7.show()
box7.pack_start(sep4, True, True, 0)
box1.pack_start(box7, False, False, 0)
box8 = Gtk.Box(spacing=6)
box8.show()
box1.pack_start(box8, False, False, 0)

# BUILT USER INTERFACE
label0 = Gtk.Label()
label0.show()
label0.set_width_chars(1)
box2.pack_start(label0, False, False, 0)
label1 = Gtk.Label()
label1.show()
label1.set_text("VPN Connection")
label1.set_width_chars(13)
box2.pack_start(label1, False, False, 0)
label1a = Gtk.Label()
label1a.show()
label1a.set_width_chars(1)
box2.pack_start(label1a, False, False, 0)

liststore1 = Gtk.ListStore(str)
liststore1.append(['Select Country  '])
liststore1.append(['au'])
liststore1.append(['be'])
liststore1.append(['br'])
liststore1.append(['ca'])
liststore1.append(['co'])
liststore1.append(['de'])
liststore1.append(['fi'])
liststore1.append(['fr'])
liststore1.append(['it'])
liststore1.append(['jp'])
liststore1.append(['nl'])
liststore1.append(['no'])
liststore1.append(['nz'])
liststore1.append(['uk'])
liststore1.append(['us'])
liststore1.append(['p2p'])
liststore1.append(['double_vpn'])
liststore1.append(['onion_over_vpn'])

cell = Gtk.CellRendererText()
combobox1 = Gtk.ComboBox()
combobox1.show()
combobox1.pack_start(cell, True)
combobox1.add_attribute(cell, 'text', 0)
combobox1.set_model(liststore1)
combobox1.set_active(0)
box2.pack_start(combobox1, False, False, 0)

button1 = Gtk.Button.new_with_label("  Connect  ")
button1.show()
button1.connect("clicked", Button_Connect_Clicked)
box2.pack_start(button1, False, False, 0)

button2 = Gtk.Button.new_with_label("Disconnect")
button2.show()
button2.connect("clicked", Button_Disconnect_Clicked)
box2.pack_start(button2, False, False, 0)

label2 = Gtk.Label()
label2.show()
box2.pack_start(label2, True, True, 0)

# CREATE THE TEXTVIEW
scrolled_window = Gtk.ScrolledWindow()
scrolled_window.show()
tbuffer = Gtk.TextBuffer()
textview = Gtk.TextView.new_with_buffer(tbuffer)
textview.show()
scrolled_window.set_size_request(350, 330)
textview.set_name("textview")
textview.set_buffer(tbuffer)
textview.set_editable(False)
textview.set_wrap_mode(Gtk.WrapMode.NONE)
scrolled_window.add(textview)
box3.pack_start(scrolled_window, True, True, 0)

label_buttons = Gtk.Label()
label_buttons.show()
label_buttons.set_width_chars(1)
box3a.pack_start(label_buttons, False, False, 0)
button_settings = Gtk.Button.new_with_label("Settings")
button_settings.set_size_request(138, -1)
button_settings.connect("clicked", Button_Settings_Clicked)
button_settings.show()
button_mshnet = Gtk.Button.new_with_label("Meshnet")
button_mshnet.set_size_request(138, -1)
button_mshnet.connect("clicked", Button_Mshnet_Clicked)
button_mshnet.show()
box3a.pack_start(button_settings, False, False, 0)
box3a.pack_start(button_mshnet, False, False, 0)

label3 = Gtk.Label()
label3.show()
label3.set_width_chars(1)
box4.pack_start(label3, False, False, 0)
liststore2 = Gtk.ListStore(str)
liststore2.append(['Technology    '])
liststore2.append(['nordlynx'])
liststore2.append(['openvpn'])
cell2 = Gtk.CellRendererText()
combobox2 = Gtk.ComboBox()
combobox2.show()
combobox2.set_name("cbbox")
combobox2.pack_start(cell2, True)
combobox2.add_attribute(cell2, 'text', 0)
combobox2.set_model(liststore2)
combobox2.set_active(0)
combobox2.connect("changed", Technology_Changed)
box4.pack_start(combobox2, False, False, 0)

label51 = Gtk.Label()
label51.show()
label51.set_width_chars(1)
box51.pack_start(label51, False, False, 0)
liststore3 = Gtk.ListStore(str)
liststore3.append(['Protocol      '])
liststore3.append(['tcp'])
liststore3.append(['udp'])
cell3 = Gtk.CellRendererText()
combobox3 = Gtk.ComboBox()
combobox3.show()
combobox3.set_name("cbbox")
combobox3.pack_start(cell3, True)
combobox3.add_attribute(cell3, 'text', 0)
combobox3.set_model(liststore3)
combobox3.set_active(0)
combobox3.connect("changed", Protocol_Changed)
box51.pack_start(combobox3, False, False, 0)

label6a = Gtk.Label()
label6a.show()
label6a.set_width_chars(1)
box6a.pack_start(label6a, False, False, 0)
liststore51 = Gtk.ListStore(str)
liststore51.append(['Routing       '])
liststore51.append(['enable'])
liststore51.append(['disable'])
cell51 = Gtk.CellRendererText()
combobox51 = Gtk.ComboBox()
combobox51.show()
combobox51.set_name("cbbox")
combobox51.pack_start(cell51, True)
combobox51.add_attribute(cell51, 'text', 0)
combobox51.set_model(liststore51)
combobox51.set_active(0)
combobox51.connect("changed", Routing_Changed)
box6a.pack_start(combobox51, False, False, 0)

liststore4 = Gtk.ListStore(str)
liststore4.append(['Kill Switch   '])
liststore4.append(['enable'])
liststore4.append(['disable'])
cell4 = Gtk.CellRendererText()
combobox4 = Gtk.ComboBox()
combobox4.show()
combobox4.set_name("cbbox")
combobox4.pack_start(cell4, True)
combobox4.add_attribute(cell4, 'text', 0)
combobox4.set_model(liststore4)
combobox4.set_active(0)
combobox4.connect("changed", Killswitch_Changed)
box4.pack_start(combobox4, False, False, 0)

liststore3a = Gtk.ListStore(str)
liststore3a.append(['Auto-Connect  '])
liststore3a.append(['enable'])
liststore3a.append(['disable'])
cell3a = Gtk.CellRendererText()
combobox3a = Gtk.ComboBox()
combobox3a.show()
combobox3a.set_name("cbbox")
combobox3a.pack_start(cell3a, True)
combobox3a.add_attribute(cell3a, 'text', 0)
combobox3a.set_model(liststore3a)
combobox3a.set_active(0)
combobox3a.connect("changed", Connect_Changed)
box51.pack_start(combobox3a, False, False, 0)

liststore4a = Gtk.ListStore(str)
liststore4a.append(['Notification  '])
liststore4a.append(['enable'])
liststore4a.append(['disable'])
cell4a = Gtk.CellRendererText()
combobox4a = Gtk.ComboBox()
combobox4a.show()
combobox4a.set_name("cbbox")
combobox4a.pack_start(cell4a, True)
combobox4a.add_attribute(cell4a, 'text', 0)
combobox4a.set_model(liststore4a)
combobox4a.set_active(0)
combobox4a.connect("changed", Notify_Changed)
box6a.pack_start(combobox4a, False, False, 0)

liststore6a = Gtk.ListStore(str)
liststore6a.append(['Analytics      '])
liststore6a.append(['enable'])
liststore6a.append(['disable'])
cell6a = Gtk.CellRendererText()
combobox6a = Gtk.ComboBox()
combobox6a.show()
combobox6a.set_name("cbbox")
combobox6a.pack_start(cell6a, True)
combobox6a.add_attribute(cell6a, 'text', 0)
combobox6a.set_model(liststore6a)
combobox6a.set_active(0)
combobox6a.connect("changed", Analytics_Changed)
box4.pack_start(combobox6a, False, False, 0)

liststore6b = Gtk.ListStore(str)
liststore6b.append(['IPV6           '])
liststore6b.append(['enable'])
liststore6b.append(['disable'])
cell6b = Gtk.CellRendererText()
combobox6b = Gtk.ComboBox()
combobox6b.show()
combobox6b.set_name("cbbox")
combobox6b.pack_start(cell6b, True)
combobox6b.add_attribute(cell6b, 'text', 0)
combobox6b.set_model(liststore6b)
combobox6b.set_active(0)
combobox6b.connect("changed", IPV6_Changed)
box51.pack_start(combobox6b, False, False, 0)
label6c = Gtk.Label()
box51.pack_start(label6c, True, True, 0)

liststore6c = Gtk.ListStore(str)
liststore6c.append(['Lan Discovery  '])
liststore6c.append(['enable'])
liststore6c.append(['disable'])
cell6c = Gtk.CellRendererText()
combobox6c = Gtk.ComboBox()
combobox6c.show()
combobox6c.set_name("cbbox")
combobox6c.pack_start(cell6c, True)
combobox6c.add_attribute(cell6c, 'text', 0)
combobox6c.set_model(liststore6c)
combobox6c.set_active(0)
combobox6c.connect("changed", Lan_Discovery_Changed)
box6a.pack_start(combobox6c, False, False, 0)

label_tpl = Gtk.Label()
label_tpl.show()
label_tpl.set_name("label")
label_tpl.set_width_chars(24)
label_tpl.set_text("Threat Protection_L")
box6b.pack_start(label_tpl, False, False, 0)
button_tpl = Gtk.CheckButton()
button_tpl.show()
button_tpl.set_active(0)
button_tpl.connect("clicked", TPL_Changed)
box6b.pack_start(button_tpl, False, False, 0)
label_tpl_status = Gtk.Label()
label_tpl_status.show()
label_tpl_status.set_size_request(95, -1)
# label_tpl_status.set_width_chars(12)
label_tpl_status.set_text("Disabled")
box6b.pack_start(label_tpl_status, False, False, 0)

# MESHNET MODULE
label_mes = Gtk.Label()
label_mes.show()
label_mes.set_name("label")
label_mes.set_width_chars(24)
label_mes.set_text("Meshnet Module")
box6c.pack_start(label_mes, False, False, 0)
button_mes = Gtk.CheckButton()
button_mes.show()
button_mes.set_active(0)
button_mes.connect("clicked", MES_Changed)
box6c.pack_start(button_mes, False, False, 0)
label_mes_status = Gtk.Label()
label_mes_status.show()
label_mes_status.set_size_request(95, -1)
label_mes_status.set_text("Disabled")
box6c.pack_start(label_mes_status, False, False, 0)
# label_mess = Gtk.Label()
# label_mess.set_size_request(10, -1)
# box6c.pack_start(label_mess, False, False, 0)
button_device = Gtk.Button.new_with_label("Show Devices")
button_device.show()
button_device.set_size_request(140, -1)
button_device.connect("clicked", Device_Clicked)
box6c.pack_start(button_device, False, False, 0)

label_fs = Gtk.Label()
label_fs.show()
label_fs.set_name("label")
label_fs.set_width_chars(24)
label_fs.set_text("Filesharing")
box6d.pack_start(label_fs, False, False, 0)
label_fss = Gtk.Label()
label_fss.show()
label_fss.set_text("Incoming (0)")
label_fss.set_size_request(117, -1)
box6d.pack_start(label_fss, False, False, 0)
# label_fsss = Gtk.Label()
# label_fsss.set_size_request(30, -1)
# box6d.pack_start(label_fsss, False, False, 0)
button_fs_list = Gtk.Button.new_with_label("   Show List   ")
button_fs_list.show()
button_fs_list.set_size_request(140, -1)
button_fs_list.connect("clicked", FS_Show_List)
box6d.pack_start(button_fs_list, False, False, 0)

label_fsi = Gtk.Label()
label_fsi.show()
label_fsi.set_name("label")
label_fsi.set_width_chars(24)
label_fsi.set_text("Get File_ID")
box6e.pack_start(label_fsi, False, False, 0)
entry_fsi = Gtk.Entry()
entry_fsi.show()
entry_fsi.set_width_chars(12)
entry_fsi.set_size_request(117, -1)
box6e.pack_start(entry_fsi, False, False, 0)
# label_fssi = Gtk.Label()
# label_fssi.set_size_request(6, -1)
# box6e.pack_start(label_fssi, False, False, 0)
button_fsi = Gtk.Button.new_with_label("Accept File")
button_fsi.show()
button_fsi.set_size_request(140, -1)
button_fsi.connect("clicked", Accept_File)
box6e.pack_start(button_fsi, False, False, 0)

label_send_file = Gtk.Label()
label_send_file.show()
label_send_file.set_name("label")
label_send_file.set_text("Send File(s)")
label_send_file.set_width_chars(24)
box6f.pack_start(label_send_file, False, False, 0)
entry_send_file = Gtk.Entry()
entry_send_file.set_width_chars(12)
entry_send_file.set_size_request(117, -1)
entry_send_file.set_editable(False)
entry_send_file.show()
box6f.pack_start(entry_send_file, False, False, 0)
button_send_file = Gtk.Button.new_with_label("Choose File")
button_send_file.set_size_request(140, -1)
button_send_file.show()
button_send_file.connect("clicked", Choose_File)
box6f.pack_start(button_send_file, False, False, 0)

label_host = Gtk.Label()
label_host.show()
label_host.set_name("label")
label_host.set_text("To Host")
label_host.set_width_chars(24)
box6g.pack_start(label_host, False, False, 0)
entry_host = Gtk.Entry()
entry_host.set_width_chars(12)
entry_host.set_size_request(117, -1)
entry_host.show()
box6g.pack_start(entry_host, False, False, 0)
button_send_host = Gtk.Button.new_with_label("Send File")
button_send_host.set_size_request(140, -1)
button_send_host.show()
button_send_host.connect("clicked", Send_Host)
box6g.pack_start(button_send_host, False, False, 0)


# ADD A STATUSBAR WITH NORDVPN VERSION
sb = Gtk.Statusbar()
sb.show()
box8.pack_start(sb, True, True, 0)
result = subprocess.Popen("/usr/bin/nordvpn version", shell=True,
						stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
rc = result.wait()
out, err = result.communicate()
line = out.split('\n')
line[3].strip()
sb.push(0, line[3])

# START A THREAD THAT GETS THE NORDVPN STATUS EVERY 4 SECONDS
thread = Thread(target=Get_Nordvpn_Status)
thread.daemon = True
thread.start()

# START A THREAD THAT GETS THE FILE LIST EVERY 10 SECONDS
thread1 = Thread(target=Get_Incoming_Files)
thread1.daemon = True
thread1.start()

# START THE APPLICATION
win.show()
Gtk.main()
