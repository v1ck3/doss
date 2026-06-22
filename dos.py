import socket
from scapy.all import *
import threading
import time

# Function to send packet to a domain name
def send_packet(domain):
    try:
        ip = socket.gethostbyname(domain)  # Resolve the IP address of the domain
        EtherLayer = Ether()
        IPLayer = IP(dst=ip)
        Packet = EtherLayer/IPLayer
        sendp(Packet, iface="eth0")   # eth0 is the interface you want to use
    except Exception as e:
        print("Error sending packet: ", str(e))  # Handle exceptions here

# Main function that creates threads and handles rate limiting
def stress_test(domain):
    while True:
        try:
            if threading.active_count() == 15000:   # Limit the number of active threads to 15000
                send_packet(domain)                 # If not sending packets, this function will create a new one
            time.sleep(0)                            # Sleep for 1 second before checking again
        except KeyboardInterrupt:                    # Handle keyboard interrupts (Ctrl+C)
            break

if __name__ == "__main__":
    domain = input("Enter the domain name to stress test: ")
    if os.path.exists(domain):                            # Domain does not exist if this file exists
        print('Domain does not exist')
    else:
        print(f'Starting stress test on {domain}...\nPress Ctrl+C to stop.')
        stress_test(domain)                               # Start the stress testing function
