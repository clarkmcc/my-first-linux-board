#!/usr/bin/env bash
set -euo pipefail

firmware_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
volume_name=boot-console-buildroot-2026-02-2
host_uid=$(id -u)
host_gid=$(id -g)

docker build --platform linux/arm64 -t boot-console-buildroot:2026.02.2 "$firmware_dir"
docker volume create "$volume_name" >/dev/null
docker run --rm --platform linux/arm64 \
  -v "$volume_name:/work" \
  boot-console-buildroot:2026.02.2 \
  chmod 0777 /work

mkdir -p "$firmware_dir/output"

docker run --rm --platform linux/arm64 \
  --user "$host_uid:$host_gid" \
  -e HOME=/tmp \
  -v "$firmware_dir:/firmware" \
  -v "$volume_name:/work" \
  -w /work \
  boot-console-buildroot:2026.02.2 \
  sh -eu -c '
    make -f /firmware/Makefile \
      FIRMWARE_DIR=/firmware \
      BUILDROOT_DIR=/work/build/buildroot-2026.02.2 \
      OUTPUT_DIR=/work/output \
      DOWNLOAD_DIR=/work/dl \
      "$@"
    cp -f /work/output/.config /firmware/output/.config
    if [ -f /work/output/images/sdcard.img ]; then
      mkdir -p /firmware/output/images \
        /firmware/output/build/linux-6.19.14 \
        /firmware/output/build/uboot-2026.01
      cp -f /work/output/build/linux-6.19.14/.config \
        /firmware/output/build/linux-6.19.14/.config
      cp -f /work/output/build/uboot-2026.01/.config \
        /firmware/output/build/uboot-2026.01/.config
      cp -f /work/output/images/boot.scr \
        /work/output/images/linux.dtb \
        /work/output/images/rootfs.ext4 \
        /work/output/images/sdcard.img \
        /work/output/images/u-boot-sunxi-with-spl.bin \
        /work/output/images/zImage \
        /firmware/output/images/
    fi
  ' sh "$@" 2>&1 | tee "$firmware_dir/output/build.log"
