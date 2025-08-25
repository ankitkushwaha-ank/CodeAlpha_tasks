# ========================================
# Basic Network Sniffer using Scapy
# Works on Windows (Layer 3 sniffing)
# ========================================

from scapy.all import sniff, # ========================================
# Basic Network Sniffer using Scapy
# Works on Windows (Layer 3 sniffing)
# ========================================

from scapy.all import sniff, IP, TCP, UDP, Raw

def packet_callback(packet):
    print("\n=== New Packet Captured ===")

    # IP Layer
    if packet.haslayer(IP):
        ip = packet[IP]
        print(f"[IP] Src: {ip.src} -> Dst: {ip.dst}")
        print(f"    Protocol: {ip.proto}, TTL: {ip.ttl}")

    # TCP Layer
    if packet.haslayer(TCP):
        tcp = packet[TCP]
        print(f"[TCP] Src Port: {tcp.sport} -> Dst Port: {tcp.dport}")

    # UDP Layer
    elif packet.haslayer(UDP):
        udp = packet[UDP]
        print(f"[UDP] Src Port: {udp.sport} -> Dst Port: {udp.dport}")

    # Payload (application data inside packet)
    if packet.haslayer(Raw):
        payload = packet[Raw].load
        try:
            text = payload.decode(errors="ignore")
            print(f"[Payload] {text}")
        except Exception:
            print(f"[Payload - Raw Bytes] {payload}")

# ========================================
# Run the Sniffer
# ========================================
if __name__ == "__main__":
    print("🚀 Starting Packet Sniffer... Press Ctrl+C to stop.")
    sniff(prn=packet_callback, store=False)  # store=False prevents memory bloat
 Raw

def packet_callback(packet):
    print("\n=== New Packet Captured ===")

    # IP Layer
    if packet.haslayer(IP):
        ip = packet[IP]
        print(f"[IP] Src: {ip.src} -> Dst: {ip.dst}")
        print(f"    Protocol: {ip.proto}, TTL: {ip.ttl}")

    # TCP Layer
    if packet.haslayer(TCP):
        tcp = packet[TCP]
        print(f"[TCP] Src Port: {tcp.sport} -> Dst Port: {tcp.dport}")

    # UDP Layer
    elif packet.haslayer(UDP):
        udp = packet[UDP]
        print(f"[UDP] Src Port: {udp.sport} -> Dst Port: {udp.dport}")

    # Payload (application data inside packet)
    if packet.haslayer(Raw):
        payload = packet[Raw].load
        try:
            text = payload.decode(errors="ignore")
            print(f"[Payload] {text}")
        except Exception:
            print(f"[Payload - Raw Bytes] {payload}")

# ========================================
# Run the Sniffer
# ========================================
if __name__ == "__main__":
    print("🚀 Starting Packet Sniffer... Press Ctrl+C to stop.")
    sniff(prn=packet_callback, store=False)  # store=False prevents memory bloat
