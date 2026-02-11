+++
title = "Transfer Tailscale As-Is Between (Linux) Hosts"
slug = "tailscale-transfer"
date = 2026-02-17

[taxonomies]
tags = [ "tailscale", "linux", "sysadmin",]
+++

[Tailscale](https://tailscale.com/) is an easy-to-use WireGuard VPN platform with a generous free tier that's popular among homelabbers. I use it pretty extensively in my setup. I've also granted access to a few hosts from my 'tailnet' (their term for your network of VPN-connected hosts) to my friends[^1], and tailscale makes that a straightforward process. 


Sometimes, though, I need to rebuild a host from scratch for whatever reason, but without breaking the existing share permissions - I need tailscale to see the new install as the same device as the old one. Here's how to do that:

1. Install tailscale on the new host as usual and authenticate to your tailnet. Make a note of the hostname and IP tailscale assigns it in the web admin portal.


2. On both the old and new hosts, stop the tailscale daemon:

  ```shell
  root@old-host# systemctl stop tailscaled
  ```

  ```shell
  root@new-host# systemctl stop tailscaled
  ```

3. Move the directory `/var/lib/tailscale` on the old host to the new one. You can use `rsync` if they're on the same LAN, or a thumb drive if they're on different physical devices. Make sure the permissions and ownership are correct - it should have `700` for permissions and `root:root` for owner

4.  On the new host, restart tailscale and re-authenticate

```shell
root@new-host# systemctl enable tailscaled --now && tailscale login 

```


5. Confirm in the web admin view that the hostname/IP first assigned to the new host is showing as offline, and that the entry for the setup you just transferred is online, then delete the now-useless entry for the new host. Now you can wipe or delete the old host safely.


---
[^1]: That setup has evolved enough complexity to deserve a post of its own, but that's for another time.
