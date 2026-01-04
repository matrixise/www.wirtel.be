---
date: 2013-02-13
slug: download_ubuntu_and_create_usb_stick_apple
tags:
- tips
- osx
- ubuntu
- usb
title: Download Ubuntu and create USB stick with your Mac

---

Today I have to re-install my laptop because there is a bug in the grub
boot-loader.

I tried the grub-rescue command and this one was really useful to list
the file systems, etc\...

But I didn't have time to find the documentation on internet, so, first
solution, re-install Ubuntu.

Here is the original link for this documentation:
<http://www.ubuntu.com/download/help/create-a-usb-stick-on-mac-osx>

In a terminal

1.  Download the Ubuntu ISO:

        wget ftp://ftp.belnet.be/pub/ubuntu.com/releases/12.10/ubuntu-12.10-desktop-amd64.iso

2.  Convert the iso file to img using the convert option of hdiutil:

        hdiutil convert -format UDRW -o ~/path/to/target.img ~/path/to/ubuntu.iso

3.  Run diskutil list to get the current list of devices:

        diskutil list

4.  Insert your flash media and run diskutil list agin and determine the
    device node assigned to your flash media (e.g. /dev/disk2).

5.  Unmount the disk (in my case, the flash media was mapped on
    /dev/disk2) :

        diskutil unmountDisk /dev/disk2

6.  Copy the .img file to the flash media:

        sudo dd if=/path/to/target.img of=/dev/rdisk2 bs=1m

7.  Eject the flash media:

        diskutil eject /dev/disk2

8.  Restart and boot with your USB stick.

Of course, these instructions will work fine with an other
distribibution.