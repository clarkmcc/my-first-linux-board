# SPDX-License-Identifier: GPL-2.0
FIRMWARE_DIR ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
BUILDROOT_VERSION := 2026.02.2
BUILDROOT_ARCHIVE := buildroot-$(BUILDROOT_VERSION).tar.xz
BUILDROOT_SHA256 := a833429929aefd4175b0651b2b356b761960cd46d36df6a0049d1f117e3ac8a6
BUILDROOT_DIR ?= $(FIRMWARE_DIR)/build/buildroot-$(BUILDROOT_VERSION)
BUILDROOT_STAMP := $(BUILDROOT_DIR)/.boot-console-extracted
OUTPUT_DIR ?= $(FIRMWARE_DIR)/output
DOWNLOAD_DIR ?= $(FIRMWARE_DIR)/dl

.PHONY: all configure build rebuild-board buildroot-source clean validate
all: build

buildroot-source: $(BUILDROOT_STAMP)

$(DOWNLOAD_DIR)/$(BUILDROOT_ARCHIVE):
	mkdir -p $(DOWNLOAD_DIR)
	curl -fL --retry 3 -o $@.tmp https://buildroot.org/downloads/$(BUILDROOT_ARCHIVE)
	printf '%s  %s\n' '$(BUILDROOT_SHA256)' '$@.tmp' | sha256sum -c -
	mv $@.tmp $@

$(BUILDROOT_STAMP): $(DOWNLOAD_DIR)/$(BUILDROOT_ARCHIVE)
	printf '%s  %s\n' '$(BUILDROOT_SHA256)' '$<' | sha256sum -c -
	mkdir -p $(dir $(BUILDROOT_DIR))
	tar -xJf $< -C $(dir $(BUILDROOT_DIR))
	touch $@

configure: $(BUILDROOT_STAMP)
	$(MAKE) -C $(BUILDROOT_DIR) O=$(OUTPUT_DIR) BR2_EXTERNAL=$(FIRMWARE_DIR) boot_console_defconfig

build: configure
	$(MAKE) -C $(BUILDROOT_DIR) O=$(OUTPUT_DIR) BR2_EXTERNAL=$(FIRMWARE_DIR)

rebuild-board: configure
	$(MAKE) -C $(BUILDROOT_DIR) O=$(OUTPUT_DIR) linux-dirclean uboot-dirclean host-uboot-tools-dirclean
	$(MAKE) -C $(BUILDROOT_DIR) O=$(OUTPUT_DIR) BR2_EXTERNAL=$(FIRMWARE_DIR)

validate: build
	python3 $(FIRMWARE_DIR)/tests/validate_artifacts.py $(OUTPUT_DIR)

clean:
	$(MAKE) -C $(BUILDROOT_DIR) O=$(OUTPUT_DIR) clean
