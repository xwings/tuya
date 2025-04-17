Load Modules
```
opkg update
opkg install kmod-hwmon-pwmfan
```

Disable
```
/bin/echo '0' > /sys/class/hwmon/hwmon2/pwm1_enable
```


Enable
```
/bin/echo '1' > /sys/class/hwmon/hwmon2/pwm1_enable
```

Control fan
```
/bin/echo '255' > /sys/class/hwmon/hwmon2/pwm1
/bin/echo '127' > /sys/class/hwmon/hwmon2/pwm1
/bin/echo '63' > /sys/class/hwmon/hwmon2/pwm1
```
