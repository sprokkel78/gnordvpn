gnordvpn-sprokkel78

A graphical user interface in PyGTK for using the nordvpn client binary on Ubuntu and other Linux distro's. 
It requires Python3.10 or higher, Pip, Venv and the PyGTK apps, it also relies on gnome-terminal for accepting
and sending files. Developed and tested on Ubuntu 23.04. 

Installation on Ubuntu 23.04

1. $sudo apt install python3 python3-dev python3-pip python3-venv
2. $sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
3. $sudo apt install gnome-terminal
4. $python3 -m venv /home/USERNAME/Python3
5. $cd /home/USERNAME/Python3/bin
6. $./pip install gnordvpn-sprokkel78
7. $cd /home/USERNAME/Python3/lib/python3.11/site-packages/gnordvpn_sprokkel78
8. $python3 ./gnordvpn.py

Note: check CHANGELOG.txt for additional notes and changes.

Added 'install.sh' script for system-wide installation.
- The startup shell script will be /usr/bin/gnordvpn
- The application is installed in /usr/share/gnordvpn-sprokkel78
- The .desktop file is placed in /usr/share/applications

Added 'uninstall.sh' script for system-wide uninstallation.
- This will delete /usr/bin/gnordvpn and /usr/share/gnordvpn-sprokkel78,
  This will also remove /usr/share/applications/gnordvpn.desktop
