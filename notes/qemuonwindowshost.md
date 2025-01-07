
```
sudo apt-get install g++-mingw-w64 mingw-w64 mingw-w64-tools mingw-w64-i686-dev mingw-w64-x86-64-dev nsis
```

```
./configure --cross-prefix=x86_64-w64-mingw32- --enable-debug --enable-debug --enable-gtk --enable-sdl –target-list=x86_64-softmmu prefix=/opt/qemuwin
```

1. Install windows tap from openvpn
2. Rename tap in windows. example tap0
3. Share network to tap0 from main network adapter


```
qemu-system-x86_64 -hda debian.qcow2 -cdrom debian-12.8.0-amd64-netinst.iso -boot d -m 2G -machine type=pc,accel=whpx,kernel-irqchip=off -smp 2 -usb  -net nic -net tap,ifname=tap101 -device nec-usb-xhci
```

```
qemu-system-x86_64 -hda debian.qcow2 -m 2G -machine type=pc,accel=whpx,kernel-irqchip=off -smp 2 -usb  -net nic -net tap,ifname=tap101 -device nec-usb-xhci
```

```
& 'C:\Program Files\qemu\qemu-system-x86_64' -hda debian.qcow2 -m 2G -machine type=q35,accel=whpx,kernel-irqchip=off -smp 2 -net nic -net tap,ifname=tap101 -usb -device qemu-xhci,id=xhci -device usb-host,bus=xhci.0,hostbus=6,hostport=4
```
