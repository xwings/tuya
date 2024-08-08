
```
https://github.com/981213/mtk_uartboot/releases
```

```
mtk_recovery.zip
```

```
sudo RUST_BACKTRACE=full ./mtk_uartboot-v0.1.1-x86_64-unknown-linux-gnu/mtk_uartboot -s /dev/ttyUSB0 -p mtk_recovery/mt7986/mt7986-ddr4-bl2.bin -a -f mt7986_zyxel_ex5700-t0-fip-uboot-mtk-20230718-09eda825-fixed-parts.bin --brom-load-baudrate 921600 --bl2-load-baudrate 1500000
```



