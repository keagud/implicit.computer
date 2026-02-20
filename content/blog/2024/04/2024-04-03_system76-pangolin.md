+++
title =  "I guess this is a review of the System76 Pangolin laptop"
slug =  "system76-pangolin"
date = 2024-04-03

[taxonomies]
tags = ["tech", "100DaysToOffload"]
+++


Earlier this year, I decided to replace my old and trusty Thinkpad E480, now getting pretty long in the tooth and having some trouble with all these newfangled web apps, with some newer hardware. I'd heard generally good things about [System76](https://system76.com/), so I ordered a 16-inch [Pangolin](https://system76.com/laptops/pangolin) laptop, preloaded with Pop!_OS, and used it as my main workhorse machine for about two weeks.

The experience was mixed, overall. There's some stuff I like a lot about System76 in general and the Pangolin in particular, but I cannot recommend it in good conscience.  

## The Good

First, I have to give extra points to System76 just for selling machines that don't bundle in Windows. They also provide out of the box first party support for Ubuntu and Pop!_OS, so for the most part if you're using one of those distros stuff just works  (what about other distros? well, read on...).

On the hardware side, the LCD screen is pretty good - not Macbook quality, but this also isn't in the Macbook's territory price-wise. The keyboard is pleasently tactile, but also quiet enough that you won't get dirty looks at the library.

## The Neutral

The Pangolin has more than a few design features that struck me as just plain odd, but not necessarily in a bad way.  First, there's the  numpad, and the decision to make the keyboard off-center to accomodate it. I didn't really use the numpad at all, but I also didn't find it to be too in the way. Maybe if you're doing tons of numeric data entry this is a killer feature, but that ain't me. The keyboard placement takes some getting used to, but it's not a huge deal. 

There's also a physical switch to enable or disable the webcam, which I guess is to court the based paranoia crowd. In practice it's a useless gimmick, since if you care about that stuff you're already using one of those stick-on camera blockers, or else you've disabled the webcam altogether in the BIOS. Notably, the switch doesn't also disable the microphone, which makes it a halfway measure at best.

Finally, the RAM is soldered in place and can't be replaced or upgraded. I think this is a quirk specific to the Pangolin and its AMD CPU and isn't a general policy for System76, so it doesn't get elevated to "bad" status in my book. Plus, 32GB is probably way more than I'll ever actually use on a laptop outside of a few occasional cases of running LLM inference locally.


## The Bad

There's really only two outright problems, but taken together they were enough to make the Pangolin unusable as my daily driver. 

First, the trackpad is... look, I'm not going to sugarcoat it, everything about it is extremely bad.  As I said, the off-center keyboard isn't necessarily a bad choice, but the trackpad's placement doesn't seem to take that choice into account at all, so you're constantly bumping it while typing and clicking on stuff you didn't mean to. You might think the solution is to disable the tap-to-click functionality, but actually that makes it unusable in a new, totally different way. 

Rather than having separate physical buttons *or* fully committing to tap-to-click, the Pangolin has opted for a compromise in which pressing down on the trackpad itself actuates the mouse click controls. But the trackpad is one continuous component, so to distinguish between left and right clicks it's significant which *side* of the pad is depressed. I've used other laptops that handle this just fine, but my experience here was that even when taking care to push on the absolute leftmost edge of the trackpad, whether my input registered as a right-click or left-click was basically down to luck. 

Occasionally it would just decide to stop working for a while, which I suspected was a hardware problem since it persisted even when I booted from a live USB. I found some advice online to hold it under a hairdryer for a minute or so when this happens; I guess this is strictly better than not having a solution, but seriously? This is a portable device I bought to use while traveling, do I need to bring a hairdryer in my luggage? I thought I was [free from that!](/blog/bald)

That's enough ragging on the hardware, let's rag on the software. The pre-installed Pop!_OS distro seemed basically fine - it's Ubuntu with some custom GNOME theming, more or less - but I only used it for long enough to download a Debian ISO and burn it to a USB. Installation complete, I booted into my new OS to find some pretty righteous input lag on the trackpad (psyche, I'm actually still hating on the trackpad!). Ok, seems like a driver problem, that shouldn't be an issue since System76 is all "Linux-first", right? 

Turns out, no, System76 is more like "Ubuntu-first". They *only* provide offical builds for drivers on Ubuntu and Pop!_OS. In fairness, the drivers are open source and you can compile them yourself as a last resort, but come on, "you need to compile your own drivers" is not what I call top tier hardware support. After some searching I found a community maintained PPA for Debian Bookworm versions of the drivers, and that worked.


Look: I get that writing software for every possible distro and configuration is not feasible. And releasing the source is a good compromise, since if some specific distro's community wants to use the drivers they're free to configure and package it for that distro (there is, of course, an AUR version). But no official support for *Debian Stable??* The old reliable, the Honda Civic of distros?  They've already got Ubuntu support, which is just Worse Debian anyway! [^1] How much extra work could an official Bookworm PPA be? 

Between that and my new need for a travel hairdryer peripheral, I opted to return my Pangolin after about 2 weeks of use. The return process was very smooth: I submitted a ticket, they sent me an insured shipping label, I dropped off the label and laptop at my local UPS store, and a week or so later I got a full refund minus the cost of shipping and insurance. I have no complaints about that at all, in fact it's maybe the smoothest tech support experience I've ever had.

In a way, though, that makes it more frustrating. This isn't the kind of negative review where I can at least take joy in trashing something bad. There's no schadenfreude here. System76 strikes me as a company that likes Linux and wants to make it more accessible to a wider audience, and that's rad. I complain because I care! I want them to do better!

For the time being, I decided to upgrade my old reliable Thinkpad with some of that return cash rather than try buying a new laptop again. If it ain't broke, don't replace it (but maybe add some more RAM). 




---
[^1]: I apologize, I got a little heated there. I did use Ubuntu for a long time and it's a pretty good general purpose distro. I'm willing to come back, Ubuntu, but you need to work on yourself first. Break your snap habit and we can talk.
