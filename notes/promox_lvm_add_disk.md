Adding disk into current /dev/mapper/pve-data
```
lvdisplay -m
cfdisk /dev/nvme0n1
vgextend pve /dev/nvme0n1p1
lvdisplay -m
lvm lvextend -l +100%FREE /dev/mapper/pve-data
```
