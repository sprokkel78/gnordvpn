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


# VERSION = 1.3.7
ver = "1.3.7"


# TODO


# GLOBAL VARIABLES
pause = 0
TPL = 0
MES = 0
sens = 0
selected_file = ""
OBF = 0
FW = 0
stat = 0
lock = 0
peer = ""
peer_permission_incoming_traffic = ""
peer_permission_routing = ""
peer_permission_lan = ""
peer_permission_sending_files = ""
peer_nickname = ""
show_devices = 0
transparent = 0


# GLOBAL GTK WIDGETS
label1 = Gtk.Label()
button_dns = Gtk.Button.new_with_label("Activate")
entry_dns = Gtk.Entry()
tbuffer = Gtk.TextBuffer()
button_fw = Gtk.CheckButton()
button_obf = Gtk.CheckButton()
button_tpl = Gtk.CheckButton()
button_mes = Gtk.CheckButton()
tbuffer_allow = Gtk.TextBuffer()
label_fw_status = Gtk.Label()
label_obf_status = Gtk.Label()
label_tpl_status = Gtk.Label()
label_mes_status = Gtk.Label()
button_fsi = Gtk.Button.new_with_label("Accept File")
label_fs = Gtk.Label()
label_fss = Gtk.Label()
label_fsi = Gtk.Label()
entry_fsi = Gtk.Entry()
label_send_file = Gtk.Label()
entry_send_file = Gtk.Entry()
button_send_file = Gtk.Button.new_with_label("Choose File")
label_host = Gtk.Label()
entry_host = Gtk.Entry()
button_send_host = Gtk.Button.new_with_label("Send File")
label_route = Gtk.Label()
entry_route = Gtk.Entry()
button_route = Gtk.Button.new_with_label("Connect")
button_fs_list = Gtk.Button.new_with_label("   Show List   ")
button_device = Gtk.Button.new_with_label("Show Devices")
combobox1 = Gtk.ComboBox()
combobox2 = Gtk.ComboBox()
combobox3 = Gtk.ComboBox()
combobox51 = Gtk.ComboBox()
combobox4 = Gtk.ComboBox()
combobox444a = Gtk.ComboBox()
combobox3a = Gtk.ComboBox()
combobox4a = Gtk.ComboBox()
combobox6a = Gtk.ComboBox()
combobox6b = Gtk.ComboBox()
combobox666b = Gtk.ComboBox()
combobox777b = Gtk.ComboBox()
combobox6c = Gtk.ComboBox()
entry_allow_net = Gtk.Entry()
entry_allow_port = Gtk.Entry()
combobox_allow_port = Gtk.ComboBox()
label_settings = Gtk.Label()
liststore_peers = Gtk.ListStore(str)
combobox_peers = Gtk.ComboBox()
cbutton_incoming_traffic = Gtk.CheckButton()
cbutton_routing = Gtk.CheckButton()
cbutton_lan = Gtk.CheckButton()
cbutton_sending_files = Gtk.CheckButton()
entry_nickname = Gtk.Entry()
entry_ratings = Gtk.Entry()

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
box_main = Gtk.HBox(spacing=6)
box_main.show()
box0 = Gtk.VBox(spacing=6)
box0.show()

box1 = Gtk.VBox(spacing=6)
box1.show()
box11a = Gtk.Box(spacing=6)
box11a.show()
box11b = Gtk.Box(spacing=6)
box11b.show()
box11c = Gtk.Box(spacing=6)
box11c.show()
box11d = Gtk.Box(spacing=6)
box11d.show()
box11e = Gtk.Box(spacing=6)
box11e.show()
box11f = Gtk.Box(spacing=6)
box11f.show()
box11g = Gtk.Box(spacing=6)
box11g.show()

# SETTINGS
box22aa = Gtk.Box(spacing=6)
box22aa.show()
box22a = Gtk.Box(spacing=6)
box22a.show()
box22b = Gtk.Box(spacing=6)
box22b.show()
box22c = Gtk.Box(spacing=6)
box22c.show()
box22d = Gtk.Box(spacing=6)
box22d.show()
box22de = Gtk.Box(spacing=6)
box22de.show()
box22e = Gtk.Box(spacing=6)
box22e.show()
box22f = Gtk.Box(spacing=6)
box22f.show()
box22g = Gtk.Box(spacing=6)
box22g.show()
box22h = Gtk.Box(spacing=6)
box22h.show()
box22i = Gtk.Box(spacing=6)
box22i.show()

# MESHNET
box33a = Gtk.Box(spacing=6)
box33b = Gtk.Box(spacing=6)
box33c = Gtk.Box(spacing=6)
box33d = Gtk.Box(spacing=6)
box33e = Gtk.Box(spacing=6)
box33f = Gtk.Box(spacing=6)
box33g = Gtk.Box(spacing=6)
box33h = Gtk.Box(spacing=6)
box33i = Gtk.Box(spacing=6)

# ALLOWLIST
box44a = Gtk.Box(spacing=6)
box44b = Gtk.Box(spacing=6)
box44c = Gtk.Box(spacing=6)
box44d = Gtk.Box(spacing=6)

# PEER PERMISSIONS
box55a = Gtk.Box(spacing=6)
box55aa = Gtk.Box(spacing=6)
box55b = Gtk.Box(spacing=6)
box55c = Gtk.Box(spacing=6)
box55d = Gtk.Box(spacing=6)
box55e = Gtk.Box(spacing=6)
box55f = Gtk.Box(spacing=6)
box55g = Gtk.Box(spacing=6)

# FOOTER
box99a = Gtk.Box(spacing=6)
box99a.show()
box99b = Gtk.Box(spacing=6)
box99b.show()

# STATUSBAR EOP
box99c = Gtk.Box(spacing=6)
box99c.show()

# STARTUP CHECKS
# CHECK IF GNORDVPN.PY IS ALREADY RUNNING
print("Check if gNordVPN is already running. please wait.")

status = subprocess.Popen("ps aux | grep \"python3 ./gnordvpn.py\" | grep -v \"grep\"",\
                          shell=True, stdout=subprocess.PIPE,\
                          stderr=subprocess.PIPE, universal_newlines=True)
rcstat = status.wait()
out = status.communicate()
test = out[0].split("\n")

if len(test) > 1:
    if "gnordvpn.py" in test[1]:
        print("gNordVPN is already running. (EXIT)\n" + test[0])
        dialog = Gtk.MessageDialog(
            title="gNordVPN",
            parent=None,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="gNordVPN is already running.\n\nPID: " + test[0]
        )
        dialog.run()
        dialog.destroy()
        sys.exit(0)


# CHECK IF WE'RE IN THE RIGHT DIRECTORY
file = "./gnordvpn.css"
if os.path.exists(file):
    print("Directory Check is OK. (CONTINUE)")
else:
    print("You must run gnordvpn.py from its own directory. (EXIT)")
    dialog = Gtk.MessageDialog(
        title="gNordVPN",
        parent=None,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text="You must run gnordvpn.py from its own directory. (EXIT)"
    )
    dialog.run()
    dialog.destroy()
    sys.exit(0)

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
        text="Can't find the nordvpn binary.\nIt should be in /usr/bin/ (EXIT)"
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
        text="You are not logged in to nordvpn.\nPlease log in to nordvpn first. (EXIT)"
    )
    dialog.run()
    dialog.destroy()
    sys.exit(0)


