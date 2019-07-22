import re as Regex

# Separates IPv4 into 4 parts with its CIDR as last entry
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
    return matches

def readIPClass(first_octet):
    if first_octet:
        number = int(first_octet)
        if (number >= 0 and number <= 127): return "A"
        elif (number >= 128 and number <= 191): return "B"
        elif  (number >= 192 and number <= 223): return "C"
        elif (number >= 224 and number <= 239): return "D"
        elif  (number >= 239 and number <= 256): return "E"
    else: raise Exception("IP is Invalid")


# Gets Subnet Mask From CIDR
def get_subnetmask(cidr):
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


# Prints IP Info
def print_ip_info():
    ip = readIP()
    *ip_octets, cidr = ip
    subnet_mask = get_subnetmask(int(cidr))
    network_id = [ip_octets[i] if bool(int(subnet_mask[i], 0))
    else 0 for i in range(4)]
    ipClass = readIPClass(ip_octets[0])
    
    print(f"""
    IP is {ip_octets}
    IP Class is {ipClass}
    CIDR is {cidr}
    Subnet is {[int(el,0) for el in subnet_mask]}
    Network ID is {network_id}
    """)

print_ip_info()

# http://www.steves-internet-guide.com/subnetting-subnet-masks-explained/