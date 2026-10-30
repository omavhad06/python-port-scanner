import socket
import argparse
import time
from concurrent.futures import ThreadPoolExecutor


def scan_port(host, port, timeout=0.5):
    """Return (port, is_open, banner) for one port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        if s.connect_ex((host, port)) == 0:
            banner = ""
            try:
                banner = s.recv(1024).decode(errors="ignore").strip()
            except Exception:
                pass  # many services stay silent until you talk first
            return port, True, banner
    except Exception:
        pass
    finally:
        s.close()
    return port, False, ""


def parse_ports(text):
    """Turn '1-1000' or '80' into a list of ports."""
    if "-" in text:
        start, end = text.split("-")
        return range(int(start), int(end) + 1)
    return [int(text)]


def service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("host", help="IP or domain to scan")
    parser.add_argument("-p", "--ports", default="1-1024", help="e.g. 1-1000 or 80")
    parser.add_argument("-t", "--threads", type=int, default=100)
    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print("Could not resolve that host.")
        return

    ports = parse_ports(args.ports)
    print(f"Scanning {args.host} ({ip}) ...")
    start_time = time.time()
    open_count = 0

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = executor.map(lambda p: scan_port(ip, p), ports)
        for port, is_open, banner in results:
            if is_open:
                open_count += 1
                line = f"Port {port:<5} OPEN  ({service_name(port)})"
                if banner:
                    line += f"  banner: {banner[:50]}"
                print(line)

    print(f"\nDone. {open_count} open port(s) in {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    main()