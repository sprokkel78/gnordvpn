gnordvpn-sprokkel78

A graphical user interface in PyGTK3 for using the nordvpn client binary on Ubuntu and other Linux distro's. 
It requires Python3.10 and the PyGTK apps, it also relies on gnome-terminal for accepting
and sending files. Developed on Fedora 40 and tested on Ubuntu 24.04. 

![Screenshot](https://github.com/sprokkel78/gnordvpn/blob/develop/screenshots/gnordvpn-5.png)

Installation on Fedora 40 & Ubuntu 24.04:

1. $git clone https://github.com/sprokkel78/gnordvpn.git
2. $cd gnordvpn
3. $python3 ./gnordvpn.py

For System-Wide Installation, run:
- $sudo ./install.sh

Then start with:
- $gnordvpn
- or by clicking the application icon.

Note: check CHANGELOG.txt for additional notes and changes.

Note: check https://github.com/NordSecurity/nordvpn-linux/issues for issue's with the nordvpn binary.

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

