#!/usr/bin/env python3

import argparse
import fuzzer
import sender


def print_banner():
    separator = "#" * 80
    banner = "# Simple Stack Based Buffer Overflow Companion v1.0" + " " * 28 + "#\n"
    banner += "# Based on tutorial and lab by Tib3rius" + " " * 40 + "#\n"
    banner += "# https://github.com/Tib3rius/Pentest-Cheatsheets" + " " * 30 + "#\n"
    banner += "# https://tryhackme.com/room/bufferoverflowprep" + " " * 32 + "#\n"
    banner += "# Modified by terasi" + " " * 59 + "#\n"
    banner += "# https://github.com/tera-si" + " " * 51 + "#"

    print(separator)
    print(banner)
    print(separator + "\n")


def main():
    description = """Simple Stack Based Buffer Overflow Companion.
Based on tutorial
  https://github.com/Tib3rius/Pentest-Cheatsheets/blob/master/exploits/buffer-overflows.rst
and lab
  https://tryhackme.com/room/bufferoverflowprep
by Tib3rius.
Modified to be semi-automated. Support both fuzzing and exploiting."""

    epilog = """Remember to change the relevant options in options.py

Attack Stages:
  1: Fuzzing
  2: Locating offset
  3: Testing EIP overwrite
  4: Identifying bad characters
  5: Exploitation"""

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=description, epilog=epilog)
    parser.add_argument("ip_addr", help="Target IP address, required.")
    parser.add_argument("port_num", help="Target port number, required.")
    parser.add_argument("-s", "--stage", help="Attack stage, required.", type=int, required=True)

    args = parser.parse_args()
    ip_addr = args.ip_addr
    port_num = int(args.port_num)
    atk_stage = args.stage

    print_banner()

    if atk_stage == 1:
        print("[*] Using fuzzer module")
        fuzzer.fuzz(ip_addr, port_num)

    elif atk_stage == 2:
        print("[*] Using locate-offset module")
        sender.send_pattern(ip_addr, port_num)

    elif atk_stage == 3:
        print("[*] Using test-EIP-overwrite module")
        sender.test_eip(ip_addr, port_num)

    elif atk_stage == 4:
        print("[*] Using identify-bad-chars module")
        sender.send_char_list(ip_addr, port_num)

    elif atk_stage == 5:
        print("[*] Using exploitation module")
        sender.exploit(ip_addr, port_num)

    else:
        print("[!] Unknown attack stage")
        print("[!] Aborting...")
        exit()


if __name__ == "__main__":
    main()
