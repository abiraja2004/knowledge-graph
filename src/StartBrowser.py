import subprocess
import webbrowser
import sys
import _thread

url = "http://localhost:7474/browser/"
if sys.platform == 'darwin':  # in case of OS X
    subprocess.Popen(['open', url])
else:
    webbrowser.open_new_tab(url)
