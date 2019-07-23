import re as Regex

 # Reads IP Class
def readIPClass(first_octet):
    if first_octet:
        number = int(first_octet)
        if (number >= 0 and number <= 127): return "A"
        elif (number >= 128 and number <= 191): return "B"
        elif  (number >= 192 and number <= 223): return "C"
        elif (number >= 224 and number <= 239): return "D"
        elif  (number >= 240 and number <= 255): return "E"
    else: raise Exception("IP is Invalid")

# Gets IP from user and separates IPv4 into 5 parts with its CIDR as last entry
def readIP():
    ip = input("""
    Enter IP like the following:
    x.x.x.x/cidr
    """)
    regexPattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\/(\d{1,2})$"
    matches = None
    if Regex.match(regexPattern, ip):
        matches = Regex.findall(regexPattern, ip).pop()
    else: raise Exception("IP is invalid")
    if (matches is not None):
        *ip_octets, cidr = matches
        return {
            "octets":ip_octets, # Octets
            "cidr":cidr, # Cidr
            "class":readIPClass(ip_octets[0]),
        }
    else: raise Exception("Unexpected error")


# Gets Subnet Mask From CIDR
def readIPSubnet(cidr):
    if cidr is not None and cidr <= 32:
        subnet_octets = []
        prepend = "0b"
        reminder = cidr % 8
        even_cidr = cidr - reminder
        for i in range(4):
            if even_cidr > 0:
               subnet_octets.append((prepend+(8 * "1")))
               even_cidr-=8
            elif reminder > 0:
                subnet_octets.append((prepend+(reminder * "1")+("0"* (8-reminder))))
                reminder-=reminder
            elif even_cidr == 0 and reminder == 0:
                subnet_octets.append(prepend+'0')
        return subnet_octets
    else: raise Exception("Unsupported CIDR Value")

# Gets the no. of Networks and IPs we can have
def readNumOfNetworksAndIPs(ipClass, cidr):
    retval = {
        "ips":"N/A",
        "hosts":"N/A",
        "subnetworks":"N/A"
    }
    no_of_borrowed_bits = 0
    no_of_host_bits = 32 - cidr

    if ipClass == "A":
        if (cidr>=8):
            no_of_borrowed_bits = cidr - 8
        else: raise Exception("Minimum Network bits are invalid")
    elif ipClass == "B":
        if (cidr>=16):
            no_of_borrowed_bits = cidr - 16
        else: raise Exception("Minimum Network bits are invalid")
    elif ipClass == "C":
        if (cidr>=24):
            no_of_borrowed_bits = cidr - 24
        else: raise Exception("Minimum Network bits are invalid")
    else: return retval

    retval["ips"] = 2**no_of_host_bits
    if (retval["ips"]>2):
        retval["hosts"] = retval["ips"] - 2
    retval["subnetworks"] = 2**no_of_borrowed_bits
    return retval

# Prints IP Info
def run():
    ip_data = readIP()
    octets = ip_data["octets"]
    cidr = ip_data["cidr"]
    ip_class = ip_data["class"]

    subnet_mask = [int(el, 0) for el in readIPSubnet(int(cidr))]
    network_id = [octets[i] if bool(subnet_mask[i])
    else 0 for i in range(4)]
    
    networks_data = readNumOfNetworksAndIPs(ip_class, int(cidr))

    print(f"""
    IP is {octets}
    IP Class is {ip_class}
    CIDR is {cidr}
    Subnet is {subnet_mask}
    Network ID is {network_id}
    Available IPs per Network {networks_data["ips"]}
    Available Hosts per Network {networks_data["hosts"]}
    No. of Networks {networks_data["subnetworks"]}
    """)

run()
