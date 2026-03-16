
# Author: Angel Mendez

from scapy.all import *
from socket import gethostbyname
from subprocess import getstatusoutput
from sys import argv

def getAsNumber(ip):
    status, output = getstatusoutput(f"whois {ip}")
    
    for line in output.split("\n"):
        if "origin" in line.lower() or "OriginAS" in line:
            parts = line.split()
            for part in parts:
                if part.startswith("AS"):
                    return part
    return None


def reverseDns(ip):
    status, output = getstatusoutput(f"host {ip}")
    
    if status == 0:
        return output.split()[-1]
    return None



def main():
    if len(argv) != 3:
        print("Usage: python3 lab7.py <target> <maxHops>")
        return

    target = argv[1]
    maxHops = int(argv[2])
    targetIp = gethostbyname(target)

    print(f"route to {target} ({targetIp}), {maxHops} hops max")

    asList = []

    for ttl in range(1, maxHops + 1):
        packet = IP(dst=targetIp, ttl=ttl) / TCP(dport=80, flags="S")
        
        reply = sr1(packet, verbose=0, timeout=3)
        
        if reply is None:
            print(f"{ttl} - * * *")
        else:
            hopIp = reply.src
            print(f"{ttl} - {hopIp}")

            name = reverseDns(hopIp)
            
            if name:
                print(f"    ({name})")

            asNumber = getAsNumber(hopIp)
            
            if asNumber:
                asList.append(asNumber)

            if hopIp == targetIp:
                break
                
                
    uniqueAs = []
    
    for a in asList:
    
        if a not in uniqueAs:
            uniqueAs.append(a)

    if uniqueAs:
        print("Traversed AS numbers: " + " -> ".join(uniqueAs))

if __name__ == "__main__":
    main()
