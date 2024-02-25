#!/bin/sh
#
# THIS SCRIPT WILL INSTALL THE GNORDVPN APP SYSTEM WIDE
# THE SCRIPT MUST BE RUN WITH SUDO
#
# It will create a startup shell script named gnordvpn in /usr/bin,
# the app will be placed in /usr/share/gnordvpn-sprokkel78
# The .desktop file will be placed in /usr/share/applications/ as com.sprokkel78.gnordvpn.desktop

FILE="/usr/share/applications/gnordvpn.desktop"
if [ -f $FILE ]
then
  rm $FILE
fi

mkdir -p /usr/share/gnordvpn-sprokkel78
cp -r ./* /usr/share/gnordvpn-sprokkel78/
echo "#!/bin/sh" > /usr/bin/gnordvpn
echo "cd /usr/share/gnordvpn-sprokkel78" >> /usr/bin/gnordvpn
echo "python3 ./gnordvpn.py" >> /usr/bin/gnordvpn
cp ./gnordvpn.desktop /usr/share/applications/com.sprokkel78.gnordvpn.desktop
chmod 755 /usr/bin/gnordvpn
chmod 644 /usr/share/gnordvpn-sprokkel78/*
chmod 644 /usr/share/gnordvpn-sprokkel78/images/*
chmod 755 /usr/share/gnordvpn-sprokkel78/images
