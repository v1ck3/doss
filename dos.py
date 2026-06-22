import os
import random
from requests_futures.sessions import FuturesSession
from ratelimiter import RateLimiter
from scapy.all import *
import threading

# User-Agents List (This is just an example, you should replace it with your own)
USER_AGENTS = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"]

# Limit the number of requests to 1 every second
rate_limiter = RateLimiter(max_calls=1, period=1)

def send_packet(domain):
    ip = socket.gethostbyname(domain)   # Resolve IP address from domain name
    EtherLayer = Ether()
    IPLayer = IP(dst=ip)
    Packet = EtherLayer/IPLayer         # Create the packet to be sent
    
    with rate_limiter:  # Applying rate limiting here
        sendp(Packet, iface="eth0")   # Send the packet

# Function for sending requests in parallel using FuturesSession() from requests-futures library.
def stress_test(domain):
    with FuturesSession() as session:
        while True:
            try:
                if threading.active_count() == 15000:   # Limit the number of active threads to 15000
                    future = session.get(domain, headers={'User-Agent': random.choice(USER_AGENTS)})
                    future.result()                      # This will wait for the response (or raise an exception if there was a problem)
                    send_packet(domain)                  # Send packet after successful request
                time.sleep(1)                            # Sleep for 1 second before checking again
            except KeyboardInterrupt:                     # Handle keyboard interrupts (Ctrl+C)
                break

if __name__ == "__main__":
    domain = input("Enter the domain name to stress test: ")
    
    if os.path.exists(domain):                            # Domain does not exist if this file exists
        print('Domain does not exist')
    else:
        print(f'Starting stress test on {domain}...\nPress Ctrl+C to stop.')
        stress_test(domain)                               # Start the stress testing function
