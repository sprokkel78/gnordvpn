import subprocess
import sys
import os
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Pango
from threading import Thread
from time import sleep

# VERSION = 1.1.5
ver = "1.1.5"


# TODO


# CHECK IF THE NORDVPN COMMANDLINE TOOL IS INSTALLED
file = "/usr/bin/nordvpn"
if os.path.exists(file):
	print("Found the nordvpn binary. (CONTINUE)")
else:
	print("Can't find the nordvpn binary. It should be in /usr/bin/ (EXIT)")
	sys.exit(0)


# CHECK IF YOU'RE LOGGED INTO NORDVPN
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
	print("technology changed" + " to " + item[0])
	if item[0] != "Select Technology":
		status = subprocess.Popen("/usr/bin/nordvpn set technology " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()


def Protocol_Changed(obj):
	item = combobox3.get_model()[combobox3.get_active()]
	print("protocol changed" + " to " + item[0])
	if item[0] != "Select Protocol      ":
		status = subprocess.Popen("/usr/bin/nordvpn set protocol " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()


def Killswitch_Changed(obj):
	item = combobox4.get_model()[combobox4.get_active()]
	print("killswitch changed" + " to " + item[0])
	if item[0] != "Select Switch         ":
		status = subprocess.Popen("/usr/bin/nordvpn set killswitch " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()


def Update_TextView(st):
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
			if "Kill" in lsettings[y]:
				txt = txt + "\n  ------\n  " + lsettings[y] + "\n"
			y = y + 1

		txt = txt.strip()
		GLib.idle_add(Update_TextView, txt)
		sleep(4)


# MAIN CODE

# CREATE THE MAIN WINDOW
win = Gtk.Window()
win.set_title("gNordVPN " + ver)
win.set_default_size(350, 440)
file = "./gnordvpn.svg"
if os.path.exists(file):
	win.set_default_icon_from_file("./gnordvpn.svg")

win.set_resizable(False)
win.connect("destroy", Stop_Application)

# CREATE SOME SEPARATORS
sep = Gtk.Separator()
sep1 = Gtk.Separator()
sep2 = Gtk.Separator()

# CREATE THE GUI CONTAINER
box1 = Gtk.VBox(spacing=6)
win.add(box1)
boxs = Gtk.Box(spacing=6)
boxs.pack_start(sep, True, True, 0)
box1.pack_start(boxs, False, False, 0)
box2 = Gtk.Box(spacing=6)
box1.pack_start(box2, False, False, 0)
boxss = Gtk.Box(spacing=6)
boxss.pack_start(sep1, True, True, 0)
box1.pack_start(boxss, False, False, 0)
box3 = Gtk.Box(spacing=6)
box1.pack_start(box3, True, True, 0)
boxsss = Gtk.Box(spacing=6)
boxsss.pack_start(sep2, True, True, 0)
box1.pack_start(boxsss, False, False, 0)
box4 = Gtk.Box(spacing=6)
box1.pack_start(box4, False, False, 0)
box5 = Gtk.Box(spacing=6)
box1.pack_start(box5, False, False, 0)
box6 = Gtk.Box(spacing=6)
box1.pack_start(box6, False, False, 0)
box7 = Gtk.Box(spacing=6)
box1.pack_start(box7, False, False, 0)
box8 = Gtk.Box(spacing=6)
box1.pack_start(box8, False, False, 0)

# BUILT USER INTERFACE
label1 = Gtk.Label()
label1.set_text(" VPN Connection")
label1.set_width_chars(15)
box2.pack_start(label1, False, False, 0)

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
combobox1.pack_start(cell, True)
combobox1.add_attribute(cell, 'text', 0)
combobox1.set_model(liststore1)
combobox1.set_active(0)
# combobox1.set_wrap_width(3)
box2.pack_start(combobox1, False, False, 0)

button1 = Gtk.Button.new_with_label("  Connect  ")
button1.connect("clicked", Button_Connect_Clicked)
box2.pack_start(button1, False, False, 0)

button2 = Gtk.Button.new_with_label("Disconnect")
button2.connect("clicked", Button_Disconnect_Clicked)
box2.pack_start(button2, False, False, 0)

label2 = Gtk.Label()
box2.pack_start(label2, True, True, 0)

tbuffer = Gtk.TextBuffer()

textview = Gtk.TextView.new_with_buffer(tbuffer)
textview.set_editable(False)
textview.modify_font(Pango.FontDescription.from_string("Monospace 9"))
box3.pack_start(textview, True, True, 0)

label3 = Gtk.Label()
label3.set_text("Technology")
label3.set_width_chars(15)
box4.pack_start(label3, False, False, 0)

liststore2 = Gtk.ListStore(str)
liststore2.append(['Select Technology'])
liststore2.append(['nordlynx'])
liststore2.append(['openvpn'])

cell2 = Gtk.CellRendererText()
combobox2 = Gtk.ComboBox()
combobox2.pack_start(cell2, True)
combobox2.add_attribute(cell2, 'text', 0)
combobox2.set_model(liststore2)
combobox2.set_active(0)
combobox2.connect("changed", Technology_Changed)
box4.pack_start(combobox2, False, False, 0)

label4 = Gtk.Label()
box4.pack_start(label4, True, True, 0)

label5 = Gtk.Label()
label5.set_text("Protocol")
label5.set_width_chars(15)
box5.pack_start(label5, False, False, 0)

liststore3 = Gtk.ListStore(str)
liststore3.append(['Select Protocol      '])
liststore3.append(['tcp'])
liststore3.append(['udp'])

cell3 = Gtk.CellRendererText()
combobox3 = Gtk.ComboBox()
combobox3.pack_start(cell3, True)
combobox3.add_attribute(cell3, 'text', 0)
combobox3.set_model(liststore3)
combobox3.set_active(0)
combobox3.connect("changed", Protocol_Changed)
box5.pack_start(combobox3, False, False, 0)

label6 = Gtk.Label()
box5.pack_start(label6, True, True, 0)

label7 = Gtk.Label()
label7.set_text("Kill Switch")
label7.set_width_chars(15)
box6.pack_start(label7, False, False, 0)

liststore4 = Gtk.ListStore(str)
liststore4.append(['Select Switch         '])
liststore4.append(['enable'])
liststore4.append(['disable'])

cell4 = Gtk.CellRendererText()
combobox4 = Gtk.ComboBox()
combobox4.pack_start(cell4, True)
combobox4.add_attribute(cell4, 'text', 0)
combobox4.set_model(liststore4)
combobox4.set_active(0)
combobox4.connect("changed", Killswitch_Changed)
box6.pack_start(combobox4, False, False, 0)

label8 = Gtk.Label()
box6.pack_start(label8, True, True, 0)

hsep1 = Gtk.Separator()
box7.pack_start(hsep1, True, True, 0)

# ADD A STATUSBAR WITH NORDVPN VERSION
sb = Gtk.Statusbar()
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

# START THE APPLICATION
win.show_all()
Gtk.main()
