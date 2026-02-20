+++
title = "You Can Just Connect Two Devices With An Ethernet Cable, That Works"
slug = "direct-ethernet"
date = 2025-11-02

[taxonomies]
tags = [ "networking",]
+++

Recently at $dayjob I encountered a scientific instrument connected to a controlling PC over IP; that's not unusual in itself, but what *was* unusual was the tiny little MikroTek router that sat between the two, connected to them and nothing else. 
Possibly there was a good reason for this at the time that I just couldn't see[^1], but more likely I think is that the (likely overworked and underpaid) vendor technician who set it up originally wasn't aware that if all you need is a direct Ethernet connection between exactly two hosts, you don't need a router. In fact, you don't need anything besides the cable. If you configure both ends with a static IP on the same network, plug one end of an Ethernet cable into host A and the other into host B, that just works[^2]. It feels like cheating somehow, but it's just a natural consequence of how IP functions.

More concretely, here's an example config to copy:

Host 1:
- IP: 192.168.100.1
- Subnet: /30 or 255.255.255.252
- Gateway and DNS: doesn't matter, leave blank or on default

Host 2:
- IP: 192.168.100.2
- Other parameters same as above



---
[^1]: In fact, the reason I was poking around that corner of the lab in the first place was that the instrument connection was borked after a power outage, because the addresses handed out by the DHCP server on the router were suddenly not what the client software was expecting. If this setup had used static addressing and a direct connection, this would have never happened.   

[^2]: Ok, it doesn't work on very old machines without a special "crossover" cable, but you're very unlikely to find a host like that in the wild nowadays.
.


