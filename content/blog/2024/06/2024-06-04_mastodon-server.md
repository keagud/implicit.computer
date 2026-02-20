+++
title="Notes on Setting Up a Mastodon Server"
date=2024-06-04
slug="mastodon-server"
[taxonomies]
tags=["#100DaysToOffload", "Protocolapalooza", "tech"]
+++

Welcome to [Protocolapalooza](/tags/protocolapalooza), my project to add support to this site for a bunch of wacky protocols other than the Web. We're starting with ActivityPub, but before we can get into the implementation there's some business to take care of.

My general plan for this project is to use third party clients to validate my work as I go, but with ActivityPub that present a unique challenge because the "client" is really another server that implements ActivityPub. In fact that's what federation - as in "fediverse" - actually means at the root. 

ActivityPub is actually two protocols, one for client-server interactions (e.g. your Mastodon app sends the toot you just wrote to your Mastodon instance) and one for server-server interactions ( e.g. your Mastodon instance informs the instances of your followers about your hot new toot.) [^1] The good news is I only need to implement the second one, but since I can't test if I'm federating correctly without a peer to federate with, I'll also need to spin up a second ActivityPub server.


Luckily, Digital Ocean has a [prebuilt image](https://marketplace.digitalocean.com/apps/mastodon) for a VPS (a 'droplet' in their lingo) with all the setup for a Mastodon instance already done. Unluckily, it doesn't seem to actually work. I ran the setup script, entered my domain name and SMTP server, and everything looked hunky-dory, but visiting the page in the browser resulted in broken CSS, unloaded assets, and a stream of errors in the console. 

Very possibly I could have corrected this without starting over, but I figured that since the whole point of this venture is learning about how protocols work under the hood it would be best to walk through all the steps myself at least once. Also, troubleshooting what I suspected to be CORS-based issues in the prebuilt image is not the chill lofi hiphop time I'd had planned for that afternoon.

I ended up doing the setup manually on a fresh Ubuntu 22.04 LTS ("jammy jellyfish") droplet, following [this guide](https://www.linuxbabe.com/ubuntu/how-to-install-mastodon-on-ubuntu) *mostly* to the letter. The guide claims Mastodon doesn't work with Node v18 or later and advises using v16 via PPA (the default Node version for Jammy is 12.22, which also won't work). Trying the setup with v16 gave me some odd errors that resolved once I tried using [nvm](https://github.com/nvm-sh/nvm) to run it with v18; I think it's safe to say that for the current stable release branch the advice to avoid newer Node versions is outdated. However, the `mastodon` user doesn't have `nvm` binaries in its PATH and I wasn't able to easily add them. My terrible hack of a solution was to run `sudo cp /root/.nvm/versions/node/v18.20.3/bin/node  /usr/bin/node` rather than actually do the proper reconfiguration in `/etc/apt/sources.list` to track the correct Node version, which, if this were anything other than a throwaway one-off, would 100% break something down the line. Don't try this at home, kids! 

One other minor deviation: the guide includes a step to install the yarn package manager, but not to actually run `yarn install` in the Mastodon directory. Maybe that part was automated at some point, but it doesn't seem to be now, so don't forget about that.


Finally - and this is not the fault of the guide, in fact it explicitly warns *against* doing this - keep in mind that Mastodon is like, a full-on Rails app. I'm so used to working with static and nearly-static sites that I instinctually selected the lowest tier VPS, with 512MiB memory and 1 CPU. At the asset pre-compilation step it ran out of memory and crashed, which was not unexpected, so I gave it an extra CPU and 3 more GB of RAM, planning to re-downgrade once the build was complete. But when I switched back to the lower tier, the web interface was unusably slow and the Mastodon process was constantly crashing and restarting. I experimented a bit and settled on 2 vCPUs / 2GB memory as the minimum workable resource allowance. On Digital Ocean that's $18 a month - more than I'd like, certainly, but it'll just be up for a week or so while I'm working on my ActivityPub implementation, so I'll bite the bullet. For comparison, the VPS where implicit.computer lives is $4/month with compute to spare. Static Websites: Save The Planet And Your Wallet!(TM)



I'd been idly considering spinning up an instance for my own Mastodon use for a while now, but this adventure convinced me that I actually do not want to do that, at least not for a primary account. For one thing, there's the aforementioned price of hosting, but I'm also not into being my own social media support tech. It's fun to dork around over SSH to troubleshoot, say, a broken Nginx rule (or it's fun to me, anyway, don't judge), but I'd prefer to do that on my own terms, and not as a forced prerequisite to accessing my memes. Plus I like the people on my instance, they're nice! 

Apparently there's services offering managed hosting for Mastodon, so that's potentially something else to explore later. For now though, I've achieved my goal of a minimal ActivityPub server, and the next step is to make another server it can federate with.

---
[^1]: I'm treating Mastodon and ActivityPub as basically synonymous here, but of course they're not. I could have set up an ActivityPub server that's *not* also a Mastodon instance - many such programs exist - but in practice I'd only consider the ActivityPub implementation a success if it works well with Mastodon anyway, so I didn't see a good reason to use something else. Plus, it's not every day I can peek under the hood of a service I use so frequently.


