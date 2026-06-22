from scapy.all import *
import time
import concurrent.futures

def send_packet(domain):
    ip = gethostbyname(domain)
    EtherLayer = Ether()
    IPLayer = IP(dst=ip)
    Packet = EtherLayer/IPLayer
    sendp(Packet, iface="eth0")   # eth0 is the interface you want to use

if __name__ == "__main__":
    domain  = input("Enter the domain: ")
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_packet, domain) for _ in range(os.cpu_count())]
