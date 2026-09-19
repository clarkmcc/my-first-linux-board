setenv bootargs console=ttyS0,115200 earlycon panic=5 rootwait root=/dev/mmcblk0p2 rootfstype=ext4 ro
if load mmc 0:1 0x82000000 linux.dtb; then
	if load mmc 0:1 0x80008000 zImage; then
		bootz 0x80008000 - 0x82000000
	fi
fi
echo Boot files could not be loaded; resetting
reset
