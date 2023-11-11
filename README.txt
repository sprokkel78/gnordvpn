# gtop

A graphical user interface in pygtk for Process and Network overview on Mac mini.
It requires Homebrew, Python3.11 and PyGObject.

1. Install Homebrew
2. $/opt/homebrew/bin/brew install python3 python3-pip
3. $/opt/homebrew/bin/brew install pygobject3 gtk+3
4. $/opt/homebrew/bin/pip3 install psutil
5. $/opt/homebrew/bin/pip3 install gtop-sprokkel78
6. $cd /opt/homebrew/lib/python3.11/site-packages/gtop_sprokkel78
7. $/opt/homebrew/bin/python3 ./gtop.py

Don't forget to run the app with the python3 binary that was installed 
with homebrew. It's in /opt/homebrew/bin/python3  

Note: You must run gtop.py from it's own directory or it won't find the css file.