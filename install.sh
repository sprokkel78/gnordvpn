#!/bin/sh
#
# THIS SCRIPT WILL INSTALL THE GNORDVPN APP SYSTEM WIDE
# THE SCRIPT MUST BE RUN WITH SUDO
#
# It will create a startup shell script named gnordvpn in /usr/bin,
# the app will be placed in /usr/share/gnordvpn-sprokkel78
# The .desktop file will be placed in /usr/share/applications/
#
mkdir -p /usr/share/gnordvpn-sprokkel78
cp -r ./* /usr/share/gnordvpn-sprokkel78/
cp ./gnordvpn.svg /usr/share/icons/hicolor/scalable/apps/
cp ./gnordvpn.png /usr/share/icons/hicolor/48x48/apps/
echo "#!/bin/sh" > /usr/bin/gnordvpn
echo "cd /usr/share/gnordvpn-sprokkel78" >> /usr/bin/gnordvpn
echo "python3 ./gnordvpn.py" >> /usr/bin/gnordvpn
cp ./gnordvpn.desktop /usr/share/applications/com.sprokkel78.gnordvpn.desktop
chmod 755 /usr/bin/gnordvpn
chmod 644 /usr/share/gnordvpn-sprokkel78/*
chmod 644 /usr/share/gnordvpn-sprokkel78/images/*
chmod 755 /usr/share/gnordvpn-sprokkel78/images
