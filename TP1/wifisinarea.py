import platform
import subprocess
import re
import time
import os
import platform



def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")    


def read_data_from_cmd():
    if platform.system() == 'Windows':
        cmd = "netsh wlan show networks mode=bssid"
    elif platform.system() == 'Linux':
        cmd = "iwconfig"
    else:
        raise Exception('Unsupported OS')

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode('cp850').strip()
    tot = []
    if platform.system() == 'Linux':
        m = re.findall(r'(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
    elif platform.system() == 'Windows':
        signal = re.findall(r'Signal\s*:\s*(\d+)%', out, re.DOTALL)
        names = re.findall(r'SSID\s\d+\s:\s([^\r\n]+)', out, re.DOTALL)
        tot = list(zip(names, signal))
        tot = [(x[0],int(x[1])) for x in tot]
        tot2=sorted(tot, key=lambda x: x[1],reverse=1)
    if tot2:
        return tot2
    
    return None

subprocess.run(['netsh', 'wlan', 'disconnect'], check=True)

while True:
    data = read_data_from_cmd()

    if data:
        for ssid, signal in data:
            print(f"SSID: {ssid}, Signal: {signal}%")

    time.sleep(2)
    clear_terminal()