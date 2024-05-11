gnordvpn-sprokkel78

A graphical user interface in PyGTK for using the nordvpn client binary on Ubuntu and other Linux distro's. 
It requires Python3.10 or higher, Pip, Venv and the PyGTK apps, it also relies on gnome-terminal for accepting
and sending files. Developed and tested on Ubuntu 24.04. 

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
