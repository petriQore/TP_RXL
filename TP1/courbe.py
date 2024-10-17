import subprocess
import platform
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def read_data_from_cmd():
    if platform.system() == 'Windows':
        cmd = "netsh wlan show interfaces"
    elif platform.system() == 'Linux':
        cmd = "iwconfig"
    else:
        raise Exception('Unsupported OS')

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()

    out = out.decode('unicode_escape').strip()

    if platform.system() == 'Linux':
        m = re.findall(r'(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
    elif platform.system() == 'Windows':
        m = re.findall(r'Signal\s+:\s+(\d+)%', out, re.DOTALL)

    if m:
        return int(m[0]) 
    return None

def update(frame):
    signal_power = read_data_from_cmd()
    if signal_power is not None:
        data.append(signal_power) 
        if len(data) > max_points:  
            data.pop(0)

        ax.clear()
        ax.plot(data, label='Signal Power (%)')
        ax.set_ylim(0, 100) 
        ax.set_ylabel('Signal Power (%)')
        ax.set_title('Real-time Wi-Fi Signal Strength')
        ax.legend(loc='upper right')

fig, ax = plt.subplots()
data = []
max_points = 100  
ani = FuncAnimation(fig, update, interval=200)

plt.show()
