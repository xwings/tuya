Notes to install LXQt in Linux Container with Debian

Hardware Acceleration 
```
lxc.apparmor.profile: unconfined
lxc.cgroup2.devices.allow: c 195:* rwm
lxc.cgroup2.devices.allow: c 226:* rwm
lxc.cgroup2.devices.allow: c 234:* rwm
lxc.mount.entry: /dev/dri dev/dri none bind,optional,create=dir
lxc.mount.entry: /dev/fb0 dev/fb0 none bind,optional,create=file

# tty8 will be the "display"
# EDIT: be sure to mount it onto a host tty >= 10 or the host's monitor will be unusable while running
lxc.mount.entry: /dev/tty10 dev/tty8 none bind,optional,create=file 
lxc.cgroup.devices.allow: c 4:10 rwm

# without tty0, loginctl will not recognize your login, you will end up with dbus errors
# EDIT: be sure to mount it onto a host tty >= 10 or the host's monitor will be unusable while running
lxc.mount.entry: /dev/tty11 dev/tty0 none bind,optional,create=file
lxc.cgroup.devices.allow: c 4:11 rwm
```

Package Installation with min. LXQt
```
apt update && apt upgrade -y && apt install -y lxqt-core libgl1-mesa-dri libglx-mesa0 mesa-vulkan-drivers xserver-xorg-video-all xrdp
``` 

x-session-manager config
```
update-alternatives --set x-session-manager /usr/bin/startlxqt
```
