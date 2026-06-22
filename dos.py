from scapy.all import *
import time
import concurrent.futures

def send_packet(domain, ip):
    EtherLayer = Ether()
    IPLayer = IP(dst=ip)
    Packet = EtherLayer/IPLayer
    sendp(Packet, iface="eth0")  # eth0 is the interface you want to use

if __name__ == "__main__":
    domain = input("Enter the domain: ")
    ip = input("Enter the IP address: ")
    
    try:
        resolved_ip = gethostbyname(domain)
        if resolved_ip != ip:
            print('Warning: The resolved IP does not match the provided IP.')
    except Exception as e:
        print(str(e))
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit a task for every CPU core in your system
        futures = [executor.submit(send_packet, domain, ip) for _ in range(os.cpu_count())]
