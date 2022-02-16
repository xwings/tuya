```
vi /etc/systemd/system/rc-local.service
```

```
[Unit]
Description=/etc/rc.local Compatibility
ConditionPathExists=/etc/rc.local

[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
StandardOutput=tty
RemainAfterExit=yes
SysVStartPriority=99

[Install]
WantedBy=multi-user.target
```

```
touch /etc/rc.local
chmod +x /etc/rc.local
systemctl enable rc-local
systemctl start rc-local
```
