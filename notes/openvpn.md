## Ubuntu OpenVPN + LEDE + Windows + Pfsense

> This is a VERY QUICK and LAZY example

LEDE Internal Network: 172.16.11.0/24
Pfsense Internal Network: 172.16.12.0/24
Windows: Mobile Notebook

Ubuntu OpenVPN - LEDE: 192.168.11.1 - 192.168.11.2  
Ubuntu OpenVPN - Pfsense: 192.168.12.1 - 192.168.13.2  
Ubuntu OpenVPN - Windows: 192.168.13.1 - 192.168.13.2  

#### How to generate static key
```
openvpn --genkey --secret static.key
```

#### Enable Forwading in Ubuntu
```
sysctl net.ipv4.ip_forward net.ipv4.ip_forward = 1
```

### Between Ubuntu and Windows


#### From Ubuntu for Windows
```
# road warrior

dev tun
daemon
lport 9913
keepalive 10 60
ping-timer-rem
persist-tun
persist-key
proto udp
cipher AES-256-CBC
ifconfig 192.168.13.1 192.168.13.2
comp-lzo adaptive

<secret>
#
# 2048 bit OpenVPN static key
#
</secret>
```

#### From Windows to Ubuntu and make sure openvpn client run as admin
```
dev tun
proto udp
remote ubuntu.myvpnserver.com 9913
ifconfig 192.168.13.2 192.168.13.1
resolv-retry infinite
nobind
#persist-key
persist-tun
cipher AES-256-CBC
comp-lzo
verb 3

route 172.16.11.0 255.255.255.0
route 172.16.12.0 255.255.255.0

<secret>
#
# 2048 bit OpenVPN static key
#
</secret>
```

### Between Ubuntu and Pfsense

#### From Ubuntu for Pfsense
```
#
# Pfsense 172.16.12.0/24
#

dev tun
daemon
lport 9912
keepalive 10 60
ping-timer-rem
persist-tun
persist-key
proto udp
cipher AES-256-CBC
ifconfig 192.168.12.1 192.168.12.2
route 172.16.12.0 255.255.255.0
comp-lzo adaptive

<secret>
#
# 2048 bit OpenVPN static key
#
</secret>
```
#### From Pfsense to Ubuntu
```
dev ovpnc0
verb 1
dev-type tun
tun-ipv6
dev-node /dev/tun0
writepid /var/run/openvpn_client0.pid
#user nobody
#group nobody
script-security 3
daemon
keepalive 10 60
ping-timer-rem
persist-tun
persist-key
proto udp
cipher AES-256-CBC
auth SHA1
up /usr/local/sbin/ovpn-linkup
down /usr/local/sbin/ovpn-linkdown
management /var/etc/openvpn/client4.sock unix
remote ubuntu.myvpnserver.com 9912
ifconfig 192.168.12.2 192.168.12.1
secret /var/etc/openvpn/client0.secret
comp-lzo adaptive
resolv-retry infinite
route 172.16.11.0 255.255.255.0
route 192.168.13.0 255.255.255.0
```

#### Firewall

1. Goto OpenVPN
2. Allow all to OpenVPN and OpenVPN to all


### Between Ubuntu and LEDE

#### From Ubuntu for LEDE
```
#
# LEDE 172.16.11.0/24
#

dev tun
daemon
lport 9911
keepalive 10 60
ping-timer-rem
persist-tun
persist-key
proto udp
cipher AES-256-CBC
ifconfig 192.168.11.1 192.168.11.2
comp-lzo adaptive

<secret>
#
# 2048 bit OpenVPN static key
#
</secret>
```

#### From LEDE to Ubuntu
``` 
config openvpn 'fromlede'
        option dev 'tun'
        option nobind '1'
        option verb '3'
        option cipher 'AES-256-CBC'
        option ifconfig '192.168.11.2 192.168.11.1'
        option comp_lzo 'adaptive'
        list remote 'ubuntu.myvpnserver.com 9911'
        option proto 'udp'
        option secret '/etc/openvpn/openvpnstatic.key'
        option enabled '1'
        option keepalive '10 60'
        option script_security '3'
```

#### update config
```
uci commit openvpn
```

#### In Firewall

1. Create a interface for VPN, eg tun0
2. Disable all IPv6
3. from LAN for VPN. Accept - Input, Output, Forward
4. From VPN to LAN. Accept - Input, Output, Forward
