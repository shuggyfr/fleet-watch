import subprocess
import socket
import platform
import os


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


 

def check_cpu_load():

    with open("/proc/loadavg") as f:

        loads = f.read().split()
        load_1 = float(loads[0])
        load_2 = float(loads[1])
        load_3 = float(loads[2])

        core_count = os.cpu_count()

        per_core_1m = load_1 / core_count
        per_core_5m = load_2 / core_count
        per_core_15m = load_3 / core_count


# if the 15 minute load per core is 1.8 or greater then the load has had a queue for a long time
# if the 5 minute load per core is is 0.8 or greater then the load per core is getting busy and should be handled
#  anything else is good
        if per_core_15m  >= 1.8:
            status = "CRIT"

        elif per_core_5m >= 0.8:
            status = "WARN"

        else:
            status = "OK"

        cpu_load = {
            "load_1min" : per_core_1m,
            "load_5min" : per_core_5m,
            "load_15min" : per_core_15m,
            "status" : status

        }

    return cpu_load

def disk_check():

    used_pct ={}
    files_info = subprocess.run('df', capture_output=True,text=True)
    for line in files_info.stdout.splitlines()[1:]:
        output = line.split()

        if output[0].startswith('/dev'):
            used_pct[output[5]]=int(output[4].strip("%"))

    values = used_pct.values()
    highest = max(values)

    if highest >= 95:
        status = "CRIT"
    
    elif highest >= 80:
        status = "WARN"

    else:
        status = "OK"

    results = {
        "disks" : used_pct,
        "status": status
    }

    return results


def check_processes():

    processes = subprocess.run(["ps", "-eo", "pid,user,%mem,comm", "--sort=-%mem"], capture_output=True, text=True)
    per_process =  []
    for line in processes.stdout.splitlines()[1:6]:
        output = line.split()

        info = {
            "pid":int(output[0]),
            "user": output[1],
            "mem_pct":float(output[2]),
            "command":output[3]
        }

        per_process.append(info)

    return per_process



def check_ssh_failures():

    ssh_failures = subprocess.run(["journalctl","_COMM=sshd-session","--since","24 hours ago"], capture_output=True, text=True)
    ips = []
    count = 0
    for line in ssh_failures.stdout.splitlines():
        
        
        if "Invalid user" in line:
            parts = line.split()
            count+=1
            output = parts[parts.index("from")+1]
            ips.append(output)

    ip_counts ={}
    for ip in ips:
        if ip in ip_counts:
            ip_counts[ip]+=1

        else:
            ip_counts[ip]=1

    result = {
                "failed_logins":count,
                "ip_counts":ip_counts
            }
    
    return result


def main():
    
    print(check_memory())
    print(check_host())
    print(check_uptime())
    print(check_cpu_load())
    print(disk_check())
    print(check_processes())
    print(check_ssh_failures())

if __name__ =="__main__":
    main()

            
