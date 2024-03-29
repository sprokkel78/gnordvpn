gnordvpn-sprokkel78

A graphical user interface in PyGTK for using the nordvpn client binary on Ubuntu and other Linux distro's. 
It requires Python3.10 or higher, Pip, Venv and the PyGTK apps, it also relies on gnome-terminal for accepting
and sending files. Developed and tested on Ubuntu 23.10. 

Installation on Ubuntu 23.10

1. $sudo apt install python3 python3-dev python3-pip python3-venv
2. $sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
3. $sudo apt install gnome-terminal
4. $python3 -m venv --system-site-packages /home/USERNAME/Python3
5. $cd /home/USERNAME/Python3/bin
6. $./pip install gnordvpn-sprokkel78
7. $cd /home/USERNAME/Python3/lib/python3.11/site-packages/gnordvpn_sprokkel78
8. $/home/USERNAME/Python3/bin/python3 ./gnordvpn.py

Note: You must start gnordvpn.py from its own directory or it will not find the css file.
Note: check CHANGELOG.txt for additional notes and changes.

Added 'install.sh' script for system-wide installation.
- The startup shell script will be /usr/bin/gnordvpn
- The application is installed in /usr/share/gnordvpn-sprokkel78
- The .desktop file is placed in /usr/share/applications/com.sprokkel78.gnordvpn.desktop

Added 'uninstall.sh' script for system-wide uninstallation.
- This will delete /usr/bin/gnordvpn and /usr/share/gnordvpn-sprokkel78,
  This will also remove /usr/share/applications/com.sprokkel78.gnordvpn.desktop
  
Check https://www.github.com/sprokkel78/gnordvpn for contributing, development features and pre-releases.

Check https://pypi.org/project/gnordvpn-sprokkel78/ for the full python package.

Funding: Paypal email: sprokkel78.bart@gmail.com
