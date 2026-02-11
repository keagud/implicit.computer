+++
title = "Resizing XFS Partitions"
slug = "xfs-resize"
date = 2026-02-13

[taxonomies]
tags = [ "xfs", "linux", "sysadmin",]
+++


Twice now I have needed to add more space to my main home server VM, and twice I have needed to re-learn how to expand a XFS filesystem. Luckily it's not hard. I'm recording it here to make my life easier when it inevitably comes up once more.

1. Expand the underlying virtual disk (I did this in the proxmox GUI)

2. Use `growpart` to grow the partition to fill the newly available space. Assuming the partition is `/dev/vda1`: 

```shell
growpart /dev/vda 1
```

3. Use `xfs_growfs` to expand the xfs filesystem to fill the whole partition

```shell
xfs_growfs -d /dev/vda1
```

No need to reboot, or even unmount `/dev/vda1`!
