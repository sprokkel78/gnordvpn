#!/bin/sh
#
# THIS SCRIPT WILL INSTALL THE GNORDVPN APP SYSTEM WIDE
# THE SCRIPT MUST BE RUN WITH SUDO
#
# It will create a startup shell script named gnordvpn in /usr/bin,
# the app will be placed in /usr/share/gnordvpn-sprokkel78
#
mkdir -p /usr/share/gnordvpn-sprokkel78
cp ./gnordvpn* /usr/share/gnordvpn-sprokkel78/
echo "#!/bin/sh" > /usr/bin/gnordvpn
echo "cd /usr/share/gnordvpn-sprokkel78" >> /usr/bin/gnordvpn
echo "python3 ./gnordvpn.py" >> /usr/bin/gnordvpn
chmod 755 /usr/bin/gnordvpn
chmod 644 /usr/share/gnordvpn-sprokkel78/*
