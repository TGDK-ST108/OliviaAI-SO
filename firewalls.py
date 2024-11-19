from scapy.all import IP, TCP, UDP

class BaseFirewall:
    """Base class for firewall rules."""
    def allow_packet(self, packet):
        """Determine if a packet is allowed. Override this method."""
        raise NotImplementedError("This method should be overridden.")

class UnderfoldFirewall(BaseFirewall):
    """Firewall that blocks packets based on IP addresses."""
    def __init__(self):
        self.blocked_ips = set()  # Set of blocked IP addresses

    def add_blocked_ip(self, ip):
        """Add an IP address to the blocked list."""
        self.blocked_ips.add(ip)

    def allow_packet(self, packet):
        """Check if the packet's source IP is blocked."""
        if IP in packet:
            if packet[IP].src in self.blocked_ips:
                return False
        return True

class BlanketFirewall(BaseFirewall):
    """Firewall that blocks all incoming packets by default."""
    def allow_packet(self, packet):
        """Allow packets based on a custom logic (currently denies all)."""
        return False  # Deny all packets

class PlateFirewall(BaseFirewall):
    """Firewall that allows specific ports."""
    def __init__(self):
        self.allowed_ports = {80, 443}  # HTTP and HTTPS by default

    def add_allowed_port(self, port):
        """Add a port to the allowed list."""
        self.allowed_ports.add(port)

    def allow_packet(self, packet):
        """Check if the packet's destination port is allowed."""
        if TCP in packet or UDP in packet:
            if packet[TCP].dport in self.allowed_ports or packet[UDP].dport in self.allowed_ports:
                return True
            else:
                return False
        return True  # Allow non-TCP/UDP packets by default

# Example usage:
if __name__ == "__main__":
    # Initialize firewalls
    underfold_firewall = UnderfoldFirewall()
    blanket_firewall = BlanketFirewall()
    plate_firewall = PlateFirewall()

    # Block specific IPs
    underfold_firewall.add_blocked_ip("192.168.1.10")

    # Check packets
    example_packet_ip_blocked = IP(src="192.168.1.10") / TCP(dport=80)
    example_packet_port_allowed = IP(src="192.168.1.20") / TCP(dport=80)
    example_packet_port_blocked = IP(src="192.168.1.20") / TCP(dport=8080)

    print("Underfold Firewall - Blocked IP:", underfold_firewall.allow_packet(example_packet_ip_blocked))  # False
    print("Plate Firewall - Allowed Port (80):", plate_firewall.allow_packet(example_packet_port_allowed))  # True
    print("Plate Firewall - Blocked Port (8080):", plate_firewall.allow_packet(example_packet_port_blocked))  # False
