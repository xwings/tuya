Not much time as i wanted, but one is always good.

This is a RE Challenge. Description as blow,

> GOTO considered harmful. How much harm did it do? Can you retrieve the password?

```
<~/hackover/goto>$ file goto.bin
goto.bin: data

<~/hackover/goto>$ xxd goto.bin | head -5
0000000: 543d 743b 6361 7420 2430 207c 2074 6169  T=t;cat $0 | tai
0000010: 6c20 2d63 202b 3735 207c 2067 756e 7a69  l -c +75 | gunzi
0000020: 7020 2d20 3e20 2454 3b63 686d 6f64 202b  p - > $T;chmod +
0000030: 7820 2454 3b2e 2f24 543b 726d 202e 2f24  x $T;./$T;rm ./$
0000040: 543b 6578 6974 2030 3b0a 1f8b 0808 efae  T;exit 0;.......

<~/hackover/goto>$ cat goto.bin | tail -c +75 | gunzip - > actual_goto

<~/hackover/goto>$ file actual_goto
test: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), for GNU/Linux 2.6.24, dynamically linked (uses shared libs), stripped
```

After some round tracing with IDA Pro, I decided to stop here

![alt tag](https://github.com/xwings/tuya/blob/master/ctf2015/hackover/goto-150/goto.jpeg)

The hex shows,

> 68 61 63 6b 6f 76 65 72 31 35 7b 49 5f 55 53 45 5f 47 4f 54 4f 5f 57 48 45 52 45 45 56 45 52 5f 49 5f 57 34 4e 54 7d

The Flag is,

> hackover15{I_USE_GOTO_WHEREEVER_I_W4NT}

Again, this is a quick flag.  I did analyze the binary.
