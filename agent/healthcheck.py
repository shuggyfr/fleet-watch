import subprocess
import json


def check_memory():
    result = {}
    meminfo = {}
    with open('/proc/meminfo') as f:
        for line in f:
           parts = line.split(":")
           number = parts[1].split()
           meminfo[parts[0]]=int(number[0])
  
    
    used = round(100 - ((meminfo['MemAvailable'])/(meminfo['MemTotal']) * 100),1)
    total = meminfo['MemTotal']
    available = meminfo['MemAvailable']
    status =""

    if used >=85 :
        status = "WARN"
    else:
        status = "OK"

    result = {'totalK_B': total, 'available':available,'used%':used, 'status': status}

    
    return result


print(check_memory())


