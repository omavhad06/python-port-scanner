# Python Port Scanner

A simple multithreaded TCP port scanner written in Python.

## What it does

Scans a host for open TCP ports using Python's `socket` module and `threading`.
For each open port it shows the common service name and, when available, the service banner.

## How to run

**Requirements:** Python 3.8 or newer. No external libraries needed.

```bash
# Scan the default range (ports 1-1024) on your own machine
python scanner.py 127.0.0.1

# Scan a larger range
python scanner.py 127.0.0.1 -p 1-10000

# Scan a single port
python scanner.py 127.0.0.1 -p 8000

# Change the number of threads (default is 100)
python scanner.py 127.0.0.1 -t 200
```

**To test with a known open port**, start a local web server in a second terminal:

```bash
python -m http.server 8000
```

Then scan port 8000 and it should show as open.

## Example output

```
Scanning 127.0.0.1 (127.0.0.1) ...
Port 8000  OPEN  (unknown)

Done. 1 open port(s) in 1.12s
```

> Replace this with the output (or a screenshot) from your own run.

## What I learned

- **Sockets:** how a TCP connection works at a basic level, and how `connect_ex()` returns 0 when a port accepts a connection and a non-zero error code when it doesn't.
- **Threading:** scanning ports one at a time is slow because of timeouts, and using `ThreadPoolExecutor` to check many ports at once makes scans much faster.
- **Comparing with Nmap:** I ran Nmap on the same target and compared its results with my scanner's. This showed me what a real tool does beyond a basic connect scan, such as service detection and different scan types.
- **Command-line tools:** using `argparse` to make a script flexible, with options for host, port range, and thread count.
- **Handling errors:** timeouts, unresolvable hostnames, and services that don't send a banner.

## Legal note

This tool is for **educational purposes and authorized testing only**.

- Only scan systems you own or have explicit written permission to test.
- Safe targets include `127.0.0.1`, your own devices and lab network, and `scanme.nmap.org` (which allows light test scanning).
- Scanning networks or systems without permission may be illegal and against terms of service. The author is not responsible for misuse.

## License

MIT License. Free to use and modify for learning.
