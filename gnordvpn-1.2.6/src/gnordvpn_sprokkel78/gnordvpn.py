import ipaddress
import subprocess
import socket
import sys
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
from threading import Thread
from time import sleep

# VERSION = 1.2.6
ver = "1.2.6"


# TODO


# GLOBALS
pause = 0
TPL = 0
MES = 0
sens = 0
selected_file = ""
OBF = 0
stat = 0
lock = 0

# CHECK IF THE NORDVPN COMMANDLINE TOOL IS INSTALLED
file = "/usr/bin/nordvpn"
if os.path.exists(file):
	print("Found the nordvpn binary. (CONTINUE)")
else:
	print("Can't find the nordvpn binary. It should be in /usr/bin/ (EXIT)")
	dialog = Gtk.MessageDialog(
		title="gNordVPN",
		parent=None,
		flags=0,
		message_type=Gtk.MessageType.INFO,
		buttons=Gtk.ButtonsType.OK,
		text="Can't find the nordvpn binary.\nIt should be in /usr/bin/."
	)
	dialog.run()
	dialog.destroy()

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
	dialog = Gtk.MessageDialog(
		title="gNordVPN",
        parent=None,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text="You are not logged in to nordvpn.\nPlease log in to nordvpn first."
	)
	dialog.run()
	dialog.destroy()
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
	global stat
	item = combobox1.get_model()[combobox1.get_active()]
	if item[0] != "Select Country  ":
		status = subprocess.Popen("/usr/bin/nordvpn c " + item[0], shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		out = status.communicate()
		if " connected " in out[0]:
			stat = 1
		else:
			stat = 0
		if " not available " in out[0]:
			dialog = Gtk.MessageDialog(
				title="gNordVPN",
				parent=win,
				flags=0,
				message_type=Gtk.MessageType.INFO,
				buttons=Gtk.ButtonsType.OK,
				text="The specified server is not available,\nor the connection settings are wrong.\nTry changing the Technology setting."
			)
			dialog.run()
			dialog.destroy()

	else:
		status = subprocess.Popen("/usr/bin/nordvpn c", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		out = status.communicate()
		if " connected " in out[0]:
			stat = 1
		else:
			stat = 0
		if " not available " in out[0]:
			dialog = Gtk.MessageDialog(
				title="gNordVPN",
				parent=win,
				flags=0,
				message_type=Gtk.MessageType.INFO,
				buttons=Gtk.ButtonsType.OK,
				text="The specified server is not available,\nor the connection settings are wrong.\nTry changing the Technology setting."
			)
			dialog.run()
			dialog.destroy()


def Button_Disconnect_Clicked(obj):
	status = subprocess.Popen("/usr/bin/nordvpn d", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	rcstat = status.wait()
	global stat
	stat = 0

def Technology_Changed(obj):
    item = combobox2.get_model()[combobox2.get_active()]
    # print("technology changed" + " to " + item[0])
    if item[0] != "Technology    ":
        status = subprocess.Popen("/usr/bin/nordvpn set technology " + item[0], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()

    combobox2.set_active(0)

    if item[0] == "nordlynx":
        label_obf_status.set_text("Disabled")
        status = subprocess.Popen("/usr/bin/nordvpn set obfuscate disable", shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
        global OBF
        OBF = 0

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

		status = subprocess.Popen(
			"/usr/bin/nordvpn set dns off",
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()

		button_dns.set_label("Activate")


def OBF_Changed(obj):
	if button_obf.get_active() == 0:
		label_obf_status.set_text("Disabled")
		status = subprocess.Popen("/usr/bin/nordvpn set obfuscate disable", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
	if button_obf.get_active() == 1:
		label_obf_status.set_text("Enabled")
		status = subprocess.Popen("/usr/bin/nordvpn set obfuscate enable ", shell=True,
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
        global stat
        global lock

        if lock == 1:
            sleep(5)

        stat = 0
        status = subprocess.Popen("/usr/bin/nordvpn status", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
        statout, staterr = status.communicate()
        statout = statout.strip('\n')
        lstatus = statout.split('\n')
        for st in lstatus:
            if st != "\r" and st != "-" and st != "/" and st != "\\" and st != "|" and st != "\n":
                if st != "":
                    txt = txt + "\n   " + st
                    if "Connected" in st:
                        stat = 1

        if stat == 1:
            # print("connected")
            label1.set_name("connected")
        else:
            # print("disconnected")
            label1.set_name("disconnected")

        status = subprocess.Popen("/usr/bin/nordvpn settings", shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
        statout, staterr = status.communicate()
        statout = statout.strip('\n')
        lsettings = statout.split('\n')

        while y < len(lsettings):
            if "Routing" in lsettings[y]:
                txt = txt + "\n   ------\n   " + lsettings[y] + "\n"
            y = y + 1
        y = 0

        while y < len(lsettings):
            if "Kill" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
            y = y + 1
        y = 0

        while y < len(lsettings):
            if "Auto" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
            y = y + 1
        y = 0

        while y < len(lsettings):
            if "Notify" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
            y = y + 1
        y = 0

        while y < len(lsettings):
            if "Analytics" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
            y = y + 1
        y = 0

        while y < len(lsettings):
            if "IPv6" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
            y = y + 1
        y = 0

        while y < len(lsettings):
            if "LAN" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
            y = y + 1
        y = 0

        while y < len(lsettings):
            if "DNS" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
                if "disabled" not in lsettings[y]:
                    mydns = lsettings[y].split(":")
                    if mydns[1] != "":
                        GLib.idle_add(Update_DNS_Stats, mydns[1])
                else:
                    GLib.idle_add(Update_DNS_Stats, 0)

            y = y + 1
        y = 0

        global OBF

        while y < len(lsettings):
            if "Obfuscate" in lsettings[y]:
                if "enabled" in lsettings[y]:
                    OBF = 1
                else:
                    OBF = 0
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
                txt = txt + "   " + lsettings[y] + "\n"
                if lock != 1:
                    if "enabled" in lsettings[y]:
                        MES = 1
                    else:
                        MES = 0
                else:
                    lock = 0

            y = y + 1
        y = 0

        txt = txt.strip()
        txt = " " + txt
        GLib.idle_add(Update_TextView, txt)

        if OBF == 0:
            GLib.idle_add(UpdateUI_OBF_Off, 1)
        else:
            GLib.idle_add(UpdateUI_OBF_On, 1)

        if TPL == 0:
            GLib.idle_add(UpdateUI_TPL_Off, 1)
        else:
            GLib.idle_add(UpdateUI_TPL_On, 1)

        if MES == 0:
            GLib.idle_add(UpdateUI_Meshnet_Off, 1)
        else:
            MES = 1
            GLib.idle_add(UpdateUI_Meshnet_On, 1)

        a = 0
        b = 0
        text = "\n Allowlist"
        while a < len(lsettings):
            if "Allowlisted" in lsettings[a]:
                text = text + "\n\n"
                b = 1
            if b == 1 and "Allowlisted" not in lsettings[a]:
                text = text + " -> " + lsettings[a].strip()

            a = a + 1

        GLib.idle_add(Update_Allowlist_View, text)

        sleep(4)


def Update_Allowlist_View(text):
    tbuffer_allow.set_text(text)


def UpdateUI_OBF_Off(value):
	if value == 1:
		button_obf.set_active(0)
		label_obf_status.set_text("Disabled")


def UpdateUI_OBF_On(value):
	if value == 1:
		button_obf.set_active(1)
		label_obf_status.set_text("Enabled")

def UpdateUI_TPL_Off(value):
	if value == 1:
		button_tpl.set_active(0)
		label_tpl_status.set_text("Disabled")


def UpdateUI_TPL_On(value):
	if value == 1:
		button_tpl.set_active(1)
		label_tpl_status.set_text("Enabled")


def UpdateUI_Meshnet_Off(value):
	global sens
	if value == 1:
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
		label_route.set_sensitive(0)
		entry_route.set_sensitive(0)
		button_route.set_sensitive(0)

		if sens == 0:
			button_fs_list.set_sensitive(0)
			button_device.set_sensitive(0)


def UpdateUI_Meshnet_On(value):
	global sens
	if value == 1:
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
		label_route.set_sensitive(1)
		entry_route.set_sensitive(1)
		button_route.set_sensitive(1)

		if sens == 1:
			button_device.set_sensitive(1)
			button_fs_list.set_sensitive(1)

def Update_DNS_Stats(mydns):
		if mydns == 0:
			button_dns.set_label("Activate")
		else:
			button_dns.set_label("Disable")



def MES_Changed(obj):
	global MES
	global pause
	global lock
	MES = 0

	if button_mes.get_active() == 0:
		lock = 1
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
		label_route.set_sensitive(0)
		entry_route.set_sensitive(0)
		button_route.set_sensitive(0)

		status = subprocess.Popen("/usr/bin/nordvpn set meshnet off", shell=True,
								stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()

		if pause == 1:
			pause = 0
			button_device.set_label("Show Devices")
			button_fs_list.set_label("   Show List   ")


	if button_mes.get_active() == 1:
		lock = 1
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
				MES = 1
			else:
				MES = 0
			y = y + 1

		if x == 1:
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
			label_route.set_sensitive(1)
			entry_route.set_sensitive(1)
			button_route.set_sensitive(1)

		else:
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
			label_route.set_sensitive(0)
			entry_route.set_sensitive(0)
			button_route.set_sensitive(0)


def Get_Peer_List():
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

		txtp = "\n "
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
						txtp = txtp + "\n\n   " + st
					else:
						if "Hostname" in st:
							txtp = txtp + "\n\n   " + st
						else:
							if "External Peers" in st:
								txtp = txtp + "\n\n   " + st
							else:
								txtp = txtp + "\n   " + st
	else:
		txtp = "  Can't update peer list. No Connection."

	return(txtp.strip())


def Device_Clicked(obj):
	global MES
	global pause
	global sens

	if MES == 1:
		if pause == 0:
			button_device.set_label("Hide Devices")
			txtp = Get_Peer_List()
			txte = "\n   " + txtp
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
		else:
			internet = 0
	except Exception:
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
					txtp = txtp + "\n   " + st

		if txtp == "\n":
			txtp = "  No incoming files."
	else:
		txtp = "  Can't update file list. No Connection."

	return(txtp.strip())



def FS_Show_List(obj):
	global MES
	global pause
	global sens

	if MES == 1:
		if pause == 0:
			button_fs_list.set_label("   Hide List   ")
			txtp = Get_File_List()
			txte = "\n   " + txtp
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
		if MES == 1:
			try:
				host = socket.gethostbyname("www.nordvpn.com")
				if host != "":
					internet = 1
				else:
					internet = 0
			except Exception:
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
							txtp = txtp + "\n   " + st
			else:
				txtp = "0"

			GLib.idle_add(Update_File_Label, txtp.strip())
		sleep(9)

def Update_File_Label(txtp):
	label_fss.set_text("Incoming (" + txtp + ")")


def Accept_File(obj):
	file_id = entry_fsi.get_text()
	if ";" not in file_id and " " not in file_id and file_id != "":
		try:
			host = socket.gethostbyname("www.nordvpn.com")
			if host != "":
				internet = 1
			else:
				internet = 0
		except Exception:
			internet = 0

		if internet == 1:
			status = subprocess.Popen("gnome-terminal --title 'gNordVPN' -- bash -c '/usr/bin/nordvpn fileshare accept " + file_id + "; sleep 5'", shell=True,
									  stdout=subprocess.PIPE,
									  stderr=subprocess.PIPE, universal_newlines=True)
			rcstat = status.wait()

		else:
			dialog = Gtk.MessageDialog(
				title="gNordVPN",
				parent=win,
				flags=0,
				message_type=Gtk.MessageType.INFO,
				buttons=Gtk.ButtonsType.OK,
				text="Can't get files. No Connection."
			)
			dialog.run()
			dialog.destroy()

		entry_fsi.set_text("")


def Button_Settings_Clicked(obj):
    box22a.show()
    box22b.show()
    box22c.show()
    box22d.show()
    box22e.show()
    box22f.show()
    box22g.show()
    box22h.show()

    box33a.hide()
    box33b.hide()
    box33c.hide()
    box33d.hide()
    box33e.hide()
    box33f.hide()
    box33g.hide()
    box33h.hide()
    box33i.hide()

    box44a.hide()
    box44b.hide()
    box44c.hide()
    box44d.hide()


def Button_Mshnet_Clicked(obj):
    box22a.hide()
    box22b.hide()
    box22c.hide()
    box22d.hide()
    box22e.hide()
    box22f.hide()
    box22g.hide()
    box22h.hide()

    box33a.show()
    box33b.show()
    box33c.show()
    box33d.show()
    box33e.show()
    box33f.show()
    box33g.show()
    box33h.show()
    box33i.show()

    box44a.hide()
    box44b.hide()
    box44c.hide()
    box44d.hide()


def Button_Allowlist_Clicked(obj):
    box22a.hide()
    box22b.hide()
    box22c.hide()
    box22d.hide()
    box22e.hide()
    box22f.hide()
    box22g.hide()
    box22h.hide()

    box33a.hide()
    box33b.hide()
    box33c.hide()
    box33d.hide()
    box33e.hide()
    box33f.hide()
    box33g.hide()
    box33h.hide()
    box33i.hide()

    box44a.show()
    box44b.show()
    box44c.show()
    box44d.show()


def Choose_File(obj):
	dialog = Gtk.FileChooserDialog(
		title="Open File",
		parent=win,
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
		print("Selected file:" + "\"" + selected_file + "\"")
	# elif response == Gtk.ResponseType.CANCEL:
		# print("Dialog closed")
		# selected_file = ""

	dialog.destroy()


def Send_Host(obj):
	global selected_file
	file_id = selected_file
	hostname = entry_host.get_text()
	if ";" not in file_id and file_id != "" and hostname != "" and ";" not in hostname:
		try:
			host = socket.gethostbyname("www.nordvpn.com")
			if host != "":
				internet = 1
			else:
				internet = 0
		except Exception:
			internet = 0

		if internet == 1 and hostname != "" and ";" not in hostname:
			status = subprocess.Popen("gnome-terminal --title 'gNordVPN' -- bash -c '/usr/bin/nordvpn fileshare send " + hostname + " " + "\"" + selected_file + "\"" + " ; sleep 5'", shell=True,
									  stdout=subprocess.PIPE,
									  stderr=subprocess.PIPE, universal_newlines=True)
			rcstat = status.wait()

		else:
			dialog = Gtk.MessageDialog(
				title="gNordVPN",
				parent=win,
				flags=0,
				message_type=Gtk.MessageType.INFO,
				buttons=Gtk.ButtonsType.OK,
				text="Can't send files. No Connection."
			)
			dialog.run()
			dialog.destroy()

		# entry_send_file.set_text("")
		# selected_file = ""

def Activate_DNS(obj):
	if button_dns.get_label() == "Activate":
		dns = entry_dns.get_text()
		if dns != "" and ";" not in dns:
			if " " in dns:
				ip_1 = ""
				ip_2 = ""
				ip_split = dns.split(" ")
				try:
					ipaddress.ip_address(ip_split[0])
					ip_1 = ip_split[0]
				except ValueError:
					ip_1 = ""

				try:
					ipaddress.ip_address(ip_split[1])
					ip_2 = ip_split[1]
				except ValueError:
					ip_2 = ""

				if ip_1 != "" and ip_2 != "":
					status = subprocess.Popen(
						"/usr/bin/nordvpn set dns " + ip_1 + " " + ip_2,
						shell=True,
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE, universal_newlines=True)
					rcstat = status.wait()
					button_dns.set_label("Disable")
			else:
				try:
					ipaddress.ip_address(dns)
					ip_1 = dns
				except ValueError:
					ip_1 = ""

				if ip_1 != "":
					status = subprocess.Popen(
									"/usr/bin/nordvpn set dns " + ip_1,
									shell=True,
									stdout=subprocess.PIPE,
									stderr=subprocess.PIPE, universal_newlines=True)
					rcstat = status.wait()
					button_dns.set_label("Disable")
	else:
		status = subprocess.Popen(
			"/usr/bin/nordvpn set dns off",
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		entry_dns.set_text("")
		button_dns.set_label("Activate")


def Route_Traffic(obj):
	host = entry_route.get_text()
	if ";" not in host and " " not in host and host != "":
		# print("Route traffic to : " + host)
		status = subprocess.Popen(
			"/usr/bin/nordvpn meshnet peer connect " + host,
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE, universal_newlines=True)
		rcstat = status.wait()
		out = status.communicate()
		#print(out)
		if "connected to meshnet" in out[0]:
			conn = 1
		else:
			if "unknown" in out[0]:
				# print("Peer is unknown")
				dialog = Gtk.MessageDialog(
					title="gNordVPN",
					parent=win,
					flags=0,
					message_type=Gtk.MessageType.INFO,
					buttons=Gtk.ButtonsType.OK,
					text="Peer is unknown, can't connect."
				)
				dialog.run()
				dialog.destroy()
			else:
				# print("Failed to connect")
				dialog = Gtk.MessageDialog(
					title="gNordVPN",
					parent=win,
					flags=0,
					message_type=Gtk.MessageType.INFO,
					buttons=Gtk.ButtonsType.OK,
					text="Failed to connect to Host."
				)
				dialog.run()
				dialog.destroy()


def Allow_Net_Add(obj):
    item = entry_allow_net.get_text()
    x = 0
    try:
        ipaddress.IPv4Network(item)
        x = 1
    except (ValueError):
        x = 0

    if x == 1 and item != "":
        status = subprocess.Popen(
            "/usr/bin/nordvpn allowlist add subnet " + item,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
    else:
        if item != "":
            dialog = Gtk.MessageDialog(
                title="gNordVPN",
                parent=win,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Error parsing subnet."
            )
            dialog.run()
            dialog.destroy()


def Allow_Port_Add(obj):
    item = entry_allow_port.get_text()
    check1 = item.split(" ")
    if len(check1) > 1:
        port1 = check1[0]
        port2 = check1[1]
    else:
        port1 = item
        port2 = ""

    x = 0
    if port1 != "":
        try:
            port = int(port1)
            if 0 < port <= 65535:
                x = 1
        except ValueError:
            x = 0

    y = 0
    if port2 != "":
        try:
            port = int(port2)
            if 0 < port <= 65535:
                y = 1
        except ValueError:
            y = 0

    protocol = combobox_allow_port.get_model()[combobox_allow_port.get_active()]
    # print(protocol[0])
    if x == 1 and y == 1 and protocol[0] == "Both":
        status = subprocess.Popen(
            "/usr/bin/nordvpn allowlist add ports " + port1 + " " + port2,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()

    if x == 1 and y == 1 and protocol[0] == "TCP":
        status = subprocess.Popen(
            "/usr/bin/nordvpn allowlist add ports " + port1 + " " + port2 + " protocol TCP",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()

    if x == 1 and y == 1 and protocol[0] == "UDP":
        status = subprocess.Popen(
            "/usr/bin/nordvpn allowlist add ports " + port1 + " " + port2 + " protocol UDP",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()


    if x == 1 and y == 0 and protocol[0] == "Both":
        status = subprocess.Popen(
            "/usr/bin/nordvpn allowlist add port " + port1,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()


    if x == 1 and y == 0 and protocol[0] == "TCP":
        status = subprocess.Popen(
            "/usr/bin/nordvpn allowlist add port " + port1 + " protocol TCP",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()

    if x == 1 and y == 0 and protocol[0] == "UDP":
        status = subprocess.Popen(
            "/usr/bin/nordvpn allowlist add ports " + port1 + " protocol UDP",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()


def Button_Allow_Clear(obj):
    status = subprocess.Popen(
        "/usr/bin/nordvpn allowlist remove all",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, universal_newlines=True)
    rcstat = status.wait()


# MAIN USER INTERFACE CODE

# CREATE THE MAIN WINDOW
win = Gtk.Window()
win.set_title("gNordVPN " + ver)
win.set_default_size(500, 800)
file = "./gnordvpn.svg"
if os.path.exists(file):
	win.set_default_icon_from_file("./gnordvpn.svg")
win.set_resizable(False)
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
sep7 = Gtk.Separator()
sep7.show()
sep8 = Gtk.Separator()
sep8.show()
sep9 = Gtk.Separator()
sep9.show()


# CREATE THE GUI CONTAINER
box1 = Gtk.VBox(spacing=6)
box1.show()
win.add(box1)
box11a = Gtk.Box(spacing=6)
box11a.show()
box11a.pack_start(sep1, True, True, 0)
box1.pack_start(box11a, False, False, 0)
box11b = Gtk.Box(spacing=6)
box11b.show()
box1.pack_start(box11b, False, False, 0)
box11c = Gtk.Box(spacing=6)
box11c.show()
box11c.pack_start(sep2, True, True, 0)
box1.pack_start(box11c, False, False, 0)
box11d = Gtk.Box(spacing=6)
box11d.show()
box1.pack_start(box11d, False, False, 0)
box11e = Gtk.Box(spacing=6)
box11e.show()
box1.pack_start(box11e, False, False, 0)
box11f = Gtk.Box(spacing=6)
box11f.show()
box1.pack_start(box11f, False, False, 0)
box11g = Gtk.Box(spacing=6)
box11g.show()
box11g.pack_start(sep3, True, True, 0)
box1.pack_start(box11g, False, False, 0)

# SETTINGS
box22a = Gtk.Box(spacing=6)
box22a.show()
box1.pack_start(box22a, False, False, 0)
box22b = Gtk.Box(spacing=6)
box22b.show()
box1.pack_start(box22b, False, False, 0)
box22c = Gtk.Box(spacing=6)
box22c.show()
box1.pack_start(box22c, False, False, 0)
box22d = Gtk.Box(spacing=6)
box22d.show()
box1.pack_start(box22d, False, False, 0)
box22e = Gtk.Box(spacing=6)
box22e.show()
box1.pack_start(box22e, False, False, 0)
box22f = Gtk.Box(spacing=6)
box22f.show()
box1.pack_start(box22f, False, False, 0)
box22g = Gtk.Box(spacing=6)
box22g.show()
box1.pack_start(box22g, False, False, 0)
box22h = Gtk.Box(spacing=6)
box22h.show()
box1.pack_start(box22h, False, False, 0)

# MESHNET
box33a = Gtk.Box(spacing=6)
box1.pack_start(box33a, False, False, 0)
box33b = Gtk.Box(spacing=6)
box1.pack_start(box33b, False, False, 0)
box33c = Gtk.Box(spacing=6)
box1.pack_start(box33c, False, False, 0)
box33d = Gtk.Box(spacing=6)
box1.pack_start(box33d, False, False, 0)
box33e = Gtk.Box(spacing=6)
box1.pack_start(box33e, False, False, 0)
box33f = Gtk.Box(spacing=6)
box1.pack_start(box33f, False, False, 0)
box33g = Gtk.Box(spacing=6)
box1.pack_start(box33g, False, False, 0)
box33h = Gtk.Box(spacing=6)
box1.pack_start(box33h, False, False, 0)
box33i = Gtk.Box(spacing=6)
box1.pack_start(box33i, False, False, 0)

# ALLOWLIST
box44a = Gtk.Box(spacing=6)
box1.pack_start(box44a, False, False, 0)
box44b = Gtk.Box(spacing=6)
box1.pack_start(box44b, False, False, 0)
box44c = Gtk.Box(spacing=6)
box1.pack_start(box44c, False, False, 0)
box44d = Gtk.Box(spacing=6)
box1.pack_start(box44d, False, False, 0)

# FOOTER
box99a = Gtk.Box(spacing=6)
box99a.show()
box1.pack_start(box99a, True, True, 0)
box99b = Gtk.Box(spacing=6)
box99b.show()
box99b.pack_start(sep4, True, True, 0)
box1.pack_start(box99b, False, False, 0)

# STATUSBAR EOP
box99c = Gtk.Box(spacing=6)
box99c.show()
box1.pack_start(box99c, False, False, 0)

# BUILT USER INTERFACE
label0 = Gtk.Label()
label0.show()
label0.set_width_chars(1)
box11b.pack_start(label0, False, False, 0)
label1 = Gtk.Label()
label1.set_xalign(0.5)
label1.set_yalign(0.5)
label1.show()
label1.set_text("NVPN Connection")
label1.set_width_chars(13)
label1.set_size_request(135, -1)
box11b.pack_start(label1, False, False, 0)

liststore1 = Gtk.ListStore(str)
liststore1.append(['Select Country  '])
liststore1.append(['al'])
liststore1.append(['ar'])
liststore1.append(['au'])
liststore1.append(['at'])
liststore1.append(['ba'])
liststore1.append(['be'])
liststore1.append(['bg'])
liststore1.append(['br'])
liststore1.append(['ca'])
liststore1.append(['ci'])
liststore1.append(['ch'])
liststore1.append(['cl'])
liststore1.append(['co'])
liststore1.append(['cr'])
liststore1.append(['cz'])
liststore1.append(['de'])
liststore1.append(['dk'])
liststore1.append(['ee'])
liststore1.append(['es'])
liststore1.append(['fi'])
liststore1.append(['fr'])
liststore1.append(['ge'])
liststore1.append(['gr'])
liststore1.append(['hk'])
liststore1.append(['hr'])
liststore1.append(['hu'])
liststore1.append(['id'])
liststore1.append(['ie'])
liststore1.append(['il'])
liststore1.append(['is'])
liststore1.append(['it'])
liststore1.append(['jp'])
liststore1.append(['kr'])
liststore1.append(['lt'])
liststore1.append(['lu'])
liststore1.append(['lv'])
liststore1.append(['md'])
liststore1.append(['mk'])
liststore1.append(['my'])
liststore1.append(['mx'])
liststore1.append(['nl'])
liststore1.append(['no'])
liststore1.append(['nz'])
liststore1.append(['pl'])
liststore1.append(['pt'])
liststore1.append(['ro'])
liststore1.append(['rs'])
liststore1.append(['se'])
liststore1.append(['sg'])
liststore1.append(['sk'])
liststore1.append(['si'])
liststore1.append(['th'])
liststore1.append(['tr'])
liststore1.append(['tw'])
liststore1.append(['ua'])
liststore1.append(['uk'])
liststore1.append(['us'])
liststore1.append(['vn'])
liststore1.append(['za'])
liststore1.append(['p2p'])
liststore1.append(['double_vpn'])
liststore1.append(['onion_over_vpn'])

cell = Gtk.CellRendererText()
combobox1 = Gtk.ComboBox()
combobox1.set_size_request(140, -1)
combobox1.show()
combobox1.pack_start(cell, True)
combobox1.add_attribute(cell, 'text', 0)
combobox1.set_model(liststore1)
combobox1.set_active(0)
combobox1.set_wrap_width(3)
box11b.pack_start(combobox1, False, False, 0)

button1 = Gtk.Button.new_with_label("  Connect  ")
button1.set_size_request(140, -1)
button1.show()
button1.connect("clicked", Button_Connect_Clicked)
box11b.pack_start(button1, False, False, 0)

button2 = Gtk.Button.new_with_label("Disconnect")
button2.set_size_request(140, -1)
button2.show()
button2.connect("clicked", Button_Disconnect_Clicked)
box11b.pack_start(button2, False, False, 0)

label2 = Gtk.Label()
label2.show()
box11b.pack_start(label2, True, True, 0)

# CREATE THE TEXTVIEW
scrolled_window = Gtk.ScrolledWindow()
scrolled_window.show()
tbuffer = Gtk.TextBuffer()
textview = Gtk.TextView.new_with_buffer(tbuffer)
textview.show()
scrolled_window.set_size_request(500, 360)
textview.set_name("textview")
textview.set_buffer(tbuffer)
textview.set_editable(False)
textview.set_wrap_mode(Gtk.WrapMode.NONE)
scrolled_window.add(textview)
box11d.pack_start(scrolled_window, True, True, 0)

# CREATE THE BUTTON BAR
label_buttons = Gtk.Label()
label_buttons.show()
label_buttons.set_width_chars(1)
box11e.pack_start(label_buttons, False, False, 0)
button_settings = Gtk.Button.new_with_label("Settings")
button_settings.set_size_request(140, -1)
button_settings.connect("clicked", Button_Settings_Clicked)
button_settings.show()
button_mshnet = Gtk.Button.new_with_label("Meshnet")
button_mshnet.set_size_request(140, -1)
button_mshnet.connect("clicked", Button_Mshnet_Clicked)
button_mshnet.show()
button_allowlist = Gtk.Button.new_with_label("Allowlist")
button_allowlist.set_size_request(140, -1)
button_allowlist.connect("clicked", Button_Allowlist_Clicked)
button_allowlist.show()
box11e.pack_start(button_settings, False, False, 0)
box11e.pack_start(button_allowlist, False, False, 0)
box11e.pack_start(button_mshnet, False, False, 0)


# CREATE EMPTY BAR
label_empty = Gtk.Label()
box11f.pack_start(label_empty, False, False, 0)

# SETTINGS BUTTON
label3 = Gtk.Label()
label3.show()
label3.set_width_chars(1)
box22a.pack_start(label3, False, False, 0)
liststore2 = Gtk.ListStore(str)
liststore2.append(['Technology    '])
liststore2.append(['nordlynx'])
liststore2.append(['openvpn'])
cell2 = Gtk.CellRendererText()
combobox2 = Gtk.ComboBox()
combobox2.set_size_request(140, -1)
combobox2.show()
combobox2.set_name("cbbox")
combobox2.pack_start(cell2, True)
combobox2.add_attribute(cell2, 'text', 0)
combobox2.set_model(liststore2)
combobox2.set_active(0)
combobox2.connect("changed", Technology_Changed)
box22a.pack_start(combobox2, False, False, 0)

label51 = Gtk.Label()
label51.show()
label51.set_width_chars(1)
box22b.pack_start(label51, False, False, 0)
liststore3 = Gtk.ListStore(str)
liststore3.append(['Protocol      '])
liststore3.append(['tcp'])
liststore3.append(['udp'])
cell3 = Gtk.CellRendererText()
combobox3 = Gtk.ComboBox()
combobox3.set_size_request(140, -1)
combobox3.show()
combobox3.set_name("cbbox")
combobox3.pack_start(cell3, True)
combobox3.add_attribute(cell3, 'text', 0)
combobox3.set_model(liststore3)
combobox3.set_active(0)
combobox3.connect("changed", Protocol_Changed)
box22b.pack_start(combobox3, False, False, 0)

label6a = Gtk.Label()
label6a.show()
label6a.set_width_chars(1)
box22c.pack_start(label6a, False, False, 0)
liststore51 = Gtk.ListStore(str)
liststore51.append(['Routing       '])
liststore51.append(['enable'])
liststore51.append(['disable'])
cell51 = Gtk.CellRendererText()
combobox51 = Gtk.ComboBox()
combobox51.set_size_request(140, -1)
combobox51.show()
combobox51.set_name("cbbox")
combobox51.pack_start(cell51, True)
combobox51.add_attribute(cell51, 'text', 0)
combobox51.set_model(liststore51)
combobox51.set_active(0)
combobox51.connect("changed", Routing_Changed)
box22c.pack_start(combobox51, False, False, 0)

liststore4 = Gtk.ListStore(str)
liststore4.append(['Kill Switch   '])
liststore4.append(['enable'])
liststore4.append(['disable'])
cell4 = Gtk.CellRendererText()
combobox4 = Gtk.ComboBox()
combobox4.set_size_request(140, -1)
combobox4.show()
combobox4.set_name("cbbox")
combobox4.pack_start(cell4, True)
combobox4.add_attribute(cell4, 'text', 0)
combobox4.set_model(liststore4)
combobox4.set_active(0)
combobox4.connect("changed", Killswitch_Changed)
box22a.pack_start(combobox4, False, False, 0)

liststore3a = Gtk.ListStore(str)
liststore3a.append(['Auto-Connect  '])
liststore3a.append(['enable'])
liststore3a.append(['disable'])
cell3a = Gtk.CellRendererText()
combobox3a = Gtk.ComboBox()
combobox3a.set_size_request(140, -1)
combobox3a.show()
combobox3a.set_name("cbbox")
combobox3a.pack_start(cell3a, True)
combobox3a.add_attribute(cell3a, 'text', 0)
combobox3a.set_model(liststore3a)
combobox3a.set_active(0)
combobox3a.connect("changed", Connect_Changed)
box22b.pack_start(combobox3a, False, False, 0)

liststore4a = Gtk.ListStore(str)
liststore4a.append(['Notification  '])
liststore4a.append(['enable'])
liststore4a.append(['disable'])
cell4a = Gtk.CellRendererText()
combobox4a = Gtk.ComboBox()
combobox4a.set_size_request(140, -1)
combobox4a.show()
combobox4a.set_name("cbbox")
combobox4a.pack_start(cell4a, True)
combobox4a.add_attribute(cell4a, 'text', 0)
combobox4a.set_model(liststore4a)
combobox4a.set_active(0)
combobox4a.connect("changed", Notify_Changed)
box22c.pack_start(combobox4a, False, False, 0)

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
box22a.pack_start(combobox6a, False, False, 0)

liststore6b = Gtk.ListStore(str)
liststore6b.append(['IPV6           '])
liststore6b.append(['enable'])
liststore6b.append(['disable'])
cell6b = Gtk.CellRendererText()
combobox6b = Gtk.ComboBox()
combobox6b.set_size_request(140, -1)
combobox6b.show()
combobox6b.set_name("cbbox")
combobox6b.pack_start(cell6b, True)
combobox6b.add_attribute(cell6b, 'text', 0)
combobox6b.set_model(liststore6b)
combobox6b.set_active(0)
combobox6b.connect("changed", IPV6_Changed)
box22b.pack_start(combobox6b, False, False, 0)
label6c = Gtk.Label()
box22b.pack_start(label6c, True, True, 0)

liststore6c = Gtk.ListStore(str)
liststore6c.append(['Lan Discovery  '])
liststore6c.append(['enable'])
liststore6c.append(['disable'])
cell6c = Gtk.CellRendererText()
combobox6c = Gtk.ComboBox()
combobox6c.set_size_request(140, -1)
combobox6c.show()
combobox6c.set_name("cbbox")
combobox6c.pack_start(cell6c, True)
combobox6c.add_attribute(cell6c, 'text', 0)
combobox6c.set_model(liststore6c)
combobox6c.set_active(0)
combobox6c.connect("changed", Lan_Discovery_Changed)
box22c.pack_start(combobox6c, False, False, 0)

box22d.pack_start(sep5, True, True, 0)

box22e.set_size_request(-1, 40)
label_obf = Gtk.Label()
label_obf.show()
label_obf.set_name("label")
label_obf.set_width_chars(21)
label_obf.set_text("Obfuscate Link")
box22e.pack_start(label_obf, False, False, 0)
button_obf = Gtk.CheckButton()
button_obf.set_size_request(31, -1)
button_obf.show()
button_obf.set_active(0)
button_obf.connect("clicked", OBF_Changed)
box22e.pack_start(button_obf, False, False, 0)
label_obf_status = Gtk.Label()
label_obf_status.set_xalign(0.0)
label_obf_status.show()
label_obf_status.set_size_request(65, -1)
label_obf_status.set_text("Disabled")
box22e.pack_start(label_obf_status, False, False, 0)
label_obf_txt = Gtk.Label()
label_obf_txt.set_xalign(0.0)
label_obf_txt.set_text("(OpenVPN Tech. only)")
label_obf_txt.show()
box22e.pack_start(label_obf_txt, False, False, 0)

box22f.set_size_request(-1, 40)
label_tpl = Gtk.Label()
label_tpl.show()
label_tpl.set_name("label")
label_tpl.set_width_chars(21)
label_tpl.set_text("Threat Pro_Lite")
box22f.pack_start(label_tpl, False, False, 0)
button_tpl = Gtk.CheckButton()
button_tpl.set_size_request(31, -1)
button_tpl.show()
button_tpl.set_active(0)
button_tpl.connect("clicked", TPL_Changed)
box22f.pack_start(button_tpl, False, False, 0)
label_tpl_status = Gtk.Label()
label_tpl_status.set_xalign(0.0)
label_tpl_status.show()
label_tpl_status.set_size_request(65, -1)
label_tpl_status.set_text("Disabled")
box22f.pack_start(label_tpl_status, False, False, 0)
label_tpl_txt = Gtk.Label()
label_tpl_txt.set_xalign(0.0)
label_tpl_txt.set_text("(Basic Protection Layer)")
label_tpl_txt.show()
box22f.pack_start(label_tpl_txt, False, False, 0)

box22g.pack_start(sep6, True, True, 0)

label_first = Gtk.Label()
label_first.show()
box22h.pack_start(label_first, False, False, 0)
label_dns = Gtk.Label()
label_dns.show()
label_dns.set_name("label")
label_dns.set_width_chars(20)
label_dns.set_text("Set Custom DNS")
box22h.pack_start(label_dns, False, False, 0)
entry_dns = Gtk.Entry()
entry_dns.show()
entry_dns.set_width_chars(15)
entry_dns.set_size_request(140, -1)
box22h.pack_start(entry_dns, False, False, 0)
button_dns = Gtk.Button.new_with_label("Activate")
button_dns.set_size_request(148, -1)
button_dns.show()
button_dns.connect("clicked", Activate_DNS)
box22h.pack_start(button_dns, False, False, 0)

# MESHNET MODULE BUTTON
label_mes = Gtk.Label()
label_mes.show()
label_mes.set_name("label")
label_mes.set_width_chars(21)
label_mes.set_text("Meshnet Module")
box33a.pack_start(label_mes, False, False, 0)
button_mes = Gtk.CheckButton()
button_mes.show()
button_mes.set_active(0)
button_mes.set_size_request(31, -1)
button_mes.connect("clicked", MES_Changed)
box33a.pack_start(button_mes, False, False, 0)
label_mes_status = Gtk.Label()
label_mes_status.show()
label_mes_status.set_size_request(103, -1)
if MES == 0:
	label_mes_status.set_text("Disabled")
if MES == 1:
	label_mes_status.set_text("Enabled")
label_mes_status.set_xalign(0.0)
box33a.pack_start(label_mes_status, False, False, 0)
button_device = Gtk.Button.new_with_label("Show Devices")
button_device.show()
button_device.set_size_request(140, -1)
button_device.connect("clicked", Device_Clicked)
box33a.pack_start(button_device, False, False, 0)

box33b.pack_start(sep7, True, True, 0)

label_fs = Gtk.Label()
label_fs.show()
label_fs.set_name("label")
label_fs.set_width_chars(21)
label_fs.set_text("Filesharing")
box33c.pack_start(label_fs, False, False, 0)
label_fss = Gtk.Label()
label_fss.show()
label_fss.set_text("Incoming (0)")
label_fss.set_xalign(0.0)
label_fss.set_size_request(140, -1)
box33c.pack_start(label_fss, False, False, 0)
button_fs_list = Gtk.Button.new_with_label("   Show List   ")
button_fs_list.show()
button_fs_list.set_size_request(140, -1)
button_fs_list.connect("clicked", FS_Show_List)
box33c.pack_start(button_fs_list, False, False, 0)

label_fsi = Gtk.Label()
label_fsi.show()
label_fsi.set_name("label")
label_fsi.set_width_chars(21)
label_fsi.set_text("Get File_ID")
box33d.pack_start(label_fsi, False, False, 0)
entry_fsi = Gtk.Entry()
entry_fsi.show()
entry_fsi.set_width_chars(14)
entry_fsi.set_size_request(140, -1)
box33d.pack_start(entry_fsi, False, False, 0)
button_fsi = Gtk.Button.new_with_label("Accept File")
button_fsi.show()
button_fsi.set_size_request(140, -1)
button_fsi.connect("clicked", Accept_File)
box33d.pack_start(button_fsi, False, False, 0)

box33e.pack_start(sep8, True, True, 0)

label_send_file = Gtk.Label()
label_send_file.show()
label_send_file.set_name("label")
label_send_file.set_text("Send File")
label_send_file.set_width_chars(21)
box33f.pack_start(label_send_file, False, False, 0)
entry_send_file = Gtk.Entry()
entry_send_file.set_width_chars(14)
entry_send_file.set_size_request(140, -1)
entry_send_file.set_editable(False)
entry_send_file.show()
box33f.pack_start(entry_send_file, False, False, 0)
button_send_file = Gtk.Button.new_with_label("Choose File")
button_send_file.set_size_request(140, -1)
button_send_file.show()
button_send_file.connect("clicked", Choose_File)
box33f.pack_start(button_send_file, False, False, 0)

label_host = Gtk.Label()
label_host.show()
label_host.set_name("label")
label_host.set_text("To Host|Peer")
label_host.set_width_chars(21)
box33g.pack_start(label_host, False, False, 0)
entry_host = Gtk.Entry()
entry_host.set_width_chars(14)
entry_host.set_size_request(140, -1)
entry_host.show()
box33g.pack_start(entry_host, False, False, 0)
button_send_host = Gtk.Button.new_with_label("Send File")
button_send_host.set_size_request(140, -1)
button_send_host.show()
button_send_host.connect("clicked", Send_Host)
box33g.pack_start(button_send_host, False, False, 0)

box33h.pack_start(sep9, True, True, 0)

label_route = Gtk.Label()
label_route.show()
label_route.set_name("label")
label_route.set_text("Route Traffic")
label_route.set_width_chars(21)
box33i.pack_start(label_route, False, False, 0)
entry_route = Gtk.Entry()
entry_route.set_width_chars(14)
entry_route.set_size_request(140, -1)
entry_route.show()
box33i.pack_start(entry_route, False, False, 0)
button_route = Gtk.Button.new_with_label("Connect")
button_route.set_size_request(140, -1)
button_route.show()
button_route.connect("clicked", Route_Traffic)
box33i.pack_start(button_route, False, False, 0)

# ALLOWLIST BUTTON
label_allow_net = Gtk.Label()
label_allow_net.show()
label_allow_net.set_text("Allow Subnet")
label_allow_net.set_width_chars(21)
label_allow_net.set_size_request(140, -1)
box44a.pack_start(label_allow_net, False, False, 0)
entry_allow_net = Gtk.Entry()
entry_allow_net.set_width_chars(14)
entry_allow_net.set_size_request(140, -1)
entry_allow_net.show()
box44a.pack_start(entry_allow_net, False, False, 0)
button_allow_net_add = Gtk.Button.new_with_label("Add to list")
button_allow_net_add.set_size_request(140, -1)
button_allow_net_add.connect("clicked", Allow_Net_Add)
button_allow_net_add.show()
box44a.pack_start(button_allow_net_add, False, False, 0)

label_allow_port = Gtk.Label()
label_allow_port.show()
label_allow_port.set_text("Allow Port(s)")
label_allow_port.set_width_chars(21)
label_allow_port.set_size_request(140, -1)
box44b.pack_start(label_allow_port, False, False, 0)
entry_allow_port = Gtk.Entry()
entry_allow_port.set_width_chars(5)
entry_allow_port.set_size_request(65, -1)
entry_allow_port.show()
box44b.pack_start(entry_allow_port, False, False, 0)
liststore_allow_port = Gtk.ListStore(str)
liststore_allow_port.append(['Both'])
liststore_allow_port.append(['TCP'])
liststore_allow_port.append(['UDP'])
cell_allow_port = Gtk.CellRendererText()
combobox_allow_port = Gtk.ComboBox()
combobox_allow_port.set_size_request(70, -1)
combobox_allow_port.show()
combobox_allow_port.set_name("cbbox")
combobox_allow_port.pack_start(cell_allow_port, True)
combobox_allow_port.add_attribute(cell_allow_port, 'text', 0)
combobox_allow_port.set_model(liststore_allow_port)
combobox_allow_port.set_active(0)
box44b.pack_start(combobox_allow_port, False, False, 0)
button_allow_port_add = Gtk.Button.new_with_label("Add to list")
button_allow_port_add.set_size_request(140, -1)
button_allow_port_add.connect("clicked", Allow_Port_Add)
button_allow_port_add.show()
box44b.pack_start(button_allow_port_add, False, False, 0)

label_start = Gtk.Label()
label_start.set_width_chars(1)
label_start.show()
box44c.pack_start(label_start, False, False, 0)
scrolled_window_allow = Gtk.ScrolledWindow()
scrolled_window_allow.show()
tbuffer_allow = Gtk.TextBuffer()
textview_allow = Gtk.TextView.new_with_buffer(tbuffer_allow)
textview_allow.show()
scrolled_window_allow.set_size_request(430, 150)
textview_allow.set_name("textview")
textview_allow.set_buffer(tbuffer_allow)
textview_allow.set_editable(False)
textview_allow.set_wrap_mode(Gtk.WrapMode.WORD)
scrolled_window_allow.add(textview_allow)
box44c.pack_start(scrolled_window_allow, False, False, 0)
tbuffer_allow.set_text("\n   AllowList")

label_start1 = Gtk.Label()
label_start1.set_width_chars(1)
label_start1.show()
box44d.pack_start(label_start1, False, False, 0)
button_allow_clear = Gtk.Button.new_with_label("Clear")
button_allow_clear.set_size_request(140, -1)
button_allow_clear.connect("clicked", Button_Allow_Clear)
button_allow_clear.show()
box44d.pack_start(button_allow_clear, False, False, 0)

# FOOTER: ADD A STATUSBAR WITH NORDVPN VERSION
sb = Gtk.Statusbar()
sb.show()
box99c.pack_start(sb, True, True, 0)
result = subprocess.Popen("/usr/bin/nordvpn version", shell=True,
						stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
rc = result.wait()
out, err = result.communicate()
line = out.split('\n')
line[3].strip()
push = " " + line[3]
sb.push(0, push)

# START A THREAD THAT GETS THE NORDVPN STATUS EVERY 4 SECONDS
thread = Thread(target=Get_Nordvpn_Status)
thread.daemon = True
thread.start()

# START A THREAD THAT GETS THE INCOMING FILE LIST EVERY 10 SECONDS
thread1 = Thread(target=Get_Incoming_Files)
thread1.daemon = True
thread1.start()

# START THE APPLICATION
win.show()
Gtk.main()