# CODE HANDLER FUNCTIONS

def Stop_Application(obj):
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
    # print("killswitch changed" + " to " + item[0])
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

def Location_Changed(obj):
    item = combobox444a.get_model()[combobox444a.get_active()]
    if item[0] != "Virt. Location":
        status = subprocess.Popen("/usr/bin/nordvpn set virtual-location " + item[0], shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
    combobox444a.set_active(0)

def Tray_Changed(obj):
    item = combobox666b.get_model()[combobox666b.get_active()]
    if item[0] != "Tray Icon":
        status = subprocess.Popen("/usr/bin/nordvpn set tray " + item[0], shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
    combobox666b.set_active(0)

def PQ_Changed(obj):
    item = combobox777b.get_model()[combobox777b.get_active()]
    if item[0] != "Post Quantum":
        status = subprocess.Popen("/usr/bin/nordvpn set post-quantum " + item[0], shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
    combobox777b.set_active(0)


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

def FW_Changed(obj):
    if button_fw.get_active() == 0:
        label_fw_status.set_text("Disabled")
        status = subprocess.Popen("/usr/bin/nordvpn set firewall disable", shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
    if button_fw.get_active() == 1:
        label_fw_status.set_text("Enabled")
        status = subprocess.Popen("/usr/bin/nordvpn set firewall enable ", shell=True,
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
        status = subprocess.Popen("/usr/bin/nordvpn status", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  universal_newlines=True)
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
            if "Firewall:" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
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

        global FW

        while y < len(lsettings):
            if "Firewall:" in lsettings[y]:
                if "enabled" in lsettings[y]:
                    FW = 1
                else:
                    FW = 0
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

        while y < len(lsettings):
            if "Virtual" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
            y = y + 1
        y = 0

        while y < len(lsettings):
            if "Tray" in lsettings[y]:
                txt = txt + "   " + lsettings[y] + "\n"
            y = y + 1
        y = 0

        txt = txt.strip()
        txt = " " + txt
        GLib.idle_add(Update_TextView, txt)

        if FW == 0:
            GLib.idle_add(UpdateUI_FW_Off, 1)
        else:
            GLib.idle_add(UpdateUI_FW_On, 1)

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



def UpdateUI_FW_Off(value):
    if value == 1:
        button_fw.set_active(0)
        label_fw_status.set_text("Disabled")


def UpdateUI_FW_On(value):
    if value == 1:
        button_fw.set_active(1)
        label_fw_status.set_text("Enabled")



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

        liststore_peers.clear()
        liststore_peers.append(['Select Peer'])
        combobox_peers.set_active(0)

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

        global show_devices
        show_devices = 0
        global pause
        pause = 0

        status = subprocess.Popen("/usr/bin/nordvpn set meshnet off", shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()

        if pause == 1:
            pause = 0
            button_device.set_label("Show Devices")
            button_fs_list.set_label("   Show List   ")

        liststore_peers.clear()
        liststore_peers.append(['Select Peer'])
        combobox_peers.set_active(0)

    if button_mes.get_active() == 1:
        lock = 1
        status = subprocess.Popen("/usr/bin/nordvpn set meshnet on", shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
        out, err = status.communicate()
        split_out = out.split("\\n")
        y = 0
        x = 0
        while y < len(split_out):
            if "enabled" in split_out[y]:
                x = 1
                MES = 1
            else:
                MES = 0
                dialog = Gtk.MessageDialog(
                    title="gNordVPN",
                    parent=win,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="We're having trouble reaching our servers. Please try again later. If the issue persists, please contact nordvpn customer support."
                )
                dialog.run()
                dialog.destroy()
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
        nickname_split = ("", " -")

        for st in lstatus:

            if st != "\r" and st != "-" and st != "/" and st != "\\" and st != "|" and st != "\\n":
                if st != "":
                    if "Local Peers" in st:
                        txtp = txtp + "\n\n   " + st
                    else:
                        if "Hostname" in st:
                            if nickname_split[1] != " -" and nickname_split != "":
                                txtp = txtp + "\n -> " + st
                                nickname_split = ("", " -")

                            else:
                                txtp = txtp + "\n\n -> " + st

                        else:
                            if "External Peers" in st:
                                txtp = txtp + "\n\n   " + st
                            else:
                                if "Nickname:" in st:
                                    #print(st)
                                    nickname_split = st.split(":")
                                    if nickname_split[1] != " -" and nickname_split[1] != "":
                                        txtp = txtp + "\n -> " + st
                                    else:
                                        txtp = txtp + "\n -> " + st
                                else:
                                    if "Fileshare" in st:
                                        txtp = txtp + "\n"
                                    else:
                                        txtp = txtp + "\n   " + st
    else:
        txtp = "  Can't update peer list. No Connection."

    return (txtp.strip())


def Device_Clicked(obj):
    global MES
    global pause
    global sens
    global show_devices

    if MES == 1:
        if pause == 0:
            button_device.set_label("Hide Devices")
            txtp = Get_Peer_List()
            txte = "\n   " + txtp
            tbuffer.set_text(txte)
            button_fs_list.set_sensitive(0)
            sens = 0
            show_devices = 1
        else:
            sleep(3)
            button_device.set_label("Show Devices")
            button_fs_list.set_sensitive(1)
            sens = 1
            show_devices = 0

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

    return (txtp.strip())


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
                status = subprocess.Popen("/usr/bin/nordvpn fileshare list | grep waiting | wc -l", shell=True,
                                          stdout=subprocess.PIPE,
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
            status = subprocess.Popen(
                "gnome-terminal --title 'gNordVPN' -- bash -c '/usr/bin/nordvpn fileshare accept " + file_id + "; sleep 5'",
                shell=True,
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
    box11d.show()
    box22a.show()
    box22b.show()
    box22c.show()
    box22d.show()
    box22de.show()
    box22e.show()
    box22f.show()
    box22g.show()
    box22h.show()
    box22i.show()

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

    box55a.hide()
    box55aa.hide()
    box55b.hide()
    box55c.hide()
    box55d.hide()
    box55e.hide()
    box55f.hide()
    box55g.hide()

    label_settings.set_text("SETTINGS")

    global show_devices
    global sens
    global pause

    if show_devices == 1:
        sleep(3)
        button_device.set_label("Show Devices")
        button_fs_list.set_sensitive(1)
        sens = 1
        show_devices = 0
        pause = 0

def Button_Mshnet_Clicked(obj):
    box11d.show()
    box22a.hide()
    box22b.hide()
    box22c.hide()
    box22d.hide()
    box22de.hide()
    box22e.hide()
    box22f.hide()
    box22g.hide()
    box22h.hide()
    box22i.hide()

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

    box55a.hide()
    box55aa.hide()
    box55b.hide()
    box55c.hide()
    box55d.hide()
    box55e.hide()
    box55f.hide()
    box55g.hide()


    label_settings.set_text("MESHNET")

    global show_devices
    global sens
    global pause

    if show_devices == 1:
        sleep(3)
        button_device.set_label("Show Devices")
        button_fs_list.set_sensitive(1)
        sens = 1
        show_devices = 0
        pause = 0


def Button_Allowlist_Clicked(obj):
    box11d.show()
    box22a.hide()
    box22b.hide()
    box22c.hide()
    box22d.hide()
    box22de.hide()
    box22e.hide()
    box22f.hide()
    box22g.hide()
    box22h.hide()
    box22i.hide()

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

    box55a.hide()
    box55aa.hide()
    box55b.hide()
    box55c.hide()
    box55d.hide()
    box55e.hide()
    box55f.hide()
    box55g.hide()


    label_settings.set_text("ALLOWLIST")

    global show_devices
    global sens
    global pause

    if show_devices == 1:
        sleep(3)
        button_device.set_label("Show Devices")
        button_fs_list.set_sensitive(1)
        sens = 1
        show_devices = 0
        pause = 0


def Button_Peer_Clicked(obj):
    global MES
    global peer_permission_incoming_traffic
    global peer_permission_routing
    global peer_permission_lan
    global peer_permission_sending_files

    peer_permission_incoming_traffic = ""
    peer_permission_routing = ""
    peer_permission_lan = ""
    peer_permission_sending_files = ""
    hostname = ""

    if MES == 1:
        #print("Updating Peers")
        liststore_peers.clear()
        liststore_peers.append(['Select Peer'])
        combobox_peers.set_active(0)
    if MES == 0:
        hostname = ""
        liststore_peers.clear()
        liststore_peers.append(['Select Peer'])
        combobox_peers.set_active(0)

    box11d.show()
    box22a.hide()
    box22b.hide()
    box22c.hide()
    box22d.hide()
    box22de.hide()
    box22e.hide()
    box22f.hide()
    box22g.hide()
    box22h.hide()
    box22i.hide()

    box33a.show()
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

    box55a.show()
    box55aa.show()
    box55b.show()
    box55c.show()
    box55d.show()
    box55e.show()
    box55f.show()
    box55g.show()

    label_settings.set_text("PEER PERMISSIONS")

    global show_devices
    global sens
    global pause

    if show_devices == 1:
        sleep(3)
        button_device.set_label("Show Devices")
        button_fs_list.set_sensitive(1)
        sens = 1
        show_devices = 0
        pause = 0


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
            status = subprocess.Popen(
                "gnome-terminal --title 'gNordVPN' -- bash -c '/usr/bin/nordvpn fileshare send " + hostname + " " + "\"" + selected_file + "\"" + " ; sleep 5'",
                shell=True,
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
        # print(out)
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


def Button_Help_Clicked(obj):
    status = subprocess.Popen(
        "gnome-terminal -- bash -c 'man nordvpn'",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, universal_newlines=True)
    rcstat = status.wait()


def Peers_Changed(obj):
    global combobox_peers
    global peer
    global peer_permission_incoming_traffic
    global peer_permission_routing
    global peer_permission_lan
    global peer_permission_sending_files
    global peer_nickname

    item = ""
    peer = ""

    active_index = combobox_peers.get_active()
    if active_index != -1:
        item = combobox_peers.get_model()[combobox_peers.get_active()]
        if item[0] != "Select Peer":
            #print(item[0])
            peer = item[0]
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer list",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()
            out = status.communicate()
            host = out[0].split("\n")
            y = 0
            x = 0
            while y < len(host) -1:
                if item[0] in host[y]:
                    x = 1
                if x == 1:
                    if host[y] == "":
                        x = 0
                    else:
                        z = y - 1
                        #print(host[z])
                        if "Allow Incoming Traffic:" in host[y]:
                            peer_permission_incoming_traffic = host[y]
                        if "Allow Routing:" in host[y]:
                            peer_permission_routing = host[y]
                        if "Allow Local Network Access:" in host[y]:
                            peer_permission_lan = host[y]
                        if "Allow Sending Files:" in host[y]:
                            peer_permission_sending_files = host[y]
                        if "Nickname:" in host[z]:
                            peer_nickname = host[z]
                            peer_nickname_split = peer_nickname.split(":")
                            if peer_nickname_split[1] != " -":
                                peer_nickname = peer_nickname_split[1]
                            else:
                                peer_nickname = ""
                y = y + 1


            if "enabled" in peer_permission_incoming_traffic:
                cbutton_incoming_traffic.set_active(1)
            else:
                cbutton_incoming_traffic.set_active(0)
            if "enabled" in peer_permission_routing:
                cbutton_routing.set_active(1)
            else:
                cbutton_routing.set_active(0)
            if "enabled" in peer_permission_lan:
                cbutton_lan.set_active(1)
            else:
                cbutton_lan.set_active(0)
            if "enabled" in peer_permission_sending_files:
                cbutton_sending_files.set_active(1)
            else:
                cbutton_sending_files.set_active(0)

            entry_nickname.set_text(peer_nickname)

        else:
            peer_permission_incoming_traffic = ""
            peer_permission_routing = ""
            peer_permission_lan = ""
            peer_permission_sending_files = ""
            peer = ""
            peer_nickname = ""
            cbutton_incoming_traffic.set_active(0)
            cbutton_routing.set_active(0)
            cbutton_lan.set_active(0)
            cbutton_sending_files.set_active(0)
            entry_nickname.set_text("")


def Button_Update_Peers_Clicked(obj):
    global MES

    global peer_permission_incoming_traffic
    global peer_permission_routing
    global peer_permission_lan
    global peer_permission_sending_files

    peer_permission_incoming_traffic = ""
    peer_permission_routing = ""
    peer_permission_lan = ""
    peer_permission_sending_files = ""

    if MES == 1:
        #print("Updating Peers")
        status = subprocess.Popen(
            "/usr/bin/nordvpn meshnet peer list | grep Hostname",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
        out = status.communicate()
        # print(out)
        host = out[0].split("\n")
        liststore_peers.clear()
        liststore_peers.append(['Select Peer'])
        y = 0
        while y < len(host) - 1:
            # print(host[y])
            hostname = host[y].split(" ")
            if y != 0:
                liststore_peers.append([hostname[1]])
            y = y + 1
        combobox_peers.set_active(0)
    if MES == 0:
        liststore_peers.clear()
        liststore_peers.append(['Select Peer'])
        combobox_peers.set_active(0)
        dialog = Gtk.MessageDialog(
            title="gNordVPN",
            parent=win,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="You must enable meshnet to update peers."
        )
        dialog.run()
        dialog.destroy()


def Cbutton_Traffic_Clicked(obj):
    global peer
    if peer != "":
        if cbutton_incoming_traffic.get_active() == 1:
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer incoming allow " + peer,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()
        else:
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer incoming deny " + peer,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()

def Cbutton_Routing_Clicked(obj):
    global peer
    if peer != "":
        if cbutton_routing.get_active() == 1:
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer routing allow " + peer,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()
        else:
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer routing deny " + peer,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()

def Cbutton_Lan_Clicked(obj):
    global peer
    if peer != "":
        if cbutton_lan.get_active() == 1:
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer local allow " + peer,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()
        else:
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer local deny " + peer,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()

def Cbutton_Sendf_Clicked(obj):
    global peer
    if peer != "":
        if cbutton_sending_files.get_active() == 1:
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer fileshare allow " + peer,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()
        else:
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer fileshare deny " + peer,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()


def Button_Unlink_Peer_Clicked(obj):
    global peer
    if peer != "":
        status = subprocess.Popen(
            "/usr/bin/nordvpn meshnet peer remove " + peer,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
        out = status.communicate()
        if "removed " in out[0]:
            dialog = Gtk.MessageDialog(
                title="gNordVPN",
                parent=win,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Peer has been removed."
            )
            dialog.run()
            dialog.destroy()

            global MES

            global peer_permission_incoming_traffic
            global peer_permission_routing
            global peer_permission_lan
            global peer_permission_sending_files

            peer_permission_incoming_traffic = ""
            peer_permission_routing = ""
            peer_permission_lan = ""
            peer_permission_sending_files = ""

            if MES == 1:
                # print("Updating Peers")
                status = subprocess.Popen(
                    "/usr/bin/nordvpn meshnet peer list | grep Hostname",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, universal_newlines=True)
                rcstat = status.wait()
                out = status.communicate()
                # print(out)
                host = out[0].split("\n")
                liststore_peers.clear()
                liststore_peers.append(['Select Peer'])
                y = 0
                while y < len(host) - 1:
                    # print(host[y])
                    hostname = host[y].split(" ")
                    if y != 0:
                        liststore_peers.append([hostname[1]])
                    y = y + 1
                combobox_peers.set_active(0)
            if MES == 0:
                liststore_peers.clear()
                liststore_peers.append(['Select Peer'])
                combobox_peers.set_active(0)
                dialog = Gtk.MessageDialog(
                    title="gNordVPN",
                    parent=win,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="You must enable meshnet to update peers."
                )
                dialog.run()
                dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(
                title="gNordVPN",
                parent=win,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Failed to remove peer."
            )
            dialog.run()
            dialog.destroy()

def Button_Nickname_Peer_Clicked(obj):
    global peer
    global peer_nickname
    global MES
    peer_nickname = entry_nickname.get_text()

    if MES == 1:
        if peer_nickname != "" and "-" not in peer_nickname and "_" not in peer_nickname\
                and " " not in peer_nickname and ";" not in peer_nickname:
            #print("update nickname")
            status = subprocess.Popen(
                "/usr/bin/nordvpn meshnet peer nickname set " + peer + " " + peer_nickname,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()
            dialog = Gtk.MessageDialog(
                title="gNordVPN",
                parent=win,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Peer nickname has been updated."
                )
            dialog.run()
            dialog.destroy()
    else:
        dialog = Gtk.MessageDialog(
            title="gNordVPN",
            parent=win,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="You must enable meshnet to update nicknames."
        )
        dialog.run()
        dialog.destroy()

def Button_Remove_Nickname_Clicked(obj):
    global peer
    global peer_nickname
    if peer != "" and peer_nickname != "":
        #print("remove nickname")
        status = subprocess.Popen(
            "/usr/bin/nordvpn meshnet peer nickname remove " + peer,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
        entry_nickname.set_text("")
        peer_nickname = ""
        dialog = Gtk.MessageDialog(
            title="gNordVPN",
            parent=win,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Peer nickname has been removed."
        )
        dialog.run()
        dialog.destroy()


def Send_Rating(obj):
    rating = entry_ratings.get_text()
    if rating == "1" or rating =="2" or rating == "3" or rating == "4" or rating == "5":
        status = subprocess.Popen(
            "/usr/bin/nordvpn rate " + rating,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True)
        rcstat = status.wait()
        dialog = Gtk.MessageDialog(
            title="gNordVPN",
            parent=win,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Thank you for your feedback."
        )
        dialog.run()
        dialog.destroy()
    entry_ratings.set_text("")



# CREATE THE GTK APPLICATION
class MyApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.sprokkel78.gnordvpn")
        GLib.set_application_name("gNordVPN")

    def do_activate(self):
        global win
        win = Gtk.ApplicationWindow(application=self, title="gnordvpn")

        global transparent
        if transparent == 1:
            # Set window transparency support
            win.set_visual(win.get_screen().get_rgba_visual())

            # Set background color to transparent
            rgba = Gdk.RGBA(0, 0, 0, 0)  # Black with full transparency
            win.override_background_color(Gtk.StateFlags.NORMAL, rgba)

        # MAIN USER INTERFACE CODE
        # CREATE THE MAIN WINDOW
        win.set_title("gNordVPN " + ver)
        win.set_default_size(500, 870)
        win.set_resizable(True)
        win.connect("destroy", Stop_Application)
        win.connect("key-press-event", Key_Event)
        win.add(box_main)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('./gnordvpn.css')

        screen = win.get_screen()
        context = win.get_style_context()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


        # BUILT USER INTERFACE


        # CONSOLE
        box_main.pack_start(box0, False, False, 0)
        box_main.pack_start(box1, False, True, 0)
        box11a.pack_start(sep1, True, True, 0)
        box1.pack_start(box11a, False, False, 0)
        box1.pack_start(box11b, False, False, 0)
        box11c.pack_start(sep2, True, True, 0)
        box1.pack_start(box11c, False, False, 0)
        box1.pack_start(box11d, False, True, 0)
        box1.pack_start(box11e, False, False, 0)
        box1.pack_start(box11f, False, False, 0)
        box11g.pack_start(sep3, True, True, 0)
        box1.pack_start(box11g, False, False, 0)

        # SETTINGS
        box1.pack_start(box22aa, False, False, 0)
        box1.pack_start(box22a, False, False, 0)
        box1.pack_start(box22b, False, False, 0)
        box1.pack_start(box22c, False, False, 0)
        box1.pack_start(box22d, False, False, 0)
        box1.pack_start(box22de, False, False, 0)
        box1.pack_start(box22e, False, False, 0)
        box1.pack_start(box22f, False, False, 0)
        box1.pack_start(box22g, False, False, 0)
        box1.pack_start(box22h, False, False, 0)
        box1.pack_start(box22i, False, False, 0)

        # MESHNET
        box1.pack_start(box33a, False, False, 0)
        box1.pack_start(box33b, False, False, 0)
        box1.pack_start(box33c, False, False, 0)
        box1.pack_start(box33d, False, False, 0)
        box1.pack_start(box33e, False, False, 0)
        box1.pack_start(box33f, False, False, 0)
        box1.pack_start(box33g, False, False, 0)
        box1.pack_start(box33h, False, False, 0)
        box1.pack_start(box33i, False, False, 0)

        # ALLOWLIST
        box1.pack_start(box44a, False, False, 0)
        box1.pack_start(box44b, False, False, 0)
        box1.pack_start(box44c, False, False, 0)
        box1.pack_start(box44d, False, False, 0)

        # PEER PERMISSIONS
        box1.pack_start(box55a, False, False, 0)
        box1.pack_start(box55b, False, False, 0)
        box1.pack_start(box55c, False, False, 0)
        box1.pack_start(box55d, False, False, 0)
        box1.pack_start(box55e, False, False, 0)
        #box1.pack_start(box55aa, False, False, 0)
        box1.pack_start(box55f, False, False, 0)
        box1.pack_start(box55g, False, False, 0)

        box1.pack_start(box99a, True, True, 0)

        # FOOTER AND STATUSBAR
        box99b.pack_start(sep4, True, True, 0)
        box1.pack_start(box99b, False, False, 0)
        box1.pack_start(box99c, False, False, 0)

        # CONSOLE
        label0 = Gtk.Label()
        label0.show()
        label0.set_width_chars(1)
        box11b.pack_start(label0, False, False, 0)
        global label1
        label1.set_xalign(0.5)
        label1.set_yalign(0.5)
        label1.show()
        label1.set_text("NORD Connection")
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
        global combobox1
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
        global tbuffer
        textview = Gtk.TextView.new_with_buffer(tbuffer)
        textview.show()
        scrolled_window.set_size_request(600, 445)
        scrolled_window.set_hexpand(False)
        scrolled_window.set_vexpand(False)

        textview.set_name("textview")
        textview.set_buffer(tbuffer)
        textview.set_editable(False)
        textview.set_wrap_mode(Gtk.WrapMode.NONE)
        textview.set_hexpand(True)
        textview.set_vexpand(False)

        scrolled_window.add(textview)
        box11d.pack_start(scrolled_window, False, True, 0)

        # CREATE THE BUTTON BAR
        label_buttons = Gtk.Separator()
        label_buttons.show()
        label_buttons.set_size_request(1, 1)
        box0.pack_start(label_buttons, False, False, 0)
        menu_button = Gtk.Button()
        menu_button.show()
        menu_image = Gtk.Image()
        menu_image.show()
        menu_image.set_from_file("./images/b_menu.png")
        menu_button.set_image(menu_image)
        menu_button.set_tooltip_text("Menu")
        box0.pack_start(menu_button, False, False, 0)
        sep_buttons = Gtk.Separator()
        sep_buttons.show()
        sep_buttons.set_size_request(1, 1)
        box0.pack_start(sep_buttons, False, False, 0)
        button_settings = Gtk.Button()
        button_settings.connect("clicked", Button_Settings_Clicked)
        button_settings.show()
        button_settings.set_tooltip_text("Settings")
        settings_image = Gtk.Image()
        settings_image.show()
        settings_image.set_from_file("./images/b_settings.png")
        button_settings.set_image(settings_image)
        button_mshnet = Gtk.Button()
        button_mshnet.connect("clicked", Button_Mshnet_Clicked)
        button_mshnet.show()
        button_mshnet.set_tooltip_text("Meshnet")
        meshnet_image = Gtk.Image()
        meshnet_image.show()
        meshnet_image.set_from_file("./images/b_meshnet.png")
        button_mshnet.set_image(meshnet_image)
        button_allowlist = Gtk.Button()
        button_allowlist.connect("clicked", Button_Allowlist_Clicked)
        button_allowlist.show()
        button_allowlist.set_tooltip_text("Allowlist")
        allowlist_image = Gtk.Image()
        allowlist_image.show()
        allowlist_image.set_from_file("./images/b_allowlist.png")
        button_allowlist.set_image(allowlist_image)
        button_peer = Gtk.Button()
        button_peer.connect("clicked", Button_Peer_Clicked)
        button_peer.show()
        button_peer.set_tooltip_text("Peers")
        peer_image = Gtk.Image()
        peer_image.show()
        peer_image.set_from_file("./images/b_peers.png")
        button_peer.set_image(peer_image)
        button_help = Gtk.Button()
        button_help.connect("clicked", Button_Help_Clicked)
        button_help.show()
        button_help.set_tooltip_text("Help")
        help_image = Gtk.Image()
        help_image.show()
        help_image.set_from_file("./images/b_help.png")
        button_help.set_image(help_image)
        box0.pack_start(button_settings, False, False, 0)
        box0.pack_start(button_allowlist, False, False, 0)
        box0.pack_start(button_mshnet, False, False, 0)
        box0.pack_start(button_peer, False, False, 0)
        box0.pack_start(button_help, False, False, 0)

        # CREATE EMPTY BAR
        label_empty = Gtk.Label()
        box11f.pack_start(label_empty, False, False, 0)

        # SETTINGS
        label3a = Gtk.Label()
        label3a.show()
        label3a.set_size_request(15, -1)
        box22aa.pack_start(label3a, False, False, 0)
        global label_settings
        label_settings.set_text("SETTINGS")
        label_settings.show()
        label_settings.set_xalign(0.0)
        label_settings.set_size_request(140, -1)
        box22aa.pack_start(label_settings, False, False, 0)

        label3 = Gtk.Label()
        label3.show()
        label3.set_width_chars(1)
        box22a.pack_start(label3, False, False, 0)
        liststore2 = Gtk.ListStore(str)
        liststore2.append(['Technology    '])
        liststore2.append(['nordlynx'])
        liststore2.append(['openvpn'])
        cell2 = Gtk.CellRendererText()
        global combobox2
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
        global combobox3
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
        global combobox51
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
        global combobox4
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
        global combobox3a
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
        global combobox4a
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
        global combobox6a
        combobox6a.show()
        combobox6a.set_name("cbbox")
        combobox6a.set_size_request(140, -1)
        combobox6a.pack_start(cell6a, True)
        combobox6a.add_attribute(cell6a, 'text', 0)
        combobox6a.set_model(liststore6a)
        combobox6a.set_active(0)
        combobox6a.connect("changed", Analytics_Changed)
        box22a.pack_start(combobox6a, False, False, 0)

        liststore6b = Gtk.ListStore(str)
        liststore6b.append(['IPV6        '])
        liststore6b.append(['enable'])
        liststore6b.append(['disable'])
        cell6b = Gtk.CellRendererText()
        global combobox6b
        combobox6b.set_size_request(140, -1)
        #combobox6b.show()
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
        global combobox6c
        combobox6c.set_size_request(140, -1)
        combobox6c.show()
        combobox6c.set_name("cbbox")
        combobox6c.pack_start(cell6c, True)
        combobox6c.add_attribute(cell6c, 'text', 0)
        combobox6c.set_model(liststore6c)
        combobox6c.set_active(0)
        combobox6c.connect("changed", Lan_Discovery_Changed)
        box22c.pack_start(combobox6c, False, False, 0)

        liststore444a = Gtk.ListStore(str)
        liststore444a.append(['Virt. Location'])
        liststore444a.append(['enable'])
        liststore444a.append(['disable'])
        cell444a = Gtk.CellRendererText()
        global combobox444a
        combobox444a.set_size_request(140, -1)
        combobox444a.show()
        combobox444a.set_name("cbbox")
        combobox444a.pack_start(cell444a, True)
        combobox444a.add_attribute(cell444a, 'text', 0)
        combobox444a.set_model(liststore444a)
        combobox444a.set_active(0)
        combobox444a.connect("changed", Location_Changed)
        box22a.pack_start(combobox444a, False, False, 0)

        liststore666b = Gtk.ListStore(str)
        liststore666b.append(['Tray Icon'])
        liststore666b.append(['enable'])
        liststore666b.append(['disable'])
        cell666b = Gtk.CellRendererText()
        global combobox666b
        combobox666b.set_size_request(140, -1)
        combobox666b.show()
        combobox666b.set_name("cbbox")
        combobox666b.pack_start(cell666b, True)
        combobox666b.add_attribute(cell666b, 'text', 0)
        combobox666b.set_model(liststore666b)
        combobox666b.set_active(0)
        combobox666b.connect("changed", Tray_Changed)
        box22b.pack_start(combobox666b, False, False, 0)
        label666c = Gtk.Label()
        box22b.pack_start(label666c, True, True, 0)

        liststore777b = Gtk.ListStore(str)
        liststore777b.append(['Post Quantum'])
        liststore777b.append(['enable'])
        liststore777b.append(['disable'])
        cell777b = Gtk.CellRendererText()
        global combobox777b
        combobox777b.set_size_request(140, -1)
        combobox777b.show()
        combobox777b.set_name("cbbox")
        combobox777b.pack_start(cell777b, True)
        combobox777b.add_attribute(cell777b, 'text', 0)
        combobox777b.set_model(liststore777b)
        combobox777b.set_active(0)
        combobox777b.connect("changed", PQ_Changed)
        box22c.pack_start(combobox777b, False, False, 0)
        label777c = Gtk.Label()
        box22c.pack_start(label777c, True, True, 0)

        box22d.pack_start(sep5, True, True, 0)

        box22de.set_size_request(-1, 40)
        label_fw_start = Gtk.Label()
        label_fw_start.show()
        label_fw_start.set_size_request(15, 10)
        box22de.pack_start(label_fw_start, False, False, 0)
        label_fw = Gtk.Label()
        label_fw.show()
        label_fw.set_xalign(0.0)
        label_fw.set_name("label")
        label_fw.set_size_request(140, -1)
        label_fw.set_text("Firewall")
        box22de.pack_start(label_fw, False, False, 0)
        global button_fw
        button_fw.set_size_request(31, -1)
        button_fw.show()
        button_fw.set_active(0)
        button_fw.connect("clicked", FW_Changed)
        box22de.pack_start(button_fw, False, False, 0)
        global label_fw_status
        label_fw_status.set_xalign(0.0)
        label_fw_status.show()
        label_fw_status.set_size_request(65, -1)
        label_fw_status.set_text("Disabled")
        box22de.pack_start(label_fw_status, False, False, 0)
        label_fw_txt = Gtk.Label()
        label_fw_txt.set_xalign(0.0)
        label_fw_txt.set_text("(Killswitch must be off to disable)")
        label_fw_txt.show()
        box22de.pack_start(label_fw_txt, False, False, 0)

        label_obf_start = Gtk.Label()
        label_obf_start.show()
        label_obf_start.set_size_request(15, 10)
        box22e.pack_start(label_obf_start, False, False, 0)
        label_obf = Gtk.Label()
        label_obf.show()
        label_obf.set_xalign(0.0)
        label_obf.set_name("label")
        label_obf.set_size_request(140, -1)
        label_obf.set_text("Obfuscate Link")
        box22e.pack_start(label_obf, False, False, 0)
        global button_obf
        button_obf.set_size_request(31, -1)
        button_obf.show()
        button_obf.set_active(0)
        button_obf.connect("clicked", OBF_Changed)
        box22e.pack_start(button_obf, False, False, 0)
        global label_obf_status
        label_obf_status.set_xalign(0.0)
        label_obf_status.show()
        label_obf_status.set_size_request(65, -1)
        label_obf_status.set_text("Disabled")
        box22e.pack_start(label_obf_status, False, False, 0)
        label_obf_txt = Gtk.Label()
        label_obf_txt.set_xalign(0.0)
        label_obf_txt.set_text("(OpenVPN Tech. only to enable)")
        label_obf_txt.show()
        box22e.pack_start(label_obf_txt, False, False, 0)

        box22f.set_size_request(-1, 40)
        label_tpl_start = Gtk.Label()
        label_tpl_start.show()
        label_tpl_start.set_size_request(15, 10)
        box22f.pack_start(label_tpl_start, False, False, 0)
        label_tpl = Gtk.Label()
        label_tpl.show()
        label_tpl.set_xalign(0.0)
        label_tpl.set_name("label")
        label_tpl.set_size_request(140, -1)
        label_tpl.set_text("Threat Pro_Lite")
        box22f.pack_start(label_tpl, False, False, 0)
        global button_tpl
        button_tpl.set_size_request(31, -1)
        button_tpl.show()
        button_tpl.set_active(0)
        button_tpl.connect("clicked", TPL_Changed)
        box22f.pack_start(button_tpl, False, False, 0)
        global label_tpl_status
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

        label_dns_start = Gtk.Label()
        label_dns_start.show()
        label_dns_start.set_size_request(15, 10)
        box22h.pack_start(label_dns_start, False, False, 0)
        label_dns = Gtk.Label()
        label_dns.set_xalign(0.0)
        label_dns.show()
        label_dns.set_name("label")
        label_dns.set_size_request(140, -1)
        label_dns.set_text("Set Custom DNS")
        box22h.pack_start(label_dns, False, False, 0)
        global entry_dns
        entry_dns.show()
        entry_dns.set_width_chars(15)
        entry_dns.set_size_request(140, -1)
        box22h.pack_start(entry_dns, False, False, 0)
        global button_dns
        button_dns.set_size_request(140, -1)
        button_dns.show()
        button_dns.connect("clicked", Activate_DNS)
        box22h.pack_start(button_dns, False, False, 0)

        # HIER VERDER

        label_rt_start = Gtk.Label()
        label_rt_start.show()
        label_rt_start.set_size_request(15, -1)
        box22i.pack_start(label_rt_start, False, False, 0
                          )
        label_ratings = Gtk.Label()
        label_ratings.set_text("Rate Connection")
        label_ratings.set_xalign(0.0)
        label_ratings.set_size_request(140, -1)
        label_ratings.show()
        box22i.pack_start(label_ratings, False, False, 0)

        global entry_ratings
        entry_ratings.show()
        entry_ratings.set_width_chars(1)
        entry_ratings.connect("activate", Send_Rating)
        box22i.pack_start(entry_ratings, False, False, 0)

        label_rt_nr = Gtk.Label()
        label_rt_nr.set_text(" > 1 (slow) > 3 (medium) > 5 (fast)")
        label_rt_nr.show()
        label_rt_nr.set_size_request(100, -1)
        box22i.pack_start(label_rt_nr, False, False, 0)

        # MESHNET MODULE BUTTON
        label_mes_start = Gtk.Label()
        label_mes_start.show()
        label_mes_start.set_size_request(15, 10)
        box33a.pack_start(label_mes_start, False, False, 0)
        label_mes = Gtk.Label()
        label_mes.show()
        label_mes.set_xalign(0.0)
        label_mes.set_name("label")
        label_mes.set_size_request(140, -1)
        label_mes.set_text("Meshnet Module")
        box33a.pack_start(label_mes, False, False, 0)
        global button_mes
        button_mes.show()
        button_mes.set_active(0)
        button_mes.set_size_request(31, -1)
        button_mes.connect("clicked", MES_Changed)
        box33a.pack_start(button_mes, False, False, 0)
        global label_mes_status
        label_mes_status.show()
        label_mes_status.set_size_request(103, -1)
        if MES == 0:
            label_mes_status.set_text("Disabled")
        if MES == 1:
            label_mes_status.set_text("Enabled")
        label_mes_status.set_xalign(0.0)
        box33a.pack_start(label_mes_status, False, False, 0)
        global button_device
        button_device.show()
        button_device.set_size_request(140, -1)
        button_device.connect("clicked", Device_Clicked)
        box33a.pack_start(button_device, False, False, 0)

        box33b.pack_start(sep7, True, True, 0)

        label_fs_start = Gtk.Label()
        label_fs_start.show()
        label_fs_start.set_size_request(15, 10)
        box33c.pack_start(label_fs_start, False, False, 0)
        global label_fs
        label_fs.show()
        label_fs.set_xalign(0.0)
        label_fs.set_name("label")
        label_fs.set_size_request(140, -1)
        label_fs.set_text("Filesharing")
        box33c.pack_start(label_fs, False, False, 0)
        global label_fss
        label_fss.show()
        label_fss.set_text("Incoming (0)")
        label_fss.set_xalign(0.0)
        label_fss.set_size_request(140, -1)
        box33c.pack_start(label_fss, False, False, 0)
        global button_fs_list
        button_fs_list.show()
        button_fs_list.set_size_request(140, -1)
        button_fs_list.connect("clicked", FS_Show_List)
        box33c.pack_start(button_fs_list, False, False, 0)

        label_fsi_start = Gtk.Label()
        label_fsi_start.show()
        label_fsi_start.set_size_request(15, 10)
        box33d.pack_start(label_fsi_start, False, False, 0)
        global label_fsi
        label_fsi.show()
        label_fsi.set_xalign(0.0)
        label_fsi.set_name("label")
        label_fsi.set_size_request(140, -1)
        label_fsi.set_text("Get File_ID")
        box33d.pack_start(label_fsi, False, False, 0)
        global entry_fsi
        entry_fsi.show()
        entry_fsi.set_width_chars(14)
        entry_fsi.set_size_request(140, -1)
        box33d.pack_start(entry_fsi, False, False, 0)
        global button_fsi
        button_fsi.show()
        button_fsi.set_size_request(140, -1)
        button_fsi.connect("clicked", Accept_File)
        box33d.pack_start(button_fsi, False, False, 0)

        box33e.pack_start(sep8, True, True, 0)

        label_sendf_start = Gtk.Label()
        label_sendf_start.show()
        label_sendf_start.set_size_request(15, 10)
        box33f.pack_start(label_sendf_start, False, False, 0)
        global label_send_file
        label_send_file.show()
        label_send_file.set_xalign(0.0)
        label_send_file.set_name("label")
        label_send_file.set_text("Send File")
        label_send_file.set_size_request(140, -1)
        box33f.pack_start(label_send_file, False, False, 0)
        global entry_send_file
        entry_send_file.set_width_chars(14)
        entry_send_file.set_size_request(140, -1)
        entry_send_file.set_editable(False)
        entry_send_file.show()
        box33f.pack_start(entry_send_file, False, False, 0)
        global button_send_file
        button_send_file.set_size_request(140, -1)
        button_send_file.show()
        button_send_file.connect("clicked", Choose_File)
        box33f.pack_start(button_send_file, False, False, 0)

        label_host_start = Gtk.Label()
        label_host_start.show()
        label_host_start.set_size_request(15, 10)
        box33g.pack_start(label_host_start, False, False, 0)
        global label_host
        label_host.show()
        label_host.set_xalign(0.0)
        label_host.set_name("label")
        label_host.set_text("To Host|Peer")
        label_host.set_size_request(140, -1)
        box33g.pack_start(label_host, False, False, 0)
        global entry_host
        entry_host.set_width_chars(14)
        entry_host.set_size_request(140, -1)
        entry_host.show()
        box33g.pack_start(entry_host, False, False, 0)
        global button_send_host
        button_send_host.set_size_request(140, -1)
        button_send_host.show()
        button_send_host.connect("clicked", Send_Host)
        box33g.pack_start(button_send_host, False, False, 0)

        box33h.pack_start(sep9, True, True, 0)

        label_route_start = Gtk.Label()
        label_route_start.show()
        label_route_start.set_size_request(15, 10)
        box33i.pack_start(label_route_start, False, False, 0)

        global label_route
        label_route.show()
        label_route.set_xalign(0.0)
        label_route.set_name("label")
        label_route.set_text("Route Traffic")
        label_route.set_size_request(140, -1)
        box33i.pack_start(label_route, False, False, 0)
        global entry_route
        entry_route.set_width_chars(14)
        entry_route.set_size_request(140, -1)
        entry_route.show()
        box33i.pack_start(entry_route, False, False, 0)
        global button_route
        button_route.set_size_request(140, -1)
        button_route.show()
        button_route.connect("clicked", Route_Traffic)
        box33i.pack_start(button_route, False, False, 0)

        # ALLOWLIST BUTTON
        label_allow_start = Gtk.Label()
        label_allow_start.show()
        label_allow_start.set_size_request(15, 10)
        box44a.pack_start(label_allow_start, False, False, 0)
        label_allow_net = Gtk.Label()
        label_allow_net.show()
        label_allow_net.set_xalign(0.0)
        label_allow_net.set_text("Allow Subnet")
        label_allow_net.set_size_request(140, -1)
        box44a.pack_start(label_allow_net, False, False, 0)
        global entry_allow_net
        entry_allow_net.set_width_chars(14)
        entry_allow_net.set_size_request(140, -1)
        entry_allow_net.show()
        box44a.pack_start(entry_allow_net, False, False, 0)
        button_allow_net_add = Gtk.Button.new_with_label("Add to list")
        button_allow_net_add.set_size_request(140, -1)
        button_allow_net_add.connect("clicked", Allow_Net_Add)
        button_allow_net_add.show()
        box44a.pack_start(button_allow_net_add, False, False, 0)

        label_port_start = Gtk.Label()
        label_port_start.show()
        label_port_start.set_size_request(15, 10)
        box44b.pack_start(label_port_start, False, False, 0)
        label_allow_port = Gtk.Label()
        label_allow_port.show()
        label_allow_port.set_xalign(0.0)
        label_allow_port.set_text("Allow Port(s)")
        label_allow_port.set_size_request(140, -1)
        box44b.pack_start(label_allow_port, False, False, 0)
        global entry_allow_port
        entry_allow_port.set_width_chars(5)
        entry_allow_port.set_size_request(65, -1)
        entry_allow_port.show()
        box44b.pack_start(entry_allow_port, False, False, 0)
        liststore_allow_port = Gtk.ListStore(str)
        liststore_allow_port.append(['Both'])
        liststore_allow_port.append(['TCP'])
        liststore_allow_port.append(['UDP'])
        cell_allow_port = Gtk.CellRendererText()
        global combobox_allow_port
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
        global tbuffer_allow
        textview_allow = Gtk.TextView.new_with_buffer(tbuffer_allow)
        textview_allow.show()
        scrolled_window_allow.set_size_request(440, 150)
        textview_allow.set_name("textview")
        textview_allow.set_buffer(tbuffer_allow)
        textview_allow.set_editable(False)
        textview_allow.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled_window_allow.add(textview_allow)
        box44c.pack_start(scrolled_window_allow, True, True, 0)
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


        # PEER PERMISSIONS
        global cbutton_incoming_traffic
        global cbutton_routing
        global cbutton_lan
        global cbutton_sending_files

        box55aa.set_size_request(-1, 15)
        box55a.set_size_request(-1, 34)
        box55b.set_size_request(-1, 34)
        box55c.set_size_request(-1, 34)
        box55d.set_size_request(-1, 34)
        box55e.set_size_request(-1, 34)
        box55f.set_size_request(-1, 34)
        #box55g.set_size_request(-1, 25)

        label55a = Gtk.Label()
        label55a.show()
        label55a.set_width_chars(1)
        box55a.pack_start(label55a, False, False, 0)

        global liststore_peers
        liststore_peers.append(['Select Peer'])
        cell_peers = Gtk.CellRendererText()
        global combobox_peers
        combobox_peers.set_size_request(293, -1)
        combobox_peers.show()
        combobox_peers.set_name("cbbox")
        combobox_peers.pack_start(cell_peers, True)
        combobox_peers.add_attribute(cell_peers, 'text', 0)
        combobox_peers.set_model(liststore_peers)
        combobox_peers.set_active(0)
        combobox_peers.connect("changed", Peers_Changed)
        box55a.pack_start(combobox_peers, False, False, 0)
        button_update_peers = Gtk.Button.new_with_label("Update Peers")
        button_update_peers.show()
        button_update_peers.set_size_request(140, -1)
        button_update_peers.connect("clicked", Button_Update_Peers_Clicked)
        box55a.pack_start(button_update_peers, False, False, 0)

        label55f = Gtk.Label()
        label55f.show()
        label55f.set_size_request(15, -1)
        box55b.pack_start(label55f, False, False, 0)

        label_nickname = Gtk.Label()
        label_nickname.set_text("Peer Nickname")
        label_nickname.set_xalign(0.0)
        label_nickname.show()
        label_nickname.set_size_request(135, -1)
        box55b.pack_start(label_nickname, False, False, 0)

        global entry_nickname
        entry_nickname.show()
        entry_nickname.set_width_chars(16)
        entry_nickname.set_size_request(75, -1)
        box55b.pack_start(entry_nickname, False, False, 0)

        button_nickname_peer = Gtk.Button.new_with_label("Set Nickname")
        button_nickname_peer.show()
        button_nickname_peer.set_size_request(140, -1)
        button_nickname_peer.connect("clicked", Button_Nickname_Peer_Clicked)
        box55b.pack_start(button_nickname_peer, False, False, 0)

        label55g = Gtk.Label()
        label55g.show()
        label55g.set_size_request(15, -1)
        box55c.pack_start(label55g, False, False, 0)

        label_incoming_traffic = Gtk.Label()
        label_incoming_traffic.show()
        label_incoming_traffic.set_text("Allow Incoming Traffic")
        label_incoming_traffic.set_xalign(0.0)
        label_incoming_traffic.set_size_request(253, -1)
        box55c.pack_start(label_incoming_traffic, False, False, 0)
        cbutton_incoming_traffic.show()
        cbutton_incoming_traffic.connect("clicked", Cbutton_Traffic_Clicked)
        box55c.pack_start(cbutton_incoming_traffic, False, False, 0)

        label55gc = Gtk.Label()
        label55gc.show()
        label55gc.set_size_request(6, -1)
        box55c.pack_start(label55gc, False, False, 0)

        button_remove_nickname = Gtk.Button.new_with_label("Remove Nickname")
        button_remove_nickname.show()
        button_remove_nickname.set_size_request(140, -1)
        button_remove_nickname.connect("clicked", Button_Remove_Nickname_Clicked)
        box55c.pack_start(button_remove_nickname, False, False, 0)

        label55b = Gtk.Label()
        label55b.show()
        label55b.set_size_request(15, -1)
        box55d.pack_start(label55b, False, False, 0)

        label_routing = Gtk.Label()
        label_routing.show()
        label_routing.set_text("Allow Routing")
        label_routing.set_xalign(0.0)
        label_routing.set_size_request(253, -1)
        box55d.pack_start(label_routing, False, False, 0)
        cbutton_routing.show()
        cbutton_routing.connect("clicked", Cbutton_Routing_Clicked)
        box55d.pack_start(cbutton_routing, False, False, 0)

        label55c = Gtk.Label()
        label55c.show()
        label55c.set_size_request(15, -1)
        box55e.pack_start(label55c, False, False, 0)

        label_lan = Gtk.Label()
        label_lan.show()
        label_lan.set_text("Allow LAN Access")
        label_lan.set_xalign(0.0)
        label_lan.set_size_request(253, -1)
        box55e.pack_start(label_lan, False, False, 0)
        cbutton_lan.show()
        cbutton_lan.connect("clicked", Cbutton_Lan_Clicked)
        box55e.pack_start(cbutton_lan, False, False, 0)

        label55e = Gtk.Label()
        label55e.show()
        label55e.set_size_request(15, -1)
        box55f.pack_start(label55e, False, False, 0)

        label_sending_files = Gtk.Label()
        label_sending_files.show()
        label_sending_files.set_text("Allow Sending Files")
        label_sending_files.set_xalign(0.0)
        label_sending_files.set_size_request(253, -1)
        box55f.pack_start(label_sending_files, False, False, 0)
        cbutton_sending_files.show()
        cbutton_sending_files.connect("clicked", Cbutton_Sendf_Clicked)
        box55f.pack_start(cbutton_sending_files, False, False, 0)

        label55gd = Gtk.Label()
        label55gd.show()
        label55gd.set_size_request(10, -1)
        box55g.pack_start(label55gd, False, False, 0)

        button_unlink_peer = Gtk.Button.new_with_label("Unlink Peer")
        button_unlink_peer.show()
        button_unlink_peer.set_size_request(140, -1)
        button_unlink_peer.connect("clicked", Button_Unlink_Peer_Clicked)
        box55g.pack_start(button_unlink_peer, False, False, 0)

        # FOOTER: ADD A STATUSBAR WITH NORDVPN VERSION
        sb = Gtk.Statusbar()
        sb.show()
        box99c.pack_start(sb, True, True, 0)
        result = subprocess.Popen("/usr/bin/nordvpn version", shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        rc = result.wait()
        out, err = result.communicate()
        push = " " + str(out).strip()
        sb.push(0, push)

        win.present()


# START A THREAD THAT GETS THE NORDVPN STATUS EVERY 4 SECONDS
thread = Thread(target=Get_Nordvpn_Status)
thread.daemon = True
thread.start()


# START A THREAD THAT GETS THE INCOMING FILE LIST EVERY 10 SECONDS
thread1 = Thread(target=Get_Incoming_Files)
thread1.daemon = True
thread1.start()


sleep(1)

# START THE APPLICATION
def main():
    app = MyApplication()
    app.run(None)

if __name__ == "__main__":
    main()
