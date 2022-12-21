#!/usr/bin/env python

import subprocess
import optparse
import re
from randmac import RandMac



def rand_mac_generator():
    example_mac = "00:00:00:00:00:00"
    generated_mac = RandMac(example_mac)
    return generated_mac

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    return options

def change_mac(interface, generated_mac):
    print("[+] Changing MAC address for " + interface + " to " + generated_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", generated_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

generated_mac = rand_mac_generator()

change_mac(options.interface,str(generated_mac))

current_mac = get_current_mac(options.interface)
if current_mac == str(generated_mac):
    print("[+] MAC address was successfully changed to : " + current_mac)
else:
    print("[-] MAC address did not changed. ")
