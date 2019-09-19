**`WIP. Rough draft. Open for comment.`**

---
##### tl;dr

- Qiling Framework is not only a Emulataion tool, but combines binary instrumentation and binary emulation into one single framework
    - *Redirect process execution flow on the fly*
    - *Hot-patching binary during execution*
    - *Code injection during execution*
    - *Partial binary execution, without running the entire file*
    - *Patch a "unpacked" content of a packed binary file*
- Qiling Framework emulates 
    - *Windows X86 32/64bit*
    - *Linux X86 32/64bit, ARM, AARCH64, MIPS*
    - *MacOS X86 32/64bit*
    - *FreeBSD X86 32/64bit*
- Qiling Framework able to run on top of Windows/MacOS/Linux/FreeBSD without CPU architecture limitation

---

### What is missing in reverse engineering world
The insecure Internet of Things (IoT) devices and malware attack are growing and they are affecting our day-to-day life. The security industry is struggling to safeguard and cope with such growth and attacks. Abominably, IoT firmware and malware sample analysis remain the two biggiest challanges for the security industry.

The attack surface swifts quickly as the IoT devices and malware are moving towards different platform (Operatiing System) and CPU archirecture. Reverse engineers are not only struggling to understand each operating systems and cpu architecture, but more discouragingly there is lack of tools to perform indept analysis.

Common techniques of analysis such as full emulation, usermode emulation, binary instrumentation tool, disassembler and sandboxing are ancient and obsolete. These tools are either limited in cross platform support or CPU architecture support.


### Why Qiling framework
Qiling Framework is targeted to change IoT research, threat analysis and reverse engineering technique. The main objective is to build a framework and not just engineer another tool. It should be easy to use and able to sustain from the work of the community.

Even before deciding on its feature and functionlity, picking a programming become the most discussed topic. Python is being choosen simply because Python is a language commonly used by revese enginners. By design, Qiling Framework must be able to executed on different types of platform and support as many CPU architures as possible. The nature of Qiling is being designed as a framework and not yet another emulation tool.

After deciding on the most fundamental requirment, it become clearer Qiling Framework is a binary instrumentation and binary emulation framework. Qiling must be able to intercept and inject arbitary code before or during a binary execution. Most importantly, it must support as many platforms and CPU architectures as possible.

### Features and Funtionality

Qiling framework is an advanced binary emulation framework, with the following features:
- Able to run on Windows/MacOS/Linux/FreeBSD without CPU architecture limitation
- Emulate Cross platform support: Windows, MacOS, Linux, BSD
- Emulate Cross architecture support: X86, X86_64, Arm, Arm64, Mips
- Supports Multiple file formats: PE, MachO, ELF, or direct binary input (shellcode)
- Emulates & sandbox machine code in an isolated environment
- Provides high level API to setup & configure the sandbox
- Provides granular instrumentation: allowing hooks at various levels (instruction/basic-block/memory-access/exception/syscall/IO/etc)
- Allows dynamic patch on-the-fly running code, including the loaded libraries
- A true framework written in Python, makes it easy to build customized security analysis tools for integration

Qiling framework is the only solution combines disassember, binary instrumentation and binary emulation into single framework and provides cross-platform and multi arch support

- Qiling framework is an advanced binary emulation framework which able to do the follow during execution
    - Redirect process execution flow on the fly
        - *Change execution flow when there is a check eg, cmp EAX,EBX always = true*
    - Hot-patching binary during execution
        - *Define a code address and patch it during execution, and keeping the original binary untouched* 
    - Code injection during execution
        - *Able to inject opcode or asm code into the binary during execution*
    - Partial binary execution, without running the entire file
        - *If the target section is only one part (example, function_targetedbug() ) of a huge binary*
        - *Each execution need to fulfill different user input before reaching function_targetedbug()*
        - *Qiling framework is able to set and pre-fulfilled the state/ requirement, so that each new execute will go directly to function_targetbug()*
    - Patch a "unpacked" content of a packed binary file
        - *Able to patch a "packed" binary during execution, without unpacking*
---

### How does it work?

##### Demo Setup
- *Hardware : X86 64bit*
- *OS : Ubuntu 18.04 64bit*

##### Catching Wannacry's killer switch
Qiling framework executes Wannacry binary, hooking address 0x40819a to catch the killerswitch url

