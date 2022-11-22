```
# I use these in my docker lxc, dont know if it matters here
lxc.apparmor.profile: unconfined
lxc.cgroup.devices.allow: a
lxc.cap.drop:
# nvidia devices
lxc.mount.entry: /dev/nvidia0 dev/nvidia0 none bind,optional,create=file
lxc.mount.entry: /dev/nvidiactl dev/nvidiactl none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-modeset dev/nvidia-modeset none bind,optional,create=file

# my system has 2 video cards, yours might be /dev/dri/card0 dev/dri/card0 and c 226:0 rwm
lxc.mount.entry: /dev/dri/card1 dev/dri/card0 none bind,optional,create=file 
lxc.cgroup.devices.allow: c 226:1 rwm

lxc.mount.entry: /dev/dri/renderD128 dev/dri/renderD128 none bind,optional,create=file
lxc.cgroup.devices.allow: c 226:128 rwm

# tty8 will be the "display"
# EDIT: be sure to mount it onto a host tty >= 10 or the host's monitor will be unusable while running
lxc.mount.entry: /dev/tty10 dev/tty8 none bind,optional,create=file 
lxc.cgroup.devices.allow: c 4:10 rwm

# without tty0, loginctl will not recognize your login, you will end up with dbus errors
# EDIT: be sure to mount it onto a host tty >= 10 or the host's monitor will be unusable while running
lxc.mount.entry: /dev/tty11 dev/tty0 none bind,optional,create=file
lxc.cgroup.devices.allow: c 4:11 rwm

# frame buffer, required for display 
# EDIT: I guess this is optional. only needed if you want to display graphics onto the hosts main monitor
#lxc.mount.entry: /dev/fb0 dev/fb0 none bind,optional,create=file
#lxc.cgroup.devices.allow: c 29:0 rwm

# for gamepad support in steam link, because why not?
lxc.mount.entry: /dev/uinput dev/uinput none bind,optional,create=file
lxc.cgroup.devices.allow: c 10:223 rwm
lxc.mount.entry: /dev/input       dev/input       none bind,create=dir 0 0
lxc.cgroup.devices.allow: c 13:* rwm
```
```
apt install xrdp
apt install libgl1-mesa-dri libglx-mesa0 mesa-vulkan-drivers xserver-xorg-video-all
apt update && apt upgrade -y && apt install -y x11vnc plasma-desktop lightdm build-essential libglvnd-dev pkg-config konsole xterm lightdm-gtk-greeter
```
```
update-alternatives --set x-session-manager /usr/bin/startplasma-x11
```
