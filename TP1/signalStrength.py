import subprocess
import platform
import re
import time
import sys

def read_data_from_cmd():
    p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    out = out.decode('unicode_escape').strip()
    # print(out)
    if platform.system() == 'Linux':
        m = re.findall(r'(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
    elif platform.system() == 'Windows':
        m = re.findall(r'Name\s+:\s+(.*?)\n.*?Signal\s+:\s+([0-9]+)%', out, re.DOTALL)
    else:
        raise Exception('Unsupported platform')
    
    if m:
        return f"Signal: {m[0][1]} dBm"
    return "No data"

while True:
    data = read_data_from_cmd()
    sys.stdout.write(f"\r{data}")
    sys.stdout.flush()
    time.sleep(0.5)