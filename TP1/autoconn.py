
import subprocess 
import re
import time

def get_wifi():
    waa = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'])
    waa = waa.decode('cp850') 
    waa= waa.replace("\r","") 
    out = re.findall(r'SSID\s*:\s*([^\r\n]+)',waa,re.DOTALL)[0]
    print(f'using default wifi {out} ')
    return out

try:
    saved_wifi = get_wifi()
except IndexError:
    saved_wifi = None 
    print("you are not connected to any wifi, a default wifi will not be used")

while True:
    subprocess.check_output(['netsh', 'wlan', 'disconnect'])

    wap = subprocess.check_output(['netsh','wlan','show','network','mode=bssid']) 

    wap = wap.decode('cp850') 
    wap= wap.replace("\r","") 

    signal = re.findall(r'Signal\s*:\s*(\d+)', wap, re.DOTALL)
    signal = [int(_) for _ in signal]
    names = re.findall(r'SSID\s\d+\s:\s([^\r\n]+)', wap, re.DOTALL)  

    a = (list(zip(signal,names)))
    test = max(a, key=lambda x: int(x[0]))
    strongest = test[1]
    print(f"the strongest wifi is : {strongest}")
    try:
        check = subprocess.check_output(['netsh', 'wlan', 'connect', 'name=' + strongest])
        check = check.decode('cp850')
        # print(check)
    except subprocess.CalledProcessError:
        if saved_wifi:
            print("Error connecting, using last connected wifi")
            subprocess.check_output(['netsh', 'wlan', 'connect', 'name=' + saved_wifi])
        else: 
            print("error connecting, no saved wifi")    
    time.sleep(10)
