
import socket
import platform


def check_memory():
    
    meminfo = {}
    with open('/proc/meminfo') as f:
        for line in f:
           parts = line.split(":")
           number = parts[1].split()
           meminfo[parts[0]]=int(number[0])
  
    
    used = round(100 - ((meminfo['MemAvailable'])/(meminfo['MemTotal']) * 100),1)
    total = meminfo['MemTotal']
    available = meminfo['MemAvailable']
    

    if used >=85 :
        status = "WARN"
    else:
        status = "OK"

    result = {
        "total_kb": total, 
        "available_kb":available,
        "used_percntage":used, 
        "status": status
    }

    
    return result





def check_host():
    hostname = socket.gethostname()
    kernel_version = platform.release()

    result = {
        "hostname": hostname,
        "kernel_version": kernel_version
    }
    return result


def check_uptime(): 

    with open('/proc/uptime') as f:

        line = f.read().split()

        days = divmod(int(float(line[0])), 86400)
        
        hours = divmod(days[1],3600)
        
        minutes = divmod(hours[1], 60)
        

        uptime = {"uptime_human":(f"{days[0]}d, {hours[0]}h, {minutes[0]}m"),
                  "uptime_seconds":float(line[0])
        }
        

        return uptime




def main():

    print(check_memory())
    print(check_host())
    print(check_uptime())

if __name__ =="__main__":
    main()

            
