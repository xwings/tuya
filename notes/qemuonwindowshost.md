1. Install windows tap from openvpn
2. Rename tap in windows. example tap0
3. Share network to tap0 from main network adapter


```
qemu-system-x86_64 -hda debian.qcow2 -cdrom debian-12.8.0-amd64-netinst.iso -boot d -m 2G -machine type=pc,accel=whpx,kernel-irqchip=off -smp 2 -usb  -net nic -net tap,ifname=tap101 -device nec-usb-xhci
```

```
qemu-system-x86_64 -hda debian.qcow2 -m 2G -machine type=pc,accel=whpx,kernel-irqchip=off -smp 2 -usb  -net nic -net tap,ifname=tap101 -device nec-usb-xhci
```
