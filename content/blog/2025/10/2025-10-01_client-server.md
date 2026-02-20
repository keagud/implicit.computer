+++
date = 2025-10-01
title =  "Living the Client-Server Lifestyle"
slug =  "client-server"

[taxonomies]
tags = ["homelab"]

+++



As I've worked on the ol' homelab over the past few months, most of my computer use outside of my day job has morphed to fit a general [client-server](https://en.wikipedia.org/wiki/Client%E2%80%93server_model) model. 
In this post I'll go over what I mean by "client-server", why it's so great, and why you should maybe give it a shot too. 


The basic idea is to divide all devices into two catagories. *Server* devices are, for a given task, the Single Canonical Device for that task, and are accessed remotely from client devices. 
By "server" I'm referring more to a role than a form factor ---  anything with a CPU and a network interface can be a server. 
*Client* devices are anything with a screen, an input method (`keyboard || mouse || touchscreen`) and a network connection.
To live the client-server lifestyle is to treat client devices like peripherals for the *real* computer, the server, the one at home that's always on and already configured just how you like.
There's a lot of ways this can cash out --- direct access over SSH or VNC, running services on the server with Web interfaces you can access from a browser, a network file share --- but the constant factor is that all the important computation and such is happening on a device designated for that purpose.


The most obvious advantage is that when you break the requirement that tasks done on a device are done *by* that device, any task becomes doable from anywhere.
I can initiate a multi-terabyte download from my phone without worrying about overtaxing whatever spotty guest WiFi I might be on, then I can browse the files from my laptop as soon as the download is complete.
I could, in theory, reconfigure my web server from my Android e-reader if that were all I had available.  


The flip side is that when each individual device has fewer responsibilities, it can specialize into a role that fits its strengths.
For example: the device I own with the nicest display is, by a mile, my M1 MacBook Air, but it also has a pathetic 128 GB of (non-upgradable)[^1] disk space, meaning the device best suited to playing high resolution video files can also hold a very limited amount of such files at one time.
I also like the MacBook for writing code, both for the nice display and the keyboard (it's pretty good for a laptop keyboard, but mostly I like Mac keyboards for coding so I can use Command-C to copy text without worrying if that'll be interpreted as a stop signal in the terminal); however I find the development experience on MacOS wanting, for reasons best left to a footnote[^2].
But if the Mac is only a *client* that connects to my media and development servers, those downsides are totally negated! Functionally, it becomes a laptop with a best-in-class display and keyboard *and* multiple terabytes of storage *and* the power efficiency of ARM *and* an x86 development environment with Linux Mint set up just how I like it.  


Speaking of having things set up just right: the time between unboxing a new device and having it fully configured and operational is minimal if it's just connecting to an existing setup.
I have a highly engineered and bespoke development environment with a fully tricked out Neovim configuration, my preferred zsh setup with plugins and aliases, a bunch of enhanced shell utilities like [bat](https://github.com/sharkdp/bat) and [starship](https://starship.rs/), etc, etc, which normally would be a huge pain to transfer to a new device. 
When I recently wiped and re-imaged the aforementioned MacBook, I just needed to install [tailscale](https://tailscale.com) and re-map my [samba](https://en.wikipedia.org/wiki/Samba_(software)) file share to be fully up and running again.


The only real downside for servermaxxing is the requirement for network connectivity from client devices.
When you're on the same LAN as the server this is a non-issue; even if my ISP is down and I can't reach the Internet, the link between my desk and my server rack is unaffected. 
Tailscale (or if you're adamant on fully self-hosting, your own homebrewed Wireguard setup) makes access from elsewhere pretty seamless, but YMMV on the usability of remote machines, especially if you're outside an urban area with good WiFi and cell access.
For coding on the go or working off a cell hotspot only,  a TUI editor workflow ([neovim](https://neovim.io/) + [tmux](https://github.com/tmux/tmux)) with [mosh](https://mosh.org/) has served me well. 


The best way to determine if this kind of setup  would work for you is to try it out yourself!
All you need is a computer with internet connectivity; it doesn't need to be especially modern or fancy, but at least 1 Gbps Ethernet is a good lower bound.
A Raspberry Pi is a classic starting point, but an old desktop PC or even a laptop rescued from e-waste or from gathering dust in the closet can also be a great server.
In practice most (but not all!) of my server devices are "actual" rack-mounted servers, or virtual machines running on such servers, but that's mostly for the same reason the men of generations past would build scale model railroad layouts in the basement, rather than any practical reason. 

A [NAS](https://en.wikipedia.org/wiki/Network-attached_storage) for network file sharing is probably the best place to start; it's simple enough you can get it going in a weekend if you're even somewhat technically inclined, and it has a high return on investment regardless of your specific needs and workflow (everybody uses files).[^3] 
This isn't primarily a how-to guide --- you can find many of those out there on the Internet already --- but I will at least recommend [TrueNAS](https://www.truenas.com/) if your hardware supports it for a nice GUI management interface, and [SMB](https://en.wikipedia.org/wiki/Server_Message_Block) as your file share protocol over the alternative [NFS](https://en.wikipedia.org/wiki/Network_File_System) to maximize compatibility with client devices.
 

---

[^1]: When did we decide that was OK, btw? I must have missed the vote.

[^2]: <div>In descending order of importance: 

- Basically all the code I write will run in "prod" on Debian or Ubuntu; it's way more straightforward to do the development on a Debian-based box as well.

-  Often I'm targeting x86 as well, and for cross compilation the only true winning move is not to play.

 - The security model of MacOS means I'm always manually approving new permission popups so I can, like, ping a remote host or something else trivial

-  I can't shake the muscle memory of `/home/username` instead of `/Users/username` 

</div>

[^3]: [The files are IN [another] computer! ](https://www.youtube.com/watch?v=L_o_O7v1ews)