[![qiling DEMO 3: Catching wannacry's killer switch](https://img.youtube.com/vi/gVtpcXBxwE8/0.jpg)](https://www.youtube.com/watch?v=gVtpcXBxwE8 "Video DEMO 3")

###### Sample code
```python
from qiling import *

def stopatkillerswtich(ql):
    ql.uc.emu_stop()

if __name__ == "__main__":
    ql = Qiling(["rootfs/x86_windows/bin/wannacry.bin"], "rootfs/x86_windows")
    ql.hook_address(stopatkillerswtich, 0x40819a)
    ql.run()
```

###### Execution output
```
0x1333804: __set_app_type(0x2)
0x13337ce: __p__fmode() = 0x500007ec
0x13337c3: __p__commode() = 0x500007f0
0x132f1e1: _controlfp(0x10000, 0x30000) = 0x8001f
0x132d151: _initterm(0x40b00c, 0x40b010)
0x1333bc0: __getmainargs(0xffffdf9c, 0xffffdf8c, 0xffffdf98, 0x0, 0xffffdf90) = 0
0x132d151: _initterm(0x40b000, 0x40b008)
0x1001e10: GetStartupInfo(0xffffdfa0)
0x104d9f3: GetModuleHandleA(0x00) = 400000
0x125b18e: InternetOpenA(0x0, 0x1, 0x0, 0x0, 0x0)
0x126f0f1: InternetOpenUrlA(0x0, "http://www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com", "", 0x0, 0x84000000, 0x0)
```

##### Hotpatching a Windows crackme
Using Qiling framework to dynamically patch a Windows crackme binary so that it always displays "Congratulation" dialog

[![qiling DEMO 1: hotpatching a Windows crackme](http://img.youtube.com/vi/p17ONUbCnUU/0.jpg)](https://www.youtube.com/watch?v=p17ONUbCnUU "Video DEMO 1")

###### Sample code
```python
from qiling import *

def force_call_dialog_func(ql):
    # get DialogFunc address
    lpDialogFunc = ql.unpack32(ql.mem_read(ql.sp - 0x8, 4))
    # setup stack memory for DialogFunc
    ql.stack_push(0)
    ql.stack_push(1001)
    ql.stack_push(273)
    ql.stack_push(0)
    ql.stack_push(0x0401018)
    # force EIP to DialogFunc
    ql.pc = lpDialogFunc


def my_sandbox(path, rootfs):
    ql = Qiling(path, rootfs)
    # NOP out some code
    ql.patch(0x004010B5, b'\x90\x90')
    ql.patch(0x004010CD, b'\x90\x90')
    ql.patch(0x0040110B, b'\x90\x90')
    ql.patch(0x00401112, b'\x90\x90')
    # hook at an address with a callback
    ql.hook_address(0x00401016, force_call_dialog_func)
    ql.run()


if __name__ == "__main__":
    my_sandbox(["rootfs/x86_windows/bin/Easy_CrackMe.exe"], "rootfs/x86_windows")
```

###### Execution output
```
0x10cae10: GetStartupInfo(0xffffdf40)
0x1121fa7: GetStdHandle(0xfffffff6) = 0xfffffff6
0x111fbc4: GetFileType(0xfffffff6) = 0x2
0x1121fa7: GetStdHandle(0xfffffff5) = 0xfffffff5
0x111fbc4: GetFileType(0xfffffff5) = 0x2
0x1121fa7: GetStdHandle(0xfffffff4) = 0xfffffff4
0x111fbc4: GetFileType(0xfffffff4) = 0x2
0x1121fd1: SetHandleCount(0x20) = 32
0x1121fbf: GetCommandLineA() = 0x501091b8
0x111fcd4: GetEnvironmentStringsW() = 0x501091e4
0x1117ffa: WideCharToMultiByte(0x0, 0x0, 0x501091e4, 0x1, 0x0, 0x0, 0x0, 0x0) = 2
0x1117ffa: WideCharToMultiByte(0x0, 0x0, 0x501091e4, 0x1, 0x50002098, 0x2, 0x0, 0x0) = 1
0x111fcbc: FreeEnvironmentStringsW(0x501091e4) = 1
0x1116a0b: GetACP() = 437
0x1121f8f: GetCPInfo(0x1b5, 0xffffdf44) = 1
0x1121f8f: GetCPInfo(0x1b5, 0xffffdf1c) = 1
0x111e43e: GetStringTypeW(0x1, 0x40541c, 0x1, 0xffffd9d8) = 0
0x10ffc95: GetStringTypeExA(0x0, 0x1, 0x405418, 0x1, 0xffffd9d8) = 0
0x111e39c: LCMapStringW(0x0, 0x100, 0x40541c, 0x1, 0x0, 0x0) = 0
0x1128a50: LCMapStringA(0x0, 0x100, 0x405418, 0x1, 0x0, 0x0) = 0
0x111e39c: LCMapStringW(0x0, 0x100, 0x40541c, 0x1, 0x0, 0x0) = 0
0x1128a50: LCMapStringA(0x0, 0x100, 0x405418, 0x1, 0x0, 0x0) = 0
0x111685a: GetModuleFileNameA(0x0, 0x40856c, 0x104) = 42
0x10cae10: GetStartupInfo(0xffffdfa0)
0x11169f3: GetModuleHandleA(0x00) = 400000
0x104cf42: DialogBoxParamA(0x400000, 0x65, 0x00, 0x401020, 0x00) = 0
Input DlgItemText :

        << enter any string or number here >>

0x1063d14: GetDlgItemTextA(0x00, 0x3e8, 0xffffdef4, 0x64) = 3
0x105ea11: MessageBoxA(0x00, "Congratulation !!", "EasyCrackMe", 0x40) = 2
0x1033ba3: EndDialog(0x00, 0x00) = 1
0x1124d12: ExitProcess(0x01)
```

---
### Qiling vs other open source emulators and tools

There are many open source emulators, but two projects closest to Qiling are [Unicorn](http://www.unicorn-engine.org) & [Qemu usermode](https://qemu.org). This section summaries the main differences.

##### Qiling framework vs Unicorn engine

Qiling framework is built on top of Unicorn. However, Qiling and Unicorn are two different beasts

- Unicorn is just a CPU emulator. Hence, it focuses on emulating CPU instructions, that can understand emulator memory. Beyond that, Unicorn is not aware of higher level concepts, such as dynamic libraries, system calls, I/O handling or executable formats like PE, MachO or ELF. In short, Unicorn only emulates raw machine instructions, without Operating System (OS) context
- Qiling is designed as a higher level framework, that leverages Unicorn to emulate CPU instructions, but Qiling understands OS: it has executable format loaders (for PE, MachO & ELF at the moment), dynamic linkers (so we can load & relocate shared libraries), syscall & IO handlers. For this reason, Qiling can run excutable binaries that normally runs in native OS

##### Qiling framework vs Qemu usermode

Qemu usermode does similar thing, that is to emulate whole executable binaries in cross-architecture way. However, Qiling offers some important differences bewteen Qemu usermode

- Qiling is a true analysis framework, that allows you to build your own dynamic analysis tools on top (in friendly Python language). Meanwhile, Qemu is just a tool, not a framework
- Qiling can perform dynamic instrumentation, and can even hotpatch code at runtime. Qemu does not do either
- Not only working cross-architecture, Qiling is also cross-platform. For example, you can run Linux ELF file on top of Windows In contrast, Qemu usermode only run binary of the same OS, such as Linux ELF on Linux host, due to the way it forwards syscall from emulated code to native OS
- Qiling supports more platforms, including Windows, MacOS, Linux & BSD. Qemu usermode only handles Linux & BSD

##### Qiling framework vs Qemu
- Qemu is a full system emulator, but not an analysis tool. Qemu comes with build-in GDB and we cannot analyze a process via qemu. In contrast, Qiling framework does not perform full system emulation but it still understands OS, syscalls & IO handlers.

##### Qiling framework vs Usercorn
- [Usercorn](https://usercorn.party) is an emulation tool with instrumentation, which is similar to Qiling framework's capability where it is able to perform syscall forwarding, instrumentation
- However, Usercorn only supports Linux (and MacOS, to some extent). Qiling framework, on the other hand, has vast support on platforms and architecture

##### Qiling framework vs Binee
- Binee is an emulation tool built with GO language but it is not an instrumentation framework. Binee does not allow dynamic hooking, hotpatching or provide any customization. Qiling framework, designed as a Python module, offers far more capability, making a lot of dynamic analysis possible
- Binee supports only Windows. Qiling framework supports more platforms and architecture

##### Qiling framework vs Wine
- Wine is an emulation tool not intended for analysis purpose. It only emulates Windows on Linux, Mac, FreeBSD, and Solaris, allowing user to run Windows applications on *NIX platforms
- Qiling framework is not built for this purpose, although it is possible to run applications from many other platforms and archirectures. Qiling is meant for security analysis

##### Qiling framework vs Cuckoo Sandbox
- Cuckoo Sandbox is an analysis tool relying on VM i.e. QEMU, Virtualbox to provide virtualized environment for binary execution
- Qiling framework executes binary without having full blown OS running. It understands OS and forwards syscalls from emulated code to OS natively

